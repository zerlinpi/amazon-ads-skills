"""Fail-closed decision-time control evidence tests (synthetic; no Ads writes)."""
import copy
import unittest

from scripts.compare_control_state import compare_control_state


def snapshot():
    return {
        "scope": {"marketplace_id": "ATVPDKIKX0DER", "profile_id": "fixture-profile"},
        "observed_at": "2026-10-23T00:00:00Z",
        "source": {"source_system": "fixture", "acquisition_channel": "test"},
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
            "control_type": "base_bid", "state": 1.0,
            "effective_at": "2026-10-22T00:00:00Z",
            "evidence_status": "observed",
        }],
    }


class ControlStateEffectiveTimeTests(unittest.TestCase):
    def assert_unknown(self, before, after, treatment=None):
        self.assertEqual(
            compare_control_state(before, after, treatment)["classification"], "Unknown"
        )

    def test_future_effective_at_on_stable_baseline_is_not_comparable(self):
        before, after = snapshot(), snapshot()
        before["controls"][0]["effective_at"] = "2026-10-23T00:00:01Z"
        self.assert_unknown(before, after)

    def test_future_effective_at_on_stable_post_is_not_comparable(self):
        before, after = snapshot(), snapshot()
        after["controls"][0]["effective_at"] = "2026-10-23T00:00:01Z"
        self.assert_unknown(before, after)

    def test_future_treatment_cannot_be_isolated(self):
        before, after = snapshot(), snapshot()
        after["controls"][0]["state"] = 1.2
        after["controls"][0]["effective_at"] = "2026-10-23T00:00:01Z"
        self.assert_unknown(before, after, "base_bid")

    def test_offset_future_instant_not_hidden_by_local_clock(self):
        before, after = snapshot(), snapshot()
        after["controls"][0]["effective_at"] = "2026-10-23T08:00:01+08:00"
        self.assert_unknown(before, after)

    def test_submicrosecond_future_instant_fails_closed(self):
        before, after = snapshot(), snapshot()
        after["observed_at"] = "2026-10-23T00:00:00.1234561Z"
        after["controls"][0]["effective_at"] = "2026-10-23T00:00:00.1234569Z"
        self.assert_unknown(before, after)

    def test_malformed_observed_timestamp_is_not_comparable(self):
        before, after = snapshot(), snapshot()
        before["observed_at"] = "not-a-timestamp"
        self.assert_unknown(before, after)

    def test_malformed_effective_timestamp_is_not_comparable(self):
        before, after = snapshot(), snapshot()
        after["controls"][0]["effective_at"] = "not-a-timestamp"
        self.assert_unknown(before, after)

    def test_unknown_offset_cannot_prove_timing(self):
        before, after = snapshot(), snapshot()
        after["controls"][0]["effective_at"] = "2026-10-22T00:00:00-00:00"
        self.assert_unknown(before, after)

    def test_same_instant_with_offset_is_valid(self):
        before, after = snapshot(), snapshot()
        after["controls"][0]["effective_at"] = "2026-10-23T08:00:00+08:00"
        self.assertEqual(compare_control_state(before, after)["classification"], "Comparable")

    def test_historical_treatment_remains_isolated(self):
        before, after = snapshot(), snapshot()
        after["controls"][0]["state"] = 1.2
        self.assertEqual(
            compare_control_state(before, after, "base_bid")["classification"],
            "Treatment Isolated",
        )


if __name__ == "__main__":
    unittest.main()
