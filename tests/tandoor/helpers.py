import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parents[1] / "plugins" / "cc-chef" / "skills" / "_shared" / "scripts"
TOOL = SCRIPTS / "tandoor.py"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(HERE))

from fake_tandoor import FakeTandoor  # noqa: E402

SEED = json.loads((HERE / "fixtures" / "seed.json").read_text(encoding="utf-8"))
TOKEN = "test-token"


def cli(url, *args, token=TOKEN):
    env = {k: v for k, v in os.environ.items() if not k.startswith("TANDOOR_")}
    if url is not None:
        env["TANDOOR_URL"] = url
    if token is not None:
        env["TANDOOR_TOKEN"] = token
    return subprocess.run([sys.executable, str(TOOL), *map(str, args)], capture_output=True, text=True, env=env)


class FakeCase(unittest.TestCase):
    """A fake instance, a scratch folder and a copy of the fixture recipe per test."""

    seed = SEED

    def setUp(self):
        self.fake = FakeTandoor(json.loads(json.dumps(self.seed)))
        self.url = self.fake.start()
        self.addCleanup(self.fake.stop)
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.recipe = self.tmp / "upload.de.md"
        shutil.copy(HERE / "fixtures" / "upload.de.md", self.recipe)
        self.plan_path = self.tmp / "plan.json"

    def run_cli(self, *args, url=None):
        return cli(url or self.url, *args)

    def plan(self):
        return json.loads(self.plan_path.read_text(encoding="utf-8"))

    def writes(self, fake=None):
        return [r for r in (fake or self.fake).requests if r["method"] != "GET"]

    def match(self):
        r = self.run_cli("match", self.recipe, "-o", self.plan_path)
        self.assertEqual(r.returncode, 0, r.stderr)
        return r

    def resolve_all(self):
        for args in (("food", "Zwiebelchen", "--id", "7"), ("food", "Drachenfrucht", "--create")):
            r = self.run_cli("resolve", self.plan_path, "--kind", args[0], "--text", args[1], *args[2:])
            self.assertEqual(r.returncode, 0, r.stderr)

    def digest(self):
        r = self.run_cli("preview", self.plan_path)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return r.stdout.split("Confirm: ")[1].split()[0]
