"""RED-first: an explicitly supplied Global SP query pagination trace must be coherent.

Synthetic data only. A trace proves internal consistency, not external API authenticity.
"""
import copy
import unittest

from test_global_sp_readback_evidence import fixture, evaluate


def with_trace():
    e = fixture()
    source = copy.deepcopy(e["readback"]["source"])
    e["readback"]["pagination_trace"] = {
        "query": {
            "global_account_id": "synthetic-global-a",
            "campaign_id": "synthetic-campaign-a",
            "ad_product": "SPONSORED_PRODUCTS",
            "marketplace_scope": "GLOBAL",
            "query_fingerprint": "synthetic-query-filter-a",
        },
        "pages": [
            {
                "request_token": None,
                "next_token": "synthetic-token-2",
                "observed_at": "2026-10-24T00:02:00Z",
                "global_account_id": "synthetic-global-a",
                "campaign_id": "synthetic-campaign-a",
                "query_fingerprint": "synthetic-query-filter-a",
                "source": copy.deepcopy(source),
            },
            {
                "request_token": "synthetic-token-2",
                "next_token": None,
                "observed_at": "2026-10-24T00:04:00Z",
                "global_account_id": "synthetic-global-a",
                "campaign_id": "synthetic-campaign-a",
                "query_fingerprint": "synthetic-query-filter-a",
                "source": copy.deepcopy(source),
            },
        ],
    }
    return e


class GlobalSpPaginationTraceTests(unittest.TestCase):
    def check(self, expected, evidence):
        result = evaluate(evidence)
        self.assertEqual(result["application_status"], expected, result)

    def test_legacy_without_trace_still_confirms(self):
        self.check("Confirmed", fixture())

    def test_complete_two_page_trace_confirms(self):
        self.check("Confirmed", with_trace())

    def test_complete_single_page_trace_confirms(self):
        e = with_trace()
        e["readback"]["pagination_trace"]["pages"] = [e["readback"]["pagination_trace"]["pages"][0]]
        e["readback"]["pagination_trace"]["pages"][0]["next_token"] = None
        self.check("Confirmed", e)

    def test_explicit_null_trace_unknown(self):
        e = with_trace()
        e["readback"]["pagination_trace"] = None
        self.check("Unknown", e)

    def test_empty_page_list_unknown(self):
        e = with_trace()
        e["readback"]["pagination_trace"]["pages"] = []
        self.check("Unknown", e)

    def test_missing_page_list_unknown(self):
        e = with_trace()
        del e["readback"]["pagination_trace"]["pages"]
        self.check("Unknown", e)

    def test_initial_request_token_must_be_null(self):
        e = with_trace()
        e["readback"]["pagination_trace"]["pages"][0]["request_token"] = "unexpected"
        self.check("Unknown", e)

    def test_missing_continuation_page_unknown(self):
        e = with_trace()
        e["readback"]["pagination_trace"]["pages"].pop()
        self.check("Unknown", e)

    def test_terminal_token_before_final_page_unknown(self):
        e = with_trace()
        e["readback"]["pagination_trace"]["pages"][0]["next_token"] = None
        e["readback"]["pagination_trace"]["pages"][1]["request_token"] = None
        self.check("Unknown", e)

    def test_missing_page_token_key_unknown(self):
        e = with_trace()
        del e["readback"]["pagination_trace"]["pages"][1]["next_token"]
        self.check("Unknown", e)

    def test_wrong_continuation_token_unknown(self):
        e = with_trace()
        e["readback"]["pagination_trace"]["pages"][1]["request_token"] = "wrong-token"
        self.check("Unknown", e)

    def test_duplicate_continuation_token_unknown(self):
        e = with_trace()
        third = copy.deepcopy(e["readback"]["pagination_trace"]["pages"][1])
        third["request_token"] = "synthetic-token-2"
        third["next_token"] = None
        e["readback"]["pagination_trace"]["pages"][1]["next_token"] = "synthetic-token-2"
        e["readback"]["pagination_trace"]["pages"].append(third)
        self.check("Unknown", e)

    def test_numeric_token_unknown(self):
        e = with_trace()
        e["readback"]["pagination_trace"]["pages"][0]["next_token"] = 2
        self.check("Unknown", e)

    def test_empty_string_token_unknown(self):
        e = with_trace()
        e["readback"]["pagination_trace"]["pages"][0]["next_token"] = ""
        self.check("Unknown", e)

    def test_query_account_mismatch_unknown(self):
        e = with_trace()
        e["readback"]["pagination_trace"]["query"]["global_account_id"] = "synthetic-other"
        self.check("Unknown", e)

    def test_query_campaign_mismatch_unknown(self):
        e = with_trace()
        e["readback"]["pagination_trace"]["query"]["campaign_id"] = "synthetic-other"
        self.check("Unknown", e)

    def test_query_resource_type_mismatch_unknown(self):
        e = with_trace()
        e["readback"]["pagination_trace"]["query"]["ad_product"] = "SPONSORED_BRANDS"
        self.check("Unknown", e)

    def test_query_marketplace_scope_mismatch_unknown(self):
        e = with_trace()
        e["readback"]["pagination_trace"]["query"]["marketplace_scope"] = "LOCAL"
        self.check("Unknown", e)

    def test_missing_query_fingerprint_unknown(self):
        e = with_trace()
        del e["readback"]["pagination_trace"]["query"]["query_fingerprint"]
        self.check("Unknown", e)

    def test_page_query_fingerprint_mismatch_unknown(self):
        e = with_trace()
        e["readback"]["pagination_trace"]["pages"][1]["query_fingerprint"] = "synthetic-other"
        self.check("Unknown", e)

    def test_page_campaign_mismatch_unknown(self):
        e = with_trace()
        e["readback"]["pagination_trace"]["pages"][1]["campaign_id"] = "synthetic-other"
        self.check("Unknown", e)

    def test_page_account_mismatch_unknown(self):
        e = with_trace()
        e["readback"]["pagination_trace"]["pages"][1]["global_account_id"] = "synthetic-other"
        self.check("Unknown", e)

    def test_page_source_mismatch_unknown(self):
        e = with_trace()
        e["readback"]["pagination_trace"]["pages"][1]["source"]["connector_id"] = "synthetic-other"
        self.check("Unknown", e)

    def test_page_missing_source_unknown(self):
        e = with_trace()
        del e["readback"]["pagination_trace"]["pages"][1]["source"]
        self.check("Unknown", e)

    def test_page_before_write_completion_unknown(self):
        e = with_trace()
        e["readback"]["pagination_trace"]["pages"][0]["observed_at"] = "2026-10-23T23:59:59Z"
        self.check("Unknown", e)

    def test_page_after_readback_envelope_unknown(self):
        e = with_trace()
        e["readback"]["pagination_trace"]["pages"][1]["observed_at"] = "2026-10-24T00:06:00Z"
        self.check("Unknown", e)

    def test_page_observation_order_reversed_unknown(self):
        e = with_trace()
        e["readback"]["pagination_trace"]["pages"][0]["observed_at"] = "2026-10-24T00:04:30Z"
        self.check("Unknown", e)

    def test_invalid_page_timestamp_unknown(self):
        e = with_trace()
        e["readback"]["pagination_trace"]["pages"][0]["observed_at"] = "not-a-timestamp"
        self.check("Unknown", e)

    def test_trace_consistent_but_state_drift_stays_drifted(self):
        e = with_trace()
        e["readback"]["marketplace_states"][1]["effective_state"] = "ENABLED"
        self.check("Drifted", e)


if __name__ == "__main__":
    unittest.main()
