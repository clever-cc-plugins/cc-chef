#!/usr/bin/env python3
"""cc-chef Tandoor CLI (standard library only). Exit codes: 0 ok, 1 error, 3 not configured.

Usage: python3 tandoor.py <command> ...   (see tandoor-api.md)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit

import recipe_tool as rt
import tandoor_client as tc
import tandoor_match as tmatch
import tandoor_model as tm

KINDS = ("food", "unit", "keyword")
ALIAS_TYPES = {"food": "FOOD_ALIAS", "unit": "UNIT_ALIAS", "keyword": "KEYWORD_ALIAS"}


def _cmd_check(args: argparse.Namespace) -> int:
    cfg = tc.load_config()
    host = urlsplit(cfg.url)
    if host.scheme == "http" and host.hostname not in ("localhost", "127.0.0.1"):
        print("Warning: TANDOOR_URL uses plain http://, so the token travels unencrypted", file=sys.stderr)
    client = tc.Client(cfg)
    version = str(client.get("api/server-settings/current/").get("version", "?"))
    client.get("api/food/", {"page_size": 1})  # proves the token
    if version.split(".")[0].isdigit() and int(version.split(".")[0]) < 2:
        print(f"Warning: Tandoor {version} is older than 2.x; this plugin is built against 2.x", file=sys.stderr)
    print(f"OK: {cfg.url}, Tandoor {version}")
    return 0


def plan_digest(plan: dict) -> str:
    return hashlib.sha256(json.dumps(plan, sort_keys=True).encode("utf-8")).hexdigest()[:8]


def _save(path: str, data: dict) -> None:
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _load_plan(path: str) -> dict:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise tc.TandoorError(f"{path}: cannot read plan ({getattr(e, 'strerror', None) or e})") from None


def _texts(payload: dict) -> dict[str, dict[str, str]]:
    """Distinct ingredient texts per kind, keyed by normalized text."""
    out: dict[str, dict[str, str]] = {k: {} for k in KINDS}
    for step in payload["steps"]:
        for ing in step["ingredients"]:
            out["food"].setdefault(tm.normalize(ing["food"]["text"]), ing["food"]["text"])
            if ing["unit"]:
                out["unit"].setdefault(tm.normalize(ing["unit"]["text"]), ing["unit"]["text"])
    for k in payload["keywords"]:
        out["keyword"].setdefault(tm.normalize(k["text"]), k["text"])
    return out


def _entries(plan: dict, kind: str):
    return plan[kind + "s"].items()


def _open_items(plan: dict) -> list[tuple[str, dict]]:
    return [(kind, e) for kind in KINDS for _, e in _entries(plan, kind) if e["decision"] is None]


def _open_line(kind: str, e: dict) -> str:
    if e["candidates"]:
        hint = "suggestions: " + "; ".join(f"{c['name']} (id {c['id']}, {c['score']})" for c in e["candidates"])
    else:
        hint = "no similar entry"
    return f"OPEN {kind} '{e['text']}': {hint}"


def _cmd_match(args: argparse.Namespace) -> int:
    recipe = rt._load(args.recipe)
    if recipe is None:
        return 1
    client = tc.Client(tc.load_config())
    payload = tm.to_payload(recipe)
    automations = [a for a in client.list_all("api/automation/") if not a.get("disabled")]
    plan = {
        "version": 1, "mode": "create", "source": str(args.recipe), "base_url": client.config.url,
        "tandoor_id": None, "updated_at": None, "payload": payload,
        "foods": {}, "units": {}, "keywords": {}, "existing": [], "problems": tm.limit_problems(payload),
    }
    for kind, texts in _texts(payload).items():
        index = tmatch.build_index(
            client.list_all(f"api/{kind}/"), [a for a in automations if a.get("type") == ALIAS_TYPES[kind]]
        )
        for key, text in texts.items():
            m = tmatch.match(text, index)
            confident = m["status"] in ("exact", "alias")
            m["decision"] = "use" if confident else ("create" if kind == "keyword" else None)
            plan[kind + "s"][key] = m
    found = client.get("api/recipe/", {"query": recipe.title, "page_size": 100})["results"]
    plan["existing"] = [{"id": r["id"], "name": r["name"]} for r in found if tm.normalize(r["name"]) == tm.normalize(recipe.title)]
    _save(args.output, plan)
    for kind, e in _open_items(plan):
        print(_open_line(kind, e))
    print(f"Plan written: {args.output} ({len(_open_items(plan))} open decisions)")
    return 0


def _cmd_resolve(args: argparse.Namespace) -> int:
    plan = _load_plan(args.plan)
    entry = plan[args.kind + "s"].get(tm.normalize(args.text))
    if entry is None:
        print(f"no {args.kind} '{args.text}' in the plan", file=sys.stderr)
        return 1
    if args.create:
        entry.update(decision="create", id=None, name=None)
    else:
        target = tc.Client(tc.load_config()).get(f"api/{args.kind}/{args.id}/")
        entry.update(decision="use", id=target["id"], name=target["name"])
    _save(args.plan, plan)
    print(f"{args.kind} '{entry['text']}': {entry['decision']}" + (f" {entry['name']} (id {entry['id']})" if entry["id"] else ""))
    return 0


def _maps(plan: dict, created: dict | None = None) -> dict[str, dict]:
    """Resolved entries per kind, keyed by normalized text; a new entry shows its text until it has an id."""
    out: dict[str, dict] = {}
    for kind in KINDS:
        out[kind] = {}
        for key, e in _entries(plan, kind):
            if e["decision"] == "use":
                out[kind][key] = {"id": e["id"], "name": e["name"]}
            elif created and key in created[kind]:
                out[kind][key] = created[kind][key]
            else:
                out[kind][key] = {"id": None, "name": e["text"]}
    return out


def _finalize(plan: dict, created: dict | None = None) -> dict:
    m = _maps(plan, created)
    return tm.finalize(plan["payload"], m["food"], m["unit"], m["keyword"])


def _cmd_preview(args: argparse.Namespace) -> int:
    plan = _load_plan(args.plan)
    open_items = _open_items(plan)
    if open_items or plan["problems"]:
        for kind, e in open_items:
            print(_open_line(kind, e))
        for problem in plan["problems"]:
            print(f"PROBLEM: {problem}")
        print("Resolve these first; no confirmation code is given while anything is open.")
        return 1
    print(tm.render_source(_finalize(plan)))
    new = [(kind, e["text"]) for kind in KINDS for _, e in _entries(plan, kind) if e["decision"] == "create"]
    print("New database entries (will be created):" if new else "New database entries: none")
    for kind, text in new:
        print(f"- {kind}: {text}")
    if plan["existing"]:
        print("A recipe with this name already exists:")
        for r in plan["existing"]:
            print(f"- {r['id']}  {r['name']}")
        print("Uploading creates a second recipe and needs --allow-duplicate.")
    print(f"Confirm: {plan_digest(plan)}")
    return 0


def _cmd_upload(args: argparse.Namespace) -> int:
    plan = _load_plan(args.plan)
    cfg = tc.load_config()
    if args.confirm != plan_digest(plan):
        print("the confirmation code does not match the plan: run preview again and use its code", file=sys.stderr)
        return 1
    if _open_items(plan) or plan["problems"]:
        print("the plan still has open decisions or problems: run preview", file=sys.stderr)
        return 1
    if plan["base_url"].rstrip("/") != cfg.url:
        print(f"the plan was made for {plan['base_url']}, but TANDOOR_URL is {cfg.url}", file=sys.stderr)
        return 1
    if plan["existing"] and not args.allow_duplicate:
        print("a recipe with this name already exists: use --allow-duplicate or update the existing recipe", file=sys.stderr)
        return 1
    client = tc.Client(cfg)
    created: dict[str, dict] = {k: {} for k in KINDS}
    try:
        for kind in KINDS:
            for key, e in _entries(plan, kind):
                if e["decision"] == "create":
                    obj = client.post(f"api/{kind}/", {"name": e["text"]})
                    created[kind][key] = {"id": obj["id"], "name": obj["name"]}
        body = _finalize(plan, created)
        recipe = client.post("api/recipe/", body)
        stored = client.get(f"api/recipe/{recipe['id']}/")
    except tc.TandoorError as e:
        print(f"upload failed: {e}", file=sys.stderr)
        made = [f"{kind} '{v['name']}' (id {v['id']})" for kind in KINDS for v in created[kind].values()]
        if made:
            print("Already created: " + ", ".join(made) + ". A new match finds them as exact.", file=sys.stderr)
        return 1
    print(f"Created: {recipe['id']} {cfg.url}/recipe/{recipe['id']}/")
    diffs = tm.read_back_diff(body, stored)
    for d in diffs:
        print(f"Difference after read-back: {d}", file=sys.stderr)
    return 1 if diffs else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="cc-chef Tandoor tool")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("check", help="verify TANDOOR_URL and TANDOOR_TOKEN")
    p.set_defaults(func=_cmd_check)
    p = sub.add_parser("match", help="match a recipe file to the database and write a plan")
    p.add_argument("recipe")
    p.add_argument("-o", "--output", required=True)
    p.set_defaults(func=_cmd_match)
    p = sub.add_parser("resolve", help="decide one open food, unit or keyword in a plan")
    p.add_argument("plan")
    p.add_argument("--kind", choices=KINDS, required=True)
    p.add_argument("--text", required=True)
    choice = p.add_mutually_exclusive_group(required=True)
    choice.add_argument("--id", type=int)
    choice.add_argument("--create", action="store_true")
    p.set_defaults(func=_cmd_resolve)
    p = sub.add_parser("preview", help="show what an upload would do; prints the confirmation code")
    p.add_argument("plan")
    p.set_defaults(func=_cmd_preview)
    p = sub.add_parser("upload", help="write the plan to Tandoor")
    p.add_argument("plan")
    p.add_argument("--confirm")
    p.add_argument("--allow-duplicate", action="store_true")
    p.set_defaults(func=_cmd_upload)
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except tc.NotConfigured as e:
        print(str(e), file=sys.stderr)
        return 3
    except tc.TandoorError as e:
        print(str(e), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
