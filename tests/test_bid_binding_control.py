import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BidBindingControlTests(unittest.TestCase):
    def read_skill(self) -> str:
        return (ROOT / "skills/bid-optimization/SKILL.md").read_text(encoding="utf-8")

    def test_bid_increase_requires_bid_to_be_binding_control(self):
        text = self.read_skill().lower()
        self.assertIn("binding control", text)
        self.assertIn("marginal headroom", text)
        self.assertIn("auction exposure", text)

    def test_budget_constraint_is_not_bid_increase_evidence(self):
        text = self.read_skill()
        self.assertNotIn("流量/预算存在扩量空间", text)
        self.assertIn("budget-optimization", text)
        self.assertIn("budget constrained", text.lower())
        self.assertIn("does not prove bid is the binding control", text)

    def test_general_scale_question_routes_to_growth_qualification(self):
        text = self.read_skill()
        self.assertIn("growth-opportunity-finder", text)
        self.assertIn("historical average efficiency", text.lower())
        self.assertIn("does not prove marginal profitability", text.lower())


if __name__ == "__main__":
    unittest.main()
