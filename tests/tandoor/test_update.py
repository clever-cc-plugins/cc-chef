import json
import os
import stat
import unittest

from helpers import FakeCase

ALLOWED = {"name", "description", "servings", "servings_text", "working_time", "waiting_time", "source_url", "keywords", "steps"}
PULLED_AT = "2026-11-01T08:00:00Z"


def ing(food_id, food, unit=None):
    return {"id": food_id * 10, "food": {"id": food_id, "name": food}, "unit": unit, "amount": 1.0, "no_amount": False, "note": "", "is_header": False}


def live_recipe(rid=60, name="Altes Gericht", keywords=("Familie",), **step_extra):
    steps = [
        {"id": n, "name": f"Schritt {n}", "order": n - 1, "instruction": "Tun.", "ingredients": [ing(7, "Zwiebel")], "step_recipe": None, "file": None}
        for n in (1, 2, 3)
    ]
    steps[0].update(step_extra)
    return {"id": rid, "name": name, "description": "", "servings": 2, "keywords": [{"id": i + 1, "name": k} for i, k in enumerate(keywords)],
            "steps": steps, "updated_at": PULLED_AT, "image": "photo.jpg", "rating": 5}


class UpdateTests(FakeCase):
    def setUp(self):
        super().setUp()
        self.fake.db["keyword"] = [{"id": 1, "name": "Familie"}]
        self.fake.db["recipe"] = [live_recipe()]
        text = self.recipe.read_text(encoding="utf-8").replace(
            "tags: [Test]\n", f"tags: [Test]\ntandoor-id: 60\ntandoor-updated-at: {PULLED_AT}\n"
        )
        self.recipe.write_text(text, encoding="utf-8")

    def go(self, extra=()):
        self.match()
        self.resolve_all()
        return self.digest(), extra

    def test_recipes_marks_processed(self):
        self.fake.db["recipe"].append(live_recipe(61, "Neues Gericht", keywords=("Familie", "cc-chef")))
        r = self.run_cli("recipes")
        self.assertEqual(r.returncode, 0, r.stderr)
        lines = {line.split("  ")[0]: line for line in r.stdout.splitlines()}
        self.assertNotIn("[cc-chef]", lines["60"])
        self.assertIn("Altes Gericht", lines["60"])
        self.assertIn("[cc-chef]", lines["61"])
        r = self.run_cli("recipes", "--query", "neues")
        self.assertNotIn("Altes", r.stdout)
        self.assertIn("Neues", r.stdout)

    def test_pull_saves_backup_and_prints_frontmatter(self):
        backup = self.tmp / "backup.json"
        r = self.run_cli("pull", 60, "-o", backup)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(backup.read_text(encoding="utf-8"))["id"], 60)
        self.assertIn("Altes Gericht", r.stdout)
        self.assertIn("tandoor-id: 60", r.stdout)
        self.assertIn(f"tandoor-updated-at: {PULLED_AT}", r.stdout)

    def test_pull_backup_is_owner_only(self):
        backup = self.tmp / "backup.json"
        self.assertEqual(self.run_cli("pull", 60, "-o", backup).returncode, 0)
        self.assertEqual(stat.S_IMODE(os.stat(backup).st_mode), 0o600)

    def test_pull_never_overwrites_an_earlier_backup(self):
        backup = self.tmp / "backup.json"
        backup.write_text("state before the rework", encoding="utf-8")
        r = self.run_cli("pull", 60, "-o", backup)
        self.assertEqual(r.returncode, 1)
        self.assertIn("already exists", r.stderr)
        self.assertEqual(backup.read_text(encoding="utf-8"), "state before the rework")

    def test_pull_unknown_id(self):
        r = self.run_cli("pull", 999, "-o", self.tmp / "b.json")
        self.assertEqual(r.returncode, 1)
        self.assertIn("999", r.stderr)
        self.assertNotIn("Traceback", r.stderr)
        self.assertFalse((self.tmp / "b.json").exists())

    def test_update_patches_only_allowed_fields(self):
        self.match()
        plan = self.plan()
        self.assertEqual((plan["mode"], plan["tandoor_id"], plan["existing"]), ("update", 60, []))
        self.resolve_all()
        r = self.run_cli("preview", self.plan_path)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("Steps: 3 before, 2 after", r.stdout)
        self.assertIn("pull 60", r.stdout)
        r = self.run_cli("upload", self.plan_path, "--confirm", self.digest())
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("Updated: 60", r.stdout)
        patches = [w for w in self.writes() if w["method"] == "PATCH"]
        self.assertEqual([p["path"] for p in patches], ["/api/recipe/60/"])
        self.assertLessEqual(set(patches[0]["body"]), ALLOWED)
        self.assertFalse([w for w in self.writes() if w["method"] == "POST" and w["path"] == "/api/recipe/"])
        stored = self.fake.db["recipe"][0]
        self.assertEqual((stored["name"], len(stored["steps"]), stored["image"], stored["rating"]), ("Testgericht", 2, "photo.jpg", 5))

    def test_update_keeps_existing_keywords(self):
        self.match()
        self.resolve_all()
        self.run_cli("upload", self.plan_path, "--confirm", self.digest())
        names = [k["name"] for k in self.fake.db["recipe"][0]["keywords"]]
        self.assertEqual(sorted(names), ["Familie", "Test", "cc-chef"])

    def upload_with_servings(self, servings_line):
        self.fake.db["recipe"][0].update(servings=12, servings_text="Muffins")
        self.recipe.write_text(self.recipe.read_text(encoding="utf-8").replace("servings: 2\n", servings_line), encoding="utf-8")
        self.match()
        self.resolve_all()
        preview = self.run_cli("preview", self.plan_path).stdout
        r = self.run_cli("upload", self.plan_path, "--confirm", self.digest())
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        stored = self.fake.db["recipe"][0]
        return stored["servings"], stored["servings_text"], preview

    def test_update_keeps_the_servings_label_when_the_file_has_a_bare_number(self):
        servings, label, preview = self.upload_with_servings("servings: 12\n")
        self.assertEqual((servings, label), (12, "Muffins"))
        self.assertIn("Servings: 12 (Muffins)", preview)  # the preview shows what is kept

    def test_update_takes_the_servings_label_from_the_file(self):
        self.assertEqual(self.upload_with_servings("servings: 24 Mini-Muffins\n")[:2], (24, "Mini-Muffins"))

    def refused(self, needle):
        self.match()
        self.resolve_all()
        r = self.run_cli("preview", self.plan_path)
        self.assertEqual(r.returncode, 1)
        self.assertNotIn("Confirm:", r.stdout)
        self.assertIn(needle, r.stdout)
        r = self.run_cli("upload", self.plan_path, "--confirm", "00000000")
        self.assertEqual(r.returncode, 1)
        self.assertEqual([w for w in self.writes() if w["method"] == "PATCH"], [])

    def test_update_refused_when_changed_since_pull(self):
        self.fake.db["recipe"][0]["updated_at"] = "2026-11-02T09:00:00Z"
        self.refused("edited in Tandoor")

    def test_update_refused_for_embedded_recipe(self):
        self.fake.db["recipe"][0]["steps"][0]["step_recipe"] = 5
        self.refused("embeds another recipe")

    def test_update_refused_for_step_file(self):
        self.fake.db["recipe"][0]["steps"][0]["file"] = {"id": 1}
        self.refused("file")

    def test_update_refused_when_changed_before_upload(self):
        self.match()
        self.resolve_all()
        digest = self.digest()
        self.fake.db["recipe"][0]["updated_at"] = "2026-11-02T09:00:00Z"
        r = self.run_cli("upload", self.plan_path, "--confirm", digest)
        self.assertEqual(r.returncode, 1)
        self.assertEqual(self.writes(), [])

    def test_update_read_back(self):
        self.match()
        self.resolve_all()
        digest = self.digest()
        self.fake.recipe_mutator = lambda rec: rec["steps"][0]["ingredients"].pop()
        r = self.run_cli("upload", self.plan_path, "--confirm", digest)
        self.assertEqual(r.returncode, 1)
        self.assertIn("ingredient count", r.stdout + r.stderr)
        self.assertIn("Updated: 60", r.stdout)


if __name__ == "__main__":
    unittest.main()
