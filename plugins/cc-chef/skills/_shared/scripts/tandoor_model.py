"""Pure mapping between the cc-chef recipe model and Tandoor JSON (standard library only)."""
from __future__ import annotations

import copy
import re
import unicodedata
from fractions import Fraction

from recipe_tool import Recipe, ingredient_line

MARKER = "cc-chef"

LIMITS = {"name": 128, "description": 512, "step name": 128, "note": 256, "food": 128, "unit": 128, "source_url": 1024}
_VULGAR = re.compile(r"([¼-¾⅐-⅞])")
_RANGE = re.compile(r"\s*[-–]\s*")


def normalize(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", text).casefold().split())


def _number(s: str) -> float:
    total = Fraction(0)
    for tok in _VULGAR.sub(r" \1", s.strip()).replace(",", ".").split():
        if "/" in tok:
            total += Fraction(tok)
        elif len(tok) == 1 and not tok.isdigit():
            total += Fraction(unicodedata.numeric(tok)).limit_denominator(16)
        else:
            total += Fraction(tok)
    return float(total)


def parse_amount(raw: str | None) -> tuple[float | None, float | None]:
    if not raw or not raw.strip():
        return None, None
    parts = _RANGE.split(raw.strip(), maxsplit=1)
    low = _number(parts[0])
    return low, _number(parts[1]) if len(parts) == 2 else None


def _ingredient(i, order: int) -> dict:
    low, high = parse_amount(i.amount)
    note = i.note or ""
    if high is not None:
        note = ", ".join(p for p in (" ".join(p for p in (i.amount, i.unit) if p), note) if p)
    return {
        "food": {"text": i.food},
        "unit": {"text": i.unit} if i.unit else None,
        "amount": low if low is not None else 0,
        "no_amount": low is None,
        "note": note,
        "order": order,
        "is_header": False,
    }


def _notes_step(r: Recipe, order: int) -> dict | None:
    heading, body = "Notes", r.notes.strip()
    if body.startswith("## "):
        first, _, body = body.partition("\n")
        heading, body = first[3:].strip() or heading, body.strip()
    parts = [str(r.meta.get(k) or "").strip() for k in ("oven", "signature", "source")] + [body]
    parts = [p for p in parts if p]
    if not parts:
        return None
    return {
        "name": heading,
        "instruction": "\n\n".join(parts),
        "order": order,
        "show_as_header": True,
        "show_ingredients_table": False,
        "time": 0,
        "ingredients": [],
    }


def to_payload(r: Recipe) -> dict:
    servings = r.meta.get("servings")
    steps = [
        {
            "name": s.title,
            "instruction": s.text,
            "order": k,
            "show_as_header": True,
            "time": 0,
            "ingredients": [_ingredient(i, j) for j, i in enumerate(s.ingredients)],
        }
        for k, s in enumerate(r.steps)
    ]
    notes = _notes_step(r, len(steps))
    if notes:
        steps.append(notes)
    tags = r.meta.get("tags") or []
    tags = tags if isinstance(tags, list) else [str(tags)]
    keywords = list(dict.fromkeys([*map(str, tags), MARKER]))
    minutes = lambda k: r.meta[k] if isinstance(r.meta.get(k), int) else 0  # noqa: E731
    return {
        "name": r.title,
        "description": r.description,
        "servings": servings if isinstance(servings, int) else 1,
        "servings_text": "" if servings in (None, "") or isinstance(servings, int) else str(servings),
        "working_time": minutes("prep-minutes"),
        "waiting_time": minutes("cook-minutes"),
        "source_url": str(r.meta.get("source-url") or ""),
        "keywords": [{"text": k} for k in keywords],
        "steps": steps,
    }


def finalize(payload: dict, foods: dict, units: dict, keywords: dict) -> dict:
    out = copy.deepcopy(payload)

    def swap(ref: dict, table: dict, kind: str) -> dict:
        hit = table.get(normalize(ref["text"]))
        if hit is None:
            raise ValueError(f"unresolved {kind}: {ref['text']!r}")
        return {"id": hit["id"], "name": hit["name"]}

    for step in out["steps"]:
        for ing in step["ingredients"]:
            ing["food"] = swap(ing["food"], foods, "food")
            if ing["unit"] is not None:
                ing["unit"] = swap(ing["unit"], units, "unit")
    out["keywords"] = [swap(k, keywords, "keyword") for k in out["keywords"]]
    return out


def limit_problems(payload: dict) -> list[str]:
    problems: list[str] = []

    def check(label: str, value, key: str):
        if value and len(value) > LIMITS[key]:
            problems.append(f"{label} is {len(value)} characters (max {LIMITS[key]})")

    check("recipe name", payload.get("name"), "name")
    check("description", payload.get("description"), "description")
    check("source URL", payload.get("source_url"), "source_url")
    for n, step in enumerate(payload["steps"], 1):
        check(f"step {n} name", step.get("name"), "step name")
        for ing in step["ingredients"]:
            food = ing["food"].get("text") or ing["food"].get("name") or "?"
            check(f"step {n}, ingredient {food!r}: food name", food, "food")
            check(f"step {n}, ingredient {food!r}: note", ing.get("note"), "note")
            if ing.get("unit"):
                check(f"step {n}, ingredient {food!r}: unit name", ing["unit"].get("text") or ing["unit"].get("name"), "unit")
    return problems


def _amount_text(a) -> str:
    return f"{float(a):g}"


def render_source(recipe: dict) -> str:
    lines = [f"# {recipe.get('name', '')}"]
    if recipe.get("description"):
        lines += ["", recipe["description"]]
    facts = []
    if recipe.get("servings"):
        facts.append(f"Servings: {recipe.get('servings_text') or recipe['servings']}")
    if recipe.get("working_time"):
        facts.append(f"Working time: {recipe['working_time']} min")
    if recipe.get("waiting_time"):
        facts.append(f"Waiting time: {recipe['waiting_time']} min")
    if recipe.get("source_url"):
        facts.append(f"Source: {recipe['source_url']}")
    if facts:
        lines += [""] + facts
    for n, step in enumerate(recipe.get("steps", []), 1):
        lines += ["", f"### {n}. {step.get('name') or ''}".rstrip()]
        if step.get("step_recipe"):
            lines.append("[embedded recipe]")
        if step.get("file"):
            lines.append("[file]")
        lines.append("")
        for ing in step.get("ingredients", []):
            food = (ing.get("food") or {}).get("name", "")
            if ing.get("is_header"):
                lines.append(f"- [heading] {ing.get('note') or food}")
                continue
            head = " ".join(
                p for p in (
                    "" if ing.get("no_amount") else _amount_text(ing.get("amount") or 0),
                    (ing.get("unit") or {}).get("name", ""),
                    food,
                ) if p
            )
            lines.append(f"- {head}, {ing['note']}" if ing.get("note") else f"- {head}")
        if step.get("instruction"):
            lines += ["", step["instruction"]]
    return "\n".join(lines) + "\n"


def read_back_diff(sent: dict, got: dict) -> list[str]:
    diffs: list[str] = []
    s_steps, g_steps = sent.get("steps", []), got.get("steps", [])
    if len(s_steps) != len(g_steps):
        diffs.append(f"step count: sent {len(s_steps)}, stored {len(g_steps)}")
    for n, (s, g) in enumerate(zip(s_steps, g_steps), 1):
        s_ing, g_ing = s.get("ingredients", []), g.get("ingredients", [])
        if len(s_ing) != len(g_ing):
            diffs.append(f"step {n}: ingredient count: sent {len(s_ing)}, stored {len(g_ing)}")
            continue
        for m, (a, b) in enumerate(zip(s_ing, g_ing), 1):
            where = f"step {n}, ingredient {m}"
            if (a.get("food") or {}).get("id") != (b.get("food") or {}).get("id"):
                diffs.append(f"{where}: food id sent {(a.get('food') or {}).get('id')}, stored {(b.get('food') or {}).get('id')}")
            if (a.get("unit") or {}).get("id") != (b.get("unit") or {}).get("id"):
                diffs.append(f"{where}: unit id sent {(a.get('unit') or {}).get('id')}, stored {(b.get('unit') or {}).get('id')}")
            if float(a.get("amount") or 0) != float(b.get("amount") or 0):
                diffs.append(f"{where}: amount sent {a.get('amount')}, stored {b.get('amount')}")
    return diffs
