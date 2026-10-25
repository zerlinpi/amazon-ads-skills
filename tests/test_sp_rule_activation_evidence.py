"""RED-first: explicit SP rule activation evidence must not silently become stable.

The optional activation_status field is repository-normalized read-side evidence,
not an Amazon Ads API field or proof of continuous rule execution.
No live advertising account writes are performed.
"""
import unittest

from scripts.compare_control_state import compare_control_state
from test_nested_collection_completeness import snapshot
from test_sp_rule_member_evidence import compare_rules, bid_rule, budget_rule


def activated_bid(value):
    return bid_rule(activation_status=value)


def activated_budget(value):
    return budget_rule(activation_status=value)


class SponsoredProductsRuleActivationEvidenceTests(unittest.TestCase):
    def assert_unknown(self, kind, members, after_members=None, *, budget_treatment=False):
        result = compare_rules(kind, members, after_members, budget_treatment=budget_treatment)
        self.assertEqual(result["classification"], "Unknown", result)

    def test_schedule_unknown_status_cannot_prove_stability(self):
        self.assert_unknown("schedule_rules", [activated_bid("Unknown")])

    def test_schedule_unsupported_status_cannot_prove_stability(self):
        self.assert_unknown("schedule_rules", [activated_bid("Unsupported")])

    def test_event_partial_status_cannot_prove_stability(self):
        self.assert_unknown("event_rules", [activated_bid("Partial")])

    def test_schedule_boolean_status_is_not_active(self):
        self.assert_unknown("schedule_rules", [activated_bid(True)])

    def test_event_null_status_is_not_inactive(self):
        self.assert_unknown("event_rules", [activated_bid(None)])

    def test_schedule_empty_status_is_unknown(self):
        self.assert_unknown("schedule_rules", [activated_bid("")])

    def test_schedule_numeric_status_is_unknown(self):
        self.assert_unknown("schedule_rules", [activated_bid(0)])

    def test_event_structured_status_is_unknown(self):
        self.assert_unknown("event_rules", [activated_bid({"status": "Unknown"})])

    def test_unmapped_rule_status_is_unknown_not_implicitly_inactive(self):
        self.assert_unknown("schedule_rules", [activated_bid("Paused")])

    def test_budget_unknown_activation_during_bid_treatment(self):
        self.assert_unknown("active_budget_rules", [activated_budget("Unknown")])

    def test_budget_unsupported_activation_during_budget_treatment(self):
        self.assert_unknown("active_budget_rules", [activated_budget("Unsupported")], budget_treatment=True)

    def test_one_sided_schedule_activation_evidence_is_unknown(self):
        self.assert_unknown("schedule_rules", [activated_bid("active")], [bid_rule()])

    def test_one_sided_budget_activation_evidence_is_unknown(self):
        self.assert_unknown("active_budget_rules", [budget_rule()], [activated_budget("active")], budget_treatment=True)

    def test_normalized_active_schedule_status_remains_valid(self):
        result = compare_rules("schedule_rules", [activated_bid("active")])
        self.assertEqual(result["classification"], "Treatment Isolated", result)

    def test_normalized_inactive_budget_status_remains_valid(self):
        result = compare_rules("active_budget_rules", [activated_budget("inactive")], budget_treatment=True)
        self.assertEqual(result["classification"], "Treatment Isolated", result)

    def test_normalized_scheduled_event_status_remains_valid(self):
        result = compare_rules("event_rules", [activated_bid("scheduled")])
        self.assertEqual(result["classification"], "Treatment Isolated", result)

    def test_observed_activation_change_is_competing_control(self):
        result = compare_rules("schedule_rules", [activated_bid("inactive")], [activated_bid("active")])
        self.assertEqual(result["classification"], "Confounded", result)
        self.assertIn("schedule_or_event_rule", result.get("changed_controls", []))

    def test_empty_verified_rule_collection_remains_valid(self):
        result = compare_rules("schedule_rules", [])
        self.assertEqual(result["classification"], "Treatment Isolated", result)


if __name__ == "__main__":
    unittest.main()
