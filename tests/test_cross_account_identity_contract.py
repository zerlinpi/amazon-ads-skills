import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDENTITY = ROOT / "references/cross-account-identity.md"
EVENT_SCHEMA = ROOT / "schemas/optimization-event.json"


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

    def test_global_advertiser_upgrade_preserves_global_regional_and_legacy_identity(self):
        text = IDENTITY.read_text(encoding="utf-8")
        for token in (
            "global_advertiser_account_id",
            "regional_advertiser_account_id",
            "legacy_advertiser_account_id",
            "identity_mapping_provenance",
        ):
            self.assertIn(token, text)

    def test_optimization_event_can_persist_account_identity_envelope(self):
        schema = json.loads(EVENT_SCHEMA.read_text(encoding="utf-8"))
        props = schema["properties"]
        self.assertIn("account_identity", props)
        identity_props = props["account_identity"]["properties"]
        for field in (
            "global_advertiser_account_id",
            "regional_advertiser_account_id",
            "legacy_advertiser_account_id",
            "regional_profile_id",
            "country_code",
            "identity_mapping_provenance",
        ):
            self.assertIn(field, identity_props)


if __name__ == "__main__":
    unittest.main()
