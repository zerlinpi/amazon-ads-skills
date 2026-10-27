"""RED-first: a single observed event readback cannot certify incompatible SP routing and placement.

Synthetic read-only evidence. Event logs remain optional/non-exhaustive and do not
authenticate Amazon API observations or authorize advertising writes.
"""
import copy
import unittest

from scripts.compare_control_state import compare_control_state
from test_control_intervening_event_evidence import fixture


def paired_events(*, same_readback=True, retailer="ACROSS_RETAILERS", business=True,
                  include_readbacks=True):
    baseline, post, placement = fixture("placement_adjustment")
    placement["event_id"] = "placement-event"
    placement["after_state"]["top_of_search"] = 25
    if business:
        placement["before_state"]["amazon_business"] = 0
        placement["after_state"]["amazon_business"] = 10

    routing = copy.deepcopy(placement)
    routing["event_id"] = "routing-event"
    routing["control_type"] = "targeting_or_routing"
    routing["before_state"] = {
        "site_restriction": "ALL_ELIGIBLE",
        "retailer_scope": "AMAZON_STORE",
    }
    routing["after_state"] = {
        "site_restriction": "ALL_ELIGIBLE",
        "retailer_scope": retailer,
    }
    if retailer == "AMAZON_STORE":
        routing["before_state"]["site_restriction"] = "AMAZON_BUSINESS"
    if include_readbacks:
        placement["source"]["readback_id"] = "batch-observation-1"
        routing["source"]["readback_id"] = (
            "batch-observation-1" if same_readback else "batch-observation-2"
        )
    post["control_events"] = [placement, routing]
    return baseline, post


class InterveningBatchRoutingPlacementCoherenceTests(unittest.TestCase):
    def classify(self, **kwargs):
        before, after = paired_events(**kwargs)
        return compare_control_state(before, after, "base_bid")["classification"]

    def test_same_readback_across_retailers_with_business_placement_is_unknown(self):
        self.assertEqual(self.classify(), "Unknown")

    def test_same_readback_conflicting_before_states_are_unknown(self):
        baseline, post = paired_events(retailer="AMAZON_STORE")
        routing = post["control_events"][1]
        routing["before_state"]["site_restriction"] = "ALL_ELIGIBLE"
        routing["before_state"]["retailer_scope"] = "ACROSS_RETAILERS"
        self.assertEqual(
            compare_control_state(baseline, post, "base_bid")["classification"],
            "Unknown",
        )

    def test_distinct_readbacks_do_not_infer_simultaneous_cross_control_state(self):
        self.assertEqual(self.classify(same_readback=False), "Confounded")

    def test_missing_readbacks_do_not_infer_cross_control_state(self):
        self.assertEqual(self.classify(include_readbacks=False), "Confounded")

    def test_same_readback_without_business_placement_remains_confounder(self):
        self.assertEqual(self.classify(business=False), "Confounded")

    def test_same_readback_business_placement_with_amazon_store_remains_confounder(self):
        self.assertEqual(self.classify(retailer="AMAZON_STORE"), "Confounded")


if __name__ == "__main__":
    unittest.main()
