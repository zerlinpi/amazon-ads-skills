"""RED-first opt-in, side-specific collection proof for observed mid-window rules.

Synthetic normalized read-side evidence only. Never invokes Amazon Ads or an Executor.
Omitted optional proof preserves legacy non-exhaustive event compatibility.
"""
import copy
import json
import unittest
from pathlib import Path

from scripts.compare_control_state import compare_control_state
from test_control_intervening_event_evidence import fixture

ROOT = Path(__file__).resolve().parents[1]
COMPLETE = {
    "enumeration_status": "Complete",
    "pagination_status": "Complete",
    "capability_status": "Supported",
}


def proven_event(control_type="schedule_or_event_rule"):
    before, post, event = fixture(control_type)
    collections = (
        ("schedule_rules", "event_rules")
        if control_type == "schedule_or_event_rule"
        else ("active_budget_rules",)
    )
    event["rule_collection_evidence"] = {
        phase: {field: copy.deepcopy(COMPLETE) for field in collections}
        for phase in ("before", "after")
    }
    return before, post, event


class InterveningRuleCollectionEvidenceTests(unittest.TestCase):
    def assert_class(self, before, post, expected):
        result = compare_control_state(before, post, "base_bid")
        self.assertEqual(result["classification"], expected, result)

    def test_complete_schedule_and_event_rule_proof_is_accepted(self):
        before, post, _ = proven_event()
        self.assert_class(before, post, "Confounded")

    def test_complete_budget_rule_proof_is_accepted(self):
        before, post, _ = proven_event("budget_or_pacing")
        self.assert_class(before, post, "Confounded")

    def test_before_schedule_enumeration_partial_is_unknown(self):
        before, post, event = proven_event()
        event["rule_collection_evidence"]["before"]["schedule_rules"]["enumeration_status"] = "Partial"
        self.assert_class(before, post, "Unknown")

    def test_after_event_rules_truncated_is_unknown(self):
        before, post, event = proven_event()
        event["rule_collection_evidence"]["after"]["event_rules"]["pagination_status"] = "Truncated"
        self.assert_class(before, post, "Unknown")

    def test_before_budget_rule_capability_partial_is_unknown(self):
        before, post, event = proven_event("budget_or_pacing")
        event["rule_collection_evidence"]["before"]["active_budget_rules"]["capability_status"] = "Partial"
        self.assert_class(before, post, "Unknown")

    def test_one_sided_proof_is_unknown(self):
        before, post, event = proven_event()
        del event["rule_collection_evidence"]["before"]
        self.assert_class(before, post, "Unknown")

    def test_missing_one_nested_collection_proof_is_unknown(self):
        before, post, event = proven_event()
        del event["rule_collection_evidence"]["after"]["event_rules"]
        self.assert_class(before, post, "Unknown")

    def test_unmapped_collection_key_is_unknown(self):
        before, post, event = proven_event()
        event["rule_collection_evidence"]["before"]["unmapped_rule_list"] = copy.deepcopy(COMPLETE)
        self.assert_class(before, post, "Unknown")

    def test_malformed_proof_is_unknown(self):
        before, post, event = proven_event()
        event["rule_collection_evidence"]["after"]["schedule_rules"] = ["Complete"]
        self.assert_class(before, post, "Unknown")

    def test_proof_on_non_rule_control_is_unknown(self):
        before, post, event = fixture("placement_adjustment")
        event["rule_collection_evidence"] = {"before": {}, "after": {}}
        self.assert_class(before, post, "Unknown")

    def test_omitted_legacy_proof_preserves_confounder(self):
        before, post, _ = fixture()
        self.assert_class(before, post, "Confounded")

    def test_omitted_proof_preserves_treatment_only_event(self):
        before, post, _ = fixture("base_bid")
        self.assert_class(before, post, "Treatment Isolated")

    def test_schema_has_optional_side_specific_proof(self):
        schema = json.loads((ROOT / "schemas/control-state-snapshot.json").read_text(encoding="utf-8"))
        event = schema["properties"]["control_events"]["items"]
        self.assertNotIn("rule_collection_evidence", event["required"])
        proof = event["properties"]["rule_collection_evidence"]
        self.assertEqual(set(proof["required"]), {"before", "after"})
        for phase in ("before", "after"):
            self.assertEqual(proof["properties"][phase]["additionalProperties"]["$ref"],
                             "#/$defs/collectionEvidence")


if __name__ == "__main__":
    unittest.main()
