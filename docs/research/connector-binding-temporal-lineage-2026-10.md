# Verified connector binding temporal lineage — 2026-10-25

## Verified gap
`evaluate_connector_capability_gate.py` previously checked a Verified binding's `observed_at` and dated supporting evidence only when the caller supplied `freshness_requirement`. Without that optional parameter, a Supported capability with a Verified binding observed *after its snapshot*, or supporting evidence observed *after binding verification*, could return `Pass` with `high_confidence_allowed=true`. This is a source-provenance contradiction, not merely stale evidence.

## Contract and limitations
Always check the chronological ordering of snapshot `captured_at`, Verified binding `observed_at`, and explicitly dated supporting evidence `observed_at`. Require valid timezone-aware instants and reject unknown `-00:00` offsets for these verification timestamps. Invalid bindings are excluded from `verified_binding_ids` and cannot alone yield high confidence. Other independently valid bindings may still qualify. Undated supporting evidence is backward-compatible only when no freshness requirement is requested; its absence of a timestamp does not prove freshness. The caller's freshness horizon, when supplied, still imposes stricter age checks.

This is connector-neutral, read-only chronology validation. It does not verify cryptographic signatures, native Amazon Ads API semantics, marketplace/advertiser/campaign eligibility, complete HTTP provenance, or whether a campaign change improved performance. No Ads writes or Executor changes.

## Source and reuse boundary
Amazon Ads official MCP connection documentation (reviewed 2026-10-25): https://advertising.amazon.com/API/docs/en-us/mcp/get-started ; Amazon Business exclusive campaign announcement (2025-05-05): https://advertising.amazon.com/en-gb/resources/whats-new/amazon-business-exclusive-campaign-for-sponsored-product/ . These are platform context, not a definition of this repository's verification timestamps. Open-source candidates and licenses are documented in `docs/SOURCES.md`; no third-party code, prompts, schemas, workflows, or templates copied.

## RED → GREEN
- RED: `756675229383114e7ee3604b76ce7902c6db6afb`, 13 deterministic tests; 1328 total, 10 failures. GitHub Actions 40170267499.
- GREEN: `a7869872f2871ec5c5e64524e9f4b6a759fe6468`, 1328/1328 tests, 15 Skill directories and 55 eval fixtures. GitHub Actions 40170330502.

## Next evidence gaps
P0 Amazon Business marketplace/advertiser/campaign eligibility bound to exact connector capability and time; P1 continuous rule activation coverage; P2 authenticated raw adapter HTTP provenance; P3 cross-control causal and marginal economics.
