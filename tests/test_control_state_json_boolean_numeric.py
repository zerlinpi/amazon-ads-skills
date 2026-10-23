"""Deterministic JSON-type regression for read-only material-control comparison.

Python considers False == 0 and True == 1; JSON boolean state and numeric
state must not be silently treated as the same observed control configuration.
"""
import copy
import unittest

from scripts.compare_control_state import compare_control_state


COMPLETE = {
    "enumeration_status": "Complete",
    "pagination_status": "Complete",
    "capability_status": "Supported",
}


def snapshot(extra_state, *, base_bid=1.0, list_state=False):
    controls = [
        {
            "control_type": "base_bid",
            "state": base_bid,
            "effective_at": "2026-10-22T00:00:00Z",
            "evidence_status": "observed",
        },
        {
            "control_type": "other_material_control",
            "state": extra_state,
            "effective_at": "2026-10-22T00:00:00Z",
            "evidence_status": "observed",
        },
    ]
    if list_state:
        controls[1]["collection_evidence"] = copy.deepcopy(COMPLETE)
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
        "controls": controls,
    }


class JsonBooleanNumericControlStateTests(unittest.TestCase):
    def test_false_to_numeric_zero_is_not_comparable(self):
        result = compare_control_state(snapshot(False), snapshot(0))
        self.assertEqual(result["classification"], "Directional")
        self.assertIn("other_material_control", result["changed_controls"])

    def test_true_to_numeric_one_is_not_comparable(self):
        result = compare_control_state(snapshot(True), snapshot(1))
        self.assertEqual(result["classification"], "Directional")
        self.assertIn("other_material_control", result["changed_controls"])

    def test_nested_object_boolean_to_numeric_is_not_comparable(self):
        result = compare_control_state(snapshot({"enabled": False}), snapshot({"enabled": 0}))
        self.assertEqual(result["classification"], "Directional")

    def test_complete_list_boolean_to_numeric_is_not_comparable(self):
        result = compare_control_state(snapshot([False], list_state=True), snapshot([0], list_state=True))
        self.assertEqual(result["classification"], "Directional")

    def test_boolean_numeric_collision_cannot_isolate_another_treatment(self):
        result = compare_control_state(
            snapshot(False, base_bid=1.0),
            snapshot(0, base_bid=1.2),
            intended_treatment="base_bid",
        )
        self.assertEqual(result["classification"], "Confounded")
        self.assertEqual(set(result["changed_controls"]), {"base_bid", "other_material_control"})

    def test_identical_boolean_states_remain_comparable(self):
        self.assertEqual(compare_control_state(snapshot(False), snapshot(False))["classification"], "Comparable")

    def test_numerically_equal_integer_float_remain_comparable(self):
        self.assertEqual(compare_control_state(snapshot(0), snapshot(0.0))["classification"], "Comparable")


if __name__ == "__main__":
    unittest.main()
