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


if __name__ == "__main__":
    unittest.main()
