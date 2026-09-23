import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "references/multi-touch-attribution.md"


class MultiTouchAttributionPolicyTests(unittest.TestCase):
    def test_shared_reference_exists_and_separates_attribution_variants(self):
        self.assertTrue(REFERENCE.is_file())
        text = REFERENCE.read_text(encoding="utf-8").lower()
        self.assertIn("multi-touch", text)
        self.assertIn("last-touch", text)
        self.assertIn("attribution_variant", text)
        self.assertIn("not interchangeable", text)

    def test_mta_availability_is_scoped_not_assumed_global(self):
        text = REFERENCE.read_text(encoding="utf-8").lower()
        self.assertIn("united states", text)
        self.assertIn("most report types", text)
        self.assertIn("marketing stream conversion", text)
        self.assertIn("connector", text)
        self.assertIn("missing", text)
        self.assertIn("zero", text)

    def test_unreconciled_variant_shift_is_not_business_cause(self):
        text = REFERENCE.read_text(encoding="utf-8").lower()
        self.assertIn("observation", text)
        self.assertIn("hypothesis", text)
        self.assertIn("not comparable", text)
        self.assertIn("do not use the unreconciled delta alone", text)


if __name__ == "__main__":
    unittest.main()
