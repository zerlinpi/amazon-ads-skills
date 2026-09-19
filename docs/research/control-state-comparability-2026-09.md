# Control-state comparability — 2026-09

Reviewed: 2026-09-19

## Gap

The repository already had strong measurement comparability and placement-specific coupled-control rules, but the post-change causal loop did not have one shared gate requiring baseline/post advertiser-control state to be comparable. That gate was added first. A follow-up gap remained: the policy was prose-only, so connector evidence, replay fixtures, and reviewers had no shared machine-readable envelope for scope, provenance, effective timestamps, or explicit unknown control state.

## Current Amazon evidence

Amazon Ads Unified Reporting became generally available on 2026-06-08. Amazon states that it can combine multiple dimensions including campaign, placement, and audience and standardizes metrics/dimensions across ad products. That is valuable measurement evidence, but standardized reporting does not itself establish that advertiser controls were stable between compared windows.

Source: https://advertising.amazon.com/resources/whats-new/streamline-campaign-analysis-with-unified-reporting

Amazon Ads documents Sponsored Products placement bid adjustments as advertiser controls across top of search, rest of search, and product pages, including use with fixed and dynamic bidding strategies.

Source: https://advertising.amazon.com/resources/whats-new/improve-campaign-performance

Amazon Ads separately documents Sponsored Products audience bid boosting, where an audience can receive a bid multiplier and has audience-level performance reporting.

Source: https://advertising.amazon.com/resources/whats-new/audience-bid-boosting-in-sponsored-products

Amazon Ads' Sponsored Products bidding help, updated 2026-09-14, documents dynamic, fixed, and rule-based bidding and audience bid adjustment. This reinforces that control identity can change independently of metric/report identity.

Source: https://advertising.amazon.com/help/GCU2BUWJH2W3A8Z7

Together these official sources support a conservative decision-safety conclusion: multiple advertiser controls can coexist and alter realized exposure, so a before/after metric comparison is not sufficient evidence that one intended control caused the outcome.

## Machine-readable adoption

`schemas/control-state-snapshot.json` is repository-owned and independently designed. It is intentionally an evidence envelope rather than a copy of an Amazon API schema. It records:

- marketplace/profile scope plus optional narrower entity scope;
- observation timestamp;
- source system and acquisition channel provenance;
- material control type and source-supported state;
- effective timestamp;
- explicit evidence status including `unsupported` and `unknown`.

The contract preserves the existing invariant that missing or unsupported evidence is not zero, false, absent, or unchanged. It does not authorize writes and does not require connectors to expose unsupported controls.

## Adoption boundary

Adopt only the abstract causal-safety rule and independently authored evidence contract:

- measurement comparability and control-state comparability are separate gates;
- capture material control state and effective timestamps when causal attribution matters;
- overlapping placement, audience, bidding-strategy, rule, budget/pacing, or routing changes are potential confounders;
- missing control state is `Unknown`, not unchanged;
- cap causal language at `Directional` / `Confounded` / `Unknown` when isolation is unsupported;
- do not invent an auction-level formula for how Amazon composes controls.

No Amazon prose, API schema, prompt, workflow, implementation, or private interface is copied. Amazon documentation retains Amazon copyright. Repository-owned policy, schema, and tests remain MIT.

## GitHub review note

This round re-ran multiple discovery queries for Amazon Ads/PPC/MCP and agent/evaluation/data-lineage projects. `KuudoAI/amazon_ads_mcp` (MIT; about 69 stars when reviewed) remains useful engineering evidence for identity/tool separation but does not define Amazon measurement semantics; the surfaced `vaibuep/amazon-ads-mcp` explicitly identifies itself as a fork and was therefore not counted as independent evidence. `ppcprophet/amazon-ads-mcp` surfaced again with a proprietary hosted-service boundary and only a small public repository footprint, so it was not used as implementation evidence. `hologrow/hologrow-mcp` surfaced as a connector/skills architecture candidate with explicit coverage/freshness middleware, but this round did not establish enough license/reuse evidence from the search result to copy any implementation; only the already-independent repository principle of checking coverage/freshness is retained. No third-party code, prompt, schema, threshold, or workflow was copied into this change.
