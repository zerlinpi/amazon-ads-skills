import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DeduplicatedReachContractTests(unittest.TestCase):
    def test_deduplicated_reach_reference_guards_non_additive_aggregation(self):
        path = ROOT / "references" / "deduplicated-reach-frequency.md"
        self.assertTrue(path.exists(), "shared reach/frequency measurement contract is missing")
        text = path.read_text(encoding="utf-8").lower()
        required = [
            "deduplicated reach",
            "non-additive",
            "do not sum",
            "frequency",
            "time grain",
            "scope",
            "cross-account",
            "missing",
            "not zero",
            "comparable",
        ]
        for token in required:
            with self.subTest(token=token):
                self.assertIn(token, text)

    def test_data_lineage_routes_reach_frequency_semantics(self):
        text = (ROOT / "references" / "data-lineage.md").read_text(encoding="utf-8").lower()
        self.assertIn("deduplicated-reach-frequency.md", text)
        self.assertIn("non-additive", text)


if __name__ == "__main__":
    unittest.main()
