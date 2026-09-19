import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ControlStateComparabilityTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8").lower()

    def test_shared_reference_requires_control_state_identity_for_causal_comparison(self):
        text = self.read("references/control-state-comparability.md")
        self.assertIn("control-state comparability", text)
        self.assertIn("audience bid adjustment", text)
        self.assertIn("bidding strategy", text)
        self.assertIn("placement", text)
        self.assertIn("confound", text)
        self.assertIn("directional", text)

    def test_post_change_review_gates_on_control_state_comparability(self):
        text = self.read("skills/post-change-review/SKILL.md")
        self.assertIn("control-state-comparability.md", text)
        self.assertIn("baseline", text)
        self.assertIn("post-change", text)
        self.assertIn("directional", text)

    def test_machine_readable_snapshot_preserves_unknown_and_provenance(self):
        schema = json.loads((ROOT / "schemas/control-state-snapshot.json").read_text(encoding="utf-8"))
        required = set(schema["required"])
        self.assertTrue({"scope", "observed_at", "source", "controls"}.issubset(required))
        control = schema["properties"]["controls"]["items"]
        self.assertTrue({"control_type", "state", "effective_at", "evidence_status"}.issubset(set(control["required"])))
        self.assertIn("unknown", control["properties"]["evidence_status"]["enum"])
        self.assertNotIn(0, control["properties"]["state"].get("enum", []))

    def test_shared_reference_routes_machine_contract(self):
        text = self.read("references/control-state-comparability.md")
        self.assertIn("schemas/control-state-snapshot.json", text)
        self.assertIn("missing", text)
        self.assertIn("unknown", text)

    def test_deterministic_comparator_exists_and_is_fail_closed(self):
        text = self.read("scripts/compare_control_state.py")
        for token in ["treatment isolated", "directional", "confounded", "unknown", "marketplace_id", "profile_id", "effective_at", "evidence_status"]:
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
