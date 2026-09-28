import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ExampleActionContractTests(unittest.TestCase):
    def test_documented_action_example_matches_canonical_scalar_contract(self):
        text = (ROOT / "examples" / "README.md").read_text(encoding="utf-8")
        blocks = re.findall(r"```json\n(.*?)\n```", text, flags=re.DOTALL)
        actions = []
        for block in blocks:
            payload = json.loads(block)
            if isinstance(payload, dict) and "action_type" in payload:
                actions.append(payload)

        self.assertTrue(actions, "examples/README.md must contain an optimization-action example")
        for action in actions:
            with self.subTest(action_type=action.get("action_type")):
                confidence = action.get("confidence")
                self.assertIsInstance(
                    confidence,
                    (int, float),
                    "optimization-action confidence must follow schemas/optimization-action.json",
                )
                self.assertNotIsInstance(confidence, bool)
                self.assertGreaterEqual(confidence, 0)
                self.assertLessEqual(confidence, 1)
                for field in (
                    "action_type",
                    "entity_type",
                    "reason",
                    "evidence",
                    "mode",
                    "guardrails",
                    "validation_window",
                    "rollback_condition",
                ):
                    self.assertIn(field, action)


if __name__ == "__main__":
    unittest.main()
