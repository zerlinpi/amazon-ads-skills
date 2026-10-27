"""RED-first: side-specific JSON Pointer proof for nested SP rule-event arrays.

Synthetic normalized read-only evidence; no Ads API or Executor calls.
An outer Complete rule collection does not certify any descendant list.
"""
import copy
import unittest

from scripts.compare_control_state import compare_control_state
from test_intervening_rule_collection_proof import proven_event, COMPLETE
from test_control_intervening_event_evidence import fixture


def nested_event(control_type="schedule_or_event_rule", *, deep=False, empty=False):
    before, post, event = proven_event(control_type)
    collection = "active_budget_rules" if control_type == "budget_or_pacing" else "schedule_rules"
    for phase in ("before_state", "after_state"):
        member = event[phase][collection][0]
        if deep:
            member["metadata"] = {"targets": [] if empty else ["x"]}
        else:
            member["conditions"] = [] if empty else ["x"]
    pointer = f"/{collection}/0/" + ("metadata/targets" if deep else "conditions")
    event["rule_descendant_collection_evidence"] = {
        "before": {pointer: copy.deepcopy(COMPLETE)},
        "after": {pointer: copy.deepcopy(COMPLETE)},
    }
    return before, post, event, pointer


class InterveningRuleDescendantProofTests(unittest.TestCase):
    def check(self, before, post, expected):
        result = compare_control_state(before, post, "base_bid")
        self.assertEqual(result["classification"], expected, result)

    def test_complete_paired_descendant_proof_allows_schedule_transition(self):
        before, post, _, _ = nested_event()
        self.check(before, post, "Confounded")

    def test_complete_paired_descendant_proof_allows_empty_list(self):
        before, post, _, _ = nested_event(empty=True)
        self.check(before, post, "Confounded")

    def test_complete_paired_descendant_proof_allows_deep_budget_list(self):
        before, post, _, _ = nested_event("budget_or_pacing", deep=True)
        self.check(before, post, "Confounded")

    def test_missing_before_pointer_is_unknown(self):
        before, post, event, _ = nested_event()
        event["rule_descendant_collection_evidence"]["before"] = {}
        self.check(before, post, "Unknown")

    def test_partial_after_pointer_is_unknown(self):
        before, post, event, pointer = nested_event()
        event["rule_descendant_collection_evidence"]["after"][pointer]["pagination_status"] = "Truncated"
        self.check(before, post, "Unknown")

    def test_unmapped_extra_pointer_is_unknown(self):
        before, post, event, _ = nested_event()
        event["rule_descendant_collection_evidence"]["after"]["/schedule_rules/9/phantom"] = copy.deepcopy(COMPLETE)
        self.check(before, post, "Unknown")

    def test_malformed_pointer_proof_is_unknown(self):
        before, post, event, pointer = nested_event()
        event["rule_descendant_collection_evidence"]["after"][pointer]["extra"] = "Complete"
        self.check(before, post, "Unknown")

    def test_missing_phase_is_unknown(self):
        before, post, event, _ = nested_event()
        del event["rule_descendant_collection_evidence"]["before"]
        self.check(before, post, "Unknown")

    def test_descendant_proof_requires_outer_rule_collection_proof(self):
        before, post, event, _ = nested_event()
        del event["rule_collection_evidence"]
        self.check(before, post, "Unknown")

    def test_descendant_proof_on_non_rule_event_is_unknown(self):
        before, post, event = fixture("placement_adjustment")
        event["rule_descendant_collection_evidence"] = {"before": {}, "after": {}}
        self.check(before, post, "Unknown")

    def test_flat_rule_event_with_explicit_empty_descendant_proof_remains_compatible(self):
        before, post, event = proven_event()
        event["rule_descendant_collection_evidence"] = {"before": {}, "after": {}}
        self.check(before, post, "Confounded")

    def test_legacy_nested_rule_event_without_proof_stays_unknown(self):
        before, post, event, _ = nested_event()
        del event["rule_descendant_collection_evidence"]
        self.check(before, post, "Unknown")

    def test_legacy_flat_rule_event_without_optional_proof_stays_confounder(self):
        before, post, _ = fixture()
        self.check(before, post, "Confounded")

    def test_schema_declares_optional_side_specific_pointer_proof(self):
        import json
        from pathlib import Path
        schema = json.loads((Path(__file__).resolve().parents[1] / "schemas/control-state-snapshot.json").read_text(encoding="utf-8"))
        event = schema["properties"]["control_events"]["items"]
        self.assertNotIn("rule_descendant_collection_evidence", event["required"])
        self.assertIn("rule_descendant_collection_evidence", event["properties"])
        proof = event["properties"]["rule_descendant_collection_evidence"]
        self.assertEqual(set(proof["required"]), {"before", "after"})
        for phase in ("before", "after"):
            self.assertEqual(proof["properties"][phase]["additionalProperties"]["$ref"], "#/$defs/collectionEvidence")


if __name__ == "__main__":
    unittest.main()
