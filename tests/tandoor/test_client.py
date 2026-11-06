import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parents[1] / "plugins" / "cc-chef" / "skills" / "_shared" / "scripts"
TOOL = SCRIPTS / "tandoor.py"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(HERE))

import tandoor_client as tc  # noqa: E402
from fake_tandoor import FakeTandoor  # noqa: E402

SEED = json.loads((HERE / "fixtures" / "seed.json").read_text(encoding="utf-8"))
TOKEN = "test-token"


def seed_with_foods(n):
    s = json.loads(json.dumps(SEED))
    s["food"] = [{"id": i, "name": f"Food {i}"} for i in range(1, n + 1)]
    return s


def cli(url, *args, token=TOKEN):
    env = {k: v for k, v in os.environ.items() if not k.startswith("TANDOOR_")}
    if url is not None:
        env["TANDOOR_URL"] = url
    if token is not None:
        env["TANDOOR_TOKEN"] = token
    return subprocess.run([sys.executable, str(TOOL), *args], capture_output=True, text=True, env=env)


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.fake = FakeTandoor(SEED)
        self.url = self.fake.start()
        self.addCleanup(self.fake.stop)

    def client(self, url=None, token=TOKEN):
        return tc.Client(tc.load_config({"TANDOOR_URL": url or self.url, "TANDOOR_TOKEN": token}))

    def test_missing_env_raises_not_configured(self):
        with self.assertRaises(tc.NotConfigured):
            tc.load_config({"TANDOOR_URL": "http://x"})
        with self.assertRaises(tc.NotConfigured):
            tc.load_config({"TANDOOR_TOKEN": "t"})

    def test_base_url_subpath(self):
        self.client(self.url + "/recipes/").get("api/food/")
        self.assertEqual(self.fake.requests[-1]["path"], "/recipes/api/food/")

    def test_list_all_counts_pages(self):
        self.fake.stop()
        self.fake = FakeTandoor(seed_with_foods(450))
        url = self.fake.start()
        self.addCleanup(self.fake.stop)
        items = self.client(url).list_all("api/food/")
        self.assertEqual(len(items), 450)
        self.assertEqual(len(self.fake.requests), 3)
        self.assertTrue(all(r["path"] == "/api/food/" for r in self.fake.requests))

    def test_redirect_not_followed(self):
        other = FakeTandoor(SEED)
        other_url = other.start()
        self.addCleanup(other.stop)
        self.fake.redirect_to = other_url + "/api/food/"
        with self.assertRaises(tc.TandoorError) as cm:
            self.client().get("api/food/")
        self.assertEqual(other.requests, [])
        self.assertIn(other_url, str(cm.exception))

    def test_html_response_is_error(self):
        self.fake.html_everywhere = True
        with self.assertRaises(tc.TandoorError) as cm:
            self.client().get("api/food/")
        self.assertIn("TANDOOR_URL", str(cm.exception))

    def test_401_and_403_messages(self):
        with self.assertRaises(tc.TandoorError) as cm:
            self.client(token="wrong").get("api/food/")
        self.assertEqual(cm.exception.status, 401)
        self.assertIn("token", str(cm.exception).lower())
        self.fake.read_only = True
        with self.assertRaises(tc.TandoorError) as cm:
            self.client().post("api/food/", {"name": "X"})
        self.assertEqual(cm.exception.status, 403)
        self.assertIn("write scope", str(cm.exception))

    def test_400_shows_field_errors(self):
        self.fake.can("POST", "api/food/", 400, {"name": ["too long"]})
        with self.assertRaises(tc.TandoorError) as cm:
            self.client().post("api/food/", {"name": "X"})
        self.assertIn('"name"', str(cm.exception))
        self.assertIn("too long", str(cm.exception))
        self.fake.can("POST", "api/food/", 400, {"name": ["x" * 1000]})
        with self.assertRaises(tc.TandoorError) as cm:
            self.client().post("api/food/", {"name": "X"})
        self.assertLessEqual(len(str(cm.exception)), 400)

    def test_token_never_in_output(self):
        errors = []
        with self.assertRaises(tc.TandoorError) as cm:
            self.client(token="wrong-secret-token").get("api/food/")
        errors.append((cm.exception, "wrong-secret-token"))
        self.fake.can("POST", "api/food/", 400, {"detail": f"bad {TOKEN}"})
        with self.assertRaises(tc.TandoorError) as cm:
            self.client().post("api/food/", {"name": "X"})
        errors.append((cm.exception, TOKEN))
        self.fake.stop()
        with self.assertRaises(tc.TandoorError) as cm:
            self.client().get("api/food/")
        errors.append((cm.exception, TOKEN))
        for e, secret in errors:
            self.assertNotIn(secret, str(e))
            self.assertNotIn(secret, repr(e))
        cfg = tc.load_config({"TANDOOR_URL": self.url, "TANDOOR_TOKEN": "s3cret"})
        self.assertNotIn("s3cret", repr(cfg))

    def test_check_cli(self):
        r = cli(self.url, "check")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("OK:", r.stdout)
        self.assertIn(self.url, r.stdout)
        self.assertIn("2.7.2", r.stdout)
        self.assertNotIn(TOKEN, r.stdout + r.stderr)
        r = cli(None, "check", token=None)
        self.assertEqual(r.returncode, 3)

    def test_check_warns_on_http(self):
        r = cli("http://tandoor.invalid", "check")
        self.assertIn("http://", r.stderr)
        self.assertIn("warning", r.stderr.lower())
        ok = cli(self.url, "check")
        self.assertNotIn("warning", ok.stderr.lower())

    def test_check_warns_on_old_version(self):
        self.fake.version = "1.5.3"
        r = cli(self.url, "check")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("warning", r.stderr.lower())


if __name__ == "__main__":
    unittest.main()
