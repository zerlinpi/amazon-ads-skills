"""Synthetic RED-first Global SP multi-ad-group default-bid batch contract."""
import copy
import unittest


def fixture():
    from test_global_sp_adgroup_bid_readback import fixture as single
    a, b = single(), single()
    b["request"]["request_id"] = "synthetic-request-02"
    b["request"]["ad_group_id"] = "synthetic-adgroup-b"
    b["receipt"]["request_id"] = "synthetic-request-02"
    b["receipt"]["ad_group_id"] = "synthetic-adgroup-b"
    b["readback"]["ad_group_id"] = "synthetic-adgroup-b"
    return {
        "requests": [a["request"], b["request"]],
        "receipt": {"resource_type": "ad_group", "http_status": 207,
                    "global_account_id": "synthetic-global-a",
                    "success": [{"index": 0}, {"index": 1}],
                    "error": [], "partialSuccess": []},
        "readbacks": [
            {"request_id": a["request"]["request_id"], "readback": a["readback"]},
            {"request_id": b["request"]["request_id"], "readback": b["readback"]},
        ],
    }


def evaluate(evidence):
    from scripts.evaluate_global_sp_adgroup_batch_readback import (
        evaluate_global_sp_adgroup_batch_readback,
    )
    return evaluate_global_sp_adgroup_batch_readback(evidence)


class GlobalSpAdgroupBatchTests(unittest.TestCase):
    def check(self, status, change=None):
        data = fixture()
        if change:
            change(data)
        result = evaluate(data)
        self.assertEqual(result["application_status"], status, result)
        self.assertTrue(result["reasons"])
        return result

    def test_two_distinct_adgroups_confirm(self):
        result = self.check("Confirmed")
        self.assertEqual([i["index"] for i in result["items"]], [0, 1])
        self.assertEqual([i["application_status"] for i in result["items"]],
                         ["Confirmed", "Confirmed"])

    def test_reordered_readbacks_are_correlated_by_request_id(self):
        self.check("Confirmed", lambda d: d["readbacks"].reverse())

    def test_second_marketplace_bid_drift(self):
        self.check("Drifted", lambda d: d["readbacks"][1]["readback"][
            "marketplace_default_bids"][1].update(amount="0.55"))

    def test_second_currency_drift(self):
        self.check("Drifted", lambda d: d["readbacks"][1]["readback"][
            "marketplace_default_bids"][0].update(currency_code="CAD"))

    def test_partial_item(self):
        def change(d):
            d["receipt"]["success"].pop()
            d["receipt"]["partialSuccess"] = [{"index": 1}]
            d["readbacks"].pop()
        self.check("Partial", change)

    def test_error_item(self):
        def change(d):
            d["receipt"]["success"].pop()
            d["receipt"]["error"] = [{"index": 1}]
            d["readbacks"].pop()
        self.check("Partial", change)

    def test_partial_and_stale_success_unknown(self):
        def change(d):
            d["receipt"]["success"].pop()
            d["receipt"]["partialSuccess"] = [{"index": 1}]
            d["readbacks"].pop()
            d["readbacks"][0]["readback"]["observed_at"] = "2026-10-24T00:00:00Z"
        self.check("Unknown", change)

    def test_missing_success_readback_unknown(self):
        self.check("Unknown", lambda d: d["readbacks"].pop())

    def test_extra_readback_unknown(self):
        self.check("Unknown", lambda d: d["readbacks"].append(copy.deepcopy(d["readbacks"][0])))

    def test_swapped_adgroup_identity_unknown(self):
        def change(d):
            d["readbacks"][0]["readback"]["ad_group_id"] = "synthetic-adgroup-b"
            d["readbacks"][1]["readback"]["ad_group_id"] = "synthetic-adgroup-a"
        self.check("Unknown", change)

    def test_duplicate_adgroup_request_unknown(self):
        self.check("Unknown", lambda d: d["requests"][1].update(
            ad_group_id="synthetic-adgroup-a"))

    def test_duplicate_request_id_unknown(self):
        self.check("Unknown", lambda d: d["requests"][1].update(
            request_id="synthetic-request-01"))

    def test_cross_account_unknown(self):
        self.check("Unknown", lambda d: d["requests"][1].update(
            global_account_id="synthetic-global-b"))

    def test_duplicate_receipt_index_unknown(self):
        self.check("Unknown", lambda d: d["receipt"]["success"].append({"index": 0}))

    def test_missing_receipt_index_unknown(self):
        self.check("Unknown", lambda d: d["receipt"]["success"].pop())

    def test_boolean_receipt_index_unknown(self):
        self.check("Unknown", lambda d: d["receipt"]["success"][0].update(index=True))

    def test_out_of_range_index_unknown(self):
        self.check("Unknown", lambda d: d["receipt"]["success"][0].update(index=2))

    def test_receipt_returned_resource_conflict_unknown(self):
        self.check("Unknown", lambda d: d["receipt"]["success"][1].update(
            ad_group={"ad_group_id": "synthetic-adgroup-a"}))

    def test_receipt_explicit_identity_conflict_unknown(self):
        self.check("Unknown", lambda d: d["receipt"]["success"][1].update(
            campaign_id="synthetic-campaign-other"))

    def test_malformed_receipt_account_unknown(self):
        self.check("Unknown", lambda d: d["receipt"].update(
            global_account_id=["synthetic-global-a"]))

    def test_partial_capability_unknown(self):
        self.check("Unknown", lambda d: d["readbacks"][0]["readback"].update(
            capability_status="Partial"))

    def test_truncated_pagination_unknown(self):
        self.check("Unknown", lambda d: d["readbacks"][0]["readback"].update(
            pagination_status="Truncated"))

    def test_unverified_extra_intent_unknown(self):
        self.check("Unknown", lambda d: d["requests"][0].update(
            expected_target_bid={}))

    def test_unverified_batch_level_intent_unknown(self):
        self.check("Unknown", lambda d: d.update(expected_target_bid={}))

    def test_wrong_resource_unknown(self):
        self.check("Unknown", lambda d: d["receipt"].update(resource_type="target"))

    def test_wrong_http_status_unknown(self):
        self.check("Unknown", lambda d: d["receipt"].update(http_status=200))

    def test_one_item_batch_confirmed(self):
        def change(d):
            d["requests"].pop()
            d["readbacks"].pop()
            d["receipt"]["success"].pop()
        self.check("Confirmed", change)

    def test_empty_batch_unknown(self):
        self.check("Unknown", lambda d: d.update(requests=[], readbacks=[]))


if __name__ == "__main__":
    unittest.main()
