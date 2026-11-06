import json
import unittest

from helpers import FakeCase
import tandoor_cleanup as tcl  # noqa: E402


def food(i, name, plural=None, props=False, slug=None, n=0, parent=None):
    return {"id": i, "name": name, "plural_name": plural, "properties": [{"id": 1}] if props else [], "open_data_slug": slug, "numrecipe": n, "parent": parent}


class PureTests(unittest.TestCase):
    def test_split_food_name(self):
        for name, want in [
            ("Zwiebel, fein gehackt", ("Zwiebel", "fein gehackt")),
            ("Tomaten (gewürfelt)", ("Tomaten", "gewürfelt")),
            ("200 g Mehl", ("Mehl", "200 g")),
            ("Mehl", ("Mehl", None)),
            ("2 EL Öl, kalt", ("Öl", "2 EL, kalt")),
            ("2 Eier", ("2 Eier", None)),  # a number without a known unit stays in the name
        ]:
            self.assertEqual(tcl.split_food_name(name, {"g", "EL"}), want, name)

    def groups(self, entries, kind="food"):
        return tcl.duplicate_groups(entries, {"g"}, kind)

    def test_group_same_core(self):
        g = self.groups([food(1, "Zwiebel"), food(2, "zwiebel"), food(3, "Zwiebel, gehackt"), food(4, "Mehl")])
        self.assertEqual(len(g), 1)
        self.assertEqual((g[0]["confidence"], g[0]["kind"], sorted(m["id"] for m in g[0]["members"])), ("same", "food", [1, 2, 3]))

    def test_group_plural(self):
        g = self.groups([food(1, "Karotte", "Karotten"), food(2, "Karotten"), food(3, "Salz")])
        self.assertEqual([sorted(m["id"] for m in x["members"]) for x in g], [[1, 2]])

    def test_group_maybe(self):
        g = self.groups([food(1, "Tomatenmark"), food(2, "Tomatenmarkt"), food(3, "Salz")])
        self.assertEqual(len(g), 1)
        self.assertEqual((g[0]["confidence"], sorted(m["id"] for m in g[0]["members"])), ("maybe", [1, 2]))

    def test_unit_groups(self):
        g = self.groups([food(1, "Esslöffel"), food(2, "esslöffel")], "unit")
        self.assertEqual((g[0]["kind"], len(g[0]["members"])), ("unit", 2))

    def test_suggest_keep_prefers_properties(self):
        members = [food(1, "Zwiebel", n=50), food(2, "Zwiebeln", props=True, n=1), food(3, "zwiebel", slug="onion", n=99)]
        self.assertEqual(tcl.suggest_keep(members), 2)
        self.assertEqual(tcl.suggest_keep([food(1, "Zwiebel", n=50), food(3, "zwiebel", slug="onion", n=1)]), 3)
        self.assertEqual(tcl.suggest_keep([food(1, "Zwiebel", n=5), food(3, "Zwiebeln", n=9)]), 3)
        self.assertEqual(tcl.suggest_keep([food(5, "Zwiebeln", n=5), food(3, "Zwiebel", n=5)]), 3)
        self.assertEqual(tcl.suggest_keep([food(5, "Zwiebel", n=5), food(3, "Zwiebel", n=5)]), 3)

    def test_descendants_tree(self):
        foods = [food(1, "A"), food(2, "B", parent=1), food(3, "C", parent={"id": 2}), food(4, "D", parent=1), food(5, "E")]
        self.assertEqual(tcl.descendants(1, foods), {2, 3, 4})
        self.assertEqual(tcl.descendants(5, foods), set())


class ReportTests(FakeCase):
    def setUp(self):
        super().setUp()
        self.fake.db["food"] = [food(1, "Zwiebel", n=1), food(2, "zwiebel", n=1), food(3, "Tomatenmark", n=5), food(4, "Tomatenmarkt", n=5), food(5, "Mehl, gesiebt")]
        self.fake.db["unit"] = [{"id": 1, "name": "g", "plural_name": None}]
        self.report = self.tmp / "report.json"

    def test_report_read_only_and_counts(self):
        r = self.run_cli("foods-report", "-o", self.report)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.writes(), [])
        for name in ("Zwiebel", "Tomatenmark", "Mehl"):
            self.assertNotIn(name, r.stdout)
        self.assertRegex(r.stdout, r"5 foods")
        data = json.loads(self.report.read_text(encoding="utf-8"))
        self.assertEqual(set(data), {"base_url", "foods", "units", "groups", "polluted", "conversions", "aliases"})
        self.assertEqual(data["base_url"], self.url)
        self.assertEqual([p["id"] for p in data["polluted"]], [5])
        self.assertEqual(data["polluted"][0]["details"], "gesiebt")
        self.assertEqual(len(data["aliases"]), 1)

    def test_report_sorted_by_recipes(self):
        self.run_cli("foods-report", "-o", self.report)
        groups = json.loads(self.report.read_text(encoding="utf-8"))["groups"]
        self.assertEqual([g["id"] for g in groups], ["f1", "f2"])
        self.assertEqual({m["id"] for m in groups[0]["members"]}, {3, 4})  # 10 recipes before 2
        self.assertEqual(groups[0]["confidence"], "maybe")
        self.assertIn("keep", groups[1])

    def test_maybe_group_offers_the_most_used_entry_of_a_cluster(self):
        # "Basilikum" is the shortest name, "Basilikum, Topf" has the recipes; the list carries no counts to tell them apart
        self.fake.db["food"] += [food(11, "Basilikum", n=0), food(12, "Basilikum, Topf", n=40), food(13, "Basilikumm", n=0)]
        self.run_cli("foods-report", "-o", self.report)
        groups = json.loads(self.report.read_text(encoding="utf-8"))["groups"]
        maybe = next(g for g in groups if g["confidence"] == "maybe" and {m["id"] for m in g["members"]} & {11, 12, 13})
        self.assertEqual({m["id"] for m in maybe["members"]}, {12, 13})

    def test_report_counts_recipes_per_member_because_lists_omit_them(self):
        self.fake.db["food"] += [food(6, "Salz", n=1), food(7, "salz", n=8)]
        self.run_cli("foods-report", "-o", self.report)
        data = json.loads(self.report.read_text(encoding="utf-8"))
        self.assertNotIn("numrecipe", next(f for f in data["foods"] if f["id"] == 5))  # like the real list: only group members are counted
        salz = next(g for g in data["groups"] if {m["id"] for m in g["members"]} == {6, 7})
        self.assertEqual({m["id"]: m["numrecipe"] for m in salz["members"]}, {6: 1, 7: 8})
        self.assertEqual(salz["keep"], 7)  # the more used entry wins the tie-break
        self.assertEqual(data["groups"][0]["id"], "f1")
        self.assertEqual({m["id"] for m in data["groups"][0]["members"]}, {3, 4})  # 10 recipes, still first


if __name__ == "__main__":
    unittest.main()
