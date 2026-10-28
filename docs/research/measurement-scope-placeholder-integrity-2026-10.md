# Measurement scope placeholder integrity (2026-10)

## Reproducible gap

At main `6910a5e641d78e981bd33d0ea857d814d641898b` (v2.7.0), `scripts/project_measurement_history.py` required non-empty scope strings but treated whole-label values such as `Unknown`, `N/A`, `Partial`, and padded identities as usable measurement scope. A requested scope and observed event could therefore agree on an unresolved placeholder and still project a latest measurement state.

This is an internal provenance defect. It does not authenticate Amazon Ads account/marketplace data or prove complete history.

## RED → GREEN

- RED: `f1832c7646d701a72a30defa9fdc639c93e900df` added four deterministic tests that fail under the old projector.
- GREEN: `4d64341fa91891f9851182d3af011eb375e5e99f` rejects unresolved or padded expected/observed scope values while preserving concrete identifiers that merely contain placeholder substrings.

## Scope

The projector now keeps missing/unknown/unsupported scope unresolved rather than promoting it to a usable identity. It remains read-only; live Ads writes, retries, idempotency and reconciliation remain with the external authorized Executor.

## Source and reuse boundary

Amazon Ads official materials and public lineage/evaluation projects motivate preserving identity and uncertainty, but do not define this repository's normalized scope contract. No third-party code, prompt, schema, workflow or template was copied.
