"""RED-first: mid-window SP rule activation metadata needs paired evidence.

All fixtures are synthetic, read-only. A positive event is not proof of
complete capture, continuous rule execution, or Amazon API authenticity.
"""
import copy
import unittest

from scripts.compare_control_state import compare_control_state
from test_control_intervening_event_evidence import fixture

EARLIER = "2026-09-21T10:00:00Z"
LATER = "2026-09-21T11:00:00Z"


def event_with_rule(collection="schedule_rules"):
    control = "budget_or_pacing" if collection == "active_budget_rules" else "schedule_or_event_rule"
    baseline, post, event = fixture(control)
    if collection == "event_rules":
        rule = {"rule_id": "event-rule-1", "bid_increase": 10}
        event["before_state"]["event_rules"] = [copy.deepcopy(rule)]
        changed = copy.deepcopy(rule)
        changed["bid_increase"] = 25
        event["after_state"]["event_rules"] = [changed]
    return baseline, post, event


class InterveningSPRuleActivationParityTests(unittest.TestCase):
    def check(self, collection, expected, mutate):
        baseline, post, event = event_with_rule(collection)
        mutate(event["before_state"][collection], event["after_state"][collection])
        result = compare_control_state(baseline, post, "base_bid")
        self.assertEqual(result["classification"], expected, result)
        return result

    def test_schedule_status_only_after_is_unknown(self):
        result = self.check("schedule_rules", "Unknown",
            lambda before, after: after[0].update(activation_status="active"))
        self.assertIn("activation_status", str(result["reasons"]))

    def test_schedule_status_only_before_is_unknown(self):
        self.check("schedule_rules", "Unknown",
            lambda before, after: before[0].update(activation_status="inactive"))

    def test_event_rule_status_only_after_is_unknown(self):
        self.check("event_rules", "Unknown",
            lambda before, after: after[0].update(activation_status="scheduled"))

    def test_budget_rule_status_only_before_is_unknown(self):
        self.check("active_budget_rules", "Unknown",
            lambda before, after: before[0].update(activation_status="active"))

    def test_schedule_effective_time_only_after_is_unknown(self):
        def mutate(before, after):
            before[0]["activation_status"] = "active"
            after[0].update(activation_status="active", activation_effective_at=LATER)
        self.check("schedule_rules", "Unknown", mutate)

    def test_budget_effective_time_only_before_is_unknown(self):
        def mutate(before, after):
            before[0].update(activation_status="active", activation_effective_at=EARLIER)
            after[0]["activation_status"] = "active"
        self.check("active_budget_rules", "Unknown", mutate)

    def test_both_absent_activation_fields_remain_valid(self):
        self.check("schedule_rules", "Confounded", lambda before, after: None)

    def test_observed_schedule_activation_transition_remains_confounder(self):
        def mutate(before, after):
            before[0]["activation_status"] = "inactive"
            after[0]["activation_status"] = "active"
        self.check("schedule_rules", "Confounded", mutate)

    def test_observed_event_rule_activation_transition_remains_confounder(self):
        def mutate(before, after):
            before[0]["activation_status"] = "scheduled"
            after[0]["activation_status"] = "active"
        self.check("event_rules", "Confounded", mutate)

    def test_observed_budget_activation_time_transition_remains_confounder(self):
        def mutate(before, after):
            before[0].update(activation_status="active", activation_effective_at=EARLIER)
            after[0].update(activation_status="active", activation_effective_at=LATER)
        self.check("active_budget_rules", "Confounded", mutate)

    def test_new_rule_identity_does_not_require_fabricated_prior_activation(self):
        def mutate(before, after):
            after.append({"rule_id": "schedule-new", "bid_increase": 15,
                          "activation_status": "active", "activation_effective_at": LATER})
        self.check("schedule_rules", "Confounded", mutate)


if __name__ == "__main__":
    unittest.main()
