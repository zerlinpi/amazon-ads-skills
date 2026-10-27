"""RED-first: explicit N/A material states and SP member IDs are unresolved evidence.

Synthetic read-only fixtures; no Amazon Ads API calls, mutation or account access.
"""
import unittest

from test_generic_material_state_placeholder_evidence import compare_extra
from test_sp_rule_member_evidence import compare_rules, bid_rule, budget_rule
from test_sp_audience_member_evidence import classify


class NotApplicableMaterialEvidenceTests(unittest.TestCase):
    def assert_unknown(self, result):
        self.assertEqual("Unknown", result["classification"], result)

    def test_repeated_na_scalar_cannot_isolate_bid(self):
        self.assert_unknown(compare_extra("N/A"))

    def test_repeated_not_applicable_scalar_cannot_isolate_bid(self):
        self.assert_unknown(compare_extra("Not Applicable"))

    def test_repeated_not_applicable_underscore_cannot_isolate_bid(self):
        self.assert_unknown(compare_extra("Not_Applicable"))

    def test_repeated_not_applicable_hyphen_cannot_isolate_bid(self):
        self.assert_unknown(compare_extra("not-applicable"))

    def test_repeated_not_applicable_tab_cannot_isolate_bid(self):
        self.assert_unknown(compare_extra("Not\tApplicable"))

    def test_repeated_na_nested_state_cannot_isolate_bid(self):
        self.assert_unknown(compare_extra({"control": {"eligibility": "N/A"}}))

    def test_repeated_na_complete_list_cannot_isolate_bid(self):
        self.assert_unknown(compare_extra(["N/A"], collection=True))

    def test_schedule_rule_na_identity_cannot_isolate_bid(self):
        self.assert_unknown(compare_rules("schedule_rules", [bid_rule(rule_id="N/A")]))

    def test_event_rule_not_applicable_identity_cannot_isolate_bid(self):
        self.assert_unknown(compare_rules("event_rules", [bid_rule(rule_id="Not Applicable")]))

    def test_budget_rule_na_identity_cannot_isolate_bid(self):
        self.assert_unknown(compare_rules("active_budget_rules", [budget_rule(rule_id="N/A")]))

    def test_audience_na_identity_cannot_isolate_bid(self):
        self.assertEqual("Unknown", classify([{"audience_id": "N/A", "bid_boost": 10}]))

    def test_audience_not_applicable_identity_cannot_isolate_bid(self):
        self.assertEqual("Unknown", classify([{"audience_id": "Not Applicable", "bid_boost": 10}]))

    def test_descriptive_opaque_state_containing_na_remains_valid(self):
        self.assertEqual("Treatment Isolated", compare_extra("mode-N/A-legacy")["classification"])

    def test_real_rule_identity_containing_na_remains_valid(self):
        self.assertEqual("Treatment Isolated", compare_rules("schedule_rules", [bid_rule(rule_id="rule-N/A-2026")])["classification"])

    def test_real_audience_identity_containing_not_applicable_remains_valid(self):
        self.assertEqual("Treatment Isolated", classify([{"audience_id": "aud-not-applicable-2026", "bid_boost": 10}]))

    def test_observed_zero_and_false_are_not_missing(self):
        self.assertEqual("Treatment Isolated", compare_extra({"amount": 0, "enabled": False})["classification"])

    def test_actual_rule_change_remains_confounder(self):
        result = compare_rules("schedule_rules", [bid_rule()], [bid_rule(bid_increase=25)])
        self.assertEqual("Confounded", result["classification"], result)


if __name__ == "__main__":
    unittest.main()
