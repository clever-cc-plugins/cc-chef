import json
import unittest

from helpers import FakeCase, FakeTandoor, SEED
import tandoor_cleanup as tcl  # noqa: E402


def ing(i, food, note="", unit=None):
    return {"id": i, "food": food, "unit": unit, "amount": 1.0, "no_amount": False, "note": note, "is_header": False}


def recipe(rid, name, *ings, **extra):
    return {"id": rid, "name": name, "keywords": [], "updated_at": "x", "steps": [{"id": rid, "name": "s", "ingredients": list(ings)}], **extra}


ONION = {"id": 1, "name": "Zwiebel"}
CHOPPED = {"id": 2, "name": "Zwiebel, gehackt"}


class PureTests(unittest.TestCase):
    def test_merged_note(self):
        self.assertEqual(tcl.merged_note(None, "gehackt"), "gehackt")
        self.assertEqual(tcl.merged_note("fein", "gehackt"), "fein, gehackt")
        self.assertEqual(tcl.merged_note("fein, gehackt", "gehackt"), "fein, gehackt")
        self.assertEqual(tcl.merged_note("", "2 EL, kalt"), "2 EL, kalt")
        self.assertEqual(tcl.merged_note("kalt, 2 EL", "2 EL, kalt"), "kalt, 2 EL")


class ApplyTests(FakeCase):
    def setUp(self):
        super().setUp()
        db = self.fake.db
        db["food"] = [
            {"id": 1, "name": "Zwiebel", "plural_name": None, "properties": [{"id": 1}], "open_data_slug": "onion", "parent": None},
            {"id": 2, "name": "Zwiebel, gehackt", "plural_name": None, "properties": [], "open_data_slug": None, "parent": None},
            {"id": 5, "name": "Mehl, gesiebt", "plural_name": None, "properties": [], "open_data_slug": None, "parent": None},
        ]
        db["unit"] = [{"id": 1, "name": "g", "plural_name": None}, {"id": 4, "name": "Gramm", "plural_name": None}]
        db["automation"] = []
        db["recipe"] = [
            recipe(70, "Suppe", ing(701, CHOPPED, "grob")),
            recipe(71, "Eintopf", ing(711, CHOPPED)),
            recipe(72, "Salat", ing(721, ONION)),
            recipe(75, "Kuchen", ing(751, {"id": 5, "name": "Mehl, gesiebt"}), ing(752, ONION, unit={"id": 4, "name": "Gramm"})),
        ]
        self.report = self.tmp / "report.json"
        self.gplan = self.tmp / "gplan.json"

    # -- helpers --------------------------------------------------------------
    def make_plan(self, *args, kind="food", keep="1", merge="2", url=None):
        r = self.run_cli("foods-report", "-o", self.report, url=url)
        self.assertEqual(r.returncode, 0, r.stderr)
        r = self.run_cli("group-plan", self.report, "--kind", kind, "--keep", keep, "--merge", merge, *args, "-o", self.gplan)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return json.loads(self.gplan.read_text(encoding="utf-8"))

    def confirm(self):
        r = self.run_cli("group-preview", self.gplan)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return r.stdout.split("Confirm: ")[1].split()[0], r.stdout

    def apply(self):
        return self.run_cli("group-apply", self.gplan, "--confirm", self.confirm()[0])

    def methods(self):
        return [(w["method"], w["path"]) for w in self.writes()]

    def blocked(self, needle):
        r = self.run_cli("group-preview", self.gplan)
        self.assertEqual(r.returncode, 1)
        self.assertNotIn("Confirm:", r.stdout)
        self.assertIn(needle, r.stdout)
        r = self.run_cli("group-apply", self.gplan, "--confirm", "00000000")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(self.writes(), [])

    # -- tests ------------------------------------------------------------------
    def test_ops_order(self):
        plan = self.make_plan()
        self.assertEqual([o["op"] for o in plan["ops"]], ["note", "note", "merge", "alias"])
        notes = {o["ingredient"]: o["note"] for o in plan["ops"] if o["op"] == "note"}
        self.assertEqual(notes, {701: "grob, gehackt", 711: "gehackt"})
        self.assertEqual(plan["ops"][2], {"op": "merge", "source": 2, "target": 1})
        self.assertEqual(plan["ops"][3]["name"], "Zwiebel, gehackt")
        self.assertEqual(plan["ops"][3]["target"], "Zwiebel")
        self.assertEqual([s["id"] for s in plan["sources"]], [2])

    def test_apply_needs_digest(self):
        self.make_plan()
        for extra in (["--confirm", "deadbeef"], []):
            self.assertEqual(self.run_cli("group-apply", self.gplan, *extra).returncode, 1)
        self.assertEqual(self.writes(), [])

    def test_apply_other_instance_refused(self):
        self.make_plan()
        digest = self.confirm()[0]
        other = FakeTandoor(SEED)
        other_url = other.start()
        self.addCleanup(other.stop)
        r = self.run_cli("group-apply", self.gplan, "--confirm", digest, url=other_url)
        self.assertEqual(r.returncode, 1)
        self.assertEqual(other.requests, [])

    def test_notes_land_before_merge(self):
        self.make_plan()
        r = self.apply()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        order = [m for m in self.methods()]
        first_merge = next(i for i, (m, p) in enumerate(order) if m == "PUT")
        patches = [i for i, (m, p) in enumerate(order) if m == "PATCH" and "/ingredient/" in p]
        self.assertEqual(len(patches), 2)
        self.assertTrue(all(i < first_merge for i in patches))
        db = self.fake.db
        self.assertEqual([i["note"] for i in (db["recipe"][0]["steps"][0]["ingredients"][0], db["recipe"][1]["steps"][0]["ingredients"][0])], ["grob, gehackt", "gehackt"])
        self.assertEqual(db["recipe"][0]["steps"][0]["ingredients"][0]["food"]["id"], 1)
        self.assertEqual([f["id"] for f in db["food"]], [1, 5])

    def test_merge_into_descendant_blocked(self):
        self.fake.db["food"][1]["parent"] = None
        self.fake.db["food"][0]["parent"] = 2  # keep (1) is a child of the source (2)
        self.make_plan()
        self.blocked("child")

    def test_note_too_long_blocked(self):
        self.fake.db["recipe"][0]["steps"][0]["ingredients"][0]["note"] = "x" * 250
        self.make_plan()
        self.blocked("256")

    def test_properties_warning(self):
        self.fake.db["food"][1]["properties"] = [{"id": 3}, {"id": 4}]
        plan = self.make_plan()
        self.assertTrue(any("2 properties" in w for w in plan["warnings"]), plan["warnings"])
        self.assertIn("properties", self.confirm()[1])

    def test_conversions_warning(self):
        self.fake.db["unit-conversion"] = [{"id": 1, "food": {"id": 2}, "base_unit": {"id": 1}, "converted_unit": {"id": 4}}]
        plan = self.make_plan()
        self.assertTrue(any("1 unit conversion" in w for w in plan["warnings"]), plan["warnings"])

    def test_hidden_recipes_warning(self):
        self.fake.db["recipe"].append(recipe(73, "Geheim", ing(731, CHOPPED), hidden=True))
        plan = self.make_plan()
        warning = next(w for w in plan["warnings"] if "recipes" in w)
        self.assertIn("3", warning)
        self.assertIn("2", warning)
        self.assertNotIn(731, [o.get("ingredient") for o in plan["ops"]])

    def test_preview_names_the_recipes_and_does_not_warn_without_cause(self):
        # Tandoor drops used_in_recipes from the rows with ?simple=1, which once made every food look partly hidden
        self.make_plan()
        _, text = self.confirm()
        self.assertIn("Suppe", text)
        self.assertNotIn("unknown", text)
        self.assertNotIn("this token reaches", text)

    def test_group_plan_names_ids_that_are_not_in_the_report(self):
        self.run_cli("foods-report", "-o", self.report)
        for keep, merge in (("1", "2,99"), ("999", "2")):
            r = self.run_cli("group-plan", self.report, "--kind", "food", "--keep", keep, "--merge", merge, "-o", self.gplan)
            self.assertEqual(r.returncode, 1, (keep, merge))
            self.assertIn("99" if keep == "1" else "999", r.stderr)
            self.assertNotIn("Traceback", r.stderr)
        self.assertFalse(self.gplan.exists())

    def test_alias_created_once(self):
        self.make_plan()
        self.assertEqual(self.apply().returncode, 0)
        aliases = [a for a in self.fake.db["automation"] if a["type"] == "FOOD_ALIAS"]
        self.assertEqual([(a["param_1"], a["param_2"]) for a in aliases], [("Zwiebel, gehackt", "Zwiebel")])
        self.fake.db["food"].append({"id": 2, "name": "Zwiebel, gehackt", "plural_name": None, "properties": [], "open_data_slug": None, "parent": None})
        plan = self.make_plan()
        self.assertNotIn("alias", [o["op"] for o in plan["ops"]])

    def test_alias_from_a_merge_resolves_in_the_next_match(self):
        # the live check could not show this: the parser splits ", gehackt" off, so only a plain synonym needs the alias
        self.fake.db["food"] += [
            {"id": 6, "name": "Passata", "plural_name": None, "properties": [], "open_data_slug": None, "parent": None},
            {"id": 7, "name": "Tomatenpassata", "plural_name": None, "properties": [], "open_data_slug": None, "parent": None},
        ]
        self.make_plan(keep="6", merge="7")
        self.assertEqual(self.apply().returncode, 0)
        self.assertNotIn(7, [f["id"] for f in self.fake.db["food"]])
        self.recipe.write_text(self.recipe.read_text(encoding="utf-8").replace("Passata", "Tomatenpassata"), encoding="utf-8")
        self.match()
        entry = self.plan()["foods"]["tomatenpassata"]
        self.assertEqual((entry["status"], entry["decision"], entry["id"], entry["name"]), ("alias", "use", 6, "Passata"))

    def test_stale_alias_repointed(self):
        self.fake.db["automation"] = [{"id": 9, "type": "FOOD_ALIAS", "name": "a", "param_1": "Zwiebelwürfel", "param_2": "Zwiebel, gehackt", "disabled": False}]
        plan = self.make_plan()
        self.assertIn({"op": "repoint-alias", "id": 9, "target": "Zwiebel"}, plan["ops"])
        self.assertEqual(self.apply().returncode, 0)
        self.assertEqual(self.fake.db["automation"][0]["param_2"], "Zwiebel")

    def test_rename_polluted_food(self):
        plan = self.make_plan("--rename", "Mehl", keep="5", merge="")
        self.assertEqual([o["op"] for o in plan["ops"]], ["note", "rename", "alias"])
        self.assertIn({"op": "alias", "name": "Mehl, gesiebt", "target": "Mehl"}, plan["ops"])  # imports keep finding the old name
        self.assertEqual(self.apply().returncode, 0)
        order = self.methods()
        self.assertLess(next(i for i, (m, p) in enumerate(order) if "/ingredient/" in p), next(i for i, (m, p) in enumerate(order) if p == "/api/food/5/"))
        self.assertEqual(self.fake.db["food"][2]["name"], "Mehl")
        self.assertEqual(self.fake.db["recipe"][3]["steps"][0]["ingredients"][0]["note"], "gesiebt")

    def test_rename_warns_about_hidden_recipes_of_the_kept_food(self):
        self.fake.db["recipe"].append(recipe(74, "Geheim", ing(741, {"id": 5, "name": "Mehl, gesiebt"}), hidden=True))
        plan = self.make_plan("--rename", "Mehl", keep="5", merge="")
        self.assertTrue(any("Mehl, gesiebt" in w and "reaches 1" in w and "rename" in w for w in plan["warnings"]), plan["warnings"])

    def test_apply_refuses_when_an_ingredient_appeared_after_the_plan(self):
        self.make_plan()
        self.fake.db["recipe"].append(recipe(76, "Neu", ing(761, CHOPPED)))  # uses the polluted food: its detail would be lost on merge
        r = self.apply()
        self.assertEqual(r.returncode, 1)
        self.assertIn("changed since the plan was made", r.stderr)
        self.assertEqual(self.writes(), [])  # nothing was moved or merged
        self.assertIn(2, [f["id"] for f in self.fake.db["food"]])

    def test_detail_by_hand(self):
        plan = self.make_plan("--detail", "2=fein gewürfelt")
        self.assertEqual({o["note"] for o in plan["ops"] if o["op"] == "note"}, {"grob, fein gewürfelt", "fein gewürfelt"})

    def test_plural_name_is_planned_previewed_and_applied(self):
        plan = self.make_plan("--plural", "Zwiebeln")
        self.assertIn({"op": "plural", "id": 1, "name": "Zwiebeln", "before": ""}, plan["ops"])
        self.assertIn("'' -> 'Zwiebeln'", self.confirm()[1])
        self.assertEqual(self.apply().returncode, 0)
        self.assertEqual(self.fake.db["food"][0]["plural_name"], "Zwiebeln")

    def test_empty_detail_means_no_note(self):
        plan = self.make_plan("--detail", "2=")
        self.assertEqual([o for o in plan["ops"] if o["op"] == "note"], [])

    def test_rename_collision_blocked(self):
        self.make_plan("--rename", "Zwiebel", keep="2", merge="")
        self.blocked("already exists")

    def test_unit_merge_has_no_note_ops(self):
        plan = self.make_plan(kind="unit", keep="1", merge="4")
        self.assertEqual([o["op"] for o in plan["ops"]], ["merge", "alias"])
        self.assertEqual(plan["ops"][1]["name"], "Gramm")
        self.assertEqual(self.apply().returncode, 0)
        self.assertEqual([a["type"] for a in self.fake.db["automation"]], ["UNIT_ALIAS"])
        self.assertEqual(self.fake.db["recipe"][3]["steps"][0]["ingredients"][1]["unit"]["id"], 1)

    def test_stops_at_first_failure(self):
        self.make_plan()
        digest = self.confirm()[0]
        self.fake.can("PUT", "/merge/", 500, {"detail": "boom"})
        r = self.run_cli("group-apply", self.gplan, "--confirm", digest)
        out = r.stdout + r.stderr
        self.assertEqual(r.returncode, 1)
        self.assertIn("group-plan again", out)
        self.assertIn("ingredient 701", out)
        self.assertEqual([w for w in self.writes() if w["path"] == "/api/automation/"], [])

    def test_rerun_after_failure_is_idempotent(self):
        self.make_plan()
        digest = self.confirm()[0]
        self.fake.can("PUT", "/merge/", 500, {"detail": "boom"})
        self.assertEqual(self.run_cli("group-apply", self.gplan, "--confirm", digest).returncode, 1)
        plan = self.make_plan()
        self.assertEqual([o["op"] for o in plan["ops"]], ["merge", "alias"])
        self.assertEqual(self.apply().returncode, 0)
        self.assertEqual(self.fake.db["recipe"][0]["steps"][0]["ingredients"][0]["note"], "grob, gehackt")
        self.assertEqual([f["id"] for f in self.fake.db["food"]], [1, 5])

    def test_apply_refused_when_entries_changed(self):
        self.make_plan()
        digest = self.confirm()[0]
        self.fake.db["food"][1]["name"] = "Zwiebel, grob"
        r = self.run_cli("group-apply", self.gplan, "--confirm", digest)
        self.assertEqual(r.returncode, 1)
        self.assertIn("group-plan again", r.stdout + r.stderr)
        self.assertEqual(self.writes(), [])

    def test_vanished_source_is_dropped(self):
        self.run_cli("foods-report", "-o", self.report)
        self.fake.db["food"].pop(1)
        r = self.run_cli("group-plan", self.report, "--kind", "food", "--keep", "1", "--merge", "2", "-o", self.gplan)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(self.gplan.read_text(encoding="utf-8"))["sources"], [])


if __name__ == "__main__":
    unittest.main()
