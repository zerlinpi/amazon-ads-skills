import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PlatformMutationProvenanceContractTests(unittest.TestCase):
    def test_platform_mutation_provenance_is_explicit_and_fail_closed(self):
        fixture = json.loads(
            (ROOT / "evals/fixtures/platform-managed-control-transition-provenance-unknown.json").read_text(encoding="utf-8")
        )
        schema = json.loads((ROOT / "schemas/control-state-snapshot.json").read_text(encoding="utf-8"))
        skill = (ROOT / "skills/post-change-review/SKILL.md").read_text(encoding="utf-8")
        control_ref = (ROOT / "references/control-state-comparability.md").read_text(encoding="utf-8")
        memory = (ROOT / "references/optimization-memory.md").read_text(encoding="utf-8")

        forbidden = " ".join(fixture["expected"]["forbidden_behaviors"]).lower()
        self.assertIn("empty external executor mutation ledger", forbidden)
        self.assertIn("transition actor provenance is unavailable", forbidden)

        control = schema["properties"]["controls"]["items"]
        provenance = control["properties"]["transition_provenance"]
        self.assertIn("management_mode", provenance["required"])
        self.assertIn("actor_evidence_status", provenance["required"])
        self.assertIn("platform_managed", provenance["properties"]["management_mode"]["enum"])
        self.assertIn("amazon_platform", provenance["properties"]["last_transition_actor"]["enum"])
        self.assertIn("unknown", provenance["properties"]["actor_evidence_status"]["enum"])

        self.assertIn("current control state != transition provenance", skill)
        self.assertIn("complete local/external Executor ledger", skill)
        self.assertIn("Control state is not transition provenance", control_ref)
        self.assertIn("not proof of complete platform-wide mutation history", control_ref)
        self.assertIn("platform-managed mutation history unavailable", memory)


if __name__ == "__main__":
    unittest.main()
