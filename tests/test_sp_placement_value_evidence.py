"""Fail-closed Sponsored Products placement adjustment value evidence.

A complete placement map is not proof of a known numeric modifier when its
value is a status label, boolean, non-finite or negative. Synthetic only.
"""
import unittest

from scripts.compare_control_state import compare_control_state
from test_placement_control_state import snapshot

PLACEMENTS = ("top_of_search", "rest_of_search", "product_pages")
VALID = {"top_of_search": 0, "rest_of_search": 0, "product_pages": 0}


def compare_with(field, value, both=False, surface="sponsored_products_bid_change"):
    before = snapshot(1.0, dict(VALID))
    after = snapshot(1.2, dict(VALID))
    after["controls"][2]["state"][field] = value
    if both:
        before["controls"][2]["state"][field] = value
    if surface == "sponsored_products_budget_change":
        before["coverage"]["requirement_provenance"]["decision_surface"] = surface
        after["coverage"]["requirement_provenance"]["decision_surface"] = surface
    return compare_control_state(before, after, "base_bid")


class SponsoredProductsPlacementValueEvidenceTests(unittest.TestCase):
    def assert_unknown(self, field, value, both=False, surface="sponsored_products_bid_change"):
        result = compare_with(field, value, both, surface)
        self.assertEqual(result["classification"], "Unknown", result)
        self.assertTrue(any(field in reason for reason in result["reasons"]), result)

    def test_top_of_search_unknown_is_not_a_zero(self):
        self.assert_unknown("top_of_search", "Unknown")

    def test_rest_of_search_unsupported_is_not_an_observation(self):
        self.assert_unknown("rest_of_search", "Unsupported")

    def test_product_pages_partial_on_both_sides_is_not_stability(self):
        self.assert_unknown("product_pages", "Partial", both=True)

    def test_top_of_search_false_is_not_numeric_zero(self):
        self.assert_unknown("top_of_search", False)

    def test_rest_of_search_true_is_not_numeric_one(self):
        self.assert_unknown("rest_of_search", True)

    def test_product_pages_negative_modifier_is_invalid(self):
        self.assert_unknown("product_pages", -1)

    def test_top_of_search_nonfinite_modifier_is_invalid(self):
        self.assert_unknown("top_of_search", float("inf"))

    def test_rest_of_search_nan_modifier_is_invalid(self):
        self.assert_unknown("rest_of_search", float("nan"))

    def test_product_pages_structured_placeholder_is_invalid(self):
        self.assert_unknown("product_pages", {"status": "Unknown"})

    def test_top_of_search_percent_string_is_not_plain_numeric_evidence(self):
        self.assert_unknown("top_of_search", "15%")

    def test_empty_placement_value_is_not_evidence(self):
        self.assert_unknown("rest_of_search", "")

    def test_budget_causal_surface_also_requires_placement_values(self):
        self.assert_unknown("product_pages", "Unknown", both=True, surface="sponsored_products_budget_change")

    def test_complete_zero_modifiers_remain_valid(self):
        result = compare_with("top_of_search", 0)
        self.assertEqual(result["classification"], "Treatment Isolated", result)

    def test_valid_decimal_string_remains_supported(self):
        result = compare_with("rest_of_search", "12.50", both=True)
        self.assertEqual(result["classification"], "Treatment Isolated", result)

    def test_valid_numeric_float_remains_supported(self):
        result = compare_with("product_pages", 12.5, both=True)
        self.assertEqual(result["classification"], "Treatment Isolated", result)


if __name__ == "__main__":
    unittest.main()
