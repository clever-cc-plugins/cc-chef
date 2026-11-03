#!/usr/bin/env python3
"""Parser and validator for cc-chef recipe Markdown files (standard library only).

Format: see ../recipe-format.md. Usage:
    recipe_tool.py validate <file>
    recipe_tool.py newpath <folder> <title>
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path


class RecipeFormatError(Exception):
    def __init__(self, line: int, message: str):
        super().__init__(f"{line}: {message}")
        self.line = line
        self.message = message


@dataclass
class Ingredient:
    amount: str | None
    unit: str | None
    food: str
    note: str | None


@dataclass
class Step:
    number: int
    title: str
    ingredients: list[Ingredient]
    text: str


@dataclass
class Recipe:
    meta: dict[str, object]
    title: str
    description: str
    steps: list[Step]
    notes: str


_FRAC = r"[\u00bc-\u00be\u2150-\u215e]"
_NUM = rf"(?:\d+/\d+|\d+(?:[.,]\d+)?(?:\s+(?:\d+/\d+|{_FRAC})|{_FRAC})?|{_FRAC})"
_AMOUNT = re.compile(rf"^({_NUM}(?:\s*[-\u2013]\s*{_NUM})?)\s*(.*)$", re.DOTALL)
_STEP = re.compile(r"^###\s+(\d+)\.\s+(.*?)\s*$")
_BULLET = re.compile(r"^\s*[-*]\s+(.*)$")


def _parse_value(raw: str) -> object:
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        return [_unquote(p) for p in raw[1:-1].split(",") if p.strip()]
    value = _unquote(raw)
    if raw.isdigit():
        return int(raw)
    return value


def _unquote(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    return s


def _parse_frontmatter(lines: list[str]) -> tuple[dict[str, object], int]:
    """Return (meta, index of first body line)."""
    if not lines or lines[0].strip() != "---":
        raise RecipeFormatError(1, "missing frontmatter (file must start with '---')")
    meta: dict[str, object] = {}
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return meta, i + 1
        key, sep, value = lines[i].partition(":")
        if sep and key.strip():
            meta[key.strip()] = _parse_value(value)
    raise RecipeFormatError(1, "frontmatter is not closed (missing second '---')")


def _parse_ingredient(line: str, lineno: int) -> Ingredient:
    rest = _BULLET.match(line).group(1).strip()
    if rest.count("**") % 2:
        raise RecipeFormatError(lineno, "unclosed '**' in ingredient line")
    amount = unit = None
    if rest.startswith("**"):
        end = rest.index("**", 2)
        bold = rest[2:end].strip()
        rest = rest[end + 2:].strip()
        if bold:
            m = _AMOUNT.match(bold)
            if m:
                amount, unit = m.group(1), m.group(2).strip() or None
            else:
                unit = bold
    food, _, note = rest.partition(", ")
    return Ingredient(amount, unit, food.strip(), note.strip() or None)


def _parse_step_body(body: list[tuple[int, str]]) -> tuple[list[Ingredient], str]:
    ingredients: list[Ingredient] = []
    i = 0
    n = len(body)
    while i < n:
        lineno, line = body[i]
        if not line.strip():
            i += 1
        elif _BULLET.match(line):
            ingredients.append(_parse_ingredient(line, lineno))
            i += 1
        else:
            break
    text = "\n".join(line for _, line in body[i:]).strip()
    return ingredients, text


def parse_recipe(text: str) -> Recipe:
    lines = text.lstrip("\ufeff").splitlines()
    meta, start = _parse_frontmatter(lines)

    h1 = None
    step_heads: list[tuple[int, int, str]] = []  # (index, number, title)
    for i in range(start, len(lines)):
        m = _STEP.match(lines[i])
        if m:
            step_heads.append((i, int(m.group(1)), m.group(2)))
        elif h1 is None and lines[i].startswith("# "):
            h1 = (i, lines[i][2:].strip())
    # notes start at the first "## " heading after the last step
    last_step_idx = step_heads[-1][0] if step_heads else -1
    notes_idx = next(
        (i for i in range(last_step_idx + 1, len(lines)) if lines[i].startswith("## ")),
        None,
    )

    title = meta.get("title")
    title = str(title) if title not in (None, "") else (h1[1] if h1 else "")
    if not title:
        raise RecipeFormatError(start + 1, "missing title (no 'title' in frontmatter and no '# ' heading)")
    if not step_heads:
        raise RecipeFormatError(start + 1, "no steps found (expected '### 1. <title>' headings)")

    first_heading = next(
        (i for i in range(start, len(lines)) if lines[i].startswith("## ") or _STEP.match(lines[i])),
        len(lines),
    )
    desc_start = h1[0] + 1 if h1 else start
    description = "\n".join(lines[desc_start:first_heading]).strip() if h1 else ""

    steps: list[Step] = []
    for k, (idx, number, step_title) in enumerate(step_heads):
        if number != k + 1:
            raise RecipeFormatError(idx + 1, f"step number {number} out of order (expected {k + 1})")
        end = len(lines)
        if k + 1 < len(step_heads):
            end = step_heads[k + 1][0]
        if notes_idx is not None and k == len(step_heads) - 1:
            end = notes_idx
        body: list[tuple[int, str]] = []
        for j in range(idx + 1, end):
            if lines[j].startswith("## "):
                break
            body.append((j + 1, lines[j]))
        ingredients, step_text = _parse_step_body(body)
        steps.append(Step(number, step_title, ingredients, step_text))

    notes = "\n".join(lines[notes_idx:]).strip() if notes_idx is not None else ""
    return Recipe(meta, title, description, steps, notes)


def slugify(title: str) -> str:
    s = title.lower().replace("œ", "oe").replace("æ", "ae").replace("ß", "ss")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "recipe"


def unique_path(folder: Path, slug: str, ext: str = ".md") -> Path:
    path = folder / f"{slug}{ext}"
    n = 2
    while path.exists():
        path = folder / f"{slug}-{n}{ext}"
        n += 1
    return path


def _cmd_validate(args: argparse.Namespace) -> int:
    try:
        recipe = parse_recipe(Path(args.file).read_text(encoding="utf-8-sig"))
    except OSError as e:
        print(f"{args.file}: {e.strerror or e}", file=sys.stderr)
        return 1
    except UnicodeDecodeError:
        print(f"{args.file}: file is not valid UTF-8", file=sys.stderr)
        return 1
    except RecipeFormatError as e:
        print(f"{args.file}:{e.line}: {e.message}", file=sys.stderr)
        return 1
    count = sum(len(s.ingredients) for s in recipe.steps)
    print(f"OK: {recipe.title}, {len(recipe.steps)} steps, {count} ingredients")
    return 0


def _cmd_newpath(args: argparse.Namespace) -> int:
    print(unique_path(Path(args.folder), slugify(args.title)))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="cc-chef recipe tool")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("validate", help="validate a recipe Markdown file")
    p.add_argument("file")
    p.set_defaults(func=_cmd_validate)
    p = sub.add_parser("newpath", help="print a collision-free .md path for a title")
    p.add_argument("folder")
    p.add_argument("title")
    p.set_defaults(func=_cmd_newpath)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
