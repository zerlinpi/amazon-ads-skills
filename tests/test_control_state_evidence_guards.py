"""Fail-closed regressions for ambiguous control-state evidence.

Synthetic fixture only; no live Amazon Ads calls.
"""
import copy
import unittest

from scripts.compare_control_state import compare_control_state


def snapshot():
    return {
        "scope": {"marketplace_id": "ATVPDKIKX0DER", "profile_id": "synthetic-profile"},
        "observed_at": "2026-10-23T00:00:00Z",
        "source": {"source_system": "fixture", "acquisition_channel": "test"},
        "coverage": {
            "required_control_types": ["base_bid"],
            "coverage_status": "Complete",
            "requirement_provenance": {
                "decision_surface": "fixture_control_comparison",
                "derivation_status": "Verified",
                "capability_snapshot_id": "fixture-capability",
                "requirement_registry_id": "control-requirements@2026-09-29",
            },
        },
        "controls": [
            {"control_type": "base_bid", "state": 1.0,
             "effective_at": "2026-10-22T00:00:00Z", "evidence_status": "observed"}
        ],
    }


class ControlStateEvidenceGuardTests(unittest.TestCase):
    def assert_unknown(self, before, after):
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_stable_observed_is_comparable(self):
        self.assertEqual(compare_control_state(snapshot(), snapshot())["classification"], "Comparable")

    def test_derived_is_valid_evidence(self):
        before, after = snapshot(), snapshot()
        before["controls"][0]["evidence_status"] = "derived"
        after["controls"][0]["evidence_status"] = "derived"
        self.assertEqual(compare_control_state(before, after)["classification"], "Comparable")

    def test_duplicate_control_baseline_fails_closed(self):
        before, after = snapshot(), snapshot()
        duplicate = copy.deepcopy(before["controls"][0])
        duplicate["evidence_status"] = "unsupported"
        before["controls"].insert(0, duplicate)
        self.assert_unknown(before, after)

    def test_duplicate_control_post_fails_closed(self):
        before, after = snapshot(), snapshot()
        duplicate = copy.deepcopy(after["controls"][0])
        duplicate["state"] = 2.0
        after["controls"].insert(0, duplicate)
        self.assert_unknown(before, after)

    def test_missing_control_type_fails_closed(self):
        before, after = snapshot(), snapshot()
        before["controls"][0].pop("control_type")
        self.assert_unknown(before, after)

    def test_null_control_type_fails_closed(self):
        before, after = snapshot(), snapshot()
        before["controls"][0]["control_type"] = None
        self.assert_unknown(before, after)

    def test_missing_baseline_evidence_status_fails_closed(self):
        before, after = snapshot(), snapshot()
        before["controls"][0].pop("evidence_status")
        self.assert_unknown(before, after)

    def test_missing_post_evidence_status_fails_closed(self):
        before, after = snapshot(), snapshot()
        after["controls"][0].pop("evidence_status")
        self.assert_unknown(before, after)

    def test_invalid_partial_evidence_status_fails_closed(self):
        before, after = snapshot(), snapshot()
        after["controls"][0]["evidence_status"] = "partial"
        self.assert_unknown(before, after)

    def test_unsupported_evidence_status_fails_closed(self):
        before, after = snapshot(), snapshot()
        before["controls"][0]["evidence_status"] = "unsupported"
        self.assert_unknown(before, after)


if __name__ == "__main__":
    unittest.main()
