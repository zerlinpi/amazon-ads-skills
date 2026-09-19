import json
import unittest
from pathlib import Path

from scripts.compare_control_state import compare_control_state

ROOT = Path(__file__).resolve().parents[1]


def snapshot(state=1, status="observed", control="base_bid", marketplace="ATVPDKIKX0DER", profile="p1", effective="2026-09-18T00:00:00Z"):
    return {
        "scope": {"marketplace_id": marketplace, "profile_id": profile},
        "observed_at": "2026-09-19T00:00:00Z",
        "source": {"source_system": "fixture", "acquisition_channel": "test"},
        "coverage": {
            "required_control_types": [control],
            "coverage_status": "Complete",
            "requirement_provenance": {
                "decision_surface": "fixture_control_comparison",
                "derivation_status": "Verified",
                "capability_snapshot_id": "fixture-capability-snapshot",
                "evidence_note": "Deterministic test fixture requirement set."
            },
        },
        "controls": [{"control_type": control, "state": state, "effective_at": effective, "evidence_status": status}],
    }


class ControlStateComparabilityTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8").lower()

    def test_shared_reference_requires_control_state_identity_for_causal_comparison(self):
        text = self.read("references/control-state-comparability.md")
        for token in ["control-state comparability", "audience bid adjustment", "bidding strategy", "placement", "confound", "directional"]:
            self.assertIn(token, text)

    def test_post_change_review_gates_on_control_state_comparability(self):
        text = self.read("skills/post-change-review/SKILL.md")
        for token in ["control-state-comparability.md", "baseline", "post-change", "directional"]:
            self.assertIn(token, text)

    def test_machine_readable_snapshot_preserves_unknown_provenance_and_coverage(self):
        schema = json.loads((ROOT / "schemas/control-state-snapshot.json").read_text(encoding="utf-8"))
        self.assertTrue({"scope", "observed_at", "source", "coverage", "controls"}.issubset(set(schema["required"])))
        coverage = schema["properties"]["coverage"]
        self.assertTrue({"required_control_types", "coverage_status", "requirement_provenance"}.issubset(set(coverage["required"])))
        self.assertIn("Unknown", coverage["properties"]["coverage_status"]["enum"])
        provenance = coverage["properties"]["requirement_provenance"]
        self.assertTrue({"decision_surface", "derivation_status"}.issubset(set(provenance["required"])))
        self.assertIn("Verified", provenance["properties"]["derivation_status"]["enum"])
        control = schema["properties"]["controls"]["items"]
        self.assertTrue({"control_type", "state", "effective_at", "evidence_status"}.issubset(set(control["required"])))
        self.assertIn("unknown", control["properties"]["evidence_status"]["enum"])

    def test_shared_reference_routes_machine_contract(self):
        text = self.read("references/control-state-comparability.md")
        for token in ["schemas/control-state-snapshot.json", "missing", "unknown", "coverage", "requirement provenance"]:
            self.assertIn(token, text)

    def test_comparator_classifies_stable_state_as_comparable(self):
        self.assertEqual(compare_control_state(snapshot(), snapshot())["classification"], "Comparable")

    def test_comparator_fails_closed_when_coverage_is_unknown(self):
        before, after = snapshot(), snapshot()
        before["coverage"]["coverage_status"] = "Unknown"
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_comparator_fails_closed_when_requirement_provenance_is_unverified(self):
        before, after = snapshot(), snapshot()
        before["coverage"]["requirement_provenance"]["derivation_status"] = "Unknown"
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_comparator_fails_closed_when_required_control_is_not_evidenced(self):
        before, after = snapshot(), snapshot()
        before["coverage"]["required_control_types"].append("audience_bid_adjustment")
        after["coverage"]["required_control_types"].append("audience_bid_adjustment")
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_comparator_isolates_intended_treatment(self):
        self.assertEqual(compare_control_state(snapshot(1), snapshot(2), "base_bid")["classification"], "Treatment Isolated")

    def test_comparator_fails_closed_on_unknown_evidence(self):
        self.assertEqual(compare_control_state(snapshot(), snapshot(status="unsupported"))["classification"], "Unknown")

    def test_comparator_fails_closed_on_scope_mismatch(self):
        self.assertEqual(compare_control_state(snapshot(), snapshot(profile="p2"))["classification"], "Unknown")

    def test_comparator_marks_overlapping_change_confounded(self):
        before = snapshot(1)
        after = snapshot(2)
        before["coverage"]["required_control_types"].append("budget_or_pacing")
        after["coverage"]["required_control_types"].append("budget_or_pacing")
        before["controls"].append({"control_type": "budget_or_pacing", "state": 10, "effective_at": "2026-09-18T00:00:00Z", "evidence_status": "observed"})
        after["controls"].append({"control_type": "budget_or_pacing", "state": 20, "effective_at": "2026-09-19T00:00:00Z", "evidence_status": "observed"})
        self.assertEqual(compare_control_state(before, after, "base_bid")["classification"], "Confounded")


if __name__ == "__main__":
    unittest.main()
