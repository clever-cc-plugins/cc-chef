import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parents[1] / "plugins" / "cc-chef" / "skills" / "_shared" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import recipe_tool as rt  # noqa: E402
import tandoor_model as tm  # noqa: E402

FIX = HERE.parent / "recipe-tool" / "fixtures"


def rouladen():
    return rt.parse_recipe((FIX / "rouladen.de.md").read_text(encoding="utf-8"))


def mini(ingredient="- **1 l** Wasser", title="Suppe", meta="", notes=""):
    return rt.parse_recipe(
        f"---\ncc-chef: 1\ntitle: {title}\n{meta}---\n\n# {title}\n\n## Zubereitung\n\n"
        f"### 1. Kochen\n\n{ingredient}\n\nKochen.\n\n{notes}"
    )


class ModelTests(unittest.TestCase):
    def test_parse_amount(self):
        for raw, want in [("½", (.5, None)), ("0,5", (.5, None)), ("1 1/2", (1.5, None)), ("1–2", (1.0, 2.0)), ("1-2", (1.0, 2.0)), (None, (None, None))]:
            self.assertEqual(tm.parse_amount(raw), want, raw)

    def test_normalize(self):
        self.assertEqual(tm.normalize("  Zwiebel \t"), "zwiebel")
        self.assertEqual(tm.normalize("Käse"), tm.normalize("Käse"))

    def test_no_amount(self):
        ing = tm.to_payload(mini("- Salz"))["steps"][0]["ingredients"][0]
        self.assertEqual((ing["amount"], ing["no_amount"], ing["unit"]), (0, True, None))
        self.assertEqual(ing["food"], {"text": "Salz"})

    def test_range_goes_to_note(self):
        ing = tm.to_payload(mini("- **1–2 EL** Öl, kalt"))["steps"][0]["ingredients"][0]
        self.assertEqual(ing["amount"], 1.0)
        self.assertEqual(ing["note"], "1–2 EL, kalt")
        self.assertEqual(ing["unit"], {"text": "EL"})

    def test_payload_rouladen(self):
        p = tm.to_payload(rouladen())
        self.assertEqual(len(p["steps"]), 4)
        self.assertEqual([s["order"] for s in p["steps"]], [0, 1, 2, 3])
        self.assertEqual(len(p["steps"][0]["ingredients"]), 6)
        self.assertEqual(p["steps"][0]["name"], "Rouladen füllen")
        self.assertTrue(all(s["show_as_header"] and s["time"] == 0 for s in p["steps"]))
        self.assertEqual((p["working_time"], p["waiting_time"]), (40, 120))
        self.assertEqual((p["name"], p["servings"], p["servings_text"]), ("Rinderrouladen", 4, ""))
        self.assertEqual(p["source_url"], "https://example.com/rinderrouladen")

    def test_servings_text_when_not_integer(self):
        p = tm.to_payload(mini(meta="servings: 4–6 Portionen\n"))
        self.assertEqual((p["servings"], p["servings_text"]), (1, "4–6 Portionen"))

    def test_notes_step(self):
        last = tm.to_payload(rouladen())["steps"][-1]
        self.assertEqual(last["name"], "Hinweise")
        self.assertEqual(last["ingredients"], [])
        self.assertFalse(last["show_ingredients_table"])
        text = last["instruction"]
        for part in ("160 °C Ober-/Unterhitze", "Ein Löffel Gurkenwasser", "Beispielautorin", "Kartoffelklöße"):
            self.assertIn(part, text)
        self.assertLess(text.index("160 °C"), text.index("Ein Löffel"))
        self.assertLess(text.index("Ein Löffel"), text.index("Beispielautorin"))
        self.assertLess(text.index("Beispielautorin"), text.index("Kartoffelklöße"))
        self.assertNotIn("## ", text)

    def test_notes_step_default_name(self):
        p = tm.to_payload(mini(meta="oven: 180 °C\n"))
        self.assertEqual(p["steps"][-1]["name"], "Notes")

    def test_no_notes_step_when_empty(self):
        self.assertEqual(len(tm.to_payload(mini())["steps"]), 1)

    def test_marker_keyword_always_present(self):
        kws = [k["text"] for k in tm.to_payload(rouladen())["keywords"]]
        self.assertEqual(kws, ["Hauptgericht", "Schmoren", tm.MARKER])
        self.assertEqual([k["text"] for k in tm.to_payload(mini())["keywords"]], [tm.MARKER])

    def test_finalize_uses_database_name(self):
        p = tm.to_payload(mini("- **2** Zwiebeln"))
        out = tm.finalize(
            p,
            {tm.normalize("Zwiebeln"): {"id": 7, "name": "Zwiebel", "extra": 1}},
            {},
            {tm.normalize(tm.MARKER): {"id": 3, "name": tm.MARKER}},
        )
        ing = out["steps"][0]["ingredients"][0]
        self.assertEqual(ing["food"], {"id": 7, "name": "Zwiebel"})
        self.assertEqual(out["keywords"], [{"id": 3, "name": tm.MARKER}])
        self.assertIn("text", p["steps"][0]["ingredients"][0]["food"])  # input untouched

    def test_finalize_refuses_unresolved(self):
        p = tm.to_payload(mini("- **2** Zwiebeln"))
        with self.assertRaises(ValueError):
            tm.finalize(p, {}, {}, {tm.normalize(tm.MARKER): {"id": 3, "name": tm.MARKER}})
        with self.assertRaises(ValueError):
            tm.finalize(tm.to_payload(mini()), {tm.normalize("Wasser"): {"id": 1, "name": "Wasser"}}, {}, {})

    def test_limit_problems(self):
        p = tm.to_payload(mini("- **1 l** Wasser, " + "n" * 260, title="T" * 129))
        p["description"] = "d" * 513
        p["steps"][0]["name"] = "s" * 129
        problems = tm.limit_problems(p)
        self.assertEqual(len(problems), 4, problems)
        joined = " ".join(problems)
        self.assertIn("step 1", joined)
        self.assertIn("Wasser", joined)
        self.assertEqual(tm.limit_problems(tm.to_payload(rouladen())), [])

    def test_render_source(self):
        recipe = {
            "name": "Kuchen", "description": "Saftig", "source_url": "https://example.com/k", "servings": 4,
            "steps": [
                {"name": "Teig", "order": 0, "instruction": "Rühren.", "step_recipe": None, "file": None, "ingredients": [
                    {"is_header": True, "note": "Für den Teig", "food": None, "unit": None, "amount": 0, "no_amount": True},
                    {"is_header": False, "amount": 200.0, "unit": {"name": "g"}, "food": {"name": "Mehl"}, "note": "gesiebt", "no_amount": False},
                    {"is_header": False, "amount": 0, "unit": None, "food": {"name": "Salz"}, "note": "", "no_amount": True},
                ]},
                {"name": "Backen", "order": 1, "instruction": "Backen.", "step_recipe": 5, "file": {"id": 1}, "ingredients": []},
            ],
        }
        out = tm.render_source(recipe)
        self.assertIn("Teig", out)
        self.assertIn("200 g Mehl, gesiebt", out)
        self.assertIn("[heading] Für den Teig", out)
        self.assertIn("Salz", out)
        self.assertIn("[embedded recipe]", out)
        self.assertIn("[file]", out)
        self.assertIn("https://example.com/k", out)

    def test_read_back_diff(self):
        def rec(*steps):
            return {"steps": [{"ingredients": list(s)} for s in steps]}

        def ing(food, unit, amount):
            return {"food": {"id": food}, "unit": {"id": unit} if unit else None, "amount": amount}

        sent = rec([ing(7, 1, 200.0), ing(8, None, 0)], [ing(9, 2, 1.5)])
        self.assertEqual(tm.read_back_diff(sent, rec([ing(7, 1, "200.0"), ing(8, None, 0)], [ing(9, 2, 1.5)])), [])
        self.assertEqual(len(tm.read_back_diff(sent, rec([ing(7, 1, 200.0), ing(8, None, 0)]))), 1)
        diff = tm.read_back_diff(sent, rec([ing(7, 1, 200.0), ing(99, None, 0)], [ing(9, 2, 1.5)]))
        self.assertEqual(len(diff), 1)
        self.assertIn("food", diff[0])
        self.assertEqual(len(tm.read_back_diff(sent, rec([ing(7, 1, 200.0)], [ing(9, 2, 1.5)]))), 1)


if __name__ == "__main__":
    unittest.main()
