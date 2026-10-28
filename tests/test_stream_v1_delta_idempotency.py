"""RED-first Stream v1 delta deduplication/coverage evidence guard.

Synthetic read-only metadata only; the external connector owns actual delivery,
deduplication, retries and source authentication.
"""
import unittest

from scripts.evaluate_metric_aggregation_gate import evaluate_metric_aggregation_gate


VERIFIED_V1 = {
    "idempotency_id_coverage": "Verified",
    "idempotency_id_deduplication": "Verified",
    "delivery_window_coverage": "Verified",
}


def additive(**extra):
    return {
        "operation": "sum",
        "metric_name": "spend",
        "metric_semantics": {"aggregation_semantics": "additive"},
        "source_relation": "disjoint",
        "acquisition_channel": "amazon_marketing_stream_v1",
        **extra,
    }


class StreamV1DeltaIdempotencyTests(unittest.TestCase):
    def assert_unknown(self, payload):
        result = evaluate_metric_aggregation_gate(payload)
        self.assertEqual(result["aggregation_status"], "Unknown", result)
        self.assertFalse(result["direct_sum_allowed"], result)
        self.assertEqual(result["stream_reconciliation_status"], "Unknown", result)

    def test_v1_missing_delta_proof_is_not_direct_sum_safe(self):
        self.assert_unknown(additive())

    def test_v1_partial_idempotency_coverage_is_not_verified(self):
        self.assert_unknown(additive(stream_delta_reconciliation={
            **VERIFIED_V1, "idempotency_id_coverage": "Partial",
        }))

    def test_v1_missing_deduplication_proof_is_not_verified(self):
        proof = {k: v for k, v in VERIFIED_V1.items()
                 if k != "idempotency_id_deduplication"}
        self.assert_unknown(additive(stream_delta_reconciliation=proof))

    def test_v1_missing_window_coverage_is_not_verified(self):
        proof = {k: v for k, v in VERIFIED_V1.items()
                 if k != "delivery_window_coverage"}
        self.assert_unknown(additive(stream_delta_reconciliation=proof))

    def test_v1_unverified_window_is_not_a_measured_zero(self):
        self.assert_unknown(additive(stream_delta_reconciliation={
            **VERIFIED_V1, "delivery_window_coverage": "Unknown",
        }))

    def test_v1_malformed_proof_is_not_verified(self):
        self.assert_unknown(additive(stream_delta_reconciliation="Verified"))

    def test_v1_v2_reconciliation_does_not_substitute_for_delta_proof(self):
        self.assert_unknown(additive(stream_record_reconciliation={
            "record_identity_coverage": "Verified",
            "highest_version_per_record": "Verified",
        }, stream_delta_reconciliation=VERIFIED_V1))

    def test_non_stream_cannot_use_v1_delta_proof(self):
        self.assert_unknown(additive(
            acquisition_channel="reporting_api",
            stream_delta_reconciliation=VERIFIED_V1,
        ))

    def test_v2_cannot_use_v1_delta_proof(self):
        self.assert_unknown(additive(
            acquisition_channel="amazon_marketing_stream_v2",
            stream_delta_reconciliation=VERIFIED_V1,
            stream_record_reconciliation={
                "record_identity_coverage": "Verified",
                "highest_version_per_record": "Verified",
            },
        ))

    def test_verified_v1_delta_evidence_allows_disjoint_additive_sum(self):
        result = evaluate_metric_aggregation_gate(additive(
            stream_delta_reconciliation=VERIFIED_V1,
        ))
        self.assertEqual(result["aggregation_status"], "Allowed", result)
        self.assertTrue(result["direct_sum_allowed"], result)
        self.assertEqual(result["stream_reconciliation_status"], "Verified", result)

    def test_verified_generic_v1_channel_is_equivalent(self):
        result = evaluate_metric_aggregation_gate(additive(
            acquisition_channel="amazon_marketing_stream",
            stream_generation="v1",
            stream_delta_reconciliation=VERIFIED_V1,
        ))
        self.assertEqual(result["aggregation_status"], "Allowed", result)
        self.assertTrue(result["direct_sum_allowed"], result)
        self.assertEqual(result["stream_reconciliation_status"], "Verified", result)

    def test_verified_v2_record_reconciliation_remains_supported(self):
        result = evaluate_metric_aggregation_gate(additive(
            acquisition_channel="amazon_marketing_stream_v2",
            stream_record_reconciliation={
                "record_identity_coverage": "Verified",
                "highest_version_per_record": "Verified",
            },
        ))
        self.assertEqual(result["aggregation_status"], "Allowed", result)
        self.assertTrue(result["direct_sum_allowed"], result)
        self.assertEqual(result["stream_reconciliation_status"], "Verified", result)

    def test_reporting_api_additive_disjoint_remains_supported(self):
        result = evaluate_metric_aggregation_gate(additive(
            acquisition_channel="reporting_api",
        ))
        self.assertEqual(result["aggregation_status"], "Allowed", result)
        self.assertTrue(result["direct_sum_allowed"], result)

    def test_non_additive_v1_remains_blocked(self):
        result = evaluate_metric_aggregation_gate(additive(
            metric_semantics={"aggregation_semantics": "non_additive_deduplicated"},
        ))
        self.assertEqual(result["aggregation_status"], "Blocked", result)
        self.assertFalse(result["direct_sum_allowed"], result)


if __name__ == "__main__":
    unittest.main()
