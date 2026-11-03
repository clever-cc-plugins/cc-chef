import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parents[1] / "plugins" / "cc-chef" / "skills" / "_shared" / "scripts"
TOOL = SCRIPTS / "recipe_tool.py"
FIX = HERE / "fixtures"
sys.path.insert(0, str(SCRIPTS))

import recipe_tool as rt  # noqa: E402


def read(name):
    return (FIX / name).read_text(encoding="utf-8")


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(TOOL), *map(str, args)],
        capture_output=True,
        text=True,
    )


class ParseTests(unittest.TestCase):
    def test_parse_rouladen(self):
        r = rt.parse_recipe(read("rouladen.de.md"))
        self.assertEqual(r.title, "Rinderrouladen")
        self.assertEqual(r.meta["servings"], 4)
        self.assertEqual(r.meta["prep-minutes"], 40)
        self.assertEqual(r.meta["cook-minutes"], 120)
        self.assertEqual(r.meta["tags"], ["Hauptgericht", "Schmoren"])
        self.assertEqual(r.meta["language"], "de")
        self.assertTrue(r.meta["source-url"].startswith("https://"))
        self.assertGreaterEqual(len(r.steps), 2)
        step1 = r.steps[0]
        self.assertEqual(step1.number, 1)
        self.assertEqual(step1.title, "Rouladen füllen")
        self.assertEqual(len(step1.ingredients), 6)
        self.assertEqual(
            step1.ingredients[0],
            rt.Ingredient("4", "Scheiben", "Rinderoberschale", "je ca. 180 g"),
        )
        self.assertIn(rt.Ingredient(None, None, "Salz", None), step1.ingredients)
        self.assertIn(rt.Ingredient("4", "Scheiben", "Frühstücksspeck", None), step1.ingredients)
        self.assertIn("Küchengarn", step1.text)
        self.assertTrue(r.description.startswith("Klassische"))
        self.assertTrue(r.notes.startswith("## Hinweise"))
        self.assertIn("Rotkohl", r.notes)

    def test_parse_english(self):
        r = rt.parse_recipe(read("shakshuka.en.md"))
        self.assertEqual(r.title, "Shakshuka")
        self.assertEqual(len(r.steps), 2)
        self.assertEqual(
            r.steps[0].ingredients[7], rt.Ingredient(None, None, "Salt", "a pinch at the start and the rest at the end")
        )

    def test_lenient_amounts(self):
        r = rt.parse_recipe(read("messy.de.md"))
        ings = r.steps[0].ingredients
        self.assertEqual(ings[0], rt.Ingredient("½", "Tasse", "Zucker", None))
        self.assertEqual(ings[1], rt.Ingredient("0,5", "l", "Milch", "warm"))
        self.assertEqual(ings[2], rt.Ingredient("1–2", "EL", "Honig", "nach Geschmack"))
        self.assertEqual(ings[3], rt.Ingredient("2", None, "Eier", None))
        self.assertEqual(ings[4], rt.Ingredient(None, "eine Prise", "Salz", None))
        self.assertEqual(ings[5], rt.Ingredient(None, "etwas", "Petersilie", None))
        self.assertEqual(ings[6], rt.Ingredient("1-2", None, "Knoblauchzehen", None))
        self.assertEqual(ings[7], rt.Ingredient("500", "g", "Mehl", None))
        self.assertEqual(ings[8], rt.Ingredient("2", "EL", "Öl", None))
        self.assertEqual(ings[9], rt.Ingredient("1 ½", "EL", "Butter", None))
        self.assertEqual(ings[10], rt.Ingredient("1 - 2", "EL", "Rum", None))
        self.assertEqual(ings[11], rt.Ingredient("1 1/2", "TL", "Zimt", None))
        self.assertEqual(ings[12], rt.Ingredient("2", "EL", "Sahne", None))
        self.assertEqual(len(ings), 13)
        # bullets after instruction text belong to the text
        self.assertIn("- Dieser Punkt gehört zum Text", r.steps[0].text)
        self.assertEqual(r.steps[1].ingredients, [])
        self.assertEqual(r.steps[1].text, "Bei 180 °C 30 Minuten backen.")

    def test_unknown_frontmatter_kept(self):
        r = rt.parse_recipe(read("messy.de.md"))
        self.assertEqual(r.meta["extra-key"], "something custom")
        self.assertEqual(r.meta["title"], "Quark-Auflauf")
        self.assertEqual(r.meta["tags"], ["Dessert", "Süß"])

    def test_title_falls_back_to_h1(self):
        r = rt.parse_recipe("---\nservings: 2\n---\n\n# Suppe\n\n### 1. Kochen\n\nKochen.\n")
        self.assertEqual(r.title, "Suppe")

    def test_missing_title(self):
        with self.assertRaises(rt.RecipeFormatError):
            rt.parse_recipe("---\nservings: 2\n---\n\n### 1. Kochen\n\nKochen.\n")

    def test_missing_frontmatter(self):
        with self.assertRaises(rt.RecipeFormatError) as c:
            rt.parse_recipe("# Suppe\n\n### 1. Kochen\n")
        self.assertEqual(c.exception.line, 1)

    def test_unclosed_frontmatter(self):
        with self.assertRaises(rt.RecipeFormatError):
            rt.parse_recipe("---\ntitle: X\n\n# X\n")

    def test_no_steps(self):
        with self.assertRaises(rt.RecipeFormatError):
            rt.parse_recipe("---\ntitle: X\n---\n\n# X\n\nNur Text.\n")

    def test_step_numbers_out_of_order(self):
        with self.assertRaises(rt.RecipeFormatError) as c:
            rt.parse_recipe("---\ntitle: X\n---\n\n### 1. A\n\nx\n\n### 3. B\n\ny\n")
        self.assertEqual(c.exception.line, 9)


class IngredientTests(unittest.TestCase):
    def test_plain_fractions_and_nbsp(self):
        cases = {
            "- **1/2 TL** x": ("1/2", "TL"),
            "- **3/4 l** x": ("3/4", "l"),
            "- **1/2** x": ("1/2", None),
            "- **2\u00a0EL** x": ("2", "EL"),
            "- **1 1/2 TL** x": ("1 1/2", "TL"),
        }
        for line, expected in cases.items():
            with self.subTest(line=line):
                ing = rt._parse_ingredient(line, 1)
                self.assertEqual((ing.amount, ing.unit), expected)


class CliTests(unittest.TestCase):
    def test_validate_ok(self):
        p = run_cli("validate", FIX / "rouladen.de.md")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertTrue(p.stdout.startswith("OK: Rinderrouladen, 3 steps, "))

    def test_validate_reports_line(self):
        p = run_cli("validate", FIX / "broken.md")
        self.assertEqual(p.returncode, 1)
        self.assertIn("broken.md:10:", p.stdout + p.stderr)

    def test_validate_missing_file(self):
        p = run_cli("validate", FIX / "nope.md")
        self.assertEqual(p.returncode, 1)
        self.assertIn("nope.md:", p.stderr)
        self.assertNotIn("Traceback", p.stderr)

    def test_validate_non_utf8(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "x.md"
            f.write_bytes(b"---\ntitle: \xff\xfe\n---\n")
            p = run_cli("validate", f)
            self.assertEqual(p.returncode, 1)
            self.assertNotIn("Traceback", p.stderr)

    def test_validate_bom(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "x.md"
            f.write_bytes(b"\xef\xbb\xbf" + (FIX / "shakshuka.en.md").read_bytes())
            p = run_cli("validate", f)
            self.assertEqual(p.returncode, 0, p.stderr)

    def test_newpath(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "kasespatzle.md").write_text("x")
            p = run_cli("newpath", d, "Käsespätzle")
            self.assertEqual(p.returncode, 0)
            self.assertEqual(p.stdout.strip(), str(Path(d) / "kasespatzle-2.md"))


class SlugTests(unittest.TestCase):
    def test_slug(self):
        self.assertEqual(rt.slugify("Käsespätzle"), "kasespatzle")
        self.assertEqual(rt.slugify("Bœuf bourguignon"), "boeuf-bourguignon")
        self.assertEqual(rt.slugify("Weißwurst & Brezn!"), "weisswurst-brezn")
        self.assertEqual(rt.slugify("肉じゃが"), "recipe")

    def test_unique_path(self):
        with tempfile.TemporaryDirectory() as d:
            folder = Path(d)
            self.assertEqual(rt.unique_path(folder, "a"), folder / "a.md")
            (folder / "a.md").write_text("x")
            self.assertEqual(rt.unique_path(folder, "a"), folder / "a-2.md")
            (folder / "a-2.md").write_text("x")
            self.assertEqual(rt.unique_path(folder, "a"), folder / "a-3.md")


if __name__ == "__main__":
    unittest.main()
