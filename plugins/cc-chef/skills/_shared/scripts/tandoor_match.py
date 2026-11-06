"""Pure matching of ingredient, unit and keyword texts to database entries (standard library only).

Only exact (name or plural_name) and alias matches are confident. Fuzzy results are
suggestions for the user and never resolve by themselves.
"""
from __future__ import annotations

import difflib
from dataclasses import dataclass, field

from tandoor_model import normalize

CANDIDATE_CUTOFF = 0.75


@dataclass
class Index:
    exact: dict[str, dict] = field(default_factory=dict)
    alias: dict[str, dict] = field(default_factory=dict)


def build_index(entries: list[dict], aliases: list[dict]) -> Index:
    idx = Index()
    for e in entries:
        for name in (e.get("name"), e.get("plural_name")):
            if name:
                idx.exact.setdefault(normalize(name), e)
    for a in aliases:
        target = idx.exact.get(normalize(a.get("param_2") or ""))
        if target is not None and a.get("param_1"):
            idx.alias.setdefault(normalize(a["param_1"]), target)
    return idx


def _result(text: str, status: str, entry: dict | None = None, candidates: list[dict] | None = None) -> dict:
    return {
        "text": text,
        "status": status,
        "id": entry["id"] if entry else None,
        "name": entry["name"] if entry else None,
        "candidates": candidates or [],
    }


def match(text: str, index: Index) -> dict:
    key = normalize(text)
    if key in index.exact:
        return _result(text, "exact", index.exact[key])
    if key in index.alias:
        return _result(text, "alias", index.alias[key])
    best: dict[int, dict] = {}
    for name in difflib.get_close_matches(key, list(index.exact), n=10, cutoff=CANDIDATE_CUTOFF):
        entry = index.exact[name]
        score = round(difflib.SequenceMatcher(None, key, name).ratio(), 2)
        if score > best.get(entry["id"], {"score": 0})["score"]:
            best[entry["id"]] = {"id": entry["id"], "name": entry["name"], "score": score}
    candidates = sorted(best.values(), key=lambda c: -c["score"])[:3]
    return _result(text, "candidate" if candidates else "unmatched", None, candidates)
