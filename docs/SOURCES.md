## 2026-10-29 — Realization observed-scope integrity (v2.10.0)

- Internal reproduction: `scripts/project_realization_history.py` returned supplied observed scope without validating marketplace/profile/entity fields when `expected_scope` was omitted. This allowed placeholder or padded scope values to enter realization projection.
- Minimal change: validate concrete unpadded scope whenever a scope-bearing entity event is supplied; preserve missing scope as missing and preserve concrete opaque IDs.
- RED tests were added before the production change. No live Amazon Ads calls, write authority, retries, idempotency or reconciliation were added.
- Official Amazon Ads API materials are used only as abstract context for explicit profile/account scope and reporting grain; they do not define this repository's internal event schema or authenticate external connector evidence.
- No third-party code, prompt, schema, workflow or template copied; no dependency added. Sources with unclear or restrictive reuse terms remain principles-only.

null