# Amazon Ads multi-touch attribution variant

Load this reference only when a decision uses, compares, diagnoses, or reconciles Amazon Ads purchase-conversion metrics where multi-touch attribution (MTA) may coexist with standard last-touch attribution.

## Measurement identity

Amazon Ads multi-touch attribution is a distinct attribution variant. It distributes purchase-conversion credit across multiple Amazon Ads touchpoints according to their estimated contribution, while standard reporting traditionally uses last-touch attribution. Preserve the exact variant in measurement lineage:

```text
attribution_variant = standard_last_touch | multi_touch | other_verified_variant | unknown
```

`Orders (multi-touch)`, `Sales (multi-touch)`, and `ROAS (multi-touch)` are **not interchangeable** with familiar last-touch Orders, Sales, and ROAS merely because they describe the same purchase outcome family.

Do not splice, compare, rank, or diagnose conversion movement across variants until the decision has either selected one compatible variant for both windows or established an evidence-backed reconciliation. A shift in attribution credit is an Observation; it is not by itself proof that shopper conversion propensity changed.

## Availability is scoped

Amazon's public launch material reviewed in September 2026 describes multi-touch metrics for United States advertisers and says they are available alongside last-touch metrics in the ad console, Amazon DSP campaign manager, sponsored-ads downloadable reports, Amazon DSP downloadable custom reports, most report types in Amazon Ads API v3, and Amazon Marketing Stream conversion datasets for Amazon DSP, Sponsored Products, Sponsored Brands, and Sponsored Display.

Treat those statements as scoped capability evidence, not a universal promise for every marketplace, profile, report type, dimension, connector, or row. Before depending on MTA:

- verify marketplace/locale and advertiser eligibility;
- verify the exact report type / Marketing Stream conversion dataset and requested dimensions expose the MTA metric;
- verify the active connector preserves the variant label and does not silently map MTA into a generic Orders/Sales/ROAS field;
- preserve reporting generation, acquisition channel, grain, date-attribution semantics, maturity, scope, and metric definition alongside `attribution_variant`;
- when both variants are present, keep them as separate observations unless an explicit analysis intentionally compares attribution methodologies.

Missing MTA from an active connector or report is a capability/observability gap. It is **not evidence that the multi-touch value is zero**, that last-touch is equivalent, or that the Amazon Ads product lacks MTA globally. Use `connector-capability.md` and `report-coverage.md` when availability or request compatibility is uncertain.

## Decision safety

When an apparent performance break coincides with a change between last-touch and multi-touch fields, variant availability, connector mapping, or report generation:

1. classify the measured delta as an attribution/measurement hypothesis before a business cause;
2. replay both windows under one verified variant when possible;
3. otherwise keep the comparison `Directional`, `Not Comparable`, or `Unknown` according to `data-lineage.md`;
4. do not use the unreconciled delta alone to justify bid cuts, budget reductions, pauses, negatives, scaling, or rollback;
5. keep Observation / Hypothesis / Cause / Action / Outcome separate.

This reference is measurement-only. It does not authorize Amazon Ads writes; execution remains with an explicitly authorized external Connector/Executor.
