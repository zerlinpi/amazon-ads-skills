import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CROSS_ACCOUNT = ROOT / "references" / "cross-account-identity.md"


class CurrencyConversionLineagePolicyTests(unittest.TestCase):
    def test_cross_country_currency_conversion_preserves_measurement_identity(self):
        text = CROSS_ACCOUNT.read_text(encoding="utf-8").lower()
        for concept in (
            "native_currency",
            "reporting_currency",
            "currency_conversion_status",
            "currency conversion timing",
        ):
            self.assertIn(concept, text)

    def test_converted_money_is_not_treated_as_native_money_without_provenance(self):
        text = CROSS_ACCOUNT.read_text(encoding="utf-8").lower()
        self.assertIn("converted", text)
        self.assertIn("not comparable", text)
        self.assertIn("exchange-rate", text)
        self.assertIn("unknown", text)


if __name__ == "__main__":
    unittest.main()
