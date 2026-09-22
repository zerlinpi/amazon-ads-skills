import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COVERAGE = ROOT / "references/report-coverage.md"
LINEAGE = ROOT / "references/data-lineage.md"


class ReportCompletenessContractTests(unittest.TestCase):
    def test_report_coverage_distinguishes_generation_row_eligibility_and_extraction_completeness(self):
        coverage = COVERAGE.read_text(encoding="utf-8")
        for concept in (
            "generation_status",
            "pagination_status",
            "truncation_status",
            "row_inclusion_rule",
        ):
            self.assertIn(concept, coverage)

    def test_partial_or_truncated_extraction_cannot_be_interpreted_as_zero_or_full_population(self):
        coverage = COVERAGE.read_text(encoding="utf-8")
        self.assertIn("partial/truncated extraction", coverage)
        self.assertIn("not evidence of zero", coverage)
        self.assertIn("not evidence of full population coverage", coverage)

    def test_report_request_compatibility_is_separate_from_metric_zero(self):
        coverage = COVERAGE.read_text(encoding="utf-8")
        for concept in (
            "request_compatibility_status",
            "reportTypeId",
            "groupBy",
            "columns",
            "timeUnit",
            "unsupported request configuration",
            "not evidence of metric zero",
        ):
            self.assertIn(concept, coverage)

    def test_daily_and_summary_time_units_preserve_date_column_contract(self):
        coverage = COVERAGE.read_text(encoding="utf-8")
        self.assertIn("timeUnit=DAILY", coverage)
        self.assertIn("date` column", coverage)
        self.assertIn("timeUnit=SUMMARY", coverage)
        self.assertIn("startDate", coverage)
        self.assertIn("endDate", coverage)

    def test_filters_must_be_supported_by_every_requested_groupby(self):
        coverage = COVERAGE.read_text(encoding="utf-8")
        self.assertIn("every requested `groupBy`", coverage)
        self.assertIn("filter", coverage.lower())

    def test_data_lineage_routes_population_completeness_through_report_coverage(self):
        lineage = LINEAGE.read_text(encoding="utf-8")
        self.assertIn("report-coverage.md", lineage)
        self.assertIn("Population completeness is separate", lineage)


if __name__ == "__main__":
    unittest.main()
