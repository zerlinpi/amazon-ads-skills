# Measurement composition memory — 2026-09

## Gap

Decision-time measurement identity preserved reporting generation, metric semantics, date attribution and historical availability, but not whether conversion metrics combined modeled and directly measured conversions or whether lower-grain conversion allocation was complete. That omission can make a later outcome review mistake a measurement-composition/allocation change for the effect of an optimization action.

## Primary evidence

Amazon Ads, **Modeled conversions now reported for Sponsored Display campaigns** (2024-07-01): modeled conversions are reported in the same conversion columns as directly attributed conversions. When meaningful estimates cannot be produced at the requested reporting breakdown, Amazon reports conversions on an `Unallocated` row; API targeting-grouped reports may expose `Unallocated` / `-20`. Source: https://advertising.amazon.com/resources/whats-new/modeled-conversions-for-sponsored-display-campaigns

Amazon Ads, **Amazon DSP provides modeled attribution for off-Amazon conversions for US advertisers** (2024-08-16): directly measured and modeled conversions are reported together as a combined result in campaign reporting. Source: https://advertising.amazon.com/resources/whats-new/modeled-attribution-for-off-amazon-conversions-for-us-advertiser

These are Amazon-published reporting semantics. We adopt only the abstract safety requirement: preserve known measurement composition/allocation state and keep unknown state unknown. No Amazon text, schema, code or workflow is copied into runtime implementation.

## GitHub / ecosystem review

- `coaxon/amazon-mcp` — MIT; active Amazon SP-API/Ads API MCP with read paths and dry-run defaults. Useful connector engineering reference, but it does not establish Amazon reporting semantics and is not needed as a dependency for this change. No code copied.
- `KuudoAI/amazon_ads_mcp` — broad Amazon Ads MCP/API surface with tests/validation claims and explicit Ads API v1 beta warning. Already reviewed by this repository; no new non-duplicate measurement-memory primitive found this round. No implementation copied.
- `ppcprophet/amazon-ads-mcp` — proprietary hosted service. Useful ecosystem evidence only; rejected for implementation reuse and dependency introduction.
- `vaibuep/amazon-ads-mcp` — search-visible content substantially overlaps the Kuudo/Openbridge implementation. Treated as duplicate/mirror evidence rather than an independent source.

Stars/popularity are discovery context only and are not adoption criteria. The behavior change below is grounded in Amazon official semantics and the repository's existing append-first evidence-identity architecture.

## Decision

Extend the existing evidence snapshot and bounded measurement projection with a nullable `measurement_composition` envelope. Preserve only explicitly observed fields. If the envelope is absent, project `null` and warn that composition/allocation comparability is unresolved; never infer direct-only measurement, zero modeled conversions, or complete lower-grain allocation.

This remains read-only/Suggest-safe. It adds no Amazon Ads write, retry, idempotency or reconciliation behavior.
