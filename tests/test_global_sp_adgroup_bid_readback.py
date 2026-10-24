"""Synthetic RED contract for Global SP single-ad-group marketplace default-bid readback.

The campaign state gate must not be reused to certify ad-group bids. This
separate, read-only gate requires an executor-bound 207 receipt and independent
post-write ad-group query evidence for every requested marketplace.
"""
import copy
import unittest


def fixture():
    return {
        "request": {
            "resource_type": "ad_group",
            "request_id": "synthetic-request-01",
            "global_account_id": "synthetic-global-a",
            "campaign_id": "synthetic-campaign-a",
            "ad_group_id": "synthetic-adgroup-a",
            "marketplaces": ["US", "GB"],
            "expected_marketplace_default_bids": {
                "US": {"currency_code": "USD", "amount": "0.98"},
                "GB": {"currency_code": "GBP", "amount": "0.57"},
            },
            "completed_at": "2026-10-24T00:00:00Z",
        },
        "receipt": {
            "resource_type": "ad_group",
            "request_id": "synthetic-request-01",
            "global_account_id": "synthetic-global-a",
            "campaign_id": "synthetic-campaign-a",
            "ad_group_id": "synthetic-adgroup-a",
            "http_status": 207,
            "success": [{"index": 0}],
            "error": [],
            "partialSuccess": [],
        },
        "readback": {
            "resource_type": "ad_group",
            "global_account_id": "synthetic-global-a",
            "campaign_id": "synthetic-campaign-a",
            "ad_group_id": "synthetic-adgroup-a",
            "source": {
                "source_system": "synthetic-ads-api",
                "acquisition_channel": "query",
                "connector_id": "synthetic-connector",
            },
            "observed_at": "2026-10-24T00:05:00Z",
            "coverage_status": "Complete",
            "pagination_status": "Complete",
            "capability_status": "Supported",
            "marketplace_default_bids": [
                {"marketplace": "US", "currency_code": "USD", "amount": "0.980",
                 "evidence_status": "observed"},
                {"marketplace": "GB", "currency_code": "GBP", "amount": "0.57",
                 "evidence_status": "observed"},
            ],
        },
    }


def evaluate(evidence):
    try:
        from scripts.evaluate_global_sp_adgroup_bid_readback import evaluate_global_sp_adgroup_bid_readback
    except ImportError as exc:
        raise AssertionError("independent Global SP ad-group bid readback gate is missing") from exc
    return evaluate_global_sp_adgroup_bid_readback(evidence)


class GlobalSpAdgroupBidReadbackTests(unittest.TestCase):
    def check(self, expected, mutate=None):
        data = fixture()
        if mutate:
            mutate(data)
        result = evaluate(data)
        self.assertEqual(result["application_status"], expected, result)
        self.assertTrue(result["reasons"], result)

    def test_verified_all_markets_confirmed(self):
        self.check("Confirmed")

    def test_decimal_string_equivalence(self):
        self.check("Confirmed", lambda d: d["readback"]["marketplace_default_bids"][0].update(amount="0.9800"))

    def test_explicit_observed_zero_is_not_missing(self):
        self.check("Confirmed", lambda d: (
            d["request"]["expected_marketplace_default_bids"]["GB"].update(amount="0"),
            d["readback"]["marketplace_default_bids"][1].update(amount="0.00"),
        ))

    def test_mismatched_bid_is_drifted(self):
        self.check("Drifted", lambda d: d["readback"]["marketplace_default_bids"][1].update(amount="0.56"))

    def test_currency_mismatch_is_drifted_no_fx(self):
        self.check("Drifted", lambda d: d["readback"]["marketplace_default_bids"][0].update(currency_code="CAD"))

    def test_missing_marketplace_unknown(self):
        self.check("Unknown", lambda d: d["readback"].update(marketplace_default_bids=d["readback"]["marketplace_default_bids"][:1]))

    def test_duplicate_marketplace_unknown(self):
        self.check("Unknown", lambda d: d["readback"]["marketplace_default_bids"].append(copy.deepcopy(d["readback"]["marketplace_default_bids"][0])))

    def test_extra_marketplace_unknown(self):
        self.check("Unknown", lambda d: d["readback"]["marketplace_default_bids"].append(
            {"marketplace": "DE", "currency_code": "EUR", "amount": "0.47", "evidence_status": "observed"}))

    def test_unobserved_row_unknown(self):
        self.check("Unknown", lambda d: d["readback"]["marketplace_default_bids"][0].update(evidence_status="unknown"))

    def test_missing_row_amount_unknown(self):
        self.check("Unknown", lambda d: d["readback"]["marketplace_default_bids"][0].pop("amount"))

    def test_nonfinite_bid_unknown(self):
        self.check("Unknown", lambda d: d["readback"]["marketplace_default_bids"][0].update(amount="NaN"))

    def test_json_float_bid_unknown(self):
        self.check("Unknown", lambda d: d["readback"]["marketplace_default_bids"][0].update(amount=0.98))

    def test_negative_bid_unknown(self):
        self.check("Unknown", lambda d: d["request"]["expected_marketplace_default_bids"]["US"].update(amount="-0.1"))

    def test_missing_readback_unknown(self):
        self.check("Unknown", lambda d: d.pop("readback"))

    def test_truncated_pagination_unknown(self):
        self.check("Unknown", lambda d: d["readback"].update(pagination_status="Truncated"))

    def test_partial_connector_unknown(self):
        self.check("Unknown", lambda d: d["readback"].update(capability_status="Partial"))

    def test_partial_coverage_unknown(self):
        self.check("Unknown", lambda d: d["readback"].update(coverage_status="Partial"))

    def test_stale_readback_unknown(self):
        self.check("Unknown", lambda d: d["readback"].update(observed_at="2026-10-24T00:00:00Z"))

    def test_row_time_before_completion_unknown(self):
        self.check("Unknown", lambda d: d["readback"]["marketplace_default_bids"][0].update(observed_at="2026-10-23T23:59:00Z"))

    def test_row_source_mismatch_unknown(self):
        self.check("Unknown", lambda d: d["readback"]["marketplace_default_bids"][0].update(
            source={"source_system": "synthetic-other", "acquisition_channel": "query", "connector_id": "synthetic-connector"}))

    def test_row_identity_mismatch_unknown(self):
        self.check("Unknown", lambda d: d["readback"]["marketplace_default_bids"][0].update(ad_group_id="synthetic-other"))

    def test_receipt_resource_mismatch_unknown(self):
        self.check("Unknown", lambda d: d["receipt"].update(resource_type="campaign"))

    def test_receipt_request_id_mismatch_unknown(self):
        self.check("Unknown", lambda d: d["receipt"].update(request_id="synthetic-other"))

    def test_receipt_adgroup_id_mismatch_unknown(self):
        self.check("Unknown", lambda d: d["receipt"].update(ad_group_id="synthetic-other"))

    def test_receipt_partial_is_partial(self):
        self.check("Partial", lambda d: d["receipt"].update(success=[], partialSuccess=[{"index": 0}]))

    def test_receipt_error_is_partial(self):
        self.check("Partial", lambda d: d["receipt"].update(success=[], error=[{"index": 0}]))

    def test_receipt_multi_item_unknown(self):
        self.check("Unknown", lambda d: d["receipt"].update(success=[{"index": 0}, {"index": 1}]))

    def test_duplicate_receipt_index_unknown(self):
        self.check("Unknown", lambda d: d["receipt"].update(partialSuccess=[{"index": 0}]))

    def test_unknown_extra_expected_intent_unknown(self):
        self.check("Unknown", lambda d: d["request"].update(expected_target_bids={}))

    def test_readback_campaign_identity_mismatch_unknown(self):
        self.check("Unknown", lambda d: d["readback"].update(campaign_id="synthetic-other"))

    def test_receipt_http200_unknown(self):
        self.check("Unknown", lambda d: d["receipt"].update(http_status=200))

    def test_request_duplicate_markets_unknown(self):
        self.check("Unknown", lambda d: d["request"].update(marketplaces=["US", "US"]))

    def test_invalid_request_expected_market_scope_unknown(self):
        self.check("Unknown", lambda d: d["request"]["expected_marketplace_default_bids"].pop("GB"))

    def test_readback_source_missing_unknown(self):
        self.check("Unknown", lambda d: d["readback"].pop("source"))

    def test_valid_offset_timestamp_equivalence(self):
        self.check("Confirmed", lambda d: d["readback"]["marketplace_default_bids"][0].update(
            observed_at="2026-10-24T08:04:00+08:00"))


if __name__ == "__main__":
    unittest.main()
