import json
import os
import tempfile
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parents[1] / "plugins" / "cc-chef" / "skills" / "_shared" / "scripts"
TOOL = SCRIPTS / "tandoor.py"
NO_DOTENV = "/nonexistent/.env"
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
        env["TANDOOR_API_TOKEN"] = token
    with tempfile.TemporaryDirectory() as cwd:  # empty, so a real .env in the repo is never read
        return subprocess.run([sys.executable, str(TOOL), *args], capture_output=True, text=True, env=env, cwd=cwd)


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.fake = FakeTandoor(SEED)
        self.url = self.fake.start()
        self.addCleanup(self.fake.stop)

    def client(self, url=None, token=TOKEN):
        return tc.Client(tc.load_config({"TANDOOR_URL": url or self.url, "TANDOOR_API_TOKEN": token}))

    def test_config_from_dotenv_file(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, ".env")
            with open(path, "w") as f:
                f.write('# c\nTANDOOR_URL=http://x/\nexport TANDOOR_API_TOKEN="tok"\n')
            cfg = tc.load_config({}, path)
            self.assertEqual((cfg.url, cfg.token), ("http://x", "tok"))
            # a partly set environment is never completed from .env
            with self.assertRaises(tc.NotConfigured):
                tc.load_config({"TANDOOR_API_TOKEN": "env"}, path)
            with self.assertRaises(tc.NotConfigured):
                tc.load_config({"TANDOOR_URL": "http://other"}, path)
            self.assertEqual(tc.load_config({"TANDOOR_URL": "http://o", "TANDOOR_API_TOKEN": "env"}, path).token, "env")
            with self.assertRaises(tc.NotConfigured):
                tc.load_config({}, os.path.join(d, "missing.env"))

    def test_missing_env_raises_not_configured(self):
        with self.assertRaises(tc.NotConfigured):
            tc.load_config({"TANDOOR_URL": "http://x"}, NO_DOTENV)
        with self.assertRaises(tc.NotConfigured):
            tc.load_config({"TANDOOR_API_TOKEN": "t"}, NO_DOTENV)

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
        cfg = tc.load_config({"TANDOOR_URL": self.url, "TANDOOR_API_TOKEN": "s3cret"})
        self.assertNotIn("s3cret", repr(cfg))

    def test_cli_reads_dotenv_in_working_directory(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, ".env"), "w") as f:
                f.write(f"TANDOOR_URL={self.url}\nTANDOOR_API_TOKEN={TOKEN}\n")
            env = {k: v for k, v in os.environ.items() if not k.startswith("TANDOOR_")}
            r = subprocess.run([sys.executable, str(TOOL), "check"], capture_output=True, text=True, env=env, cwd=d)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("OK:", r.stdout)
        self.assertNotIn(TOKEN, r.stdout + r.stderr)

    def test_a_read_is_repeated_after_a_dropped_connection(self):
        client = self.client()
        client.retry_delay = 0
        self.fake.drop = 2
        self.assertEqual(client.get("api/server-settings/current/")["version"], "2.7.2")
        self.assertEqual(self.fake.drop, 0)

    def test_a_read_gives_up_after_three_attempts(self):
        client = self.client()
        client.retry_delay = 0
        self.fake.drop = 4
        with self.assertRaisesRegex(tc.TandoorError, "cannot reach"):
            client.get("api/server-settings/current/")
        self.assertEqual(self.fake.drop, 1)

    def test_a_write_is_never_repeated(self):
        client = self.client()
        client.retry_delay = 0
        self.fake.drop = 2
        with self.assertRaisesRegex(tc.TandoorError, "cannot reach"):
            client.post("api/food/", {"name": "Test"})
        self.assertEqual(self.fake.drop, 1)

    def test_an_error_answer_is_not_repeated(self):
        client = self.client(token="wrong")
        client.retry_delay = 0
        with self.assertRaises(tc.TandoorError) as caught:
            client.get("api/food/")
        self.assertEqual(caught.exception.status, 401)
        self.assertEqual(len([r for r in self.fake.requests if r["path"].endswith("/api/food/")]), 1)

    def test_check_cli(self):
        r = cli(self.url, "check")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("OK:", r.stdout)
        self.assertIn(self.url, r.stdout)
        self.assertIn("2.7.2", r.stdout)
        self.assertNotIn(TOKEN, r.stdout + r.stderr)
        r = cli(None, "check", token=None)
        self.assertEqual(r.returncode, 3)

    def test_url_without_scheme_is_a_setup_error_not_a_traceback(self):
        r = cli("tandoor.example.com", "check")
        self.assertEqual(r.returncode, 3)
        self.assertIn("http://", r.stderr)
        self.assertNotIn("Traceback", r.stderr)

    def test_every_command_warns_on_http_not_only_check(self):
        r = cli("http://tandoor.invalid", "recipes")
        self.assertIn("plain http://", r.stderr)
        self.assertNotIn("plain http://", cli(self.url, "recipes").stderr)

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
