# Amazon Store view-attribution methodology cutover

## Why this matters

Amazon Ads introduced a shopping-signal enhanced last-touch attribution model for eligible Amazon Store ad inventory on January 1, 2026. Amazon states that Purchases, Sales and ROAS under the new methodology became the standard reporting metrics for affected view-attributed inventory, while separate `all views` conversion metrics remain available for eligible campaigns using all ad views within a 14-day window.

That creates a measurement-lineage risk even when the analyst stays inside Amazon Ads and the displayed metric family still says Purchases, Sales or ROAS. A pre-cutover or all-views baseline can be materially different from a post-cutover standard metric series without any change in campaign controls or underlying shopper demand.

## Primary source reviewed

Amazon Ads, **View Attribution Updates for Amazon Store ads**, published January 1, 2026:

- https://advertising.amazon.com/resources/whats-new/view-attribution-updates-for-amazon-store-ads

Facts used from the public announcement:

- effective date: January 1, 2026;
- the new standard is described as a shopping-signal enhanced last-touch attribution model;
- the update can affect Sponsored Brands, Sponsored Display campaigns billed on a viewable-impression basis, including branded keyword campaigns, and Amazon DSP campaigns serving ads in the Store;
- Purchases, Sales and ROAS using the new methodology become standard reporting for the affected scope;
- eligible campaigns can still access separate `all views` conversion metrics covering all ad views within a 14-day window through Unified Reporting interfaces/APIs;
- Amazon states that click-based attribution is unchanged by this specific update;
- other campaign/inventory types outside the documented scope should not be assumed to have changed.

## Clean-room adaptation

Amazon's page is public vendor documentation, not an open-source implementation license. This repository does **not** copy Amazon prose, UI, screenshots, API field definitions, report templates, attribution algorithms, weighting logic, or proprietary implementation details.

Only factual platform behavior is used to derive an independently written Amazon Ads decision-safety rule:

```text
same source system
+ same campaign
+ same conversion metric family
+ different attribution variant/methodology
≠ automatically comparable performance series
```

The repository therefore records `attribution_variant` as part of metric identity and requires reconciliation before aggressive bid, negative, pause, scaling or rollback actions when an apparent break aligns with an attribution-methodology cutover.

## Why this is separate from Unified Reporting migration

The existing Unified Reporting migration policy handles reporting-generation and traffic-date versus conversion-date semantics. This January 2026 change is different: multiple conversion attribution variants can coexist inside the same modern reporting environment.

A reporting system can simultaneously expose:

- standard/default conversion metrics under one methodology; and
- `all views` conversion metrics under another window/definition.

Therefore `reporting_generation` alone is insufficient measurement identity.

## Safety implications adopted

1. Preserve attribution model/window/variant when multiple variants coexist.
2. Do not splice standard/default and `all views` Purchases, Sales or ROAS as one continuous trend.
3. Do not substitute one variant for another to fill missing history without labeling the semantic break.
4. Treat a methodology cutover coincident with a performance break as a competing measurement cause.
5. Use compatible click-side evidence only as supporting context when the platform explicitly documents click-based attribution as unchanged; it is not proof that conversion economics were unchanged.
6. Apply the documented change only to eligible campaign/inventory scope.
7. If a Connector strips variant identity or cannot expose the required variant, keep the comparison `Unknown / Directional / Hold` rather than guessing.

## Repository changes linked to this research

- `references/data-lineage.md` — adds `attribution_variant` to measurement identity and documents coexistence/reconciliation rules.
- `skills/performance-drop-diagnosis/SKILL.md` — adds attribution-methodology cutovers to the reliability and causal gates.
- `evals/fixtures/amazon-store-attribution-variant-cutover.json` — regression case that blocks false ROAS-drop diagnosis from mixed attribution variants.

## License/adoption boundary

No third-party code or schema was adopted for this change. The implementation is repository-authored policy and synthetic eval data based only on the factual behavior documented by Amazon Ads.
