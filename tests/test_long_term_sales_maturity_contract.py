import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LongTermSalesMaturityContractTests(unittest.TestCase):
    def test_fixture_and_skill_keep_modeled_estimate_separate_from_realized_outcome(self):
        fixture = json.loads(
            (ROOT / "evals/fixtures/long-term-sales-estimate-vs-realized-maturity.json").read_text(encoding="utf-8")
        )
        skill = (ROOT / "skills/post-change-review/SKILL.md").read_text(encoding="utf-8")
        lineage = (ROOT / "references/data-lineage.md").read_text(encoding="utf-8")

        forbidden = " ".join(fixture["expected_result"]["forbidden_behaviors"]).lower()
        self.assertIn("long-term sales", forbidden)
        self.assertIn("realized", forbidden)
        self.assertIn("modeled/projected long-horizon sales", skill)
        self.assertIn("does not justify `Worked` / `Likely Worked`", skill)
        self.assertIn("modeled/projected estimate ≠ realized outcome", lineage)
        self.assertIn("immature/unavailable/unsupported realized evidence ≠ zero", lineage)


if __name__ == "__main__":
    unittest.main()
