"""Global SP configured-state row lineage must not contradict its readback envelope.

All inputs are synthetic. This is a read-only evidence classifier, not an
Amazon Ads API adapter or authorized executor.
"""
import copy
import unittest

from test_global_sp_readback_evidence import evaluate, fixture


class GlobalSpStateRowLineageTests(unittest.TestCase):
    def check(self, expected, mutate):
        evidence = fixture()
        mutate(evidence)
        result = evaluate(evidence)
        self.assertEqual(result["application_status"], expected, result)

    def test_stale_state_row_observation_is_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["marketplace_states"][0].update(
            observed_at="2026-10-23T23:59:59Z"))

    def test_state_row_at_write_completion_is_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["marketplace_states"][0].update(
            observed_at=e["request"]["completed_at"]))

    def test_state_row_later_than_envelope_is_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["marketplace_states"][1].update(
            observed_at="2026-10-24T00:06:00Z"))

    def test_malformed_state_row_timestamp_is_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["marketplace_states"][0].update(
            observed_at="not-an-instant"))

    def test_state_row_connector_mismatch_is_unknown(self):
        def mutate(e):
            source = copy.deepcopy(e["readback"]["source"])
            source["connector_id"] = "other-connector"
            e["readback"]["marketplace_states"][0]["source"] = source
        self.check("Unknown", mutate)

    def test_state_row_acquisition_channel_mismatch_is_unknown(self):
        def mutate(e):
            source = copy.deepcopy(e["readback"]["source"])
            source["acquisition_channel"] = "export"
            e["readback"]["marketplace_states"][1]["source"] = source
        self.check("Unknown", mutate)

    def test_state_row_source_system_mismatch_is_unknown(self):
        def mutate(e):
            source = copy.deepcopy(e["readback"]["source"])
            source["source_system"] = "unverified-other-system"
            e["readback"]["marketplace_states"][0]["source"] = source
        self.check("Unknown", mutate)

    def test_incomplete_state_row_source_is_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["marketplace_states"][0].update(
            source={"source_system": "synthetic-ads-api"}))

    def test_state_row_campaign_identity_mismatch_is_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["marketplace_states"][0].update(
            campaign_id="other-campaign"))

    def test_state_row_global_account_identity_mismatch_is_unknown(self):
        self.check("Unknown", lambda e: e["readback"]["marketplace_states"][1].update(
            global_account_id="other-global-account"))

    def test_consistent_state_row_lineage_remains_confirmed(self):
        def mutate(e):
            for row in e["readback"]["marketplace_states"]:
                row["source"] = copy.deepcopy(e["readback"]["source"])
                row["observed_at"] = "2026-10-24T00:03:00Z"
                row["global_account_id"] = e["request"]["global_account_id"]
                row["campaign_id"] = e["request"]["campaign_id"]
        self.check("Confirmed", mutate)

    def test_equivalent_timezone_offset_remains_confirmed(self):
        self.check("Confirmed", lambda e: e["readback"]["marketplace_states"][0].update(
            observed_at="2026-10-24T08:03:00+08:00"))

    def test_complete_state_row_lineage_still_detects_drift(self):
        def mutate(e):
            row = e["readback"]["marketplace_states"][0]
            row["source"] = copy.deepcopy(e["readback"]["source"])
            row["observed_at"] = "2026-10-24T00:03:00Z"
            row["effective_state"] = "PAUSED"
        self.check("Drifted", mutate)

    def test_partial_receipt_precedes_bad_state_row_lineage(self):
        def mutate(e):
            e["receipt"]["success"] = []
            e["receipt"]["partialSuccess"] = [{"index": 0}]
            e["readback"]["marketplace_states"][0]["observed_at"] = "2026-10-23T23:59:59Z"
        self.check("Partial", mutate)

    def test_absent_optional_row_lineage_remains_compatible(self):
        self.check("Confirmed", lambda e: None)


if __name__ == "__main__":
    unittest.main()
