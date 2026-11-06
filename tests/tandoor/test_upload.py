import re
import unittest

from helpers import SEED, FakeCase, FakeTandoor


class UploadTests(FakeCase):
    def test_match_writes_plan_and_lists_open_items(self):
        r = self.match()
        plan = self.plan()
        self.assertEqual((plan["version"], plan["mode"], plan["base_url"]), (1, "create", self.url))
        self.assertEqual(plan["foods"]["zwiebeln"]["decision"], "use")
        self.assertEqual(plan["foods"]["zwiebeln"]["id"], 7)
        self.assertEqual((plan["foods"]["passata"]["status"], plan["foods"]["passata"]["id"]), ("alias", 8))
        self.assertEqual(plan["foods"]["zwiebelchen"]["status"], "candidate")
        self.assertIsNone(plan["foods"]["zwiebelchen"]["decision"])
        self.assertEqual(plan["foods"]["drachenfrucht"]["status"], "unmatched")
        self.assertEqual(plan["keywords"]["cc-chef"]["decision"], "create")
        self.assertEqual(plan["existing"], [])
        self.assertIn("Zwiebelchen", r.stdout)
        self.assertIn("Zwiebel", r.stdout.split("Zwiebelchen")[1])  # the suggestion
        self.assertIn("Drachenfrucht", r.stdout)
        self.assertNotIn("Mehl", r.stdout)
        self.assertEqual(self.writes(), [])

    def test_resolve_create_and_map(self):
        self.match()
        r = self.run_cli("resolve", self.plan_path, "--kind", "food", "--text", "Zwiebelchen", "--id", "7")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.plan()["foods"]["zwiebelchen"]["decision"], "use")
        self.assertEqual(self.plan()["foods"]["zwiebelchen"]["name"], "Zwiebel")
        r = self.run_cli("resolve", self.plan_path, "--kind", "food", "--text", "Drachenfrucht", "--create")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.plan()["foods"]["drachenfrucht"]["decision"], "create")
        r = self.run_cli("resolve", self.plan_path, "--kind", "food", "--text", "Gibtsnicht", "--create")
        self.assertEqual(r.returncode, 1)
        r = self.run_cli("resolve", self.plan_path, "--kind", "food", "--text", "Zwiebelchen", "--id", "999")
        self.assertEqual(r.returncode, 1)

    def test_preview_refuses_open_items(self):
        self.match()
        r = self.run_cli("preview", self.plan_path)
        self.assertEqual(r.returncode, 1)
        self.assertNotIn("Confirm:", r.stdout)
        self.assertIn("Zwiebelchen", r.stdout + r.stderr)

    def test_preview_shows_new_entries(self):
        self.match()
        self.resolve_all()
        r = self.run_cli("preview", self.plan_path)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertRegex(r.stdout, r"Confirm: [0-9a-f]{8}")
        new = r.stdout.split("New database entries")[1]
        self.assertIn("Drachenfrucht", new)
        self.assertIn("cc-chef", new)
        self.assertNotIn("Mehl", new)
        self.assertIn("Ansetzen", r.stdout)
        self.assertIn("Mehl", r.stdout)

    def test_preview_warns_existing_recipe(self):
        self.fake.db["recipe"] = [{"id": 50, "name": "Testgericht", "keywords": [], "steps": [], "updated_at": "x"}]
        self.match()
        self.assertEqual([e["id"] for e in self.plan()["existing"]], [50])
        self.resolve_all()
        r = self.run_cli("preview", self.plan_path)
        self.assertIn("already exists", r.stdout)
        self.assertIn("50", r.stdout)
        digest = r.stdout.split("Confirm: ")[1].split()[0]
        r = self.run_cli("upload", self.plan_path, "--confirm", digest)
        self.assertEqual(r.returncode, 1)
        self.assertEqual(self.writes(), [])
        r = self.run_cli("upload", self.plan_path, "--confirm", digest, "--allow-duplicate")
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_upload_needs_digest(self):
        self.match()
        self.resolve_all()
        self.digest()
        for extra in (["--confirm", "deadbeef"], []):
            r = self.run_cli("upload", self.plan_path, *extra)
            self.assertEqual(r.returncode, 1, extra)
        self.assertEqual(self.writes(), [])

    def test_digest_changes_after_resolve(self):
        self.match()
        self.resolve_all()
        old = self.digest()
        self.run_cli("resolve", self.plan_path, "--kind", "food", "--text", "Drachenfrucht", "--id", "9")
        r = self.run_cli("upload", self.plan_path, "--confirm", old)
        self.assertEqual(r.returncode, 1)
        self.assertEqual(self.writes(), [])
        self.assertNotEqual(self.digest(), old)

    def test_upload_other_instance_refused(self):
        self.match()
        self.resolve_all()
        digest = self.digest()
        other = FakeTandoor(SEED)
        other_url = other.start()
        self.addCleanup(other.stop)
        r = self.run_cli("upload", self.plan_path, "--confirm", digest, url=other_url)
        self.assertEqual(r.returncode, 1)
        self.assertEqual(other.requests, [])

    def test_upload_sends_only_ids(self):
        self.match()
        self.resolve_all()
        r = self.run_cli("upload", self.plan_path, "--confirm", self.digest())
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertRegex(r.stdout, r"Created: \d+ " + re.escape(self.url) + r"/recipe/\d+/")
        posts = [w for w in self.writes() if w["path"] == "/api/recipe/"]
        self.assertEqual(len(posts), 1)
        db_food = {f["id"]: f["name"] for f in self.fake.db["food"]}
        db_unit = {u["id"]: u["name"] for u in self.fake.db["unit"]}
        sent = posts[0]["body"]
        for step in sent["steps"]:
            for ing in step["ingredients"]:
                self.assertEqual(set(ing["food"]), {"id", "name"})
                self.assertEqual(db_food[ing["food"]["id"]], ing["food"]["name"])
                if ing["unit"]:
                    self.assertEqual(db_unit[ing["unit"]["id"]], ing["unit"]["name"])
        names = [i["food"]["name"] for s in sent["steps"] for i in s["ingredients"]]
        self.assertEqual(names.count("Zwiebel"), 2)  # "Zwiebeln" and the approved "Zwiebelchen"
        self.assertEqual(len(self.fake.db["food"]), len(SEED["food"]) + 1)
        self.assertEqual(len(self.fake.db["unit"]), len(SEED["unit"]))

    def test_upload_read_back(self):
        self.match()
        self.resolve_all()
        digest = self.digest()
        self.fake.recipe_mutator = lambda rec: rec["steps"][0]["ingredients"].pop()
        r = self.run_cli("upload", self.plan_path, "--confirm", digest)
        self.assertEqual(r.returncode, 1)
        self.assertIn("ingredient count", r.stdout + r.stderr)

    def test_failed_post_lists_created(self):
        self.match()
        self.resolve_all()
        digest = self.digest()
        self.fake.can("POST", "/api/recipe/", 500, {"detail": "boom"})
        r = self.run_cli("upload", self.plan_path, "--confirm", digest)
        self.assertEqual(r.returncode, 1)
        self.assertIn("Drachenfrucht", r.stdout + r.stderr)
        self.match()
        self.assertEqual(self.plan()["foods"]["drachenfrucht"]["status"], "exact")


if __name__ == "__main__":
    unittest.main()
