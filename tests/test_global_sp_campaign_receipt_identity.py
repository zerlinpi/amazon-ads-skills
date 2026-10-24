"""RED-first regression: a 207 campaign receipt cannot contradict its request.

The independent query may agree with the request while the update receipt
actually identifies a different campaign. All identities are synthetic.
"""
import unittest

from test_global_sp_readback_evidence import fixture
from scripts.evaluate_global_sp_readback import evaluate_global_sp_readback


class CampaignReceiptIdentityTests(unittest.TestCase):
    def check(self, expected, mutation=None):
        evidence = fixture()
        if mutation is not None:
            mutation(evidence)
        result = evaluate_global_sp_readback(evidence)
        self.assertEqual(result["application_status"], expected, result)
        return result

    def test_legacy_index_only_receipt_remains_compatible(self):
        self.check("Confirmed")

    def test_matching_normalized_receipt_identity_confirmed(self):
        def mutate(e):
            e["receipt"].update(global_account_id=e["request"]["global_account_id"],
                                campaign_id=e["request"]["campaign_id"])
        self.check("Confirmed", mutate)

    def test_matching_native_returned_campaign_id_confirmed(self):
        def mutate(e):
            e["receipt"]["success"][0]["campaign"] = {
                "campaignId": e["request"]["campaign_id"]}
        self.check("Confirmed", mutate)

    def test_top_level_receipt_account_conflict_unknown(self):
        self.check("Unknown", lambda e: e["receipt"].update(
            global_account_id="synthetic-other-account"))

    def test_top_level_receipt_campaign_conflict_unknown(self):
        self.check("Unknown", lambda e: e["receipt"].update(
            campaign_id="synthetic-other-campaign"))

    def test_native_returned_campaign_conflict_unknown(self):
        self.check("Unknown", lambda e: e["receipt"]["success"][0].update(
            campaign={"campaignId": "synthetic-other-campaign"}))

    def test_normalized_returned_campaign_conflict_unknown(self):
        self.check("Unknown", lambda e: e["receipt"]["success"][0].update(
            campaign={"campaign_id": "synthetic-other-campaign"}))

    def test_returned_campaign_account_conflict_unknown(self):
        self.check("Unknown", lambda e: e["receipt"]["success"][0].update(
            campaign={"global_account_id": "synthetic-other-account"}))

    def test_malformed_returned_campaign_unknown(self):
        self.check("Unknown", lambda e: e["receipt"]["success"][0].update(
            campaign=[]))

    def test_conflicting_native_and_normalized_aliases_unknown(self):
        self.check("Unknown", lambda e: e["receipt"]["success"][0].update(
            campaign={"campaignId": e["request"]["campaign_id"],
                      "campaign_id": "synthetic-other-campaign"}))

    def test_unbound_receipt_request_id_unknown(self):
        self.check("Unknown", lambda e: e["receipt"].update(
            request_id="synthetic-request-without-request-identity"))

    def test_mismatched_receipt_request_id_unknown(self):
        def mutate(e):
            e["request"]["request_id"] = "synthetic-request-a"
            e["receipt"]["request_id"] = "synthetic-request-b"
        self.check("Unknown", mutate)

    def test_matching_receipt_request_id_confirmed(self):
        def mutate(e):
            e["request"]["request_id"] = "synthetic-request-a"
            e["receipt"]["request_id"] = "synthetic-request-a"
        self.check("Confirmed", mutate)

    def test_receipt_resource_type_conflict_unknown(self):
        self.check("Unknown", lambda e: e["receipt"].update(resource_type="target"))

    def test_receipt_resource_type_campaign_confirmed(self):
        self.check("Confirmed", lambda e: e["receipt"].update(resource_type="campaign"))


if __name__ == "__main__":
    unittest.main()
