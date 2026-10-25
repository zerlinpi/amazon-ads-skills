"""RED-first: generic material-control state cannot launder missing evidence.

A verified collection inventory and evidence_status=observed do not turn
explicit Unknown/Unsupported/Partial state values into observations.
Synthetic fixture only; no Amazon Ads API calls or live writes.
"""
import copy
import unittest

from scripts.compare_control_state import compare_control_state
from test_control_state_extra_material_evidence import COMPLETE, add_extra, snapshot


def compare_extra(value, *, post_value=None, treatment=True, collection=False):
    before, after = snapshot(), snapshot()
    if treatment:
        after["controls"][0]["state"] = 1.2
    other = copy.deepcopy(value) if post_value is None else post_value
    proof = COMPLETE if collection else None
    add_extra(before, value, proof)
    add_extra(after, other, proof)
    return compare_control_state(before, after, "base_bid" if treatment else None)


class GenericMaterialStatePlaceholderEvidenceTests(unittest.TestCase):
    def assert_unknown(self, value, *, collection=False):
        result = compare_extra(value, collection=collection)
        self.assertEqual(result["classification"], "Unknown", result)

    def test_repeated_unknown_scalar_is_not_stable(self):
        self.assert_unknown("Unknown")

    def test_repeated_unsupported_scalar_is_not_stable(self):
        self.assert_unknown("Unsupported")

    def test_repeated_partial_scalar_is_not_stable(self):
        self.assert_unknown("Partial")

    def test_repeated_missing_scalar_is_not_stable(self):
        self.assert_unknown("Missing")

    def test_repeated_unavailable_scalar_is_not_stable(self):
        self.assert_unknown("Unavailable")

    def test_repeated_not_available_scalar_is_not_stable(self):
        self.assert_unknown("Not Available")

    def test_repeated_blank_scalar_is_not_stable(self):
        self.assert_unknown("")

    def test_repeated_whitespace_scalar_is_not_stable(self):
        self.assert_unknown("  ")

    def test_repeated_unknown_nested_field_is_not_stable(self):
        self.assert_unknown({"mode": "enabled", "source_state": "Unknown"})

    def test_repeated_unsupported_deep_nested_field_is_not_stable(self):
        self.assert_unknown({"mode": {"eligibility": "Unsupported"}})

    def test_repeated_unknown_member_of_complete_list_is_not_stable(self):
        self.assert_unknown(["Unknown"], collection=True)

    def test_repeated_positive_infinity_is_not_stable(self):
        self.assert_unknown(float("inf"))

    def test_repeated_negative_infinity_is_not_stable(self):
        self.assert_unknown(float("-inf"))

    def test_repeated_nan_is_unknown_not_a_competing_change(self):
        self.assert_unknown(float("nan"))

    def test_nonfinite_nested_numeric_is_unknown(self):
        self.assert_unknown({"bid": float("inf")})

    def test_required_control_placeholder_is_not_comparable(self):
        before, after = snapshot(), snapshot()
        before["controls"][0]["state"] = "Unknown"
        after["controls"][0]["state"] = "Unknown"
        result = compare_control_state(before, after)
        self.assertEqual(result["classification"], "Unknown", result)

    def test_required_control_nested_placeholder_is_not_comparable(self):
        before, after = snapshot(), snapshot()
        before["controls"][0]["state"] = {"bid": "Partial"}
        after["controls"][0]["state"] = {"bid": "Partial"}
        result = compare_control_state(before, after)
        self.assertEqual(result["classification"], "Unknown", result)

    def test_verified_zero_remains_distinct_from_missing(self):
        self.assertEqual(compare_extra(0)["classification"], "Treatment Isolated")

    def test_verified_boolean_switch_remains_usable(self):
        self.assertEqual(compare_extra(False)["classification"], "Treatment Isolated")

    def test_verified_descriptive_string_remains_usable(self):
        self.assertEqual(compare_extra("enabled")["classification"], "Treatment Isolated")

    def test_verified_structured_state_remains_usable(self):
        state = {"mode": "enabled", "weight": 0, "switch": False}
        self.assertEqual(compare_extra(state)["classification"], "Treatment Isolated")

    def test_verified_complete_list_remains_usable(self):
        self.assertEqual(compare_extra(["enabled"], collection=True)["classification"], "Treatment Isolated")

    def test_genuine_extra_material_change_remains_confounded(self):
        result = compare_extra("enabled", post_value="disabled")
        self.assertEqual(result["classification"], "Confounded", result)


if __name__ == "__main__":
    unittest.main()
