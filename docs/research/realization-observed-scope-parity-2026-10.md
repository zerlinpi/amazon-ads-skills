# Realization observed-scope parity — 2026-10-29

## Internal reproducible gap

The realization-history projector returned a supplied event scope unchanged when expected_scope was omitted. That allowed unresolved or padded marketplace / profile_scope values to enter the read-only realization projection. It also treated legacy entity-only events as if they carried a scope tuple containing null fields.

## RED → GREEN

- RED: deterministic tests reject marketplace="Unknown" and padded profile_scope without expected_scope, while preserving a legacy entity-only event.
- GREEN: the projector now distinguishes absent marketplace/profile scope from a supplied scope, validates all four scope fields whenever scope is supplied, and keeps expected-scope matching fail-closed.
- No live Amazon Ads calls, writes, retries, idempotency, reconciliation, or new Skill/schema/dependency.

## External evidence and rights boundary

Amazon Ads reporting/profile documentation was treated only as context for preserving account/profile/marketplace identity and grain. It does not define this repository's internal event shape or authenticate supplied evidence. Previously reviewed open-source lineage/eval/MCP projects were not imported because this narrow standard-library consistency guard needs no framework and cannot be made source-authentic by one. No third-party code, prompt, schema, workflow, template, or protected prose was copied. Public practitioner/Reddit anecdotes remain hypotheses, not platform rules or causal proof.
