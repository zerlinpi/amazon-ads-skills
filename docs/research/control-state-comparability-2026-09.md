# Control-state comparability — 2026-09

Reviewed: 2026-09-19

## Gap

The repository already had strong measurement comparability and placement-specific coupled-control rules, then added a shared causal gate and machine-readable control-state snapshot. The remaining gap was operational: two snapshots could be captured consistently, but replay/eval/review had no deterministic way to classify scope mismatch, unknown evidence, intended-treatment isolation, or overlapping control changes. That allowed prose interpretation to drift between Skills and reviewers.

## Current Amazon evidence

Amazon Ads Unified Reporting became generally available on 2026-06-08. Amazon states that it can combine multiple dimensions including campaign, placement, and audience and standardizes metrics/dimensions across ad products. That is valuable measurement evidence, but standardized reporting does not itself establish that advertiser controls were stable between compared windows.

Source: https://advertising.amazon.com/resources/whats-new/streamline-campaign-analysis-with-unified-reporting

Amazon Ads documents Sponsored Products placement bid adjustments as advertiser controls across top of search, rest of search, and product pages, including use with fixed and dynamic bidding strategies.

Source: https://advertising.amazon.com/resources/whats-new/improve-campaign-performance

Amazon Ads separately documents Sponsored Products audience bid boosting, where an audience can receive a bid multiplier and has audience-level performance reporting.

Source: https://advertising.amazon.com/resources/whats-new/audience-bid-boosting-in-sponsored-products

Amazon Ads documents event-based bid rules as another independently scheduled control surface for Sponsored Products. A concurrent event rule can therefore be a real confounder rather than a reporting artifact.

Source: https://advertising.amazon.com/resources/whats-new/event-based-bid-rules-for-sponsored-products-advertisers

Together these official sources support a conservative decision-safety conclusion: multiple advertiser controls can coexist and alter realized exposure, so a before/after metric comparison is not sufficient evidence that one intended control caused the outcome.

## Machine-readable adoption

`schemas/control-state-snapshot.json` is repository-owned and independently designed. `scripts/compare_control_state.py` is likewise repository-owned and intentionally conservative. It compares only source-supported configured state; it does not model Amazon's auction composition or claim causal identification.

The comparator fails closed when marketplace/profile identity differs, material control evidence is absent on either side, evidence is stale/unsupported/unknown, or a changed control lacks an effective timestamp. With an explicitly named intended treatment, only a sole evidenced treatment change can be `Treatment Isolated`; any additional evidenced material control change is `Confounded`. Without an intended treatment, changed controls are only `Directional`.

This is deliberately stricter than guessing from report movement. It preserves the invariant that missing or unsupported evidence is not zero, false, absent, unchanged, or evidence of no confounding.

## Adoption boundary

Adopt only the abstract causal-safety rule and independently authored evidence/comparison contract:

- measurement comparability and control-state comparability are separate gates;
- capture material control state and effective timestamps when causal attribution matters;
- overlapping placement, audience, bidding-strategy, rule, budget/pacing, or routing changes are potential confounders;
- missing control state is `Unknown`, not unchanged;
- do not invent an auction-level formula for how Amazon composes controls;
- deterministic replay should fail closed rather than infer unsupported causal isolation.

No Amazon prose, API schema, prompt, workflow, implementation, or private interface is copied. Amazon documentation retains Amazon copyright. Repository-owned policy, schema, comparator, and tests remain MIT.

## GitHub review note

This round re-ran multiple discovery queries across Amazon Ads/PPC/MCP and agent/evaluation/data-lineage projects. `KuudoAI/amazon_ads_mcp` (MIT; about 69 stars when reviewed) remains the strongest directly relevant open-source engineering reference surfaced: it has a real MCP implementation and explicit identity/profile handling, but it does not define Amazon measurement/control semantics, so no code or schema was copied. `vaibuep/amazon-ads-mcp` explicitly identifies itself as a Kuudo fork and was deduplicated rather than counted as independent evidence. `ppcprophet/amazon-ads-mcp` surfaced again with a proprietary hosted-service boundary and a small public repository footprint, so it was rejected as implementation evidence. `hologrow/hologrow-mcp` again surfaced with a useful coverage/freshness-first architecture, but the search evidence did not establish a sufficiently clear license/reuse boundary for implementation adoption; no code, prompt, schema, or workflow was copied.

`agentevals-dev/agentevals` surfaced as an active framework-agnostic evaluation project using OpenTelemetry traces and golden eval sets. Its trace-derived deterministic evaluation principle is directionally relevant, but adding an OTel/eval framework would materially expand this repository's dependency and runtime surface without improving the specific Amazon control-state decision gate. It was therefore rejected for this change; the repository keeps a small deterministic Python comparator and unit fixtures instead.
