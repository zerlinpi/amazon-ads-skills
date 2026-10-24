"""RED-first: optional native query request filters must bind to paginated Global SP evidence.

Synthetic adapter assertions only: internal consistency, not HTTP authenticity.
"""
import copy
import unittest

from test_global_sp_readback_evidence import evaluate
from test_global_sp_query_pagination_trace import with_trace


def with_request_binding():
    evidence = with_trace()
    filters = {
        "adProductFilter": {"include": ["SPONSORED_PRODUCTS"]},
        "marketplaceScopeFilter": {"include": ["GLOBAL"]},
        "campaignIdFilter": {"include": ["synthetic-campaign-a"]},
        "maxResults": 100,
    }
    trace = evidence["readback"]["pagination_trace"]
    trace["query"]["request_filters"] = copy.deepcopy(filters)
    for page in trace["pages"]:
        body = copy.deepcopy(filters)
        if page["request_token"] is not None:
            body["nextToken"] = page["request_token"]
        page["request_body"] = body
    return evidence


class GlobalSpQueryRequestBindingTests(unittest.TestCase):
    def check(self, expected, mutate=None, *, legacy=False):
        evidence = with_trace() if legacy else with_request_binding()
        if mutate:
            mutate(evidence)
        result = evaluate(evidence)
        self.assertEqual(result["application_status"], expected, result)

    def test_legacy_fingerprint_only_remains_compatible(self):
        self.check("Confirmed", legacy=True)

    def test_exact_two_page_request_chain_confirms(self):
        self.check("Confirmed")

    def test_exact_single_page_request_confirms(self):
        def mutate(e):
            pages = e["readback"]["pagination_trace"]["pages"]
            pages[:] = pages[:1]
            pages[0]["next_token"] = None
        self.check("Confirmed", mutate)

    def test_request_binding_does_not_hide_real_drift(self):
        self.check("Drifted", lambda e: e["readback"]["marketplace_states"][1].update(effective_state="ENABLED"))

    def test_query_filters_explicit_null_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["pagination_trace"]["query"].update(request_filters=None))

    def test_query_filters_missing_required_ad_product_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["pagination_trace"]["query"]["request_filters"].pop("adProductFilter"))

    def test_query_filters_wrong_product_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["pagination_trace"]["query"]["request_filters"]["adProductFilter"].update(include=["SPONSORED_BRANDS"]))

    def test_query_filters_wrong_scope_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["pagination_trace"]["query"]["request_filters"]["marketplaceScopeFilter"].update(include=["LOCAL"]))

    def test_query_filters_wrong_campaign_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["pagination_trace"]["query"]["request_filters"]["campaignIdFilter"].update(include=["synthetic-other"]))

    def test_query_filters_extra_campaign_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["pagination_trace"]["query"]["request_filters"]["campaignIdFilter"].update(include=["synthetic-campaign-a", "synthetic-other"]))

    def test_query_filters_unverified_extra_state_filter_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["pagination_trace"]["query"]["request_filters"].update(stateFilter={"include": ["ENABLED"]}))

    def test_query_filters_cannot_include_continuation_token(self):
        self.check("Unknown", lambda e: e["readback"]["pagination_trace"]["query"]["request_filters"].update(nextToken="synthetic-token-2"))

    def test_query_filters_boolean_max_results_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["pagination_trace"]["query"]["request_filters"].update(maxResults=True))

    def test_query_filters_zero_max_results_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["pagination_trace"]["query"]["request_filters"].update(maxResults=0))

    def test_missing_page_request_body_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["pagination_trace"]["pages"][1].pop("request_body"))

    def test_page_request_body_wrong_campaign_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["pagination_trace"]["pages"][1]["request_body"]["campaignIdFilter"].update(include=["synthetic-other"]))

    def test_page_request_body_wrong_max_results_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["pagination_trace"]["pages"][1]["request_body"].update(maxResults=200))

    def test_page_request_body_wrong_continuation_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["pagination_trace"]["pages"][1]["request_body"].update(nextToken="wrong-token"))

    def test_first_page_unexpected_continuation_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["pagination_trace"]["pages"][0]["request_body"].update(nextToken="synthetic-token-2"))

    def test_page_request_body_extra_filter_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["pagination_trace"]["pages"][1]["request_body"].update(nameFilter={"include": ["something"]}))

    def test_page_request_body_wrong_type_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["pagination_trace"]["pages"][0].update(request_body=[]))

    def test_orphan_page_request_body_without_query_filters_unknown(self):
        def mutate(e):
            e["readback"]["pagination_trace"]["query"].pop("request_filters")
        self.check("Unknown", mutate)

    def test_explicit_query_filters_without_any_pages_request_body_unknown(self):
        def mutate(e):
            for page in e["readback"]["pagination_trace"]["pages"]:
                page.pop("request_body")
        self.check("Unknown", mutate)

    def test_query_filters_invalid_include_shape_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["pagination_trace"]["query"]["request_filters"]["campaignIdFilter"].update(include="synthetic-campaign-a"))


if __name__ == "__main__":
    unittest.main()
