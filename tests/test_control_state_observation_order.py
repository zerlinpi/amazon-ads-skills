"""Decision-time observation-order regression tests (synthetic, read-only)."""
import copy
import unittest

from scripts.compare_control_state import compare_control_state


def snapshot(observed_at="2026-10-23T00:00:00Z", bid=1.0):
    return {
        "scope": {"marketplace_id": "ATVPDKIKX0DER", "profile_id": "synthetic-profile"},
        "observed_at": observed_at,
        "source": {"source_system": "synthetic-fixture", "acquisition_channel": "test"},
        "coverage": {
            "required_control_types": ["base_bid"],
            "coverage_status": "Complete",
            "requirement_provenance": {
                "decision_surface": "fixture_control_comparison",
                "derivation_status": "Verified",
                "requirement_registry_id": "control-requirements@2026-09-29",
            },
        },
        "controls": [{
            "control_type": "base_bid",
            "state": bid,
            "effective_at": "2026-10-22T00:00:00Z",
            "evidence_status": "observed",
        }],
    }


class ControlStateObservationOrderTests(unittest.TestCase):
    def test_reversed_stable_snapshots_are_not_comparable(self):
        baseline = snapshot("2026-10-23T02:00:00Z")
        post = snapshot("2026-10-23T01:00:00Z")
        self.assertEqual(compare_control_state(baseline, post)["classification"], "Unknown")

    def test_reversed_treatment_cannot_be_isolated(self):
        baseline = snapshot("2026-10-23T02:00:00Z", 1.0)
        post = snapshot("2026-10-23T01:00:00Z", 1.2)
        self.assertEqual(compare_control_state(baseline, post, "base_bid")["classification"], "Unknown")

    def test_reversed_utc_instant_is_not_hidden_by_local_clock(self):
        baseline = snapshot("2026-10-23T10:00:00+08:00")
        post = snapshot("2026-10-23T01:30:00Z")
        self.assertEqual(compare_control_state(baseline, post)["classification"], "Unknown")

    def test_submicrosecond_reversal_is_not_truncated(self):
        baseline = snapshot("2026-10-23T00:00:00.1234569Z")
        post = snapshot("2026-10-23T00:00:00.1234561Z")
        self.assertEqual(compare_control_state(baseline, post)["classification"], "Unknown")

    def test_same_instant_with_offset_remains_comparable(self):
        baseline = snapshot("2026-10-23T00:00:00Z")
        post = snapshot("2026-10-23T08:00:00+08:00")
        self.assertEqual(compare_control_state(baseline, post)["classification"], "Comparable")

    def test_forward_observation_with_treatment_remains_isolated(self):
        baseline = snapshot("2026-10-23T00:00:00Z", 1.0)
        post = snapshot("2026-10-23T01:00:00Z", 1.2)
        self.assertEqual(compare_control_state(baseline, post, "base_bid")["classification"], "Treatment Isolated")


if __name__ == "__main__":
    unittest.main()
