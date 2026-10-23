"""Regression: RFC3339 offset bounds must be validated before datetime normalization."""
import unittest
from scripts.project_measurement_comparison_history import _timestamp


class Rfc3339OffsetBoundsTests(unittest.TestCase):
    def test_invalid_offset_minutes_rejected(self):
        for offset in ("+00:60", "+01:99", "-01:60", "+23:99"):
            with self.subTest(offset=offset):
                with self.assertRaisesRegex(ValueError, "timezone-aware RFC3339"):
                    _timestamp({"timestamp": "2026-10-09T02:00:00" + offset})

    def test_valid_offsets_retained(self):
        for offset in ("Z", "+08:00", "-07:30", "+23:59"):
            with self.subTest(offset=offset):
                self.assertIsNotNone(_timestamp({"timestamp": "2026-10-09T02:00:00" + offset}))

    def test_unknown_local_offset_rejected(self):
        with self.assertRaisesRegex(ValueError, "timezone-aware RFC3339"):
            _timestamp({"timestamp": "2026-10-09T02:00:00-00:00"})


if __name__ == "__main__":
    unittest.main()
