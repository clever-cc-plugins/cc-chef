"""Pure logic for cleaning up a Tandoor food and unit database (standard library only)."""
from __future__ import annotations

import difflib
import re

from tandoor_model import normalize

MAYBE_RATIO = 0.9
_QTY = re.compile(r"^\s*(\d+(?:[.,]\d+)?(?:/\d+)?)\s+(\S+)\s+(.+)$")
_PAREN = re.compile(r"^(.*?)\s*\(([^)]*)\)\s*$")


def split_food_name(name: str, unit_names: set[str]) -> tuple[str, str | None]:
    """(core, details): details are quantity, preparation or qualifiers that belong in an ingredient note."""
    units = {normalize(u) for u in unit_names}
    rest, details = name.strip(), []
    m = _QTY.match(rest)
    if m and normalize(m.group(2)) in units:
        details.append(f"{m.group(1)} {m.group(2)}")
        rest = m.group(3)
    rest, _, tail = rest.partition(", ")
    if tail.strip():
        details.append(tail.strip())
    m = _PAREN.match(rest)
    if m and m.group(1):
        rest = m.group(1)
        details.append(m.group(2).strip())
    if not rest.strip():
        return name.strip(), None
    return rest.strip(), ", ".join(d for d in details if d) or None


def suggest_keep(members: list[dict]) -> int:
    """Properties first, then open-data slug, then most recipes, then shortest name, then lowest id."""
    return min(
        members,
        key=lambda m: (not m.get("properties"), not m.get("open_data_slug"), -(m.get("numrecipe") or 0), len(m["name"]), m["id"]),
    )["id"]


def _keys(entry: dict, kind: str, unit_names: set[str]) -> set[str]:
    core = split_food_name(entry["name"], unit_names)[0] if kind == "food" else entry["name"]
    keys = {normalize(core)}
    if entry.get("plural_name"):
        keys.add(normalize(entry["plural_name"]))
    return keys


def _group(kind: str, key: str, members: list[dict], confidence: str) -> dict:
    return {"key": key, "kind": kind, "members": members, "keep": suggest_keep(members), "confidence": confidence}


def duplicate_groups(entries: list[dict], unit_names: set[str], kind: str = "food") -> list[dict]:
    """`same`: equal core name or plural. `maybe`: near-identical names, offering the best entry of each cluster."""
    parent = list(range(len(entries)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    owner: dict[str, int] = {}
    keys = [_keys(e, kind, unit_names) for e in entries]
    for i, ks in enumerate(keys):
        for k in ks:
            parent[find(i)] = find(owner.setdefault(k, i))
    clusters: dict[int, list[int]] = {}
    for i in range(len(entries)):
        clusters.setdefault(find(i), []).append(i)
    cluster_list = list(clusters.values())
    cluster_keys = [set().union(*(keys[i] for i in c)) for c in cluster_list]

    groups = [
        _group(kind, min(cluster_keys[n]), [entries[i] for i in c], "same")
        for n, c in enumerate(cluster_list)
        if len(c) > 1
    ]

    # near matches between clusters, blocked by the first two letters to stay fast on large databases
    link = list(range(len(cluster_list)))

    def find_c(i: int) -> int:
        while link[i] != i:
            link[i] = link[link[i]]
            i = link[i]
        return i

    buckets: dict[str, list[tuple[int, str]]] = {}
    for n, ks in enumerate(cluster_keys):
        for k in ks:
            buckets.setdefault(k[:2], []).append((n, k))
    for items in buckets.values():
        for a in range(len(items)):
            for b in range(a + 1, len(items)):
                (n1, k1), (n2, k2) = items[a], items[b]
                if n1 != n2 and find_c(n1) != find_c(n2):
                    sm = difflib.SequenceMatcher(None, k1, k2)
                    if sm.real_quick_ratio() >= MAYBE_RATIO and sm.quick_ratio() >= MAYBE_RATIO and sm.ratio() >= MAYBE_RATIO:
                        link[find_c(n1)] = find_c(n2)
    components: dict[int, list[int]] = {}
    for n in range(len(cluster_list)):
        components.setdefault(find_c(n), []).append(n)
    for comp in components.values():
        if len(comp) > 1:
            best = []
            for n in comp:
                members = [entries[i] for i in cluster_list[n]]
                keep = suggest_keep(members)
                best.append(next(m for m in members if m["id"] == keep))
            groups.append(_group(kind, min(min(cluster_keys[n]) for n in comp), best, "maybe"))
    return groups


def descendants(food_id: int, foods: list[dict]) -> set[int]:
    def parent_of(f: dict):
        p = f.get("parent")
        return p.get("id") if isinstance(p, dict) else p

    children: dict[int, list[int]] = {}
    for f in foods:
        if parent_of(f) is not None:
            children.setdefault(parent_of(f), []).append(f["id"])
    out: set[int] = set()
    todo = [food_id]
    while todo:
        for c in children.get(todo.pop(), []):
            if c not in out:
                out.add(c)
                todo.append(c)
    return out


NOTE_LIMIT = 256
ALIAS_TYPES = {"food": "FOOD_ALIAS", "unit": "UNIT_ALIAS"}


def merged_note(note: str | None, detail: str) -> str:
    """Append `detail` to a note with ', ', unless the note already holds every part of it."""
    note = (note or "").strip()
    have = {normalize(p) for p in note.split(", ")}
    if all(normalize(p) in have for p in detail.split(", ")):
        return note
    return f"{note}, {detail}" if note else detail


def _ref_id(x):
    return x.get("id") if isinstance(x, dict) else x


def _involves(conversion: dict, kind: str, entry_id: int) -> bool:
    if kind == "food":
        return _ref_id(conversion.get("food")) == entry_id
    return entry_id in (_ref_id(conversion.get("base_unit")), _ref_id(conversion.get("converted_unit")))


def build_group_plan(report, kind, keep, merge, details, ingredients, rename=None) -> dict:
    """Plan the note moves, merges, rename and aliases for one approved group.

    `report` holds the entries to act on (refreshed from the live instance by the caller), `ingredients` maps a
    food id to its ingredients, `details` maps an id to a hand-written detail that replaces the one found in its name.
    """
    entries = {e["id"]: e for e in report[kind + "s"]}
    keep_entry, sources = entries[keep], [entries[i] for i in merge if i in entries]
    unit_names = {u["name"] for u in report["units"]} | {u["plural_name"] for u in report["units"] if u.get("plural_name")}
    target_name = rename or keep_entry["name"]
    alias_type = ALIAS_TYPES[kind]
    ops: list[dict] = []
    warnings: list[str] = []
    problems: list[str] = []

    if keep in merge:
        problems.append("the entry to keep is also listed as a source")
    if not sources and not rename:
        problems.append("nothing to do: no source entry is left and no --rename was given")
    if rename and any(e["id"] != keep and normalize(e["name"]) == normalize(rename) for e in report[kind + "s"]):
        problems.append(f"'{rename}' already exists: merge into it instead of renaming")
    if kind == "food":
        for src in sources:
            if keep in descendants(src["id"], report["foods"]):
                problems.append(f"'{keep_entry['name']}' is a child of '{src['name']}': Tandoor does not merge a food into its own descendant")

    note_holders = sources + ([keep_entry] if rename else [])
    if kind == "food":
        for src in note_holders:
            detail = details.get(src["id"]) or split_food_name(src["name"], unit_names)[1]
            if not detail:
                continue
            for item in ingredients.get(src["id"], []):
                before = (item.get("note") or "").strip()
                after = merged_note(before, detail)
                if after == before:
                    continue
                if len(after) > NOTE_LIMIT:
                    problems.append(f"the note of ingredient {item['id']} would be {len(after)} characters (max {NOTE_LIMIT})")
                    continue
                recipes = [r["name"] for r in item.get("used_in_recipes", [])]
                ops.append({"op": "note", "ingredient": item["id"], "note": after, "before": before, "food": src["name"], "recipes": recipes})

    for src in sources:
        ops.append({"op": "merge", "source": src["id"], "target": keep})
    if rename:
        ops.append({"op": "rename", "id": keep, "name": rename})

    existing = report["aliases"]
    for src in sources:
        if normalize(src["name"]) == normalize(target_name):
            continue
        if not any(a.get("type") == alias_type and normalize(a.get("param_1") or "") == normalize(src["name"]) for a in existing):
            ops.append({"op": "alias", "name": src["name"], "target": target_name})
    gone = {normalize(s["name"]) for s in sources} | ({normalize(keep_entry["name"])} if rename else set())
    for a in existing:
        if a.get("type") == alias_type and normalize(a.get("param_2") or "") in gone and normalize(a["param_2"]) != normalize(target_name):
            ops.append({"op": "repoint-alias", "id": a["id"], "target": target_name})

    for src in sources:
        props = len(src.get("properties") or [])
        if props:
            warnings.append(f"'{src['name']}' has {props} properties (nutrition values): the merge deletes them")
        convs = sum(_involves(c, kind, src["id"]) for c in report["conversions"])
        if convs:
            warnings.append(f"'{src['name']}' has {convs} unit conversions: the merge deletes them")
        if kind == "food":
            reached = len({r["id"] for i in ingredients.get(src["id"], []) for r in i.get("used_in_recipes", [])})
            used = src.get("numrecipe") or 0
            if used > reached:
                warnings.append(
                    f"'{src['name']}' is used in {used} recipes, but this token reaches {reached}: the detail cannot be moved into the others, and the merge cannot be undone"
                )
    return {
        "version": 1, "base_url": report["base_url"], "kind": kind, "keep": keep_entry, "sources": sources,
        "ops": ops, "warnings": warnings, "problems": problems,
    }
