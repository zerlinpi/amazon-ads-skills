"""RED-first tests for contradictions across observed mid-window control events.

Synthetic read-side evidence only; these tests do not imply event-log completeness,
Amazon API authentication, causal lift or permission for live advertising writes.
"""
import copy
import unittest

from scripts.compare_control_state import compare_control_state
from test_control_intervening_event_evidence import fixture


def add_event(post, original, *, event_at="2026-09-21T13:00:00Z",
              control_type="schedule_or_event_rule", new_increase=35):
    second = copy.deepcopy(original)
    second["event_id"] = "event-2"
    second["event_at"] = event_at
    second["control_type"] = control_type
    if control_type == "base_bid":
        second["before_state"] = 1.0
        second["after_state"] = 1.2
    else:
        second["after_state"]["schedule_rules"][0]["bid_increase"] = new_increase
    post["control_events"].append(second)
    return second


class InterveningObservationCollisionTests(unittest.TestCase):
    def classify(self, baseline, post):
        return compare_control_state(baseline, post, "base_bid")

    def test_same_event_readback_id_at_different_instants_is_unknown(self):
        baseline, post, first = fixture()
        first["source"]["readback_id"] = "mid-observation-1"
        second = add_event(post, first)
        second["source"]["readback_id"] = "mid-observation-1"
        self.assertEqual(self.classify(baseline, post)["classification"], "Unknown")

    def test_same_event_readback_id_one_nanosecond_apart_is_unknown(self):
        baseline, post, first = fixture()
        first["source"]["readback_id"] = "mid-observation-1"
        second = add_event(post, first, event_at="2026-09-21T12:00:00.000000001Z")
        second["source"]["readback_id"] = "mid-observation-1"
        self.assertEqual(self.classify(baseline, post)["classification"], "Unknown")

    def test_same_control_same_instant_conflicting_transition_is_unknown(self):
        baseline, post, first = fixture()
        add_event(post, first, event_at=first["event_at"], new_increase=45)
        self.assertEqual(self.classify(baseline, post)["classification"], "Unknown")

    def test_same_control_same_instant_conflicting_before_state_is_unknown(self):
        baseline, post, first = fixture()
        second = add_event(post, first, event_at=first["event_at"], new_increase=25)
        second["before_state"]["schedule_rules"][0]["bid_increase"] = 15
        self.assertEqual(self.classify(baseline, post)["classification"], "Unknown")

    def test_distinct_readbacks_at_different_instants_remain_confounders(self):
        baseline, post, first = fixture()
        first["source"]["readback_id"] = "mid-observation-1"
        second = add_event(post, first)
        second["source"]["readback_id"] = "mid-observation-2"
        self.assertEqual(self.classify(baseline, post)["classification"], "Confounded")

    def test_legacy_missing_event_readbacks_remain_compatible(self):
        baseline, post, first = fixture()
        add_event(post, first)
        self.assertEqual(self.classify(baseline, post)["classification"], "Confounded")

    def test_one_missing_event_readback_remains_compatible(self):
        baseline, post, first = fixture()
        first["source"]["readback_id"] = "mid-observation-1"
        second = add_event(post, first)
        second["source"].pop("readback_id", None)
        self.assertEqual(self.classify(baseline, post)["classification"], "Confounded")

    def test_same_readback_offset_equivalent_instant_different_controls_valid(self):
        baseline, post, first = fixture()
        first["source"]["readback_id"] = "mid-observation-1"
        second = add_event(post, first, event_at="2026-09-21T08:00:00-04:00",
                           control_type="base_bid")
        second["source"]["readback_id"] = "mid-observation-1"
        self.assertEqual(self.classify(baseline, post)["classification"], "Confounded")

    def test_distinct_controls_same_instant_are_not_automatically_conflicting(self):
        baseline, post, first = fixture()
        add_event(post, first, event_at=first["event_at"], control_type="base_bid")
        self.assertEqual(self.classify(baseline, post)["classification"], "Confounded")

    def test_identical_duplicate_transition_different_event_ids_is_compatible(self):
        baseline, post, first = fixture()
        add_event(post, first, event_at=first["event_at"], new_increase=25)
        self.assertEqual(self.classify(baseline, post)["classification"], "Confounded")

    def test_nonexhaustive_event_log_does_not_require_adjacent_state_chain(self):
        baseline, post, first = fixture()
        second = add_event(post, first)
        second["before_state"]["schedule_rules"][0]["bid_increase"] = 15
        self.assertEqual(self.classify(baseline, post)["classification"], "Confounded")


if __name__ == "__main__":
    unittest.main()
