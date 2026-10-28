"""RED-first: explicit unresolved Stream v1 dataset identity cannot certify additive deltas.

Synthetic read-only evidence, not Amazon-native payload or source authentication.
"""
import unittest

from scripts.evaluate_metric_aggregation_gate import evaluate_metric_aggregation_gate


VERIFIED_V1 = {
    "idempotency_id_coverage": "Verified",
    "idempotency_id_deduplication": "Verified",
    "delivery_window_coverage": "Verified",
}


def verified_v1(dataset_marker=..., **extra):
    payload = {
        "operation": "sum",
        "metric_name": "spend",
        "metric_semantics": {"aggregation_semantics": "additive"},
        "source_relation": "disjoint",
        "acquisition_channel": "amazon_marketing_stream_v1",
        "stream_delta_reconciliation": VERIFIED_V1,
        **extra,
    }
    if dataset_marker is not ...:
        payload["stream_dataset"] = dataset_marker
    return payload


class StreamV1ExplicitDatasetIdentityTests(unittest.TestCase):
    def assert_unresolved(self, dataset_marker, **extra):
        result = evaluate_metric_aggregation_gate(verified_v1(dataset_marker, **extra))
        self.assertEqual(result["aggregation_status"], "Unknown", result)
        self.assertFalse(result["direct_sum_allowed"], result)
        self.assertEqual(result["stream_reconciliation_status"], "Unknown", result)

    def test_unknown_dataset_is_not_verified(self):
        self.assert_unresolved("Unknown")

    def test_partial_dataset_is_not_verified(self):
        self.assert_unresolved("Partial")

    def test_not_applicable_dataset_is_not_verified(self):
        self.assert_unresolved("Not Applicable")

    def test_null_dataset_is_not_verified(self):
        self.assert_unresolved(None)

    def test_non_string_dataset_is_not_verified(self):
        self.assert_unresolved(["sp-traffic"])

    def test_blank_dataset_is_not_verified(self):
        self.assert_unresolved(" \t ")

    def test_padded_dataset_is_not_verified(self):
        self.assert_unresolved(" sp-traffic ")

    def test_generic_v1_channel_must_not_bypass_dataset_identity(self):
        self.assert_unresolved("Missing", acquisition_channel="amazon_marketing_stream",
                               stream_generation="v1")

    def test_concrete_dataset_is_allowed(self):
        result = evaluate_metric_aggregation_gate(verified_v1("sp-traffic"))
        self.assertEqual(result["aggregation_status"], "Allowed", result)
        self.assertTrue(result["direct_sum_allowed"], result)

    def test_opaque_dataset_with_unknown_substring_is_concrete(self):
        result = evaluate_metric_aggregation_gate(verified_v1("unknown-items-stream"))
        self.assertEqual(result["aggregation_status"], "Allowed", result)
        self.assertTrue(result["direct_sum_allowed"], result)

    def test_omitted_optional_dataset_preserves_legacy(self):
        result = evaluate_metric_aggregation_gate(verified_v1())
        self.assertEqual(result["aggregation_status"], "Allowed", result)
        self.assertTrue(result["direct_sum_allowed"], result)


if __name__ == "__main__":
    unittest.main()
