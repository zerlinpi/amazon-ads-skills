import json
import unittest
from pathlib import Path

from scripts.compare_measurement_composition import compare_measurement_composition


ROOT = Path(__file__).resolve().parents[1]
FIELDS = {
    "modeled_conversion_inclusion",
    "direct_modeled_split_available",
    "allocation_coverage_status",
    "unallocated_rows_present",
    "allocation_grain",
}


def state(snapshot_id, **overrides):
    composition = {
        "modeled_conversion_inclusion": "combined_with_direct",
        "direct_modeled_split_available": False,
        "allocation_coverage_status": "Complete",
        "unallocated_rows_present": False,
        "allocation_grain": "targeting",
    }
    composition.update(overrides)
    return {
        "evidence_snapshot_id": snapshot_id,
        "measurement_composition": composition,
    }


class MeasurementComparisonAuditContractTests(unittest.TestCase):
    def schema(self):
        return json.loads(
            (ROOT / "schemas" / "optimization-event.json").read_text(encoding="utf-8")
        )

    def read(self, relative_path):
        return (ROOT / relative_path).read_text(encoding="utf-8").lower()

    def test_comparator_output_carries_stable_identity_and_snapshot_lineage(self):
        result = compare_measurement_composition(
            state(
                "baseline-snapshot-1",
                allocation_coverage_status="Partial",
                unallocated_rows_present=True,
            ),
            state("post-snapshot-1"),
        )
        self.assertEqual(result["comparator_id"], "measurement-composition@1")
        self.assertEqual(result["baseline_snapshot_id"], "baseline-snapshot-1")
        self.assertEqual(result["post_snapshot_id"], "post-snapshot-1")
        self.assertEqual(result["classification"], "Directional")
        self.assertEqual(
            set(result["changed_fields"]),
            {"allocation_coverage_status", "unallocated_rows_present"},
        )
        self.assertTrue(result["reasons"])

    def test_event_schema_preserves_measurement_comparison_audit_evidence(self):
        schema = self.schema()
        props = schema["properties"]
        self.assertIn("measurement_comparison", props)
        comparison = props["measurement_comparison"]
        self.assertEqual(comparison["type"], ["object", "null"])

        cprops = comparison["properties"]
        self.assertEqual(
            {
                "comparator_id",
                "classification",
                "changed_fields",
                "reasons",
                "baseline_snapshot_id",
                "post_snapshot_id",
            },
            set(cprops),
        )
        self.assertEqual(
            cprops["classification"]["enum"],
            ["Comparable", "Directional", "Not Comparable", "Unknown", None],
        )
        self.assertEqual(set(cprops["changed_fields"]["items"]["enum"]), FIELDS)
        for field in ("comparator_id", "baseline_snapshot_id", "post_snapshot_id"):
            self.assertIn("null", cprops[field]["type"])

    def test_post_change_review_persists_comparator_output_on_evaluated_events(self):
        skill = self.read("skills/post-change-review/SKILL.md")
        for token in [
            "measurement_comparison",
            "comparator_id",
            "changed_fields",
            "baseline_snapshot_id",
            "post_snapshot_id",
            "evaluated",
        ]:
            self.assertIn(token, skill)

    def test_memory_contract_keeps_comparison_result_auditable(self):
        memory = self.read("references/optimization-memory.md")
        for token in [
            "measurement_comparison",
            "classification",
            "changed_fields",
            "reasons",
            "baseline_snapshot_id",
            "post_snapshot_id",
        ]:
            self.assertIn(token, memory)


if __name__ == "__main__":
    unittest.main()
