# Platform-managed realized ad identity

## Why this matters

Amazon Ads increasingly supports campaign formats where the advertiser's configured controls do not fully determine the shopper-visible ad realization. A campaign can keep the same targeting/bid/budget state while Amazon changes the delivery surface, dynamically chooses a product grouping, or otherwise varies the realized ad experience.

The repository therefore separates:

```text
configured controls
!= realized ad identity
```

The shared decision policy lives in `references/realized-ad-identity.md`.

## Current Amazon Ads evidence

### Sponsored Products / Sponsored Brands prompts

Amazon Ads' March 10, 2026 launch announcement states that supported U.S. Sponsored Products and Sponsored Brands campaigns can have prompts automatically enabled for existing campaigns, with prompt-level performance reporting. This shows that shopper-visible delivery can change without an ordinary advertiser edit to campaign bid, budget, targeting or structure.

### Sponsored Brands collections

Amazon Ads' May 27, 2026 launch announcement states that Sponsored Brands collections support manual or automatic product selection. Under automatic control, Amazon AI dynamically curates relevant product groupings from the advertiser catalog based on campaign targets and shopping signals. Amazon's public setup guide further describes automatic collections as dynamically selecting products for shoppers, while manual collections use advertiser-selected products.

This establishes a second, materially different case: the same campaign/targeting configuration can produce a changing **realized product mix**.

The feature announcement lists availability across multiple marketplaces and access through Ads Console and Amazon Ads API. These facts are product-specific and time-sensitive; the repository does not generalize them into a universal rule for every ad product or account.

## Generic adaptation

The repository independently derives the following safety framework:

1. keep configured controls separate from realized surface/product/creative identity;
2. treat platform-managed realization shifts as potential causal confounders, not automatic causes;
3. require account/campaign eligibility plus realized delivery evidence before assigning causality;
4. do not equate eligible catalog products with products actually shown;
5. do not convert missing realization dimensions from an active connector into zero/unchanged state;
6. in post-change review, verify realization comparability separately from control readback;
7. downgrade ASIN-specific or single-action causal claims when realized composition is unknown or materially changes.

This extends the earlier delivery-surface rule without replacing it: delivery surface is one realization dimension; product and creative/message composition are additional dimensions.

## Sources

Primary public vendor sources:

- Amazon Ads, “Sponsored Products prompts and Sponsored Brands prompts”, launch announcement dated March 10, 2026; U.S. GA dated March 25, 2026.
- Amazon Ads, “Scale product discovery with AI-powered Sponsored Brands collections”, launch announcement dated May 27, 2026.
- Amazon Ads, “Sponsored Brands collections: Promote related products and reach more shoppers”, public setup guide, retrieved September 2026.

## Copyright / license boundary

Amazon Ads Help, What's New and guide pages are public vendor documentation, not open-source software licensed for redistribution. This repository uses only factual platform behavior and independently rewrites it into a causal/data-governance method. It does not copy Amazon UI, ad creative, report templates, API schemas, proprietary AI selection logic, prompts, screenshots, or substantial source prose.

No third-party source code was adopted in this change, so no new software-license obligations are introduced.

## Rejected adjacent candidates

A GitHub scan also surfaced general Agent Skills/Claude plugin collections. They were not adopted in this round because the repository already implements thin `SKILL.md`, progressive loading, shared references, deterministic policy checks, capability replay and multi-runtime manifests. No candidate reviewed in this pass provided a non-overlapping method with stronger evidence than the Amazon Ads realization-identity gap.

## Safety boundary

The policy changes evidence interpretation only. Live campaign/product/creative mutations remain outside the Skill layer and require an explicitly authorized external Connector / Executor.
