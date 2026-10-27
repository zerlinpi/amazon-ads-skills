"""RED-first: unknown SP placement dimensions are not observed placement evidence.

Synthetic read-only tests. The three known SP placement dimensions and the
optional Amazon Business modifier remain compatible; unknown adapter keys
cannot silently manufacture a causal confounder or isolated treatment.
"""
import unittest

from scripts.compare_control_state import compare_control_state
from test_control_intervening_event_evidence import fixture
from test_nested_collection_completeness import snapshot


def placement_control(snapshot_data):
    return next(c for c in snapshot_data["controls"] if c["control_type"] == "placement_adjustment")


class SPUnknownPlacementDimensionTests(unittest.TestCase):
    def test_event_after_only_unknown_dimension_is_unknown(self):
        before, post, event = fixture("placement_adjustment")
        event["after_state"]["unmapped_placement"] = 20
        self.assertEqual(compare_control_state(before, post, "base_bid")["classification"], "Unknown")

    def test_event_before_only_unknown_dimension_is_unknown(self):
        before, post, event = fixture("placement_adjustment")
        event["before_state"]["unmapped_placement"] = 20
        self.assertEqual(compare_control_state(before, post, "base_bid")["classification"], "Unknown")

    def test_event_repeated_unknown_dimension_is_not_accepted(self):
        before, post, event = fixture("placement_adjustment")
        event["before_state"]["unmapped_placement"] = 0
        event["after_state"]["unmapped_placement"] = 0
        self.assertEqual(compare_control_state(before, post, "base_bid")["classification"], "Unknown")

    def test_endpoint_one_sided_unknown_dimension_is_unknown(self):
        before = snapshot("sponsored_products_bid_change", base_bid=1.0)
        post = snapshot("sponsored_products_bid_change", base_bid=1.2)
        placement_control(post)["state"]["unmapped_placement"] = 15
        self.assertEqual(compare_control_state(before, post, "base_bid")["classification"], "Unknown")

    def test_endpoint_repeated_unknown_dimension_cannot_certify_stability(self):
        before = snapshot("sponsored_products_bid_change", base_bid=1.0)
        post = snapshot("sponsored_products_bid_change", base_bid=1.2)
        for s in (before, post):
            placement_control(s)["state"]["unmapped_placement"] = 15
        self.assertEqual(compare_control_state(before, post, "base_bid")["classification"], "Unknown")

    def test_known_placement_event_remains_confounder(self):
        before, post, _ = fixture("placement_adjustment")
        self.assertEqual(compare_control_state(before, post, "base_bid")["classification"], "Confounded")

    def test_known_amazon_business_event_remains_confounder(self):
        before, post, event = fixture("placement_adjustment")
        event["before_state"]["amazon_business"] = 0
        event["after_state"]["amazon_business"] = 15
        self.assertEqual(compare_control_state(before, post, "base_bid")["classification"], "Confounded")

    def test_known_amazon_business_endpoint_remains_isolated(self):
        before = snapshot("sponsored_products_bid_change", base_bid=1.0)
        post = snapshot("sponsored_products_bid_change", base_bid=1.2)
        for s in (before, post):
            placement_control(s)["state"]["amazon_business"] = 10
        self.assertEqual(compare_control_state(before, post, "base_bid")["classification"], "Treatment Isolated")


if __name__ == "__main__":
    unittest.main()
