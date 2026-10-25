# Generic material-control placeholder evidence — 2026-10-25

## Gap and risk

The read-only comparator already rejects null root states and unsupported `evidence_status`, but a `Complete` inventory with `observed` status could still repeat `Unknown`, `Unsupported`, `Partial`, `Missing` or `Unavailable` as a material state and classify a different base-bid treatment as `Treatment Isolated`. This applies to an extra material control outside the minimum registry set, and to generic registered fixture controls. Non-finite JSON-like numeric leaves could also appear stable or be misclassified as a real competing change.

## Evidence and scope

Amazon Ads official Sponsored Products and across-retailers pages (reviewed 2026-10-25) establish that advertiser controls and delivery/reporting scopes vary, not this repository's normalized evidence sentinel vocabulary. No official API response shape or cross-retailer eligibility is inferred. Reddit discussion of missing UI change history (2026-09-08) is a hypothesis generator only, not a platform rule. See `docs/SOURCES.md` for URLs, candidate metadata and licensing boundaries.

## Deterministic RED → GREEN

- Feature branch `fix/generic-material-state-placeholder-evidence-20261025`; PR #163.
- RED-first `tests/test_generic_material_state_placeholder_evidence.py`: 23 synthetic tests, 17 failing on old behavior, 1274 total (Actions 40159277435).
- First minimal implementation left four sentinel-normalization tests failing (Actions 40159315750); corrected the regex and re-ran. GREEN: 1274/1274, 15 Skills and 55 eval fixtures (Actions 40159327265).
- Reject reserved exact missing/unsupported state strings, blank scalar strings and non-finite numeric leaves recursively across material control state. Preserve observed zero, False, descriptive strings, independently complete lists and actual competing changes. No Ads write or third-party implementation.

## Boundaries and next work

This guard cannot prove whether a valid-looking normalized value was actually observed, whether a connector supports a marketplace or retailer scope, whether rules were active throughout the evaluation window, or whether a measured outcome was caused by the intended treatment. Maintain Read-only/Suggest/Shadow and leave live execution to an authorized external Executor. Revisit Amazon Business placement eligibility/capability as a separate dated evidence contract; do not infer ineligibility from absent B2B modifiers.
