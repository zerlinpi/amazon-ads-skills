"""Fail closed on explicitly supplied Amazon Business placement bid modifiers.

Amazon Ads distinguishes Amazon Business placements from the three general
Sponsored Products placements. These synthetic tests do not assert universal
marketplace or connector eligibility. No live advertising API calls.
"""
import unittest

from scripts.compare_control_state import compare_control_state
from test_placement_control_state import snapshot


STANDARD = {"top_of_search": 0, "rest_of_search": 0, "product_pages": 0}


def comparison(business_before, business_after, *, omit_before=False, omit_after=False):
    before_placement = dict(STANDARD)
    after_placement = dict(STANDARD)
    if not omit_before:
        before_placement["amazon_business"] = business_before
    if not omit_after:
        after_placement["amazon_business"] = business_after
    before = snapshot(1.0, before_placement)
    after = snapshot(1.2, after_placement)
    return compare_control_state(before, after, "base_bid")


class AmazonBusinessPlacementEvidenceTests(unittest.TestCase):
    def assert_unknown(self, before, after, **kwargs):
        result = comparison(before, after, **kwargs)
        self.assertEqual(result["classification"], "Unknown", result)
        self.assertTrue(any("amazon_business" in reason for reason in result["reasons"]), result)

    def test_unknown_on_both_sides_is_not_stability(self):
        self.assert_unknown("Unknown", "Unknown")

    def test_unsupported_is_not_zero(self):
        self.assert_unknown("Unsupported", "Unsupported")

    def test_partial_is_not_observed_modifier(self):
        self.assert_unknown("Partial", "Partial")

    def test_boolean_false_is_not_numeric_zero(self):
        self.assert_unknown(False, False)

    def test_boolean_true_is_not_numeric_one(self):
        self.assert_unknown(True, True)

    def test_negative_is_not_valid_modifier(self):
        self.assert_unknown(-5, -5)

    def test_infinity_is_not_valid_modifier(self):
        self.assert_unknown(float("inf"), float("inf"))

    def test_nan_is_not_valid_modifier(self):
        self.assert_unknown(float("nan"), float("nan"))

    def test_percent_string_is_not_plain_numeric_evidence(self):
        self.assert_unknown("25%", "25%")

    def test_structured_unknown_is_not_numeric_evidence(self):
        self.assert_unknown({"status": "Unknown"}, {"status": "Unknown"})

    def test_one_sided_missing_baseline_cannot_prove_unchanged(self):
        self.assert_unknown(0, 0, omit_before=True)

    def test_one_sided_missing_post_cannot_prove_unchanged(self):
        self.assert_unknown(0, 0, omit_after=True)

    def test_explicit_observed_zero_remains_valid(self):
        self.assertEqual(comparison(0, 0)["classification"], "Treatment Isolated")

    def test_explicit_decimal_string_remains_valid(self):
        self.assertEqual(comparison("25.5", "25.5")["classification"], "Treatment Isolated")

    def test_business_modifier_change_is_confounded(self):
        result = comparison(0, 25)
        self.assertEqual(result["classification"], "Confounded", result)
        self.assertIn("placement_adjustment", result.get("changed_controls", []))

    def test_legacy_three_placements_remain_compatible_without_b2b_proof(self):
        result = comparison(None, None, omit_before=True, omit_after=True)
        self.assertEqual(result["classification"], "Treatment Isolated", result)


if __name__ == "__main__":
    unittest.main()
