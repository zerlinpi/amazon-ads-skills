"""Fail closed on invalid Sponsored Products video bid-adjustment evidence.

Synthetic causal-control tests only. Amazon Ads video bid boosts are separate
from placement controls; this module never performs live advertising writes.
"""
import unittest

from scripts.compare_control_state import compare_control_state
from test_placement_control_state import snapshot


PLACEMENTS = {"top_of_search": 0, "rest_of_search": 0, "product_pages": 0}


def video_comparison(before_value, after_value, *, treatment="base_bid"):
    baseline = snapshot(1.0, dict(PLACEMENTS))
    post = snapshot(1.2, dict(PLACEMENTS))
    for record, value in ((baseline, before_value), (post, after_value)):
        next(item for item in record["controls"] if item["control_type"] == "video_bid_adjustment")["state"] = value
    return compare_control_state(baseline, post, treatment)


class VideoBidValueEvidenceTests(unittest.TestCase):
    def assert_unknown(self, value):
        result = video_comparison(value, value)
        self.assertEqual(result["classification"], "Unknown", result)
        self.assertTrue(any("video_bid_adjustment" in reason for reason in result["reasons"]), result)

    def test_unknown_is_not_an_observed_zero(self):
        self.assert_unknown("Unknown")

    def test_unsupported_is_not_observed_zero(self):
        self.assert_unknown("Unsupported")

    def test_partial_is_not_observed_zero(self):
        self.assert_unknown("Partial")

    def test_missing_label_is_not_observed_zero(self):
        self.assert_unknown("Missing")

    def test_boolean_false_is_not_numeric_zero(self):
        self.assert_unknown(False)

    def test_boolean_true_is_not_numeric_one(self):
        self.assert_unknown(True)

    def test_negative_modifier_is_invalid(self):
        self.assert_unknown(-1)

    def test_infinity_is_invalid(self):
        self.assert_unknown(float("inf"))

    def test_nan_is_invalid(self):
        self.assert_unknown(float("nan"))

    def test_percent_string_is_not_plain_numeric_evidence(self):
        self.assert_unknown("15%")

    def test_structured_unknown_is_not_a_numeric_modifier(self):
        self.assert_unknown({"status": "Unknown"})

    def test_null_is_not_observed_modifier(self):
        self.assert_unknown(None)

    def test_explicit_zero_remains_valid(self):
        self.assertEqual(video_comparison(0, 0)["classification"], "Treatment Isolated")

    def test_plain_decimal_string_remains_valid(self):
        self.assertEqual(video_comparison("15.5", "15.5")["classification"], "Treatment Isolated")

    def test_real_video_boost_change_remains_confounded(self):
        result = video_comparison(0, 15)
        self.assertEqual(result["classification"], "Confounded", result)
        self.assertIn("video_bid_adjustment", result.get("changed_controls", []))


if __name__ == "__main__":
    unittest.main()
