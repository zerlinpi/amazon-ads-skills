"""RED-first: Ready experiment identity and optional control-arm scope must be concrete.

Synthetic fixtures only; this validator never calls or writes Amazon Ads.
"""
import copy
import unittest

from scripts.validate_experiment_plan import validate_experiment_plan
from test_validate_experiment_plan import base_plan


class ReadyExperimentIdentityBoundaryTests(unittest.TestCase):
    def assert_rejected(self, plan, field):
        errors = validate_experiment_plan(plan)
        self.assertTrue(errors, "Ready experiment must not accept unresolved identity")
        self.assertIn(field, " | ".join(errors), errors)

    def test_ready_rejects_unknown_marketplace(self):
        plan = base_plan()
        plan["scope"]["marketplace"] = "Unknown"
        self.assert_rejected(plan, "scope.marketplace")

    def test_ready_rejects_unsupported_profile(self):
        plan = base_plan()
        plan["scope"]["profile_scope"] = "Not Supported"
        self.assert_rejected(plan, "scope.profile_scope")

    def test_ready_rejects_partial_entity_type(self):
        plan = base_plan()
        plan["scope"]["entity_type"] = "Partial"
        self.assert_rejected(plan, "scope.entity_type")

    def test_ready_rejects_missing_entity_id_label(self):
        plan = base_plan()
        plan["scope"]["entity_ids"] = ["Missing"]
        self.assert_rejected(plan, "scope.entity_ids")

    def test_ready_rejects_mixed_valid_and_unknown_entity_ids(self):
        plan = base_plan()
        plan["scope"]["entity_ids"] = ["campaign-synthetic-1", "Unavailable"]
        self.assert_rejected(plan, "scope.entity_ids")

    def test_ready_rejects_padded_profile_identity(self):
        plan = base_plan()
        plan["scope"]["profile_scope"] = " profile-synthetic-a "
        self.assert_rejected(plan, "scope.profile_scope")

    def test_ready_rejects_duplicate_treatment_entity_ids(self):
        plan = base_plan()
        plan["scope"]["entity_ids"] = ["campaign-synthetic-1", "campaign-synthetic-1"]
        self.assert_rejected(plan, "scope.entity_ids")

    def test_ready_rejects_placeholder_control_entity_ids_when_supplied(self):
        plan = base_plan()
        plan["comparison"]["control_entity_ids"] = ["Unknown"]
        self.assert_rejected(plan, "control_entity_ids")

    def test_ready_rejects_treatment_control_identity_overlap(self):
        plan = base_plan()
        plan["comparison"]["control_entity_ids"] = ["campaign-synthetic-1"]
        self.assert_rejected(plan, "control_entity_ids")

    def test_ready_rejects_duplicate_control_ids(self):
        plan = base_plan()
        plan["comparison"]["control_entity_ids"] = ["control-a", "control-a"]
        self.assert_rejected(plan, "control_entity_ids")

    def test_ready_accepts_concrete_ids_containing_reserved_substrings(self):
        plan = base_plan()
        plan["scope"]["entity_ids"] = ["campaign-unknown-but-real-123"]
        plan["comparison"]["control_entity_ids"] = ["control-not-supported-but-real-456"]
        self.assertEqual(validate_experiment_plan(plan), [])

    def test_ready_holdout_without_explicit_control_ids_remains_compatible(self):
        self.assertEqual(validate_experiment_plan(base_plan()), [])

    def test_shadow_only_preserves_unresolved_identity(self):
        plan = base_plan(status="Shadow Only")
        plan["scope"]["marketplace"] = "Unknown"
        plan["scope"]["entity_ids"] = ["Missing"]
        plan["comparison"]["control_entity_ids"] = ["Unknown"]
        self.assertEqual(validate_experiment_plan(plan), [])


if __name__ == "__main__":
    unittest.main()
