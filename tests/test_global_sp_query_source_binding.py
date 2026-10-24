"""RED-first: explicit Global SP query-level source lineage must bind to its pages.

Synthetic evidence only. This detects internal adapter contradictions and
does not authenticate Amazon Ads HTTP responses or query completeness.
"""
import copy
import unittest

from test_global_sp_readback_evidence import evaluate
from test_global_sp_query_pagination_trace import with_trace


class GlobalSpQuerySourceBindingTests(unittest.TestCase):
    def assert_status(self, expected, mutate=None):
        evidence = with_trace()
        if mutate is not None:
            mutate(evidence)
        result = evaluate(evidence)
        self.assertEqual(result["application_status"], expected, result)

    def test_legacy_trace_without_query_source_still_confirms(self):
        self.assert_status("Confirmed")

    def test_explicit_query_source_matching_envelope_confirms(self):
        self.assert_status("Confirmed", lambda e: e["readback"]["pagination_trace"]["query"].update(
            source=copy.deepcopy(e["readback"]["source"])))

    def test_query_source_connector_conflict_is_unknown(self):
        def mutate(e):
            source = copy.deepcopy(e["readback"]["source"])
            source["connector_id"] = "synthetic-other-connector"
            e["readback"]["pagination_trace"]["query"]["source"] = source
        self.assert_status("Unknown", mutate)

    def test_query_source_system_conflict_is_unknown(self):
        def mutate(e):
            source = copy.deepcopy(e["readback"]["source"])
            source["source_system"] = "synthetic-other-system"
            e["readback"]["pagination_trace"]["query"]["source"] = source
        self.assert_status("Unknown", mutate)

    def test_query_source_acquisition_channel_conflict_is_unknown(self):
        def mutate(e):
            source = copy.deepcopy(e["readback"]["source"])
            source["acquisition_channel"] = "synthetic-other-channel"
            e["readback"]["pagination_trace"]["query"]["source"] = source
        self.assert_status("Unknown", mutate)

    def test_query_source_explicit_null_is_unknown(self):
        self.assert_status("Unknown", lambda e: e["readback"]["pagination_trace"]["query"].update(source=None))

    def test_query_source_incomplete_object_is_unknown(self):
        self.assert_status("Unknown", lambda e: e["readback"]["pagination_trace"]["query"].update(
            source={"connector_id": e["readback"]["source"]["connector_id"]}))

    def test_query_source_wrong_type_is_unknown(self):
        self.assert_status("Unknown", lambda e: e["readback"]["pagination_trace"]["query"].update(source="unverified"))

    def test_query_source_conflict_cannot_be_overridden_by_matching_page_source(self):
        def mutate(e):
            e["readback"]["pagination_trace"]["query"]["source"] = {
                "source_system": "other",
                "acquisition_channel": "other",
                "connector_id": "other",
            }
            # Every page still echoes the readback envelope, but the query
            # declaration explicitly contradicts that evidence.
            self.assertTrue(all(page["source"] == e["readback"]["source"]
                                for page in e["readback"]["pagination_trace"]["pages"]))
        self.assert_status("Unknown", mutate)


if __name__ == "__main__":
    unittest.main()
