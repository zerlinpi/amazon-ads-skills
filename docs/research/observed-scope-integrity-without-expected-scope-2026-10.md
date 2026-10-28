# Observed scope integrity without expected scope

Date: 2026-10-28

## Internal gap

The measurement-history projector validated observed scope values only when a caller supplied expected_scope. When expected_scope was omitted, a supplied event scope could contain whole-label unresolved placeholders such as Unknown or padded values and still participate in the projected latest measurement state.

## RED->GREEN

- RED test commit: fce567d20dd45f945cd1dbd6eea874879d0a9257
- GREEN production commit: e47ddd585928eba38d80980d0a816faaa0597553

The deterministic tests cover unresolved observed scope, padded observed scope, and a concrete opaque scope that remains accepted.

## Boundary

This is an internal read-only provenance consistency check. It does not authenticate Amazon Ads source data, prove full-window event capture, or add write/retry/idempotency/reconciliation authority. Missing scope remains distinct from supplied-but-unresolved scope. No third-party code, prompt, schema, workflow, or template was copied.
