import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINEAGE = ROOT / "references/data-lineage.md"
SCHEMA = ROOT / "references/data-schema.md"


class CrossAccountIdentityContractTests(unittest.TestCase):
    def test_lineage_requires_composite_identity_for_multi_account_reporting(self):
        text = LINEAGE.read_text(encoding="utf-8")
        for token in (
            "advertiser_account_id",
            "manager_account_id",
            "country_code",
            "regional_profile_id",
            "entity_id alone",
            "identity collision",
        ):
            self.assertIn(token, text)

    def test_schema_exposes_cross_account_identity_dimensions(self):
        text = SCHEMA.read_text(encoding="utf-8")
        for token in (
            '"advertiser_account_id"',
            '"manager_account_id"',
            '"country_code"',
            '"regional_profile_id"',
        ):
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
