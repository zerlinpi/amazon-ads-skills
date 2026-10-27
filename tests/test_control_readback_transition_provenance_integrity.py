"""RED-first: one readback observation cannot have contradictory transition provenance.

Synthetic read-only snapshots. Transition authorship is not inferred from
current control state, and no Amazon Ads API request or mutation occurs.
"""
import copy
import unittest

from scripts.compare_control_state import compare_control_state
from test_control_readback_effective_evidence_integrity import pair, control


def provenance(**overrides):
    value = {
        "management_mode": "advertiser_managed",
        "last_transition_actor": "advertiser",
        "transition_reason": "manual change",
        "transition_observed_at": "2026-09-20T23:00:00Z",
        "actor_evidence_status": "observed",
    }
    value.update(overrides)
    return value


def with_provenance():
    before, after = pair()
    control(before, "base_bid")["transition_provenance"] = provenance()
    control(after, "base_bid")["transition_provenance"] = provenance()
    return before, after


class ReusedReadbackTransitionProvenanceTests(unittest.TestCase):
    def assert_unresolved(self, before, after):
        result = compare_control_state(before, after)
        self.assertEqual("Unknown", result["classification"], result)
        self.assertIn("readback_id", " | ".join(result["reasons"]), result)

    def test_same_readback_conflicting_management_mode(self):
        before, after = with_provenance()
        control(after, "base_bid")["transition_provenance"]["management_mode"] = "platform_managed"
        self.assert_unresolved(before, after)

    def test_same_readback_conflicting_actor(self):
        before, after = with_provenance()
        control(after, "base_bid")["transition_provenance"]["last_transition_actor"] = "amazon_platform"
        self.assert_unresolved(before, after)

    def test_same_readback_conflicting_actor_evidence_status(self):
        before, after = with_provenance()
        control(after, "base_bid")["transition_provenance"]["actor_evidence_status"] = "derived"
        self.assert_unresolved(before, after)

    def test_same_readback_conflicting_transition_reason(self):
        before, after = with_provenance()
        control(after, "base_bid")["transition_provenance"]["transition_reason"] = "automatic rule"
        self.assert_unresolved(before, after)

    def test_same_readback_conflicting_transition_observed_at(self):
        before, after = with_provenance()
        control(after, "base_bid")["transition_provenance"]["transition_observed_at"] = "2026-09-20T23:00:01Z"
        self.assert_unresolved(before, after)

    def test_same_readback_nanosecond_transition_difference(self):
        before, after = with_provenance()
        control(after, "base_bid")["transition_provenance"]["transition_observed_at"] = "2026-09-20T23:00:00.000000001Z"
        self.assert_unresolved(before, after)

    def test_same_readback_one_sided_provenance(self):
        before, after = with_provenance()
        del control(after, "base_bid")["transition_provenance"]
        self.assert_unresolved(before, after)

    def test_same_readback_one_sided_null_provenance(self):
        before, after = with_provenance()
        control(after, "base_bid")["transition_provenance"] = None
        self.assert_unresolved(before, after)

    def test_same_readback_conflict_in_other_control(self):
        before, after = with_provenance()
        control(before, "budget_or_pacing")["transition_provenance"] = provenance()
        control(after, "budget_or_pacing")["transition_provenance"] = provenance(last_transition_actor="external_executor")
        self.assert_unresolved(before, after)

    def test_same_readback_equivalent_timezone_transition_instants(self):
        before, after = with_provenance()
        control(after, "base_bid")["transition_provenance"]["transition_observed_at"] = "2026-09-21T07:00:00+08:00"
        self.assertEqual("Comparable", compare_control_state(before, after)["classification"])

    def test_same_readback_equivalent_fractional_instants(self):
        before, after = with_provenance()
        control(before, "base_bid")["transition_provenance"]["transition_observed_at"] = "2026-09-20T23:00:00.123456789Z"
        control(after, "base_bid")["transition_provenance"]["transition_observed_at"] = "2026-09-21T07:00:00.123456789+08:00"
        self.assertEqual("Comparable", compare_control_state(before, after)["classification"])

    def test_same_readback_same_provenance_remains_comparable(self):
        before, after = with_provenance()
        self.assertEqual("Comparable", compare_control_state(before, after)["classification"])

    def test_distinct_readbacks_do_not_require_equal_transition_provenance(self):
        before, after = with_provenance()
        after["source"]["readback_id"] = "readback-002"
        control(after, "base_bid")["transition_provenance"]["last_transition_actor"] = "amazon_platform"
        self.assertEqual("Comparable", compare_control_state(before, after)["classification"])

    def test_legacy_missing_readback_ids_remain_compatible(self):
        before, after = with_provenance()
        del before["source"]["readback_id"]
        del after["source"]["readback_id"]
        control(after, "base_bid")["transition_provenance"]["last_transition_actor"] = "amazon_platform"
        self.assertEqual("Comparable", compare_control_state(before, after)["classification"])

    def test_both_absent_optional_transition_provenance(self):
        before, after = pair()
        self.assertEqual("Comparable", compare_control_state(before, after)["classification"])


if __name__ == "__main__":
    unittest.main()
