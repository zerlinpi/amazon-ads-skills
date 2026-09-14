import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RealizationProjectionPolicyTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_entity_history_separates_last_observed_realization_from_current_observability(self):
        text = self.read("schemas/entity-history.json")
        self.assertIn('"last_observed_realization"', text)
        self.assertIn('"current_realization_observability"', text)
        self.assertIn('"observed_at"', text)

    def test_projection_preserves_prior_known_state_without_claiming_it_is_current(self):
        text = self.read("references/realized-ad-identity.md")
        self.assertIn("newer unavailable observation", text.lower())
        self.assertIn("must not erase", text.lower())
        self.assertIn("must not be presented as current truth", text.lower())

    def test_projection_distinguishes_observation_recency_from_event_recency(self):
        text = self.read("references/realized-ad-identity.md")
        self.assertIn("observation freshness", text.lower())
        self.assertIn("current observability", text.lower())
        self.assertIn("last observed realization", text.lower())


if __name__ == "__main__":
    unittest.main()
