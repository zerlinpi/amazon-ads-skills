# Platform-managed delivery surfaces and traffic-mix confounding

## Why this matters

Amazon Ads can introduce advertiser-visible delivery experiences that reuse existing campaign controls and may be enabled for eligible existing campaigns without an advertiser manually editing the campaign. A causal diagnosis that audits only advertiser-initiated bid, budget, targeting, placement, state, negative, or structure changes can therefore miss a real change in realized traffic mix.

The repository adopts the generic rule:

```text
no manual campaign-control change
!= proof that delivery conditions stayed constant
```

A platform-managed rollout is a **competing cause**, not automatic proof of causality. Account/campaign eligibility must be connected to realized delivery evidence before assigning the outcome to that surface.

## Current Amazon Ads example

Amazon Ads announced on March 10, 2026 that Sponsored Products prompts and Sponsored Brands prompts would move to general availability in the United States on March 25, 2026.

Amazon's public launch documentation states that, for supported U.S. Sponsored Products and Sponsored Brands advertisers:

- eligible existing campaigns are automatically enrolled in prompts;
- prompts reuse existing campaign parameters such as campaign targeting;
- prompts can appear in shopping results and product detail pages;
- prompt clicks participate in CPC bidding/billing;
- prompt performance can be inspected in Ads Console and via API;
- a Prompts report exposes prompt-level delivery/performance metrics.

These facts make prompts a concrete example of a platform-managed delivery-surface change that can overlap a performance break even when the advertiser's ordinary campaign-control timeline is empty.

## Adaptation into this repository

We do **not** encode a permanent rule that prompts are always material, always harmful, or always enabled in every marketplace/account. We use the launch only to justify a general diagnostic requirement:

1. include platform-managed surfaces / auto-enrollment in the causal change timeline;
2. distinguish advertiser changes from external automation and platform-managed changes;
3. connect rollout eligibility to actual surface-level delivery before declaring causality;
4. if surface-level fields are unavailable from the active connector, keep exposure unknown rather than converting missing data to zero;
5. reconcile surface-level impressions/clicks/spend/orders/sales before suppressing unrelated campaign controls.

This integrates with the existing acquisition-channel lineage rule: a metric/report may exist in the Amazon Ads product while being unavailable through the currently connected data path.

## Source and copyright boundary

Primary source:

- Amazon Ads, "Sponsored Products prompts and Sponsored Brands prompts", launch announcement dated March 10, 2026; U.S. general availability dated March 25, 2026.

Amazon Ads Help / What's New content is public vendor documentation, not open-source software licensed for redistribution. This repository therefore uses only factual platform behavior and independently rewrites it into a generic causal-diagnosis framework. We do not copy Amazon's UI, report templates, API implementation, proprietary prompt-generation logic, or substantial source text.

## Safety boundary

This research does not authorize live writes. Prompt pausing or any other live Amazon Ads mutation remains outside the Skill layer and requires an explicitly authorized external Connector / Executor.
