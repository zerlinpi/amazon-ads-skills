"""RED-first: SP rule-event extra direct arrays lack independent completeness proof.

Synthetic read-only control events. No Amazon Ads calls or writes.
"""
import unittest

from scripts.compare_control_state import compare_control_state
from test_intervening_rule_collection_proof import proven_event
from test_control_intervening_event_evidence import fixture


class InterveningRuleExtraDirectListTests(unittest.TestCase):
    def assert_class(self, baseline, post, expected):
        result = compare_control_state(baseline, post, "base_bid")
        self.assertEqual(result["classification"], expected, result)

    def test_schedule_before_extra_empty_list_is_unknown(self):
        before, post, event = proven_event()
        event["before_state"]["unmapped_targets"] = []
        self.assert_class(before, post, "Unknown")

    def test_schedule_after_extra_empty_list_is_unknown(self):
        before, post, event = proven_event()
        event["after_state"]["unmapped_targets"] = []
        self.assert_class(before, post, "Unknown")

    def test_schedule_repeated_extra_nonempty_list_is_unknown(self):
        before, post, event = proven_event()
        for side in ("before_state", "after_state"):
            event[side]["unmapped_targets"] = ["target-1"]
        self.assert_class(before, post, "Unknown")

    def test_budget_before_extra_empty_list_is_unknown(self):
        before, post, event = proven_event("budget_or_pacing")
        event["before_state"]["unmapped_targets"] = []
        self.assert_class(before, post, "Unknown")

    def test_budget_after_extra_nonempty_list_is_unknown(self):
        before, post, event = proven_event("budget_or_pacing")
        event["after_state"]["unmapped_targets"] = ["target-1"]
        self.assert_class(before, post, "Unknown")

    def test_valid_schedule_and_event_lists_with_outer_proof_stay_confounder(self):
        before, post, _ = proven_event()
        self.assert_class(before, post, "Confounded")

    def test_valid_budget_list_with_outer_proof_stays_confounder(self):
        before, post, _ = proven_event("budget_or_pacing")
        self.assert_class(before, post, "Confounded")

    def test_scalar_extra_evidence_stays_compatible(self):
        before, post, event = proven_event()
        for side in ("before_state", "after_state"):
            event[side]["source_note"] = "observed"
        self.assert_class(before, post, "Confounded")

    def test_legacy_flat_rule_event_without_optional_proof_stays_confounder(self):
        before, post, _ = fixture()
        self.assert_class(before, post, "Confounded")


if __name__ == "__main__":
    unittest.main()
