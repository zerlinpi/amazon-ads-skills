import unittest

from scripts.compare_measurement_composition import compare_measurement_composition


def state(**overrides):
    composition = {
        "modeled_conversion_inclusion": "combined_with_direct",
        "direct_modeled_split_available": False,
        "allocation_coverage_status": "Complete",
        "unallocated_rows_present": False,
        "allocation_grain": "targeting",
    }
    composition.update(overrides)
    return {"measurement_composition": composition}


class MeasurementCompositionComparabilityTests(unittest.TestCase):
    def test_identical_complete_composition_is_comparable(self):
        result = compare_measurement_composition(state(), state())
        self.assertEqual(result["classification"], "Comparable")
        self.assertEqual(result["changed_fields"], [])

    def test_missing_composition_fails_closed_to_unknown(self):
        result = compare_measurement_composition({}, state())
        self.assertEqual(result["classification"], "Unknown")
        self.assertTrue(any("missing" in reason.lower() for reason in result["reasons"]))

    def test_missing_field_fails_closed_to_unknown(self):
        baseline = state()
        baseline["measurement_composition"].pop("unallocated_rows_present")
        result = compare_measurement_composition(baseline, state())
        self.assertEqual(result["classification"], "Unknown")

    def test_unknown_string_state_is_not_treated_as_comparable(self):
        result = compare_measurement_composition(
            state(allocation_coverage_status="Unknown"),
            state(allocation_coverage_status="Unknown"),
        )
        self.assertEqual(result["classification"], "Unknown")

    def test_allocation_coverage_drift_is_directional(self):
        result = compare_measurement_composition(
            state(allocation_coverage_status="Partial", unallocated_rows_present=True),
            state(allocation_coverage_status="Complete", unallocated_rows_present=False),
        )
        self.assertEqual(result["classification"], "Directional")
        self.assertEqual(
            set(result["changed_fields"]),
            {"allocation_coverage_status", "unallocated_rows_present"},
        )

    def test_allocation_grain_change_is_not_comparable(self):
        result = compare_measurement_composition(
            state(allocation_grain="targeting"),
            state(allocation_grain="campaign"),
        )
        self.assertEqual(result["classification"], "Not Comparable")
        self.assertIn("allocation_grain", result["changed_fields"])

    def test_modeled_inclusion_change_is_not_comparable(self):
        result = compare_measurement_composition(
            state(modeled_conversion_inclusion="combined_with_direct"),
            state(modeled_conversion_inclusion="direct_only"),
        )
        self.assertEqual(result["classification"], "Not Comparable")
        self.assertIn("modeled_conversion_inclusion", result["changed_fields"])

    def test_split_availability_change_is_directional(self):
        result = compare_measurement_composition(
            state(direct_modeled_split_available=False),
            state(direct_modeled_split_available=True),
        )
        self.assertEqual(result["classification"], "Directional")
        self.assertIn("direct_modeled_split_available", result["changed_fields"])


    def test_post_change_skill_routes_two_composition_states_through_comparator(self):
        from pathlib import Path

        root = Path(__file__).resolve().parents[1]
        skill = (root / "skills/post-change-review/SKILL.md").read_text(encoding="utf-8").lower()
        self.assertIn("compare_measurement_composition.py", skill)
        self.assertIn("not comparable", skill)
        self.assertIn("directional", skill)
        self.assertIn("unknown", skill)
        self.assertIn("inconclusive", skill)


if __name__ == "__main__":
    unittest.main()
