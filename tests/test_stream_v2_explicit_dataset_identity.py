"""RED-first: explicit unresolved Stream v2 dataset identity cannot certify additive totals.

Synthetic read-only metadata only; not an Amazon API payload or source authentication.
"""
import unittest

from scripts.evaluate_metric_aggregation_gate import evaluate_metric_aggregation_gate


def verified_v2(dataset_marker=...):
    payload = {
        "operation": "sum",
        "metric_name": "spend",
        "metric_semantics": {"aggregation_semantics": "additive"},
        "source_relation": "disjoint",
        "acquisition_channel": "amazon_marketing_stream_v2",
        "stream_record_reconciliation": {
            "record_identity_coverage": "Verified",
            "highest_version_per_record": "Verified",
        },
    }
    if dataset_marker is not ...:
        payload["stream_dataset"] = dataset_marker
    return payload


class StreamV2ExplicitDatasetIdentityTests(unittest.TestCase):
    def assert_unresolved(self, value):
        result = evaluate_metric_aggregation_gate(verified_v2(value))
        self.assertEqual(result["aggregation_status"], "Unknown", result)
        self.assertFalse(result["direct_sum_allowed"], result)
        self.assertEqual(result["stream_reconciliation_status"], "Unknown", result)

    def test_explicit_unknown_dataset_is_not_verified(self):
        self.assert_unresolved("Unknown")

    def test_explicit_partial_dataset_is_not_verified(self):
        self.assert_unresolved("Partial")

    def test_explicit_missing_dataset_is_not_verified(self):
        self.assert_unresolved("Missing")

    def test_explicit_unsupported_dataset_is_not_verified(self):
        self.assert_unresolved("Unsupported")

    def test_explicit_not_applicable_dataset_is_not_verified(self):
        self.assert_unresolved("Not Applicable")

    def test_explicit_null_dataset_is_not_verified(self):
        self.assert_unresolved(None)

    def test_explicit_non_string_dataset_is_not_verified(self):
        self.assert_unresolved(["ads-performance-v1"])

    def test_explicit_whitespace_dataset_is_not_verified(self):
        self.assert_unresolved("  ")

    def test_explicit_padded_dataset_is_not_verified(self):
        self.assert_unresolved(" ads-performance-v1 ")

    def test_known_concrete_dataset_preserves_additive_gate(self):
        result = evaluate_metric_aggregation_gate(verified_v2("ads-performance-v1"))
        self.assertEqual(result["aggregation_status"], "Allowed", result)
        self.assertTrue(result["direct_sum_allowed"], result)

    def test_opaque_dataset_containing_unknown_substring_is_concrete(self):
        result = evaluate_metric_aggregation_gate(verified_v2("unknown-items-dataset"))
        self.assertEqual(result["aggregation_status"], "Allowed", result)
        self.assertTrue(result["direct_sum_allowed"], result)

    def test_omitted_legacy_dataset_remains_compatible(self):
        result = evaluate_metric_aggregation_gate(verified_v2())
        self.assertEqual(result["aggregation_status"], "Allowed", result)
        self.assertTrue(result["direct_sum_allowed"], result)


if __name__ == "__main__":
    unittest.main()
