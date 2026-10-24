"""RED-first: retained Global SP query responses must contain their claimed native campaign.

Synthetic adapter evidence only. This is not raw HTTP authentication.
"""
import copy
import unittest

from test_global_sp_native_page_provenance import combined
from test_global_sp_readback_evidence import evaluate


def with_responses():
    evidence = combined()
    readback = evidence["readback"]
    pages = readback["pagination_trace"]["pages"]
    pages[0]["response_body"] = {
        "campaigns": [copy.deepcopy(readback["raw_campaign"])],
        "nextToken": "synthetic-token-2",
    }
    pages[1]["response_body"] = {"campaigns": [], "nextToken": None}
    return evidence


class GlobalSpNativeResponseMembershipTests(unittest.TestCase):
    def check(self, expected, mutate=None):
        evidence = with_responses()
        if mutate:
            mutate(evidence)
        actual = evaluate(evidence)
        self.assertEqual(actual["application_status"], expected, actual)

    def test_complete_two_page_response_membership_confirms(self):
        self.check("Confirmed")

    def test_legacy_provenance_without_response_bodies_confirms(self):
        evidence = combined()
        self.assertEqual(evaluate(evidence)["application_status"], "Confirmed")

    def test_complete_single_page_response_confirms(self):
        def mutate(e):
            page = e["readback"]["pagination_trace"]["pages"][0]
            page["next_token"] = None
            page["response_body"]["nextToken"] = None
            e["readback"]["pagination_trace"]["pages"] = [page]
        self.check("Confirmed", mutate)

    def test_missing_second_page_response_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["pagination_trace"]["pages"][1].pop("response_body"))

    def test_explicit_null_response_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["pagination_trace"]["pages"][1].update(response_body=None))

    def test_wrong_response_type_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["pagination_trace"]["pages"][0].update(response_body=[]))

    def test_missing_response_campaigns_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["pagination_trace"]["pages"][0]["response_body"].pop("campaigns"))

    def test_response_campaigns_wrong_type_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["pagination_trace"]["pages"][0]["response_body"].update(campaigns={}))

    def test_response_next_token_mismatch_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["pagination_trace"]["pages"][0]["response_body"].update(nextToken=None))

    def test_response_next_token_missing_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["pagination_trace"]["pages"][1]["response_body"].pop("nextToken"))

    def test_campaign_missing_from_claimed_page_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["pagination_trace"]["pages"][0]["response_body"].update(campaigns=[]))

    def test_claimed_page_index_does_not_match_membership_unknown(self):
        def mutate(e):
            p = e["readback"]["pagination_trace"]["pages"]
            p[1]["response_body"]["campaigns"] = p[0]["response_body"]["campaigns"]
            p[0]["response_body"]["campaigns"] = []
        self.check("Unknown", mutate)

    def test_same_campaign_repeated_on_another_page_unknown(self):
        def mutate(e):
            p = e["readback"]["pagination_trace"]["pages"]
            p[1]["response_body"]["campaigns"] = copy.deepcopy(p[0]["response_body"]["campaigns"])
        self.check("Unknown", mutate)

    def test_duplicate_campaign_within_claimed_page_unknown(self):
        def mutate(e):
            campaigns = e["readback"]["pagination_trace"]["pages"][0]["response_body"]["campaigns"]
            campaigns.append(copy.deepcopy(campaigns[0]))
        self.check("Unknown", mutate)

    def test_wrong_campaign_in_second_page_unknown(self):
        def mutate(e):
            p = e["readback"]["pagination_trace"]["pages"]
            other = copy.deepcopy(e["readback"]["raw_campaign"])
            other["campaignId"] = "synthetic-unrelated"
            p[1]["response_body"]["campaigns"] = [other]
        self.check("Unknown", mutate)

    def test_same_identity_but_different_native_state_unknown(self):
        def mutate(e):
            p = e["readback"]["pagination_trace"]["pages"][0]
            p["response_body"]["campaigns"][0]["state"] = "PAUSED"
        self.check("Unknown", mutate)

    def test_malformed_campaign_entry_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["pagination_trace"]["pages"][0]["response_body"].update(campaigns=[None]))

    def test_response_without_native_snapshot_unknown(self):
        self.check("Unknown", lambda e: e["readback"].pop("raw_campaign"))

    def test_response_without_provenance_unknown(self):
        self.check("Unknown", lambda e: e["readback"].pop("raw_campaign_provenance"))

    def test_complete_response_preserves_actual_drift(self):
        def mutate(e):
            e["request"]["expected_effective_states"]["GB"] = "ENABLED"
        self.check("Drifted", mutate)


if __name__ == "__main__":
    unittest.main()
