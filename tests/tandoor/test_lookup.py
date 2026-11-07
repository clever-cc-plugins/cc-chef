import unittest

from helpers import FakeCase, cli


class LookupTests(FakeCase):
    def test_lookup_reports_each_text_and_writes_nothing(self):
        r = self.run_cli("lookup", "--food", "zwiebeln", "Passata", "Zwiebelchen", "Drachenfrucht")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("food 'zwiebeln': use 'Zwiebel'", r.stdout)
        self.assertIn("food 'Passata': use 'Passierte Tomaten'", r.stdout)  # alias
        self.assertIn("food 'Zwiebelchen': no confident match, similar: 'Zwiebel'", r.stdout)
        self.assertIn("food 'Drachenfrucht': not in the database", r.stdout)
        self.assertEqual(self.writes(), [])

    def test_lookup_units(self):
        r = self.run_cli("lookup", "--unit", "Unbekannteeinheit")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("unit 'Unbekannteeinheit': not in the database", r.stdout)

    def test_lookup_not_configured(self):
        self.assertEqual(cli(None, "lookup", "--food", "x", token=None).returncode, 3)


if __name__ == "__main__":
    unittest.main()
