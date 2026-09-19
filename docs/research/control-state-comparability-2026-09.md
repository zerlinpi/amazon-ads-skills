# Control-state comparability — 2026-09

Reviewed: 2026-09-19

## Gap

The repository already had strong measurement comparability and placement-specific coupled-control rules, but the post-change causal loop did not have one shared gate requiring baseline/post advertiser-control state to be comparable. A clean metric series could therefore be over-interpreted when another material control changed during the evaluation window.

## Current Amazon evidence

Amazon Ads Unified Reporting became generally available on 2026-06-08. Amazon states that it can combine multiple dimensions including campaign, placement, and audience and standardizes metrics/dimensions across ad products. That is valuable measurement evidence, but standardized reporting does not itself establish that advertiser controls were stable between compared windows.

Source: https://advertising.amazon.com/resources/whats-new/streamline-campaign-analysis-with-unified-reporting

Amazon Ads documents Sponsored Products placement bid adjustments as advertiser controls across top of search, rest of search, and product pages, including use with fixed and dynamic bidding strategies.

Source: https://advertising.amazon.com/resources/whats-new/improve-campaign-performance

Amazon Ads separately documents Sponsored Products audience bid boosting, where an audience can receive a bid multiplier and has audience-level performance reporting.

Source: https://advertising.amazon.com/resources/whats-new/audience-bid-boosting-in-sponsored-products

Amazon Ads also documents event-based schedule bid rules that can automatically increase bids during declared high-traffic events.

Source: https://advertising.amazon.com/resources/whats-new/event-based-bid-rules-for-sponsored-products-advertisers

Together these official sources support a conservative decision-safety conclusion: multiple advertiser controls can coexist and alter realized exposure, so a before/after metric comparison is not sufficient evidence that one intended control caused the outcome.

## Adoption boundary

Adopt only the abstract causal-safety rule:

- measurement comparability and control-state comparability are separate gates;
- capture material control state and effective timestamps when causal attribution matters;
- overlapping placement, audience, bidding-strategy, rule, budget/pacing, or routing changes are potential confounders;
- missing control state is `Unknown`, not unchanged;
- cap causal language at `Directional` / `Confounded` / `Unknown` when isolation is unsupported;
- do not invent an auction-level formula for how Amazon composes controls.

No Amazon prose, API schema, prompt, workflow, implementation, or private interface is copied. Amazon documentation retains Amazon copyright. Repository-owned policy and tests remain MIT.

## GitHub review note

This round also re-ran multiple GitHub discovery queries for Amazon Ads/PPC/MCP and agent/evaluation projects. The directly relevant Amazon Ads repositories surfaced were already reviewed in `docs/SOURCES.md` (including `nospicyplease/amazon-ppc-advanced-skills` and `ppcprophet/amazon-ads-mcp`). Search also surfaced obvious same-name copies of `amazon-ppc-advanced-skills` and `advertising-hub`; these were not counted as independent evidence. No newly discovered repository supplied stronger platform evidence for this specific control-interaction gap than current Amazon official documentation, so no third-party code, prompt, schema, threshold, or workflow was adopted in this change.
