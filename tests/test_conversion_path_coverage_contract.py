import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_COVERAGE = ROOT / "references" / "report-coverage.md"


class ConversionPathCoverageContractTests(unittest.TestCase):
    def test_conversion_path_top5_is_not_full_population(self):
        text = REPORT_COVERAGE.read_text(encoding="utf-8").lower()
        required = [
            "conversion path",
            "top 5",
            "selected subset",
            "full path population",
            "not zero",
            "population coverage",
        ]
        missing = [term for term in required if term not in text]
        self.assertFalse(
            missing,
            "report coverage must fail closed when Conversion Path Reporting exposes only "
            f"a top-path subset; missing contract terms: {missing}",
        )


if __name__ == "__main__":
    unittest.main()
