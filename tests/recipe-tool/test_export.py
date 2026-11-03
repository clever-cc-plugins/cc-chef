import gzip
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from test_recipe_tool import FIX, read, run_cli, rt


def make(meta_extra="", title="Suppe"):
    return rt.parse_recipe(
        f"---\ncc-chef: 1\ntitle: {title}\n{meta_extra}---\n\n# {title}\n\n## Zubereitung\n\n"
        "### 1. Kochen\n\n- **1 l** Wasser\n\nKochen.\n"
    )


class ExportTests(unittest.TestCase):
    def test_ingredient_line(self):
        self.assertEqual(rt.ingredient_line(rt.Ingredient("200", "g", "Mehl", "gesiebt")), "200 g Mehl, gesiebt")
        self.assertEqual(rt.ingredient_line(rt.Ingredient(None, None, "Salz", None)), "Salz")
        self.assertEqual(rt.ingredient_line(rt.Ingredient("2", None, "Eier", None)), "2 Eier")

    def test_jsonld_rouladen(self):
        r = rt.parse_recipe(read("rouladen.de.md"))
        d = rt.to_jsonld(r)
        self.assertEqual(d["@type"], "Recipe")
        self.assertEqual(d["recipeYield"], "4")
        self.assertEqual(d["prepTime"], "PT40M")
        self.assertEqual(d["cookTime"], "PT2H")
        self.assertEqual(d["totalTime"], "PT2H40M")
        self.assertEqual(len(d["recipeInstructions"]), len(r.steps))
        self.assertEqual(d["inLanguage"], "de")
        self.assertEqual(d["keywords"], "Hauptgericht, Schmoren")
        self.assertEqual(d["isBasedOn"], "https://example.com/rinderrouladen")
        self.assertEqual(d["recipeInstructions"][0]["@type"], "HowToStep")

    def test_jsonld_omits_empty_and_bad_times(self):
        d = rt.to_jsonld(make("prep-minutes: viel\ncook-minutes: 30\nservings: vier\n"))
        self.assertNotIn("prepTime", d)
        self.assertNotIn("totalTime", d)
        self.assertEqual(d["cookTime"], "PT30M")
        self.assertEqual(d["recipeYield"], "vier")
        self.assertNotIn("isBasedOn", d)
        self.assertNotIn("description", d)

    def test_paprika_times_and_hash(self):
        p = rt.to_paprika(make("prep-minutes: 5\ncook-minutes: 120\n"))
        self.assertEqual((p["prep_time"], p["cook_time"], p["total_time"]), ("5 min", "120 min", "125 min"))
        self.assertEqual(p["servings"], "")
        self.assertEqual(p["ingredients"], "Kochen:\n1 l Wasser")
        self.assertEqual(p["directions"], "1. Kochen\nKochen.")
        h = p.pop("hash")
        self.assertEqual(len(h), 64)

    def test_paprika_archive_roundtrip(self):
        with tempfile.TemporaryDirectory() as t:
            out = Path(t) / "out.paprikarecipes"
            res = run_cli("paprika", FIX / "rouladen.de.md", "-o", out)
            self.assertEqual(res.returncode, 0, res.stderr)
            with zipfile.ZipFile(out) as z:
                names = z.namelist()
                self.assertEqual(names, ["rinderrouladen.paprikarecipe"])
                d = json.loads(gzip.decompress(z.read(names[0])).decode("utf-8"))
        self.assertEqual(d["name"], "Rinderrouladen")
        self.assertTrue(d["ingredients"].split("\n")[0].endswith(":"))
        self.assertEqual(d["categories"], ["Hauptgericht", "Schmoren"])

    def test_paprika_duplicate_slugs(self):
        with tempfile.TemporaryDirectory() as t:
            out = Path(t) / "out.paprikarecipes"
            f = FIX / "rouladen.de.md"
            res = run_cli("paprika", f, f, "-o", out)
            self.assertEqual(res.returncode, 0, res.stderr)
            with zipfile.ZipFile(out) as z:
                self.assertEqual(z.namelist(), ["rinderrouladen.paprikarecipe", "rinderrouladen-2.paprikarecipe"])

    def test_paprika_parse_failure_writes_nothing(self):
        with tempfile.TemporaryDirectory() as t:
            bad = Path(t) / "bad.md"
            bad.write_text("no frontmatter", encoding="utf-8")
            out = Path(t) / "out.paprikarecipes"
            res = run_cli("paprika", FIX / "rouladen.de.md", bad, "-o", out)
            self.assertEqual(res.returncode, 1)
            self.assertIn(f"{bad}:1:", res.stderr)
            self.assertFalse(out.exists())

    def test_jsonld_cli(self):
        with tempfile.TemporaryDirectory() as t:
            out = Path(t) / "out.json"
            self.assertEqual(run_cli("jsonld", FIX / "rouladen.de.md", "-o", out).returncode, 0)
            self.assertEqual(json.loads(out.read_text(encoding="utf-8"))["name"], "Rinderrouladen")
        res = run_cli("jsonld", FIX / "rouladen.de.md")
        self.assertEqual(json.loads(res.stdout)["@type"], "Recipe")


if __name__ == "__main__":
    unittest.main()
