"""Deterministic Global SP identity provenance regression tests.

A repeated unavailable identity is not a verified campaign, account, source,
or raw marketplace crosswalk. Synthetic fixtures; no live Ads access.
"""
import copy
import unittest

from test_global_sp_readback_evidence import evaluate, fixture
from test_global_sp_raw_marketplace_identity import add_identity_map
from test_global_sp_marketplace_budget_readback import budget_fixture


class GlobalSpConcreteIdentityEvidenceTests(unittest.TestCase):
    def assert_status(self, evidence, expected):
        result = evaluate(evidence)
        self.assertEqual(result["application_status"], expected, result)

    def test_unknown_account_echo_cannot_confirm(self):
        e = fixture()
        e["request"]["global_account_id"] = "Unknown"
        e["readback"]["global_account_id"] = "Unknown"
        self.assert_status(e, "Unknown")

    def test_unsupported_campaign_echo_cannot_confirm(self):
        e = fixture()
        e["request"]["campaign_id"] = "Unsupported"
        e["readback"]["campaign_id"] = "Unsupported"
        self.assert_status(e, "Unknown")

    def test_padded_account_echo_cannot_confirm(self):
        e = fixture()
        e["request"]["global_account_id"] = " synthetic-global-a "
        e["readback"]["global_account_id"] = " synthetic-global-a "
        self.assert_status(e, "Unknown")

    def test_unknown_explicit_request_id_echo_cannot_confirm(self):
        e = fixture()
        e["request"]["request_id"] = "Partial"
        e["receipt"]["request_id"] = "Partial"
        self.assert_status(e, "Unknown")

    def test_unknown_request_id_without_receipt_echo_cannot_confirm(self):
        e = fixture()
        e["request"]["request_id"] = "Not Available"
        self.assert_status(e, "Unknown")

    def test_unknown_connector_source_cannot_confirm(self):
        e = fixture()
        e["readback"]["source"]["connector_id"] = "Unknown"
        self.assert_status(e, "Unknown")

    def test_unavailable_source_system_cannot_confirm(self):
        e = fixture()
        e["readback"]["source"]["source_system"] = "Not-Available"
        self.assert_status(e, "Unknown")

    def test_padded_acquisition_channel_cannot_confirm(self):
        e = fixture()
        e["readback"]["source"]["acquisition_channel"] = " lookup "
        self.assert_status(e, "Unknown")

    def test_raw_marketplace_unknown_echo_cannot_confirm(self):
        e = add_identity_map(fixture())
        e["readback"]["marketplace_identity_map"][0]["marketplace_id"] = "Unknown"
        e["readback"]["marketplace_states"][0]["marketplace_id"] = "Unknown"
        self.assert_status(e, "Unknown")

    def test_raw_marketplace_not_supported_echo_cannot_confirm(self):
        e = add_identity_map(fixture())
        e["readback"]["marketplace_identity_map"][0]["marketplace_id"] = "Not-Supported"
        e["readback"]["marketplace_states"][0]["marketplace_id"] = "Not-Supported"
        self.assert_status(e, "Unknown")

    def test_raw_marketplace_padded_echo_cannot_confirm(self):
        e = add_identity_map(fixture())
        e["readback"]["marketplace_identity_map"][0]["marketplace_id"] = " SYNTHETIC_MARKET_ID_US "
        e["readback"]["marketplace_states"][0]["marketplace_id"] = " SYNTHETIC_MARKET_ID_US "
        self.assert_status(e, "Unknown")

    def test_raw_marketplace_crosswalk_unknown_connector_cannot_confirm(self):
        e = add_identity_map(fixture())
        e["readback"]["marketplace_identity_map"][0]["source"]["connector_id"] = "Unknown"
        self.assert_status(e, "Unknown")

    def test_raw_marketplace_crosswalk_missing_source_cannot_confirm(self):
        e = add_identity_map(fixture())
        e["readback"]["marketplace_identity_map"][0]["source"]["source_system"] = "Missing"
        self.assert_status(e, "Unknown")

    def test_raw_marketplace_crosswalk_unsupported_channel_cannot_confirm(self):
        e = add_identity_map(fixture())
        e["readback"]["marketplace_identity_map"][0]["source"]["acquisition_channel"] = "Not Available"
        self.assert_status(e, "Unknown")

    def test_budget_crosswalk_unknown_raw_id_cannot_confirm(self):
        e = add_identity_map(budget_fixture(), with_budget=True)
        e["readback"]["marketplace_identity_map"][0]["marketplace_id"] = "Unknown"
        e["readback"]["marketplace_states"][0]["marketplace_id"] = "Unknown"
        e["readback"]["marketplace_budgets"][0]["marketplace_id"] = "Unknown"
        self.assert_status(e, "Unknown")

    def test_real_ids_containing_unknown_substring_remain_valid(self):
        e = add_identity_map(fixture())
        e["request"]["campaign_id"] = "synthetic-unknown-campaign"
        e["readback"]["campaign_id"] = "synthetic-unknown-campaign"
        e["readback"]["source"]["connector_id"] = "synthetic-unknown-connector"
        e["readback"]["marketplace_identity_map"][0]["marketplace_id"] = "SYNTHETIC_UNKNOWN_ID_US"
        e["readback"]["marketplace_states"][0]["marketplace_id"] = "SYNTHETIC_UNKNOWN_ID_US"
        self.assert_status(e, "Confirmed")

    def test_valid_crosswalk_still_confirms(self):
        self.assert_status(add_identity_map(fixture()), "Confirmed")

    def test_legacy_index_only_receipt_still_confirms(self):
        self.assert_status(fixture(), "Confirmed")


if __name__ == "__main__":
    unittest.main()
