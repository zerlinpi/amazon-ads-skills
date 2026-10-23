"""Global Sponsored Products read-side identity regression tests.

All account identifiers are synthetic; no connector calls or Ads mutations.
"""
import copy
import json
import unittest
from pathlib import Path

from scripts.compare_control_state import compare_control_state


ROOT = Path(__file__).resolve().parents[1]


def snapshot():
    return {
        "scope": {"marketplace_id": "ATVPDKIKX0DER", "profile_id": "synthetic-profile"},
        "observed_at": "2026-10-23T00:00:00Z",
        "source": {"source_system": "fixture", "acquisition_channel": "test"},
        "coverage": {
            "required_control_types": ["base_bid"],
            "coverage_status": "Complete",
            "requirement_provenance": {
                "decision_surface": "fixture_control_comparison",
                "derivation_status": "Verified",
                "requirement_registry_id": "control-requirements@2026-09-29",
            },
        },
        "controls": [{
            "control_type": "base_bid",
            "state": 1.0,
            "effective_at": "2026-10-22T00:00:00Z",
            "evidence_status": "observed",
        }],
    }


def with_identity(record, **identity):
    record["scope"]["account_identity"] = identity
    return record


class GlobalSpControlIdentityTests(unittest.TestCase):
    def assert_unknown(self, before, after):
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_legacy_profile_snapshots_remain_comparable(self):
        self.assertEqual(compare_control_state(snapshot(), snapshot())["classification"], "Comparable")

    def test_explicit_global_account_collision_with_same_profile_fails_closed(self):
        before = with_identity(snapshot(), global_advertiser_account_id="global-a")
        after = with_identity(snapshot(), global_advertiser_account_id="global-b")
        self.assert_unknown(before, after)

    def test_one_sided_account_identity_fails_closed(self):
        before = with_identity(snapshot(), global_advertiser_account_id="global-a")
        self.assert_unknown(before, snapshot())

    def test_global_sp_without_profile_same_verified_global_account_is_comparable(self):
        before = with_identity(snapshot(), global_advertiser_account_id="global-a", country_code="US")
        after = copy.deepcopy(before)
        before["scope"].pop("profile_id")
        after["scope"].pop("profile_id")
        self.assertEqual(compare_control_state(before, after)["classification"], "Comparable")

    def test_global_sp_without_profile_different_global_account_is_unknown(self):
        before = with_identity(snapshot(), global_advertiser_account_id="global-a")
        after = with_identity(snapshot(), global_advertiser_account_id="global-b")
        before["scope"].pop("profile_id")
        after["scope"].pop("profile_id")
        self.assert_unknown(before, after)

    def test_global_sp_with_only_manager_account_is_unknown(self):
        before = with_identity(snapshot(), manager_account_id="manager-a")
        after = copy.deepcopy(before)
        before["scope"].pop("profile_id")
        after["scope"].pop("profile_id")
        self.assert_unknown(before, after)

    def test_global_sp_with_conflicting_regional_identity_is_unknown(self):
        before = with_identity(snapshot(), global_advertiser_account_id="global-a", regional_advertiser_account_id="regional-a")
        after = with_identity(snapshot(), global_advertiser_account_id="global-a", regional_advertiser_account_id="regional-b")
        before["scope"].pop("profile_id")
        after["scope"].pop("profile_id")
        self.assert_unknown(before, after)

    def test_explicit_country_context_collision_is_unknown(self):
        before = with_identity(snapshot(), global_advertiser_account_id="global-a", country_code="US")
        after = with_identity(snapshot(), global_advertiser_account_id="global-a", country_code="CA")
        self.assert_unknown(before, after)

    def test_missing_profile_and_account_identity_fails_closed(self):
        before, after = snapshot(), snapshot()
        before["scope"].pop("profile_id")
        after["scope"].pop("profile_id")
        self.assert_unknown(before, after)

    def test_schema_accepts_global_identity_without_inventing_profile(self):
        schema = json.loads((ROOT / "schemas/control-state-snapshot.json").read_text(encoding="utf-8"))
        scope = schema["properties"]["scope"]
        self.assertIn("account_identity", scope["properties"])
        self.assertNotIn("profile_id", scope["required"])
        self.assertTrue(scope.get("anyOf"), "profile or verified global-account identity must be required")


if __name__ == "__main__":
    unittest.main()
