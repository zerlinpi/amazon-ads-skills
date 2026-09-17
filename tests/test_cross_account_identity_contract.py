import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDENTITY = ROOT / "references/cross-account-identity.md"


class CrossAccountIdentityContractTests(unittest.TestCase):
    def test_reference_requires_composite_identity_for_multi_account_reporting(self):
        self.assertTrue(IDENTITY.exists(), "missing cross-account identity reference")
        text = IDENTITY.read_text(encoding="utf-8")
        for token in (
            "advertiser_account_id",
            "manager_account_id",
            "country_code",
            "regional_profile_id",
            "entity_id alone",
            "identity collision",
        ):
            self.assertIn(token, text)

    def test_missing_identity_blocks_entity_specific_join_or_action(self):
        text = IDENTITY.read_text(encoding="utf-8")
        self.assertIn("Do not deduplicate", text)
        self.assertIn("entity-specific action", text)
        self.assertIn("Missing Data", text)


if __name__ == "__main__":
    unittest.main()
