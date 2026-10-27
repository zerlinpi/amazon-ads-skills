"""RED-first: top-level rule collection proof cannot certify nested event arrays.

Synthetic normalized read-side evidence. No Amazon Ads calls or writes.
"""
import copy
import unittest

from scripts.compare_control_state import compare_control_state
from test_intervening_rule_collection_proof import proven_event


class InterveningRuleDescendantCompletenessTests(unittest.TestCase):
    def classify(self, before, post):
        return compare_control_state(before, post, "base_bid")["classification"]

    def test_schedule_rule_member_nested_list_with_complete_outer_proof_is_unknown(self):
        before, post, event = proven_event()
        for phase in ("before_state", "after_state"):
            event[phase]["schedule_rules"][0]["targeting_conditions"] = ["example"]
        self.assertEqual(self.classify(before, post), "Unknown")

    def test_schedule_rule_member_empty_nested_list_still_needs_proof(self):
        before, post, event = proven_event()
        for phase in ("before_state", "after_state"):
            event[phase]["schedule_rules"][0]["conditions"] = []
        self.assertEqual(self.classify(before, post), "Unknown")

    def test_budget_rule_member_deep_nested_list_with_complete_outer_proof_is_unknown(self):
        before, post, event = proven_event("budget_or_pacing")
        for phase in ("before_state", "after_state"):
            event[phase]["active_budget_rules"][0]["metadata"] = {"targets": ["example"]}
        self.assertEqual(self.classify(before, post), "Unknown")

    def test_legacy_event_without_outer_proof_cannot_certify_nested_rule_list(self):
        before, post, event = proven_event()
        del event["rule_collection_evidence"]
        for phase in ("before_state", "after_state"):
            event[phase]["schedule_rules"][0]["nested"] = [{"id": "a"}]
        self.assertEqual(self.classify(before, post), "Unknown")

    def test_valid_complete_outer_proof_and_scalar_members_remains_confounder(self):
        before, post, event = proven_event()
        for phase in ("before_state", "after_state"):
            event[phase]["schedule_rules"][0]["comment"] = "observed"
        self.assertEqual(self.classify(before, post), "Confounded")

    def test_valid_budget_outer_proof_without_descendant_lists_remains_confounder(self):
        before, post, _ = proven_event("budget_or_pacing")
        self.assertEqual(self.classify(before, post), "Confounded")

    def test_legacy_rule_event_without_optional_proof_remains_confounder(self):
        before, post, event = proven_event()
        del event["rule_collection_evidence"]
        self.assertEqual(self.classify(before, post), "Confounded")

    def test_top_level_empty_rule_collection_with_complete_proof_is_usable(self):
        before, post, event = proven_event()
        event["before_state"]["event_rules"] = []
        event["after_state"]["event_rules"] = []
        self.assertEqual(self.classify(before, post), "Confounded")


if __name__ == "__main__":
    unittest.main()
