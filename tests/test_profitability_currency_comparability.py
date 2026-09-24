import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ProfitabilityCurrencyComparabilityTests(unittest.TestCase):
    def read_skill(self) -> str:
        return (ROOT / "skills/profitability-analysis/SKILL.md").read_text(encoding="utf-8")

    def test_profitability_requires_currency_lineage_before_combining_money(self):
        text = self.read_skill().lower()
        self.assertIn("currency lineage", text)
        self.assertIn("native_currency", text)
        self.assertIn("reporting_currency", text)
        self.assertIn("currency_conversion_status", text)

    def test_unreconciled_currency_treatment_blocks_profitability_claims(self):
        text = self.read_skill().lower()
        self.assertIn("not comparable", text)
        self.assertIn("do not compute", text)
        self.assertIn("profit after ads", text)
        self.assertIn("break-even acos", text)


if __name__ == "__main__":
    unittest.main()
