import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PlacementAudienceControlLineageTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8").lower()

    def test_placement_skill_requires_audience_bid_adjustment_state(self):
        text = self.read("skills/placement-optimization/SKILL.md")
        self.assertIn("audience bid adjustment", text)
        self.assertIn("control state", text)
        self.assertIn("confound", text)

    def test_realized_exposure_reference_treats_audience_adjustment_as_coupled_control(self):
        text = self.read("skills/placement-optimization/references/realized-bid-exposure.md")
        self.assertIn("audience bid adjustment", text)
        self.assertIn("placement", text)
        self.assertIn("hold", text)


if __name__ == "__main__":
    unittest.main()
