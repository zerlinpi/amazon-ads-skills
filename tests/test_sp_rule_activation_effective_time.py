"""RED-first: explicit normalized rule activation transition time needs valid lineage.

activation_effective_at is an optional repository-owned read-side transition
instant, not an Amazon-native API field or proof of continuous execution.
"""
import unittest

from scripts.compare_control_state import compare_control_state
from test_sp_rule_member_evidence import compare_rules, bid_rule, budget_rule


GOOD = "2026-09-20T12:00:00Z"
EARLIER = "2026-09-19T12:00:00Z"


def timed_bid(value=GOOD, **fields):
    return bid_rule(activation_status="active", activation_effective_at=value, **fields)


def timed_budget(value=GOOD, **fields):
    return budget_rule(activation_status="active", activation_effective_at=value, **fields)


class SponsoredProductsRuleActivationEffectiveTimeTests(unittest.TestCase):
    def unknown(self, kind, before, after=None, *, budget_treatment=False):
        result = compare_rules(kind, before, after, budget_treatment=budget_treatment)
        self.assertEqual(result["classification"], "Unknown", result)

    def test_schedule_unknown_transition_time(self):
        self.unknown("schedule_rules", [timed_bid("Unknown")])

    def test_event_unsupported_transition_time(self):
        self.unknown("event_rules", [timed_bid("Unsupported")])

    def test_schedule_partial_transition_time(self):
        self.unknown("schedule_rules", [timed_bid("Partial")])

    def test_schedule_blank_transition_time(self):
        self.unknown("schedule_rules", [timed_bid("")])

    def test_event_null_transition_time(self):
        self.unknown("event_rules", [timed_bid(None)])

    def test_schedule_boolean_transition_time(self):
        self.unknown("schedule_rules", [timed_bid(False)])

    def test_budget_numeric_transition_time(self):
        self.unknown("active_budget_rules", [timed_budget(0)], budget_treatment=True)

    def test_budget_structured_unknown_transition_time(self):
        self.unknown("active_budget_rules", [timed_budget({"status": "Unknown"})])

    def test_schedule_naive_transition_time(self):
        self.unknown("schedule_rules", [timed_bid("2026-09-20T12:00:00")])

    def test_event_invalid_offset_transition_time(self):
        self.unknown("event_rules", [timed_bid("2026-09-20T12:00:00+25:00")])

    def test_schedule_future_transition_time(self):
        self.unknown("schedule_rules", [timed_bid("2026-09-22T00:00:00Z")])

    def test_budget_future_transition_time(self):
        self.unknown("active_budget_rules", [timed_budget("2026-09-22T00:00:00Z")], budget_treatment=True)

    def test_transition_time_without_status_cannot_prove_activation(self):
        self.unknown("schedule_rules", [bid_rule(activation_effective_at=GOOD)])

    def test_one_sided_schedule_transition_time(self):
        self.unknown("schedule_rules", [timed_bid()], [bid_rule(activation_status="active")])

    def test_one_sided_budget_transition_time(self):
        self.unknown("active_budget_rules", [budget_rule(activation_status="active")], [timed_budget()], budget_treatment=True)

    def test_valid_transition_time_remains_compatible(self):
        result = compare_rules("schedule_rules", [timed_bid()])
        self.assertEqual(result["classification"], "Treatment Isolated", result)

    def test_valid_budget_transition_time_remains_compatible(self):
        result = compare_rules("active_budget_rules", [timed_budget()], budget_treatment=True)
        self.assertEqual(result["classification"], "Treatment Isolated", result)

    def test_real_transition_time_change_is_confounded(self):
        result = compare_rules("schedule_rules", [timed_bid(EARLIER)], [timed_bid(GOOD)])
        self.assertEqual(result["classification"], "Confounded", result)
        self.assertIn("schedule_or_event_rule", result.get("changed_controls", []))


if __name__ == "__main__":
    unittest.main()
