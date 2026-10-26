"""RED-first: explicit unresolved monitoring fields cannot silently become absence.

Synthetic Ready holdout evidence only; no remote source authentication or Ads writes.
"""
import unittest

from scripts.validate_experiment_plan import validate_experiment_plan
from test_validate_experiment_plan import base_plan


def ready_with_monitoring():
    plan = base_plan()
    plan["comparison"]["boundary_monitoring"] = {
        "current_status": "Clean",
        "latest_verified_at": "2026-10-25T10:00:00Z",
        "material_scope_changes": [],
    }
    return plan


class ReadyHoldoutExplicitMonitoringTests(unittest.TestCase):
    def assert_monitoring_rejected(self, value, field="boundary_monitoring"):
        plan = base_plan()
        plan["comparison"]["boundary_monitoring"] = value
        errors = validate_experiment_plan(plan)
        self.assertIn(field, " | ".join(errors), errors)

    def test_explicit_null_monitoring_is_not_absence(self):
        self.assert_monitoring_rejected(None)

    def test_explicit_unknown_string_monitoring_is_not_absence(self):
        self.assert_monitoring_rejected("Unknown")

    def test_explicit_empty_string_monitoring_is_not_absence(self):
        self.assert_monitoring_rejected("")

    def test_explicit_list_monitoring_is_not_absence(self):
        self.assert_monitoring_rejected([])

    def test_explicit_boolean_monitoring_is_not_absence(self):
        self.assert_monitoring_rejected(False)

    def test_explicit_zero_monitoring_is_not_absence(self):
        self.assert_monitoring_rejected(0)

    def test_explicit_null_launch_verified_at_is_not_omitted(self):
        plan = ready_with_monitoring()
        plan["comparison"]["boundary_monitoring"]["launch_verified_at"] = None
        self.assertIn("launch_verified_at", " | ".join(validate_experiment_plan(plan)))

    def test_explicit_null_material_scope_changes_is_not_empty_list(self):
        plan = ready_with_monitoring()
        plan["comparison"]["boundary_monitoring"]["material_scope_changes"] = None
        self.assertIn("material_scope_changes", " | ".join(validate_experiment_plan(plan)))

    def test_explicit_nonlist_material_scope_changes_is_not_empty_list(self):
        plan = ready_with_monitoring()
        plan["comparison"]["boundary_monitoring"]["material_scope_changes"] = "Unknown"
        self.assertIn("material_scope_changes", " | ".join(validate_experiment_plan(plan)))

    def test_absent_monitoring_stays_legacy_ready(self):
        self.assertEqual([], validate_experiment_plan(base_plan()))

    def test_clean_monitoring_with_empty_changes_stays_ready(self):
        self.assertEqual([], validate_experiment_plan(ready_with_monitoring()))

    def test_omitted_optional_launch_verified_at_stays_ready(self):
        plan = ready_with_monitoring()
        self.assertNotIn("launch_verified_at", plan["comparison"]["boundary_monitoring"])
        self.assertEqual([], validate_experiment_plan(plan))

    def test_shadow_only_preserves_explicit_null_monitoring(self):
        plan = base_plan(status="Shadow Only")
        plan["comparison"]["boundary_monitoring"] = None
        self.assertEqual([], validate_experiment_plan(plan))

    def test_shadow_only_preserves_explicit_null_material_changes(self):
        plan = ready_with_monitoring()
        plan["status"] = "Shadow Only"
        plan["comparison"]["boundary_monitoring"]["material_scope_changes"] = None
        self.assertEqual([], validate_experiment_plan(plan))


if __name__ == "__main__":
    unittest.main()
