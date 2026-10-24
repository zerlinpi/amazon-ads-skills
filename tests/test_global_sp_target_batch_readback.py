"""RED-first contract: Global SP multi-target 207 index-to-readback reconciliation.

All evidence is synthetic and normalized by an external authorized adapter.
"""
import copy
import unittest


def one(i):
    request_id, target_id = f"req-{i}", f"target-{i}"
    req = {
        "resource_type": "target", "request_id": request_id,
        "global_account_id": "global-1", "campaign_id": "campaign-1",
        "ad_group_id": "adgroup-1", "target_id": target_id,
        "marketplace": "US", "target_type": "KEYWORD", "negative": False,
        "expected_target_bid": {"currency_code": "USD", "amount": "0.93"},
        "completed_at": "2026-10-24T00:00:00Z",
    }
    readback = {
        "resource_type": "target", "global_account_id": "global-1",
        "campaign_id": "campaign-1", "ad_group_id": "adgroup-1",
        "target_id": target_id, "marketplace": "US",
        "target_type": "KEYWORD", "negative": False,
        "source": {"source_system": "synthetic-api", "acquisition_channel": "query",
                   "connector_id": "synthetic-connector"},
        "observed_at": "2026-10-24T00:05:00Z",
        "coverage_status": "Complete", "pagination_status": "Complete",
        "capability_status": "Supported",
        "target_bid": {"marketplace": "US", "currency_code": "USD",
                       "amount": "0.930", "evidence_status": "observed"},
    }
    return req, {"request_id": request_id, "readback": readback}


def fixture():
    pairs = [one(0), one(1)]
    return {
        "requests": [p[0] for p in pairs],
        "receipt": {"resource_type": "target", "http_status": 207,
                    "success": [{"index": 0}, {"index": 1}],
                    "error": [], "partialSuccess": []},
        "readbacks": [p[1] for p in pairs],
    }


def evaluate(data):
    try:
        from scripts.evaluate_global_sp_target_batch_readback import evaluate_global_sp_target_batch_readback
    except ImportError as exc:
        raise AssertionError("batch target readback evaluator is missing") from exc
    return evaluate_global_sp_target_batch_readback(data)


class GlobalSpTargetBatchTests(unittest.TestCase):
    def check(self, expected, change=None):
        data = fixture()
        if change:
            change(data)
        result = evaluate(data)
        self.assertEqual(result["application_status"], expected, result)
        self.assertTrue(result["reasons"], result)
        return result

    def test_two_successes_with_complete_distinct_readbacks_confirmed(self):
        result = self.check("Confirmed")
        self.assertEqual([x["index"] for x in result["items"]], [0, 1])
        self.assertEqual([x["application_status"] for x in result["items"]],
                         ["Confirmed", "Confirmed"])

    def test_order_of_readbacks_does_not_rebind_targets(self):
        self.check("Confirmed", lambda d: d["readbacks"].reverse())

    def test_second_bid_drift_prevents_batch_confirmation(self):
        result = self.check("Drifted", lambda d:
                            d["readbacks"][1]["readback"]["target_bid"].update(amount="0.89"))
        self.assertEqual(result["items"][1]["application_status"], "Drifted")

    def test_partial_success_remains_partial(self):
        def change(d):
            d["receipt"]["success"].pop()
            d["receipt"]["partialSuccess"] = [{"index": 1}]
            d["readbacks"].pop()
        result = self.check("Partial", change)
        self.assertEqual(result["items"][1]["application_status"], "Partial")

    def test_error_remains_partial(self):
        def change(d):
            d["receipt"]["success"].pop()
            d["receipt"]["error"] = [{"index": 1}]
            d["readbacks"].pop()
        self.check("Partial", change)

    def test_partial_plus_success_drift_is_not_confirmed(self):
        def change(d):
            d["receipt"]["success"].pop()
            d["receipt"]["partialSuccess"] = [{"index": 1}]
            d["readbacks"].pop()
            d["readbacks"][0]["readback"]["target_bid"]["amount"] = "0.89"
        self.check("Partial", change)

    def test_missing_success_readback_unknown(self):
        self.check("Unknown", lambda d: d["readbacks"].pop())

    def test_truncated_success_query_unknown(self):
        self.check("Unknown", lambda d: d["readbacks"][1]["readback"].update(
            pagination_status="Truncated"))

    def test_unknown_precedes_partial_when_success_unverified(self):
        def change(d):
            d["receipt"]["success"].pop()
            d["receipt"]["partialSuccess"] = [{"index": 1}]
            d["readbacks"].pop(0)
        self.check("Unknown", change)

    def test_duplicate_receipt_index_unknown(self):
        self.check("Unknown", lambda d: d["receipt"]["success"].append({"index": 0}))

    def test_missing_receipt_index_unknown(self):
        self.check("Unknown", lambda d: d["receipt"]["success"].pop())

    def test_extra_receipt_index_unknown(self):
        self.check("Unknown", lambda d: d["receipt"]["success"].append({"index": 2}))

    def test_boolean_receipt_index_unknown(self):
        self.check("Unknown", lambda d: d["receipt"]["success"][0].update(index=True))

    def test_malformed_receipt_index_unknown(self):
        self.check("Unknown", lambda d: d["receipt"]["success"][0].update(index="0"))

    def test_duplicate_request_correlation_unknown(self):
        self.check("Unknown", lambda d: d["requests"][1].update(request_id="req-0"))

    def test_duplicate_target_identity_unknown(self):
        self.check("Unknown", lambda d: d["requests"][1].update(target_id="target-0"))

    def test_readback_wrong_request_correlation_unknown(self):
        self.check("Unknown", lambda d: d["readbacks"][1].update(request_id="req-other"))

    def test_duplicate_readback_request_id_unknown(self):
        self.check("Unknown", lambda d: d["readbacks"][1].update(request_id="req-0"))

    def test_extra_readback_row_unknown(self):
        self.check("Unknown", lambda d: d["readbacks"].append(copy.deepcopy(d["readbacks"][0])))

    def test_readback_target_swap_unknown(self):
        def change(d):
            d["readbacks"][0]["readback"]["target_id"] = "target-1"
            d["readbacks"][1]["readback"]["target_id"] = "target-0"
        self.check("Unknown", change)

    def test_cross_account_batch_unknown(self):
        self.check("Unknown", lambda d: d["requests"][1].update(global_account_id="global-2"))

    def test_malformed_receipt_global_account_unknown(self):
        self.check("Unknown", lambda d: d["receipt"].update(global_account_id=["global-1"]))

    def test_wrong_resource_receipt_unknown(self):
        self.check("Unknown", lambda d: d["receipt"].update(resource_type="ad_group"))

    def test_wrong_http_status_unknown(self):
        self.check("Unknown", lambda d: d["receipt"].update(http_status=200))

    def test_malformed_request_list_unknown(self):
        self.check("Unknown", lambda d: d.update(requests={"0": d["requests"][0]}))

    def test_unverified_extra_intent_unknown(self):
        self.check("Unknown", lambda d: d["requests"][0].update(expected_placement_adjustment={}))

    def test_receipt_returned_target_conflict_unknown(self):
        self.check("Unknown", lambda d: d["receipt"]["success"][1].update(
            target={"target_id": "target-0"}))

    def test_empty_batch_unknown(self):
        self.check("Unknown", lambda d: d.update(requests=[], readbacks=[]))

    def test_single_item_uses_batch_contract_without_false_positive(self):
        def change(d):
            d["requests"].pop()
            d["readbacks"].pop()
            d["receipt"]["success"].pop()
        self.check("Confirmed", change)


if __name__ == "__main__":
    unittest.main()
