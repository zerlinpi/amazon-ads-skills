import unittest

from scripts.project_measurement_comparison_history import project_measurement_comparison_history


def comparison(classification="Directional", **overrides):
    value = {"comparator_id": "measurement-composition@1", "classification": classification, "changed_fields": ["allocation_coverage_status"], "reasons": ["allocation coverage changed"], "baseline_snapshot_id": "baseline-1", "post_snapshot_id": "post-1"}
    value.update(overrides)
    return value


def event(event_id, timestamp, *, event_type="evaluated", measurement_comparison=None, supersedes_event_id=None, entity_id="keyword-1"):
    payload = {"event_id": event_id, "event_type": event_type, "timestamp": timestamp, "marketplace": "US", "profile_scope": "profile-us-1", "entity": {"type": "keyword", "id": entity_id}, "action_type": "bid_decrease", "parent_action_id": "action-1"}
    if measurement_comparison is not None:
        payload["measurement_comparison"] = measurement_comparison
    if supersedes_event_id is not None:
        payload["supersedes_event_id"] = supersedes_event_id
    return payload


class MeasurementComparisonHistoryProjectionTests(unittest.TestCase):
    def test_latest_active_comparison_is_projected(self):
        result = project_measurement_comparison_history([event("eval-1", "2026-09-20T00:00:00Z", measurement_comparison=comparison())])
        self.assertEqual(result["measurement_comparison_status"], "Available")
        self.assertEqual(result["latest_measurement_comparison"]["source_event_id"], "eval-1")
        self.assertEqual(result["latest_measurement_comparison"]["classification"], "Directional")

    def test_correction_with_replacement_comparison_supersedes_prior_audit(self):
        result = project_measurement_comparison_history([
            event("eval-1", "2026-09-20T00:00:00Z", measurement_comparison=comparison()),
            event("corr-1", "2026-09-21T00:00:00Z", event_type="corrected", measurement_comparison=comparison("Comparable", changed_fields=[], reasons=["reconciled"], baseline_snapshot_id="baseline-2", post_snapshot_id="post-2"), supersedes_event_id="eval-1"),
        ])
        latest = result["latest_measurement_comparison"]
        self.assertEqual(latest["source_event_id"], "corr-1")
        self.assertEqual(latest["classification"], "Comparable")
        self.assertEqual(latest["baseline_snapshot_id"], "baseline-2")

    def test_correction_without_replacement_clears_stale_comparison(self):
        result = project_measurement_comparison_history([
            event("eval-1", "2026-09-20T00:00:00Z", measurement_comparison=comparison()),
            event("corr-1", "2026-09-21T00:00:00Z", event_type="corrected", supersedes_event_id="eval-1"),
        ])
        self.assertIsNone(result["latest_measurement_comparison"])
        self.assertEqual(result["measurement_comparison_status"], "Superseded Without Replacement")
        self.assertTrue(any("supersed" in warning.lower() for warning in result["measurement_comparison_warnings"]))

    def test_recursive_correction_chain_does_not_resurrect_superseded_audit(self):
        result = project_measurement_comparison_history([
            event("eval-1", "2026-09-19T00:00:00Z", measurement_comparison=comparison()),
            event("corr-1", "2026-09-20T00:00:00Z", event_type="corrected", measurement_comparison=comparison("Comparable", changed_fields=[]), supersedes_event_id="eval-1"),
            event("corr-2", "2026-09-21T00:00:00Z", event_type="corrected", supersedes_event_id="corr-1"),
        ])
        self.assertIsNone(result["latest_measurement_comparison"])
        self.assertEqual(result["measurement_comparison_status"], "Superseded Without Replacement")

    def test_cross_action_correction_does_not_erase_independent_audit(self):
        original = event("eval-a", "2026-10-19T09:00:00Z", measurement_comparison=comparison("Comparable"))
        for parent_action_id in ("action-b", None, "", " "):
            with self.subTest(parent_action_id=parent_action_id):
                correction = event(
                    "corr-b", "2026-10-19T10:00:00Z",
                    event_type="corrected", supersedes_event_id="eval-a",
                )
                correction["parent_action_id"] = parent_action_id
                with self.assertRaisesRegex(ValueError, "parent_action_id"):
                    project_measurement_comparison_history([original, correction])

    def test_missing_original_action_identity_cannot_be_superseded(self):
        for parent_action_id in (None, "", " "):
            with self.subTest(parent_action_id=parent_action_id):
                original = event("eval-a", "2026-10-19T09:00:00Z", measurement_comparison=comparison("Comparable"))
                original["parent_action_id"] = parent_action_id
                correction = event(
                    "corr-a", "2026-10-19T10:00:00Z",
                    event_type="corrected", supersedes_event_id="eval-a",
                )
                with self.assertRaisesRegex(ValueError, "parent_action_id"):
                    project_measurement_comparison_history([original, correction])

    def test_mixed_entity_scope_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "single entity scope"):
            project_measurement_comparison_history([
                event("eval-1", "2026-09-20T00:00:00Z", measurement_comparison=comparison()),
                event("eval-2", "2026-09-21T00:00:00Z", measurement_comparison=comparison("Comparable"), entity_id="keyword-2"),
            ])

    def test_missing_comparator_identity_projects_unknown_not_available(self):
        partial = comparison(comparator_id=None)
        result = project_measurement_comparison_history([event("eval-1", "2026-09-20T00:00:00Z", measurement_comparison=partial)])
        self.assertEqual(result["measurement_comparison_status"], "Unknown")
        self.assertTrue(result["measurement_comparison_warnings"])


    def test_offset_aware_order_uses_actual_instant_not_timestamp_text(self):
        # 09:30 +08:00 is 01:30 UTC, earlier than 02:00 UTC.
        result = project_measurement_comparison_history([
            event("older-local", "2026-10-09T09:30:00+08:00", measurement_comparison=comparison("Directional")),
            event("newer-utc", "2026-10-09T02:00:00Z", measurement_comparison=comparison("Comparable")),
        ])
        self.assertEqual(result["latest_measurement_comparison"]["source_event_id"], "newer-utc")
        self.assertEqual(result["latest_measurement_comparison"]["classification"], "Comparable")

    def test_missing_or_naive_audit_timestamp_fails_closed(self):
        for timestamp in (None, "", "2026-10-09T02:00:00", "not-a-date"):
            with self.subTest(timestamp=timestamp):
                with self.assertRaisesRegex(ValueError, "timezone-aware RFC3339"):
                    project_measurement_comparison_history([
                        event("invalid", timestamp, measurement_comparison=comparison()),
                    ])

    def test_equal_instant_offsets_use_stable_event_id_tie_break(self):
        result = project_measurement_comparison_history([
            event("a", "2026-10-09T10:00:00+08:00", measurement_comparison=comparison("Directional")),
            event("b", "2026-10-09T02:00:00Z", measurement_comparison=comparison("Comparable")),
        ])
        self.assertEqual(result["latest_measurement_comparison"]["source_event_id"], "b")


class MeasurementComparisonAccountIdentityTests(unittest.TestCase):
    """Same legacy entity key does not authorize cross-advertiser audit reuse."""

    def _event(self, event_id, account_identity):
        item = event(
            event_id,
            "2026-10-19T10:00:00Z" if event_id == "a" else "2026-10-19T11:00:00Z",
            measurement_comparison=comparison("Comparable"),
        )
        item["account_identity"] = account_identity
        return item

    def test_conflicting_advertiser_identity_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "account identity"):
            project_measurement_comparison_history([
                self._event("a", {"global_advertiser_account_id": "global-a"}),
                self._event("b", {"global_advertiser_account_id": "global-b"}),
            ])

    def test_known_and_missing_identity_cannot_merge(self):
        with self.assertRaisesRegex(ValueError, "account identity"):
            project_measurement_comparison_history([
                self._event("a", None),
                self._event("b", {"global_advertiser_account_id": "global-b"}),
            ])

    def test_unverified_global_regional_mapping_cannot_merge(self):
        with self.assertRaisesRegex(ValueError, "account identity"):
            project_measurement_comparison_history([
                self._event("a", {"global_advertiser_account_id": "global-a"}),
                self._event("b", {"regional_advertiser_account_id": "regional-a"}),
            ])

    def test_compatible_identity_enrichment_is_allowed(self):
        result = project_measurement_comparison_history([
            self._event("a", {"global_advertiser_account_id": "global-a"}),
            self._event("b", {
                "global_advertiser_account_id": "global-a",
                "regional_advertiser_account_id": "regional-a",
            }),
        ])
        self.assertEqual(result["measurement_comparison_status"], "Available")
        self.assertEqual(result["latest_measurement_comparison"]["source_event_id"], "b")

    def test_all_legacy_missing_identity_remains_supported(self):
        result = project_measurement_comparison_history([
            self._event("a", None),
            self._event("b", None),
        ])
        self.assertEqual(result["latest_measurement_comparison"]["source_event_id"], "b")


class MeasurementComparisonExpectedScopeTests(unittest.TestCase):
    """A single-account slice must still be bound to the caller's requested account."""

    @staticmethod
    def _scope(**overrides):
        value = {
            "marketplace": "US",
            "profile_scope": "profile-us-1",
            "entity_type": "keyword",
            "entity_id": "keyword-1",
            "account_identity": {"global_advertiser_account_id": "global-a"},
        }
        value.update(overrides)
        return value

    @staticmethod
    def _event(identity):
        item = event(
            "eval-1",
            "2026-10-19T10:00:00Z",
            measurement_comparison=comparison("Comparable"),
        )
        item["account_identity"] = identity
        return item

    def test_single_event_from_wrong_account_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "expected_scope"):
            project_measurement_comparison_history(
                [self._event({"global_advertiser_account_id": "global-b"})],
                expected_scope=self._scope(),
            )

    def test_single_event_without_account_identity_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "expected_scope"):
            project_measurement_comparison_history(
                [self._event(None)],
                expected_scope=self._scope(),
            )

    def test_missing_requested_regional_identity_is_not_inferred(self):
        with self.assertRaisesRegex(ValueError, "expected_scope"):
            project_measurement_comparison_history(
                [self._event({"global_advertiser_account_id": "global-a"})],
                expected_scope=self._scope(account_identity={
                    "global_advertiser_account_id": "global-a",
                    "regional_advertiser_account_id": "regional-a",
                }),
            )

    def test_wrong_requested_entity_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "expected_scope"):
            project_measurement_comparison_history(
                [self._event({"global_advertiser_account_id": "global-a"})],
                expected_scope=self._scope(entity_id="keyword-2"),
            )

    def test_matching_account_and_scope_is_available(self):
        result = project_measurement_comparison_history(
            [self._event({"global_advertiser_account_id": "global-a"})],
            expected_scope=self._scope(),
        )
        self.assertEqual(result["measurement_comparison_status"], "Available")
        self.assertEqual(result["latest_measurement_comparison"]["source_event_id"], "eval-1")

    def test_legacy_unbound_caller_remains_supported(self):
        result = project_measurement_comparison_history([self._event(None)])
        self.assertEqual(result["measurement_comparison_status"], "Available")

    def test_invalid_requested_account_envelope_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "expected_scope"):
            project_measurement_comparison_history(
                [self._event({"global_advertiser_account_id": "global-a"})],
                expected_scope=self._scope(account_identity={"country_code": "US"}),
            )

    def test_partial_scope_without_entity_is_rejected(self):
        item = event("partial-scope", "2026-10-09T08:00:00Z", measurement_comparison=comparison())
        item.pop("entity")
        item["marketplace"] = "US"
        item["profile_scope"] = "profile-us-1"
        with self.assertRaisesRegex(ValueError, "scope"):
            project_measurement_comparison_history([item])



if __name__ == "__main__":
    unittest.main()
