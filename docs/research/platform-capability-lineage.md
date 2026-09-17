# Platform capability lineage research

Reviewed: 2026-09-17

## Problem

Amazon Ads platform controls evolve while older official pages can remain publicly accessible. A Skill that reads one live page without preserving date, product scope, control surface, eligibility, and conflicting evidence can accidentally turn a historical or adjacent rule into a current action-safe constraint.

This review is limited to public platform-behavior evidence. It does not add a live connector, private Amazon interface, or mutation authority.

## Public Amazon Ads sources reviewed

### Sponsored Products bidding strategies

Current Help page:

- `Bidding strategies for Sponsored Products`
- https://advertising.amazon.com/help/GCU2BUWJH2W3A8Z7
- Public page observed as updated September 14, 2026.

Current dynamic-bidding guide:

- `Guide to dynamic bidding - up and down with Sponsored Products`
- https://advertising.amazon.com/library/guides/dynamic-bidding-sponsored-products

The current dynamic-bidding guide states that dynamic up-and-down can increase or decrease bids by up to 100% for all placements. The product Help page is consistent with the current all-placement framing.

### Still-live broader guidance with older placement-specific framing

A separate official FBA/advertising guide remains live:

- `Combining Fulfillment by Amazon (FBA) and Amazon Ads`
- https://advertising.amazon.com/library/guides/fba

That guide still describes the older placement-specific dynamic-upward framing: up to 100% for top of search and up to 50% for other placements.

The repository therefore must not assume that "official and still live" means "current for the exact control rule." The conflict is materially relevant because copying either percentage into a permanent Skill constant could change downstream bid/exposure reasoning.

### Placement-control rollout evidence

- `Improve your campaign performance on rest of search placements using Sponsored Products rest of search bid adjustment control`
- https://advertising.amazon.com/resources/whats-new/improve-campaign-performance
- Published January 9, 2024.

This launch announcement documents a rest-of-search placement adjustment capability, its announced control range, regions, and console/API availability at launch. It is useful rollout evidence, but a launch post alone is not treated as proof that every limit or eligibility rule remains unchanged in 2026.

### Audience bid boosting evidence

- `Activate Full Funnel Strategies using AMC custom audiences via Sponsored Ads Audience Bid Boosting`
- https://advertising.amazon.com/resources/whats-new/audience-bid-boosting-in-sponsored-products
- Published November 4, 2024.

- `Increase Efficiency of campaigns with Amazon Built Audiences in SP`
- https://advertising.amazon.com/resources/whats-new/amazon-built-audience-in-sp
- Published April 30, 2025.

These pages show why capability identity must include ad product, audience type, advertiser eligibility, marketplace/region, and control surface. Availability for one audience or one Sponsored Ads product is not a universal statement about every bidding control.

## Independent adaptation

The repository adopts a conservative evidence contract rather than hardcoding a universal documentation hierarchy:

```text
platform fact
+ source kind
+ source updated/published date when exposed
+ retrieval date
+ exact ad-product/control/surface/marketplace/eligibility scope
→ capability evidence
```

If credible sources disagree, the agent first checks whether date, scope, surface, product, or eligibility explains the difference. A directly applicable and explicitly current product/reference source may supersede older generic guidance only when the overlapping scope is clear. Otherwise the capability remains `Conflicted` or `Unknown` for exact numeric reasoning.

The key safety distinction is:

```text
verified platform capability / allowed range
≠ advertiser-specific recommended change
≠ guaranteed realized auction exposure
```

Platform capability lineage therefore complements, rather than replaces, `references/action-sizing.md` and realized-delivery evidence.

## Copyright / adoption boundary

Amazon Ads pages are vendor documentation, not source code relicensed into this repository. No Amazon prose, UI assets, screenshots, API implementation, examples, or proprietary schemas are copied. This file independently summarizes factual platform behavior and the evidence-management implication needed by the repository.

The resulting policy lives in `references/platform-capability-lineage.md`; bid and placement Skills load it only when time-varying platform behavior materially affects a decision.
