"""Synthetic, read-only Global SP 207 receipt / per-market readback safety tests."""
import copy
import unittest


def evaluate(evidence):
    try:
        from scripts.evaluate_global_sp_readback import evaluate_global_sp_readback
    except ImportError as exc:
        raise AssertionError("Global SP receipt/readback safety gate is missing") from exc
    return evaluate_global_sp_readback(evidence)


def fixture():
    return {
        "request": {
            "global_account_id": "synthetic-global-a",
            "campaign_id": "synthetic-campaign-a",
            "marketplaces": ["US", "GB"],
            "expected_effective_states": {"US": "ENABLED", "GB": "PAUSED"},
            "completed_at": "2026-10-24T00:00:00Z",
        },
        "receipt": {
            "http_status": 207,
            "success": [{"index": 0}],
            "error": [],
            "partialSuccess": [],
        },
        "readback": {
            "global_account_id": "synthetic-global-a",
            "campaign_id": "synthetic-campaign-a",
            "source": {
                "source_system": "synthetic-ads-api",
                "acquisition_channel": "query",
                "connector_id": "synthetic-connector",
            },
            "observed_at": "2026-10-24T00:05:00Z",
            "coverage_status": "Complete",
            "pagination_status": "Complete",
            "capability_status": "Supported",
            "marketplace_states": [
                {"marketplace": "US", "effective_state": "ENABLED", "evidence_status": "observed"},
                {"marketplace": "GB", "effective_state": "PAUSED", "evidence_status": "observed"},
            ],
        },
    }


class GlobalSpReadbackEvidenceTests(unittest.TestCase):
    def assert_class(self, expected, mutation=None):
        evidence = fixture()
        if mutation:
            mutation(evidence)
        result = evaluate(evidence)
        self.assertEqual(result["application_status"], expected, result)
        self.assertTrue(result["reasons"], result)

    def test_verified_single_item_and_all_markets_confirmed(self):
        self.assert_class("Confirmed")

    def test_partial_success_never_confirmed(self):
        def mutate(e):
            e["receipt"]["success"] = []
            e["receipt"]["partialSuccess"] = [{"index": 0}]
        self.assert_class("Partial", mutate)

    def test_error_never_confirmed(self):
        def mutate(e):
            e["receipt"]["success"] = []
            e["receipt"]["error"] = [{"index": 0}]
        self.assert_class("Partial", mutate)

    def test_missing_receipt_index_is_unknown(self):
        self.assert_class("Unknown", lambda e: e["receipt"].update(success=[]))

    def test_duplicate_index_across_receipt_groups_is_unknown(self):
        self.assert_class("Unknown", lambda e: e["receipt"].update(partialSuccess=[{"index": 0}]))

    def test_wrong_receipt_index_is_unknown(self):
        self.assert_class("Unknown", lambda e: e["receipt"].update(success=[{"index": 1}]))

    def test_success_receipt_without_readback_is_unknown(self):
        self.assert_class("Unknown", lambda e: e.pop("readback"))

    def test_truncated_query_is_unknown(self):
        self.assert_class("Unknown", lambda e: e["readback"].update(pagination_status="Truncated"))

    def test_partial_connector_capability_is_unknown(self):
        self.assert_class("Unknown", lambda e: e["readback"].update(capability_status="Partial"))

    def test_missing_marketplace_is_unknown(self):
        self.assert_class("Unknown", lambda e: e["readback"].update(marketplace_states=e["readback"]["marketplace_states"][:1]))

    def test_duplicate_marketplace_is_unknown(self):
        self.assert_class("Unknown", lambda e: e["readback"]["marketplace_states"].append(copy.deepcopy(e["readback"]["marketplace_states"][0])))

    def test_per_market_override_drift_is_detected(self):
        self.assert_class("Drifted", lambda e: e["readback"]["marketplace_states"][1].update(effective_state="ENABLED"))

    def test_stale_readback_is_unknown(self):
        self.assert_class("Unknown", lambda e: e["readback"].update(observed_at="2026-10-23T23:59:59Z"))

    def test_mismatched_global_account_is_unknown(self):
        self.assert_class("Unknown", lambda e: e["readback"].update(global_account_id="synthetic-global-b"))

    def test_mismatched_campaign_is_unknown(self):
        self.assert_class("Unknown", lambda e: e["readback"].update(campaign_id="synthetic-campaign-b"))

    def test_missing_source_is_unknown(self):
        self.assert_class("Unknown", lambda e: e["readback"].pop("source"))

    def test_delivery_status_is_not_configured_effective_state(self):
        self.assert_class("Unknown", lambda e: e["readback"]["marketplace_states"][1].update(effective_state=None, delivery_status="NOT_DELIVERING"))

    def test_http_200_does_not_prove_multi_status(self):
        self.assert_class("Unknown", lambda e: e["receipt"].update(http_status=200))

    def test_unknown_marketplace_state_is_not_zero_or_paused(self):
        self.assert_class("Unknown", lambda e: e["readback"]["marketplace_states"][1].update(effective_state="Unknown"))

    def test_malformed_unhashable_expected_state_is_unknown(self):
        self.assert_class("Unknown", lambda e: e["request"]["expected_effective_states"].update(GB=[]))

    def test_malformed_unhashable_readback_state_is_unknown(self):
        self.assert_class("Unknown", lambda e: e["readback"]["marketplace_states"][1].update(effective_state={}))

    def test_partial_readback_coverage_is_unknown(self):
        self.assert_class("Unknown", lambda e: e["readback"].update(coverage_status="Partial"))

    def test_receipt_does_not_authorize_multi_item_batch(self):
        self.assert_class("Unknown", lambda e: e["receipt"].update(success=[{"index": 0}, {"index": 1}]))


if __name__ == "__main__":
    unittest.main()
