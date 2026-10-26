"""RED-first: explicit unresolved metric identity must never authorize direct summation.

All inputs are synthetic; this gate remains read-only and performs no Ads writes.
"""
import unittest

from scripts.evaluate_metric_aggregation_gate import evaluate_metric_aggregation_gate


def gate(name, *, include_name=True, semantic="additive", relation="disjoint"):
    payload = {
        "metric_semantics": {"aggregation_semantics": semantic},
        "source_relation": relation,
    }
    if include_name:
        payload["metric_name"] = name
    return evaluate_metric_aggregation_gate(payload)


class ExplicitMetricIdentityTests(unittest.TestCase):
    def assert_unknown(self, name):
        result = gate(name)
        self.assertEqual("Unknown", result["aggregation_status"], result)
        self.assertFalse(result["direct_sum_allowed"], result)
        self.assertIn("metric_name", result["reason"], result)

    def test_explicit_null_is_not_omission(self):
        self.assert_unknown(None)

    def test_explicit_empty_name_is_unresolved(self):
        self.assert_unknown("")

    def test_explicit_whitespace_name_is_unresolved(self):
        self.assert_unknown("   ")

    def test_explicit_unknown_label_is_unresolved(self):
        self.assert_unknown("Unknown")

    def test_explicit_partial_label_is_unresolved(self):
        self.assert_unknown("Partial")

    def test_explicit_unsupported_label_is_unresolved(self):
        self.assert_unknown("Unsupported")

    def test_explicit_not_available_label_is_unresolved(self):
        self.assert_unknown("Not Available")

    def test_explicit_underscored_not_supported_is_unresolved(self):
        self.assert_unknown("not_supported")

    def test_explicit_na_label_is_unresolved(self):
        self.assert_unknown("N/A")

    def test_explicit_object_name_is_unresolved(self):
        self.assert_unknown({"name": "Spend"})

    def test_explicit_numeric_name_is_unresolved(self):
        self.assert_unknown(0)

    def test_explicit_boolean_name_is_unresolved(self):
        self.assert_unknown(False)

    def test_omitted_legacy_metric_name_remains_compatible(self):
        self.assertEqual("Allowed", gate(None, include_name=False)["aggregation_status"])

    def test_concrete_additive_spend_is_still_allowed(self):
        self.assertEqual("Allowed", gate("Spend")["aggregation_status"])

    def test_concrete_additive_impressions_is_still_allowed(self):
        self.assertEqual("Allowed", gate("Impressions")["aggregation_status"])

    def test_valid_name_containing_unknown_word_is_not_whole_placeholder(self):
        self.assertEqual("Allowed", gate("Unknown SKU clicks")["aggregation_status"])

    def test_known_ratio_still_blocked(self):
        self.assertEqual("Blocked", gate("ROAS")["aggregation_status"])

    def test_unknown_semantics_remains_unknown(self):
        self.assertEqual("Unknown", gate("Spend", semantic="unknown")["aggregation_status"])

    def test_overlap_remains_blocked(self):
        self.assertEqual("Blocked", gate("Spend", relation="overlapping")["aggregation_status"])


if __name__ == "__main__":
    unittest.main()
