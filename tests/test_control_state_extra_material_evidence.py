"""Synthetic regressions for extra material-control evidence.

An observed extra material control is not ignorable simply because the
versioned decision surface does not list it as mandatory. No Ads writes.
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
                "requirement_registry_id": "control-requirements@2026-09-29",
            },
        },
        "controls": [
            {
                "control_type": "base_bid",
                "state": 1.0,
                "effective_at": "2026-10-22T00:00:00Z",
                "evidence_status": "observed",
            }
        ],
    }


def add_extra(snapshot_value, state, evidence=None):
    extra = {
        "control_type": "other_material_control",
        "state": state,
        "effective_at": "2026-10-22T00:00:00Z",
        "evidence_status": "observed",
    }
    if evidence is not None:
        extra["collection_evidence"] = evidence
    snapshot_value["controls"].append(extra)


COMPLETE = {
    "enumeration_status": "Complete",
    "pagination_status": "Complete",
    "capability_status": "Supported",
}


class ExtraMaterialControlEvidenceTests(unittest.TestCase):
    def test_extra_null_on_both_sides_is_unknown(self):
        before, after = snapshot(), snapshot()
        add_extra(before, None)
        add_extra(after, None)
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_extra_null_on_one_side_is_unknown(self):
        before, after = snapshot(), snapshot()
        add_extra(before, None)
        add_extra(after, 0)
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_extra_missing_state_is_unknown(self):
        before, after = snapshot(), snapshot()
        add_extra(before, 0)
        add_extra(after, 0)
        after["controls"][-1].pop("state")
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_extra_list_without_completeness_is_unknown(self):
        before, after = snapshot(), snapshot()
        add_extra(before, ["rule-a"])
        add_extra(after, ["rule-a"])
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_extra_list_with_partial_pagination_is_unknown(self):
        before, after = snapshot(), snapshot()
        add_extra(before, ["rule-a"], COMPLETE)
        partial = copy.deepcopy(COMPLETE)
        partial["pagination_status"] = "Truncated"
        add_extra(after, ["rule-a"], partial)
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_extra_complete_list_is_comparable(self):
        before, after = snapshot(), snapshot()
        add_extra(before, [], COMPLETE)
        add_extra(after, [], COMPLETE)
        self.assertEqual(compare_control_state(before, after)["classification"], "Comparable")

    def test_extra_observed_scalar_is_comparable(self):
        before, after = snapshot(), snapshot()
        add_extra(before, 0)
        add_extra(after, 0)
        self.assertEqual(compare_control_state(before, after)["classification"], "Comparable")


if __name__ == "__main__":
    unittest.main()
