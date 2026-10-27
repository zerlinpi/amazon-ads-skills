"""Deterministic RED-first: observed mid-window controls can confound identical endpoints.

Normalized synthetic evidence only. No Amazon Ads calls, writes or source claims.
"""
import copy
import json
import unittest
from pathlib import Path

from scripts.compare_control_state import compare_control_state
from test_nested_collection_completeness import snapshot

ROOT = Path(__file__).resolve().parents[1]
MIDDLE = "2026-09-21T12:00:00Z"


def fixture(control_type="schedule_or_event_rule"):
    before = snapshot("sponsored_products_bid_change", base_bid=1.0)
    after = snapshot("sponsored_products_bid_change", base_bid=1.2)
    after["observed_at"] = "2026-09-22T00:00:00Z"
    original = next(c["state"] for c in before["controls"] if c["control_type"] == control_type)
    changed = copy.deepcopy(original)
    if control_type == "schedule_or_event_rule":
        changed["schedule_rules"][0]["bid_increase"] = 25
    elif control_type == "budget_or_pacing":
        changed["active_budget_rules"][0]["increase_percent"] = 35
    elif control_type == "placement_adjustment":
        changed["top_of_search"] = 20
    elif control_type == "base_bid":
        changed = 1.2
    event = {
        "event_id": "event-1",
        "event_at": MIDDLE,
        "scope": copy.deepcopy(before["scope"]),
        "source": copy.deepcopy(before["source"]),
        "control_type": control_type,
        "before_state": copy.deepcopy(original),
        "after_state": changed,
        "evidence_status": "observed",
    }
    after["control_events"] = [event]
    return before, after, event


class InterveningControlEventEvidenceTests(unittest.TestCase):
    def check(self, before, after, expected):
        result = compare_control_state(before, after, "base_bid")
        self.assertEqual(result["classification"], expected, result)
        return result

    def test_schedule_rule_change_and_revert_confounds_bid(self):
        b, p, _ = fixture()
        self.check(b, p, "Confounded")

    def test_budget_rule_change_and_revert_confounds_bid(self):
        b, p, _ = fixture("budget_or_pacing")
        self.check(b, p, "Confounded")

    def test_placement_change_and_revert_confounds_bid(self):
        b, p, _ = fixture("placement_adjustment")
        self.check(b, p, "Confounded")

    def test_valid_treatment_only_event_remains_isolated(self):
        b, p, _ = fixture("base_bid")
        self.check(b, p, "Treatment Isolated")

    def test_explicit_empty_events_do_not_prove_continuity_or_change_endpoint_result(self):
        b, p, _ = fixture()
        p["control_events"] = []
        self.check(b, p, "Treatment Isolated")

    def test_omitted_legacy_events_remain_compatible(self):
        b, p, _ = fixture()
        del p["control_events"]
        self.check(b, p, "Treatment Isolated")

    def test_partial_event_is_unresolved(self):
        b, p, e = fixture()
        e["evidence_status"] = "Partial"
        self.check(b, p, "Unknown")

    def test_derived_event_is_not_observed_transition_proof(self):
        b, p, e = fixture()
        e["evidence_status"] = "derived"
        self.check(b, p, "Unknown")

    def test_unknown_event_id_is_unresolved(self):
        b, p, e = fixture()
        e["event_id"] = "N/A"
        self.check(b, p, "Unknown")

    def test_duplicate_event_id_is_unresolved(self):
        b, p, e = fixture()
        p["control_events"].append(copy.deepcopy(e))
        self.check(b, p, "Unknown")

    def test_event_scope_mismatch_is_unresolved(self):
        b, p, e = fixture()
        e["scope"]["campaign_id"] = "other-campaign"
        self.check(b, p, "Unknown")

    def test_event_source_mismatch_is_unresolved(self):
        b, p, e = fixture()
        e["source"]["source_system"] = "different-connector"
        self.check(b, p, "Unknown")

    def test_event_after_post_observation_is_unresolved(self):
        b, p, e = fixture()
        e["event_at"] = "2026-09-23T00:00:00Z"
        self.check(b, p, "Unknown")

    def test_event_before_baseline_observation_is_unresolved(self):
        b, p, e = fixture()
        e["event_at"] = "2026-09-20T00:00:00Z"
        self.check(b, p, "Unknown")

    def test_unknown_offset_event_is_unresolved(self):
        b, p, e = fixture()
        e["event_at"] = "2026-09-21T12:00:00-00:00"
        self.check(b, p, "Unknown")

    def test_unknown_control_event_state_is_unresolved(self):
        b, p, e = fixture()
        e["after_state"] = {"schedule_rules": "Unknown"}
        self.check(b, p, "Unknown")

    def test_noop_event_is_not_proof_of_a_change(self):
        b, p, e = fixture()
        e["after_state"] = copy.deepcopy(e["before_state"])
        self.check(b, p, "Unknown")

    def test_unknown_control_type_is_unresolved(self):
        b, p, e = fixture()
        e["control_type"] = "unsupported_rule_type"
        self.check(b, p, "Unknown")

    def test_baseline_only_event_log_is_not_silently_ignored(self):
        b, p, _ = fixture()
        b["control_events"] = p.pop("control_events")
        self.check(b, p, "Unknown")

    def test_competing_event_cannot_invent_unobserved_intended_treatment(self):
        b, p, _ = fixture()
        next(c for c in p["controls"] if c["control_type"] == "base_bid")["state"] = 1.0
        self.check(b, p, "Unknown")

    def test_event_readback_cannot_reuse_endpoint_observation(self):
        b, p, e = fixture()
        b["source"]["readback_id"] = "readback-baseline"
        p["source"]["readback_id"] = "readback-post"
        e["source"]["readback_id"] = "readback-baseline"
        self.check(b, p, "Unknown")

    def test_schema_exposes_optional_post_observation_events(self):
        schema = json.loads((ROOT / "schemas/control-state-snapshot.json").read_text(encoding="utf-8"))
        self.assertIn("control_events", schema["properties"])
        event = schema["properties"]["control_events"]["items"]
        self.assertIn("event_id", event["required"])
        self.assertIn("event_at", event["required"])
        self.assertIn("source", event["required"])
        self.assertIn("scope", event["required"])


if __name__ == "__main__":
    unittest.main()
