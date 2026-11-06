import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "plugins" / "cc-chef" / "skills" / "_shared" / "scripts"))

from tandoor_match import CANDIDATE_CUTOFF, build_index, match  # noqa: E402

ENTRIES = [
    {"id": 7, "name": "Zwiebel", "plural_name": "Zwiebeln"},
    {"id": 8, "name": "Passierte Tomaten", "plural_name": None},
    {"id": 9, "name": "Käse", "plural_name": None},
]
ALIASES = [{"param_1": "Tomaten, passiert", "param_2": "Passierte Tomaten"}]


class MatchTests(unittest.TestCase):
    def setUp(self):
        self.idx = build_index(ENTRIES, ALIASES)

    def test_match_case_and_plural(self):
        for t in ["zwiebel", "Zwiebeln", " Zwiebel "]:
            m = match(t, self.idx)
            self.assertEqual((m["status"], m["id"], m["name"]), ("exact", 7, "Zwiebel"), t)

    def test_alias(self):
        m = match("Tomaten, passiert", self.idx)
        self.assertEqual((m["status"], m["id"], m["name"]), ("alias", 8, "Passierte Tomaten"))
        self.assertEqual(match("TOMATEN, PASSIERT", self.idx)["status"], "alias")

    def test_alias_target_gone(self):
        idx = build_index(ENTRIES, [{"param_1": "Gurke", "param_2": "Salatgurke"}])
        m = match("Gurke", idx)
        self.assertEqual((m["status"], m["id"]), ("unmatched", None))
        idx = build_index(ENTRIES, [{"param_1": "Zwiebelchen", "param_2": "Gone"}])
        self.assertEqual(match("Zwiebelchen", idx)["status"], "candidate")

    def test_fuzzy_never_auto(self):
        m = match("Zwiebelchen", self.idx)
        self.assertEqual((m["status"], m["id"]), ("candidate", None))
        self.assertEqual(m["candidates"][0]["name"], "Zwiebel")
        self.assertGreaterEqual(m["candidates"][0]["score"], CANDIDATE_CUTOFF)
        self.assertLessEqual(len(m["candidates"]), 3)

    def test_unmatched(self):
        m = match("Drachenfrucht", self.idx)
        self.assertEqual((m["status"], m["id"], m["candidates"]), ("unmatched", None, []))

    def test_umlaut_forms(self):
        a, b = match("Käse", self.idx), match("Käse", self.idx)
        self.assertEqual(a, {**b, "text": a["text"]})
        self.assertEqual((a["status"], a["id"]), ("exact", 9))


if __name__ == "__main__":
    unittest.main()
