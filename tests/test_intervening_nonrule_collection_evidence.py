"""RED-first: non-rule mid-window SP event collections need independent proof.

Synthetic normalized read-only evidence; never queries or writes Amazon Ads.
"""
import copy
import unittest

from scripts.compare_control_state import compare_control_state
from test_control_intervening_event_evidence import fixture
from test_intervening_budget_routing_semantics import routing_event


def audience_event():
    before, post, event = fixture("base_bid")
    event["control_type"] = "audience_bid_adjustment"
    event["before_state"] = [{"audience_id": "aud-1", "bid_boost": 10}]
    event["after_state"] = [{"audience_id": "aud-1", "bid_boost": 20}]
    return before, post, event


class InterveningNonruleCollectionEvidenceTests(unittest.TestCase):
    def check(self, before, post, expected):
        result = compare_control_state(before, post, "base_bid")
        self.assertEqual(result["classification"], expected, result)

    def test_routing_direct_empty_list_without_proof_is_unknown(self):
        before, post, event = routing_event()
        event["before_state"]["unverified_targets"] = []
        event["after_state"]["unverified_targets"] = []
        self.check(before, post, "Unknown")

    def test_routing_direct_nonempty_list_without_proof_is_unknown(self):
        before, post, event = routing_event()
        event["before_state"]["unverified_targets"] = ["target-1"]
        event["after_state"]["unverified_targets"] = ["target-1"]
        self.check(before, post, "Unknown")

    def test_routing_deep_empty_list_without_proof_is_unknown(self):
        before, post, event = routing_event()
        event["before_state"]["extra"] = {"groups": []}
        event["after_state"]["extra"] = {"groups": []}
        self.check(before, post, "Unknown")

    def test_audience_member_empty_list_without_proof_is_unknown(self):
        before, post, event = audience_event()
        for field in ("before_state", "after_state"):
            event[field][0]["unverified_members"] = []
        self.check(before, post, "Unknown")

    def test_audience_member_deep_nonempty_list_without_proof_is_unknown(self):
        before, post, event = audience_event()
        for field in ("before_state", "after_state"):
            event[field][0]["extra"] = {"members": ["segment-1"]}
        self.check(before, post, "Unknown")

    def test_valid_flat_routing_event_remains_confounder(self):
        before, post, _ = routing_event()
        self.check(before, post, "Confounded")

    def test_valid_scalar_extra_routing_evidence_remains_compatible(self):
        before, post, event = routing_event()
        event["before_state"]["adapter_mode"] = "verified-mode"
        event["after_state"]["adapter_mode"] = "verified-mode"
        self.check(before, post, "Confounded")

    def test_valid_flat_audience_event_remains_confounder(self):
        before, post, _ = audience_event()
        self.check(before, post, "Confounded")

    def test_valid_placement_event_remains_confounder(self):
        before, post, _ = fixture("placement_adjustment")
        self.check(before, post, "Confounded")


if __name__ == "__main__":
    unittest.main()
