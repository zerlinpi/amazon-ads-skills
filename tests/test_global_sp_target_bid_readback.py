"""Deterministic contract for independent Global SP single-target bid readback.

A target is a single-marketplace resource; a campaign or ad-group receipt and
default bid cannot prove a target-specific configured bid.
"""
import copy
import unittest


def fixture():
    return {
        "request": {
            "resource_type": "target",
            "request_id": "synthetic-request-t1",
            "global_account_id": "synthetic-global",
            "campaign_id": "synthetic-campaign",
            "ad_group_id": "synthetic-adgroup",
            "target_id": "synthetic-target",
            "marketplace": "US",
            "target_type": "KEYWORD",
            "negative": False,
            "expected_target_bid": {"currency_code": "USD", "amount": "0.93"},
            "completed_at": "2026-10-24T00:00:00Z",
        },
        "receipt": {
            "resource_type": "target",
            "request_id": "synthetic-request-t1",
            "global_account_id": "synthetic-global",
            "campaign_id": "synthetic-campaign",
            "ad_group_id": "synthetic-adgroup",
            "target_id": "synthetic-target",
            "http_status": 207,
            "success": [{"index": 0}],
            "error": [],
            "partialSuccess": [],
        },
        "readback": {
            "resource_type": "target",
            "global_account_id": "synthetic-global",
            "campaign_id": "synthetic-campaign",
            "ad_group_id": "synthetic-adgroup",
            "target_id": "synthetic-target",
            "marketplace": "US",
            "target_type": "KEYWORD",
            "negative": False,
            "source": {
                "source_system": "synthetic-ads-api",
                "acquisition_channel": "query",
                "connector_id": "synthetic-connector",
            },
            "observed_at": "2026-10-24T00:05:00Z",
            "coverage_status": "Complete",
            "pagination_status": "Complete",
            "capability_status": "Supported",
            "target_bid": {
                "marketplace": "US",
                "currency_code": "USD",
                "amount": "0.930",
                "evidence_status": "observed",
            },
        },
    }


def evaluate(evidence):
    try:
        from scripts.evaluate_global_sp_target_bid_readback import evaluate_global_sp_target_bid_readback
    except ImportError as exc:
        raise AssertionError("independent target bid readback gate is missing") from exc
    return evaluate_global_sp_target_bid_readback(evidence)


class GlobalSpTargetBidReadbackTests(unittest.TestCase):
    def check(self, expected, mutate=None):
        data = fixture()
        if mutate:
            mutate(data)
        result = evaluate(data)
        self.assertEqual(result["application_status"], expected, result)
        self.assertTrue(result["reasons"], result)

    def test_verified_single_marketplace_target_confirmed(self):
        self.check("Confirmed")

    def test_decimal_equivalent_bid_confirmed(self):
        self.check("Confirmed", lambda d: d["readback"]["target_bid"].update(amount="0.93000"))

    def test_explicit_observed_zero_confirmed(self):
        self.check("Confirmed", lambda d: (
            d["request"]["expected_target_bid"].update(amount="0"),
            d["readback"]["target_bid"].update(amount="0.000"),
        ))

    def test_product_target_supported(self):
        self.check("Confirmed", lambda d: (
            d["request"].update(target_type="PRODUCT"),
            d["readback"].update(target_type="PRODUCT"),
        ))

    def test_target_bid_amount_drifted(self):
        self.check("Drifted", lambda d: d["readback"]["target_bid"].update(amount="0.92"))

    def test_target_bid_currency_drifted_without_fx(self):
        self.check("Drifted", lambda d: d["readback"]["target_bid"].update(currency_code="CAD"))

    def test_partial_success_receipt_partial(self):
        self.check("Partial", lambda d: d["receipt"].update(success=[], partialSuccess=[{"index": 0}]))

    def test_error_receipt_partial(self):
        self.check("Partial", lambda d: d["receipt"].update(success=[], error=[{"index": 0}]))

    def test_missing_readback_unknown(self):
        self.check("Unknown", lambda d: d.pop("readback"))

    def test_campaign_receipt_cannot_confirm_target(self):
        self.check("Unknown", lambda d: d["receipt"].update(resource_type="campaign"))

    def test_adgroup_receipt_cannot_confirm_target(self):
        self.check("Unknown", lambda d: d["receipt"].update(resource_type="ad_group"))

    def test_receipt_target_identity_conflict_unknown(self):
        self.check("Unknown", lambda d: d["receipt"].update(target_id="other-target"))

    def test_receipt_request_correlation_conflict_unknown(self):
        self.check("Unknown", lambda d: d["receipt"].update(request_id="other-request"))

    def test_receipt_wrong_http_status_unknown(self):
        self.check("Unknown", lambda d: d["receipt"].update(http_status=200))

    def test_receipt_duplicate_index_unknown(self):
        self.check("Unknown", lambda d: d["receipt"].update(partialSuccess=[{"index": 0}]))

    def test_receipt_multi_item_unknown(self):
        self.check("Unknown", lambda d: d["receipt"].update(success=[{"index": 0}, {"index": 1}]))

    def test_request_multi_marketplace_target_unknown(self):
        self.check("Unknown", lambda d: d["request"].update(marketplace=["US", "GB"]))

    def test_request_negative_target_unknown(self):
        self.check("Unknown", lambda d: d["request"].update(negative=True))

    def test_request_theme_without_explicit_bid_unknown(self):
        self.check("Unknown", lambda d: (
            d["request"].update(target_type="THEME"),
            d["readback"].update(target_type="THEME"),
        ))

    def test_readback_target_type_conflict_unknown(self):
        self.check("Unknown", lambda d: d["readback"].update(target_type="PRODUCT"))

    def test_readback_negative_conflict_unknown(self):
        self.check("Unknown", lambda d: d["readback"].update(negative=True))

    def test_readback_adgroup_identity_conflict_unknown(self):
        self.check("Unknown", lambda d: d["readback"].update(ad_group_id="other-adgroup"))

    def test_readback_marketplace_conflict_unknown(self):
        self.check("Unknown", lambda d: d["readback"].update(marketplace="GB"))

    def test_bid_row_marketplace_conflict_unknown(self):
        self.check("Unknown", lambda d: d["readback"]["target_bid"].update(marketplace="GB"))

    def test_missing_bid_evidence_unknown(self):
        self.check("Unknown", lambda d: d["readback"].pop("target_bid"))

    def test_unobserved_bid_unknown(self):
        self.check("Unknown", lambda d: d["readback"]["target_bid"].update(evidence_status="unknown"))

    def test_missing_amount_unknown_not_zero(self):
        self.check("Unknown", lambda d: d["readback"]["target_bid"].pop("amount"))

    def test_float_amount_unknown(self):
        self.check("Unknown", lambda d: d["readback"]["target_bid"].update(amount=0.93))

    def test_nonfinite_amount_unknown(self):
        self.check("Unknown", lambda d: d["readback"]["target_bid"].update(amount="NaN"))

    def test_negative_amount_unknown(self):
        self.check("Unknown", lambda d: d["request"]["expected_target_bid"].update(amount="-0.01"))

    def test_stale_readback_unknown(self):
        self.check("Unknown", lambda d: d["readback"].update(observed_at="2026-10-24T00:00:00Z"))

    def test_row_time_conflict_unknown(self):
        self.check("Unknown", lambda d: d["readback"]["target_bid"].update(observed_at="2026-10-23T23:59:00Z"))

    def test_row_source_conflict_unknown(self):
        self.check("Unknown", lambda d: d["readback"]["target_bid"].update(
            source={"source_system": "other", "acquisition_channel": "query", "connector_id": "synthetic-connector"}))

    def test_row_target_identity_conflict_unknown(self):
        self.check("Unknown", lambda d: d["readback"]["target_bid"].update(target_id="other-target"))

    def test_partial_connector_unknown(self):
        self.check("Unknown", lambda d: d["readback"].update(capability_status="Partial"))

    def test_truncated_pagination_unknown(self):
        self.check("Unknown", lambda d: d["readback"].update(pagination_status="Truncated"))

    def test_partial_coverage_unknown(self):
        self.check("Unknown", lambda d: d["readback"].update(coverage_status="Partial"))

    def test_unverified_extra_expected_intent_unknown(self):
        self.check("Unknown", lambda d: d["request"].update(expected_ad_group_default_bid={}))

    def test_returned_target_identity_conflict_unknown(self):
        self.check("Unknown", lambda d: d["receipt"]["success"][0].update(
            target={"target_id": "other-target"}))

    def test_valid_offset_row_time_confirmed(self):
        self.check("Confirmed", lambda d: d["readback"]["target_bid"].update(
            observed_at="2026-10-24T08:04:00+08:00"))

    def test_unhashable_target_type_unknown(self):
        self.check("Unknown", lambda d: d["request"].update(target_type=["KEYWORD"]))

    def test_bid_row_target_type_conflict_unknown(self):
        self.check("Unknown", lambda d: d["readback"]["target_bid"].update(target_type="PRODUCT"))

    def test_bid_row_negative_conflict_unknown(self):
        self.check("Unknown", lambda d: d["readback"]["target_bid"].update(negative=True))

    def test_receipt_returned_target_type_conflict_unknown(self):
        self.check("Unknown", lambda d: d["receipt"]["success"][0].update(
            target={"target_type": "PRODUCT"}))

    def test_receipt_returned_negative_conflict_unknown(self):
        self.check("Unknown", lambda d: d["receipt"]["success"][0].update(
            target={"negative": True}))


if __name__ == "__main__":
    unittest.main()
