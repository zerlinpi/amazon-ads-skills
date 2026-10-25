"""RED-first: repeated missing identity/source labels cannot prove causal isolation.

Synthetic snapshots only. No live Amazon Ads requests or mutations.
"""
import copy
import unittest

from scripts.compare_control_state import compare_control_state


def snapshot():
    return {
        "scope": {"marketplace_id": "ATVPDKIKX0DER", "profile_id": "synthetic-profile",
                  "campaign_id": "campaign-1", "entity_id": "keyword-1",
                  "entity_type": "keyword"},
        "observed_at": "2026-10-25T03:00:00Z",
        "source": {"source_system": "synthetic-ads-api",
                   "acquisition_channel": "synthetic-connector",
                   "connector_id": "connector-a"},
        "coverage": {
            "required_control_types": ["base_bid"],
            "coverage_status": "Complete",
            "requirement_provenance": {
                "decision_surface": "fixture_control_comparison",
                "derivation_status": "Verified",
                "requirement_registry_id": "control-requirements@2026-09-29",
            },
        },
        "controls": [{"control_type": "base_bid", "state": 1.0,
                      "effective_at": "2026-10-24T03:00:00Z",
                      "evidence_status": "observed"}],
    }


def compare_with_placeholder(section, key, value):
    before, after = snapshot(), snapshot()
    before[section][key] = copy.deepcopy(value)
    after[section][key] = copy.deepcopy(value)
    after["controls"][0]["state"] = 1.2
    return compare_control_state(before, after, "base_bid")


def compare_account_identity(key, value):
    before, after = snapshot(), snapshot()
    for snap in (before, after):
        snap["scope"]["account_identity"] = {
            "global_advertiser_account_id": "global-account-1",
            key: value,
        }
    after["controls"][0]["state"] = 1.2
    return compare_control_state(before, after, "base_bid")


class ScopeSourcePlaceholderEvidenceTests(unittest.TestCase):
    def assert_unknown(self, result):
        self.assertEqual(result["classification"], "Unknown", result)

    def test_repeated_unknown_marketplace_is_not_isolation(self):
        self.assert_unknown(compare_with_placeholder("scope", "marketplace_id", "Unknown"))

    def test_repeated_unsupported_marketplace_is_not_isolation(self):
        self.assert_unknown(compare_with_placeholder("scope", "marketplace_id", "Unsupported"))

    def test_repeated_partial_profile_is_not_isolation(self):
        self.assert_unknown(compare_with_placeholder("scope", "profile_id", "Partial"))

    def test_repeated_missing_profile_is_not_isolation(self):
        self.assert_unknown(compare_with_placeholder("scope", "profile_id", "Missing"))

    def test_repeated_not_available_campaign_is_not_isolation(self):
        self.assert_unknown(compare_with_placeholder("scope", "campaign_id", "Not Available"))

    def test_repeated_unknown_entity_id_is_not_isolation(self):
        self.assert_unknown(compare_with_placeholder("scope", "entity_id", "Unknown"))

    def test_repeated_unsupported_entity_type_is_not_isolation(self):
        self.assert_unknown(compare_with_placeholder("scope", "entity_type", "Unsupported"))

    def test_repeated_unknown_source_system_is_not_isolation(self):
        self.assert_unknown(compare_with_placeholder("source", "source_system", "Unknown"))

    def test_repeated_partial_acquisition_channel_is_not_isolation(self):
        self.assert_unknown(compare_with_placeholder("source", "acquisition_channel", "Partial"))

    def test_repeated_unsupported_connector_is_not_isolation(self):
        self.assert_unknown(compare_with_placeholder("source", "connector_id", "Unsupported"))

    def test_repeated_not_supported_connector_is_not_isolation(self):
        self.assert_unknown(compare_with_placeholder("source", "connector_id", "Not-Supported"))

    def test_repeated_unknown_global_account_is_not_isolation(self):
        self.assert_unknown(compare_account_identity("global_advertiser_account_id", "Unknown"))

    def test_repeated_missing_manager_account_is_not_isolation(self):
        self.assert_unknown(compare_account_identity("manager_account_id", "Missing"))

    def test_repeated_unknown_country_code_is_not_isolation(self):
        self.assert_unknown(compare_account_identity("country_code", "Unknown"))

    def test_repeated_blank_optional_campaign_is_not_isolation(self):
        self.assert_unknown(compare_with_placeholder("scope", "campaign_id", "  "))

    def test_repeated_whitespace_padded_profile_is_not_isolation(self):
        self.assert_unknown(compare_with_placeholder("scope", "profile_id", " synthetic-profile "))

    def test_repeated_whitespace_padded_connector_is_not_isolation(self):
        self.assert_unknown(compare_with_placeholder("source", "connector_id", " connector-a "))

    def test_valid_identity_and_source_remain_isolated(self):
        before, after = snapshot(), snapshot()
        after["controls"][0]["state"] = 1.2
        self.assertEqual(compare_control_state(before, after, "base_bid")["classification"], "Treatment Isolated")

    def test_valid_explicit_account_identity_remains_isolated(self):
        result = compare_account_identity("manager_account_id", "manager-1")
        self.assertEqual(result["classification"], "Treatment Isolated", result)

    def test_valid_legacy_source_without_connector_remains_isolated(self):
        before, after = snapshot(), snapshot()
        before["source"].pop("connector_id")
        after["source"].pop("connector_id")
        after["controls"][0]["state"] = 1.2
        self.assertEqual(compare_control_state(before, after, "base_bid")["classification"], "Treatment Isolated")


if __name__ == "__main__":
    unittest.main()
