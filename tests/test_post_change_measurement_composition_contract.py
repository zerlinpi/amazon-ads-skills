import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PostChangeMeasurementCompositionContractTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8").lower()

    def test_post_change_review_gates_on_measurement_composition_drift(self):
        skill = self.read("skills/post-change-review/SKILL.md")
        self.assertIn("measurement composition", skill)
        self.assertIn("allocation coverage", skill)
        self.assertIn("unallocated", skill)
        self.assertIn("composition drift", skill)
        self.assertIn("inconclusive", skill)

    def test_detailed_evaluation_compares_composition_before_outcome_classification(self):
        reference = self.read("skills/post-change-review/references/post-change-evaluation.md")
        self.assertIn("measurement composition", reference)
        self.assertIn("modeled", reference)
        self.assertIn("allocation coverage", reference)
        self.assertIn("unallocated", reference)
        self.assertIn("worked", reference)
        self.assertIn("inconclusive", reference)

    def test_weekly_review_does_not_treat_composition_drift_as_action_effect(self):
        playbook = self.read("playbooks/weekly-review.md")
        self.assertIn("measurement composition", playbook)
        self.assertIn("allocation coverage", playbook)
        self.assertIn("composition drift", playbook)


if __name__ == "__main__":
    unittest.main()
