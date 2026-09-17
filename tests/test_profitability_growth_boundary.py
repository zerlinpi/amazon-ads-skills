import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ProfitabilityGrowthBoundaryTests(unittest.TestCase):
    def read_skill(self) -> str:
        return (ROOT / "skills/profitability-analysis/SKILL.md").read_text(encoding="utf-8")

    def test_profitability_does_not_certify_scalability(self):
        text = self.read_skill()
        self.assertNotIn("Profitable & scalable", text)
        self.assertNotIn("可扩量空间", text.split("---", 2)[1])
        self.assertIn("growth-opportunity-finder", text)

    def test_profitability_separates_economic_eligibility_from_growth_headroom(self):
        text = self.read_skill().lower()
        self.assertIn("economic eligibility", text)
        self.assertIn("headroom", text)
        self.assertIn("incrementality", text)
        self.assertIn("binding control", text)

    def test_profitable_entities_are_routed_to_growth_review_before_scale_action(self):
        text = self.read_skill()
        self.assertIn("Profitable — growth review required", text)
        self.assertIn("retail readiness", text)
        self.assertIn("marginal headroom", text)


if __name__ == "__main__":
    unittest.main()
