"""RED-first: native campaign snapshot must bind to one source-attributed query page.

Synthetic adapter assertions only; never authenticates a raw Amazon Ads response.
"""
import copy
import unittest

from test_global_sp_readback_evidence import fixture, evaluate
from test_global_sp_native_campaign_configuration import native
from test_global_sp_query_pagination_trace import with_trace


def combined():
    evidence = native(with_trace())
    evidence["readback"]["raw_campaign_provenance"] = {
        "global_account_id": "synthetic-global-a",
        "campaign_id": "synthetic-campaign-a",
        "query_fingerprint": "synthetic-query-filter-a",
        "page_index": 0,
        "observed_at": "2026-10-24T00:02:00Z",
        "source": copy.deepcopy(evidence["readback"]["source"]),
    }
    return evidence


class NativeCampaignPageProvenanceTests(unittest.TestCase):
    def check(self, status, evidence):
        actual = evaluate(evidence)
        self.assertEqual(actual["application_status"], status, actual)

    def test_legacy_native_without_trace_still_confirms(self):
        self.check("Confirmed", native(fixture()))

    def test_legacy_trace_without_native_still_confirms(self):
        self.check("Confirmed", with_trace())

    def test_combined_native_and_trace_with_bound_provenance_confirms(self):
        self.check("Confirmed", combined())

    def test_combined_native_and_trace_without_provenance_unknown(self):
        evidence = combined()
        evidence["readback"].pop("raw_campaign_provenance")
        self.check("Unknown", evidence)

    def test_explicit_null_provenance_unknown(self):
        evidence = combined()
        evidence["readback"]["raw_campaign_provenance"] = None
        self.check("Unknown", evidence)

    def test_provenance_without_native_unknown(self):
        evidence = combined()
        evidence["readback"].pop("raw_campaign")
        self.check("Unknown", evidence)

    def test_provenance_without_page_trace_unknown(self):
        evidence = combined()
        evidence["readback"].pop("pagination_trace")
        self.check("Unknown", evidence)

    def test_missing_page_index_unknown(self):
        evidence = combined()
        evidence["readback"]["raw_campaign_provenance"].pop("page_index")
        self.check("Unknown", evidence)

    def test_boolean_page_index_unknown(self):
        evidence = combined()
        evidence["readback"]["raw_campaign_provenance"]["page_index"] = True
        self.check("Unknown", evidence)

    def test_out_of_range_page_index_unknown(self):
        evidence = combined()
        evidence["readback"]["raw_campaign_provenance"]["page_index"] = 2
        self.check("Unknown", evidence)

    def test_wrong_page_timestamp_unknown(self):
        evidence = combined()
        evidence["readback"]["raw_campaign_provenance"]["observed_at"] = "2026-10-24T00:03:00Z"
        self.check("Unknown", evidence)

    def test_stale_page_timestamp_unknown(self):
        evidence = combined()
        evidence["readback"]["raw_campaign_provenance"]["observed_at"] = "2026-10-23T23:59:59Z"
        self.check("Unknown", evidence)

    def test_source_connector_mismatch_unknown(self):
        evidence = combined()
        evidence["readback"]["raw_campaign_provenance"]["source"]["connector_id"] = "other"
        self.check("Unknown", evidence)

    def test_incomplete_source_unknown(self):
        evidence = combined()
        evidence["readback"]["raw_campaign_provenance"]["source"].pop("connector_id")
        self.check("Unknown", evidence)

    def test_query_fingerprint_mismatch_unknown(self):
        evidence = combined()
        evidence["readback"]["raw_campaign_provenance"]["query_fingerprint"] = "other-query"
        self.check("Unknown", evidence)

    def test_missing_query_fingerprint_unknown(self):
        evidence = combined()
        evidence["readback"]["raw_campaign_provenance"].pop("query_fingerprint")
        self.check("Unknown", evidence)

    def test_campaign_identity_mismatch_unknown(self):
        evidence = combined()
        evidence["readback"]["raw_campaign_provenance"]["campaign_id"] = "other"
        self.check("Unknown", evidence)

    def test_account_identity_mismatch_unknown(self):
        evidence = combined()
        evidence["readback"]["raw_campaign_provenance"]["global_account_id"] = "other"
        self.check("Unknown", evidence)

    def test_second_page_provenance_binds_second_page(self):
        evidence = combined()
        evidence["readback"]["raw_campaign_provenance"]["page_index"] = 1
        evidence["readback"]["raw_campaign_provenance"]["observed_at"] = "2026-10-24T00:04:00Z"
        self.check("Confirmed", evidence)

    def test_matching_native_and_normalized_but_unmet_intent_remains_drifted(self):
        evidence = combined()
        evidence["readback"]["raw_campaign"]["marketplaceConfigurations"][0]["overrides"]["state"] = "ENABLED"
        evidence["readback"]["marketplace_states"][1]["effective_state"] = "ENABLED"
        self.check("Drifted", evidence)
