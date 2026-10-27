"""RED-first: one readback cannot assert contradictory control evidence metadata.

Synthetic read-only control snapshots. The same source.readback_id names one
observation, not independent captures of different effective times or evidence
statuses. This check does not authenticate an external Amazon Ads API response.
"""
import unittest

from scripts.compare_control_state import compare_control_state
from test_nested_collection_completeness import snapshot


def pair():
    before = snapshot("sponsored_products_bid_change", base_bid=1.0)
    after = snapshot("sponsored_products_bid_change", base_bid=1.0)
    before["source"]["readback_id"] = "readback-001"
    after["source"]["readback_id"] = "readback-001"
    return before, after


def control(item, control_type):
    return next(c for c in item["controls"] if c["control_type"] == control_type)


class ReusedReadbackControlEvidenceTests(unittest.TestCase):
    def assert_reused_unknown(self, before, after):
        result = compare_control_state(before, after)
        self.assertEqual("Unknown", result["classification"], result)
        self.assertIn("readback_id", " | ".join(result["reasons"]), result)

    def test_same_readback_conflicting_bid_effective_time(self):
        before, after = pair()
        control(after, "base_bid")["effective_at"] = "2026-09-20T23:00:00Z"
        self.assert_reused_unknown(before, after)

    def test_same_readback_conflicting_budget_effective_time(self):
        before, after = pair()
        control(after, "budget_or_pacing")["effective_at"] = "2026-09-20T23:59:00Z"
        self.assert_reused_unknown(before, after)

    def test_same_readback_submicrosecond_effective_time_difference(self):
        before, after = pair()
        control(before, "base_bid")["effective_at"] = "2026-09-21T00:00:00Z"
        control(after, "base_bid")["effective_at"] = "2026-09-21T00:00:00.000000001Z"
        after["observed_at"] = "2026-09-21T00:00:00.000000001Z"
        before["observed_at"] = after["observed_at"]
        self.assert_reused_unknown(before, after)

    def test_same_readback_missing_effective_time_on_one_side(self):
        before, after = pair()
        control(after, "base_bid")["effective_at"] = None
        self.assert_reused_unknown(before, after)

    def test_same_readback_conflicting_observation_evidence_status(self):
        before, after = pair()
        control(after, "base_bid")["evidence_status"] = "derived"
        self.assert_reused_unknown(before, after)

    def test_same_readback_same_effective_instant_different_offsets(self):
        before, after = pair()
        control(after, "base_bid")["effective_at"] = "2026-09-21T08:00:00+08:00"
        self.assertEqual("Comparable", compare_control_state(before, after)["classification"])

    def test_same_readback_same_fractional_instant_different_offsets(self):
        before, after = pair()
        before["observed_at"] = "2026-09-21T00:00:00.123456789Z"
        after["observed_at"] = "2026-09-21T08:00:00.123456789+08:00"
        control(before, "base_bid")["effective_at"] = "2026-09-21T00:00:00.123456789Z"
        control(after, "base_bid")["effective_at"] = "2026-09-21T08:00:00.123456789+08:00"
        self.assertEqual("Comparable", compare_control_state(before, after)["classification"])

    def test_distinct_readback_ids_allow_effective_time_changes(self):
        before, after = pair()
        after["source"]["readback_id"] = "readback-002"
        control(after, "base_bid")["effective_at"] = "2026-09-20T23:00:00Z"
        self.assertEqual("Comparable", compare_control_state(before, after)["classification"])

    def test_legacy_omitted_readback_ids_allow_effective_time_changes(self):
        before, after = pair()
        del before["source"]["readback_id"]
        del after["source"]["readback_id"]
        control(after, "base_bid")["effective_at"] = "2026-09-20T23:00:00Z"
        self.assertEqual("Comparable", compare_control_state(before, after)["classification"])

    def test_same_readback_same_state_and_evidence_remains_comparable(self):
        before, after = pair()
        self.assertEqual("Comparable", compare_control_state(before, after)["classification"])

    def test_distinct_readback_ids_preserve_isolated_bid_treatment(self):
        before, after = pair()
        after["source"]["readback_id"] = "readback-002"
        control(after, "base_bid")["state"] = 1.2
        self.assertEqual("Treatment Isolated", compare_control_state(before, after, "base_bid")["classification"])


if __name__ == "__main__":
    unittest.main()
