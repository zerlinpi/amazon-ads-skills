"""Concrete Sponsored Products rule identity is required for causal comparisons.

Synthetic read-only snapshots only. Matching placeholder rule IDs are not
proof that a schedule/event/budget rule remained the same across snapshots.
"""
import unittest

from test_sp_rule_member_evidence import compare_rules, bid_rule, budget_rule


class SponsoredProductsConcreteRuleIdentityTests(unittest.TestCase):
    def assert_unknown(self, collection, member, *, budget_treatment=False):
        result = compare_rules(collection, [member], budget_treatment=budget_treatment)
        self.assertEqual(result["classification"], "Unknown", result)
        self.assertTrue(
            any("rule_id" in reason for reason in result["reasons"]), result
        )

    def test_schedule_unknown_id_cannot_prove_isolation(self):
        self.assert_unknown("schedule_rules", bid_rule(rule_id="Unknown"))

    def test_event_unsupported_id_cannot_prove_isolation(self):
        self.assert_unknown("event_rules", bid_rule(rule_id="Unsupported"))

    def test_budget_partial_id_cannot_prove_isolation(self):
        self.assert_unknown(
            "active_budget_rules", budget_rule(rule_id="Partial"),
            budget_treatment=True,
        )

    def test_schedule_missing_label_cannot_prove_isolation(self):
        self.assert_unknown("schedule_rules", bid_rule(rule_id="Missing"))

    def test_budget_not_available_label_cannot_prove_isolation(self):
        self.assert_unknown(
            "active_budget_rules", budget_rule(rule_id="Not-Available"),
            budget_treatment=True,
        )

    def test_event_not_supported_label_cannot_prove_isolation(self):
        self.assert_unknown("event_rules", bid_rule(rule_id="not supported"))

    def test_case_insensitive_placeholder_cannot_prove_isolation(self):
        self.assert_unknown("schedule_rules", bid_rule(rule_id="uNkNoWn"))

    def test_real_id_containing_unknown_substring_remains_valid(self):
        result = compare_rules(
            "schedule_rules", [bid_rule(rule_id="rule-unknown-history-12")]
        )
        self.assertEqual(result["classification"], "Treatment Isolated", result)

    def test_real_id_containing_partial_substring_remains_valid(self):
        result = compare_rules(
            "active_budget_rules", [budget_rule(rule_id="rule-partial-2026")],
            budget_treatment=True,
        )
        self.assertEqual(result["classification"], "Treatment Isolated", result)

    def test_explicit_zero_modifier_still_valid_with_concrete_id(self):
        result = compare_rules(
            "schedule_rules", [bid_rule(rule_id="rule-0", bid_increase=0)]
        )
        self.assertEqual(result["classification"], "Treatment Isolated", result)


if __name__ == "__main__":
    unittest.main()
