"""RED-first: N/A and Not Applicable are unresolved source/scope identities.

All inputs are synthetic; no Amazon Ads API calls or writes.
"""
import unittest

from scripts.compare_control_state import compare_control_state
from test_control_scope_source_placeholder_evidence import (
    compare_account_identity,
    compare_with_placeholder,
    snapshot,
)


class NotApplicableScopeSourceIdentityTests(unittest.TestCase):
    def assert_unresolved(self, result):
        self.assertEqual("Unknown", result["classification"], result)
        self.assertTrue(result["reasons"], result)

    def test_marketplace_na(self):
        self.assert_unresolved(compare_with_placeholder("scope", "marketplace_id", "N/A"))

    def test_profile_not_applicable(self):
        self.assert_unresolved(compare_with_placeholder("scope", "profile_id", "Not Applicable"))

    def test_campaign_not_applicable_underscore(self):
        self.assert_unresolved(compare_with_placeholder("scope", "campaign_id", "Not_Applicable"))

    def test_entity_not_applicable_hyphen(self):
        self.assert_unresolved(compare_with_placeholder("scope", "entity_id", "Not-Applicable"))

    def test_entity_type_na(self):
        self.assert_unresolved(compare_with_placeholder("scope", "entity_type", "n/a"))

    def test_source_system_na(self):
        self.assert_unresolved(compare_with_placeholder("source", "source_system", "N/A"))

    def test_acquisition_channel_not_applicable(self):
        self.assert_unresolved(compare_with_placeholder("source", "acquisition_channel", "Not Applicable"))

    def test_connector_not_applicable_underscore(self):
        self.assert_unresolved(compare_with_placeholder("source", "connector_id", "Not_Applicable"))

    def test_connector_na(self):
        self.assert_unresolved(compare_with_placeholder("source", "connector_id", "N/A"))

    def test_marketplace_not_applicable_tab(self):
        self.assert_unresolved(compare_with_placeholder("scope", "marketplace_id", "Not\tApplicable"))

    def test_source_system_not_applicable_multiple_spaces(self):
        self.assert_unresolved(compare_with_placeholder("source", "source_system", "Not  Applicable"))

    def test_global_account_na(self):
        self.assert_unresolved(compare_account_identity("global_advertiser_account_id", "N/A"))

    def test_manager_account_not_applicable(self):
        self.assert_unresolved(compare_account_identity("manager_account_id", "Not Applicable"))

    def test_country_code_na(self):
        self.assert_unresolved(compare_account_identity("country_code", "N/A"))

    def test_valid_opaque_id_containing_na_is_not_a_placeholder(self):
        result = compare_with_placeholder("scope", "campaign_id", "campaign-N/A-2026")
        self.assertEqual("Treatment Isolated", result["classification"], result)

    def test_valid_opaque_id_containing_not_applicable_is_not_a_placeholder(self):
        result = compare_with_placeholder("source", "source_system", "connector-not-applicable-v2")
        self.assertEqual("Treatment Isolated", result["classification"], result)

    def test_existing_real_source_and_scope_still_isolate_treatment(self):
        before, after = snapshot(), snapshot()
        after["controls"][0]["state"] = 1.2
        self.assertEqual(
            "Treatment Isolated",
            compare_control_state(before, after, "base_bid")["classification"],
        )


if __name__ == "__main__":
    unittest.main()
