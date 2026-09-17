# Amazon Ads Unified Reporting migration research

Reviewed September 17, 2026.

## Public sources

Amazon Ads public documentation reviewed:

- `Understand unified reporting` — updated August 12, 2026.
- `Data availability in unified reporting` — updated August 17, 2026.
- `Migrate your sponsored ads and Amazon DSP reports` — updated September 1, 2026.
- `Streamline campaign analysis with unified reporting, now generally available` — published June 8, 2026.

These are vendor documentation pages, not source code licensed for redistribution. This repository adopts only factual platform behavior and independently written measurement-safety rules. No Amazon prose, UI assets, report templates, API implementation, or proprietary examples are copied.

## High-value facts retained

Amazon Ads states that Unified Reporting:

- standardizes metric names, definitions and entity terminology across ad products;
- reports conversion metrics on **traffic date** (the date of the ad interaction);
- differs from legacy Amazon DSP and legacy Sponsored Brands reporting that could place conversions on **conversion date**;
- exposes historical data with maximum ranges that vary by time grain and can be shorter for specific dimensions/metrics;
- is replacing the legacy Sponsored Ads and Amazon DSP report centers, which Amazon currently plans to shut down on December 31, 2026;
- will permanently delete remaining saved reports, scheduled reports and historical data from the legacy report-center pages at that shutdown, so post-cutover inability to retrieve legacy history is an availability/lineage state rather than evidence that the historical metric value was zero or that no historical activity occurred.

Amazon's September 1 migration guidance also says net-new report creation and editing on the legacy pages is planned to stop on December 17, 2026 while existing reports remain read-only until shutdown. These dates are vendor migration dates and may change; agents should verify current Amazon documentation when a decision depends on the exact cutoff.

## Independent adaptation

The repository treats reporting-generation migration as a measurement-lineage boundary:

```text
same metric label
+ different reporting generation/date attribution
≠ automatically comparable daily series
```

A safe longitudinal review should preserve reporting generation and date-attribution semantics, verify history availability, and prefer replaying both windows under one compatible definition. When only mixed generations are available, use an overlap bridge and downgrade unresolved conclusions rather than attributing the discontinuity to advertising performance.

A legacy-history retrieval failure after a documented retirement/deletion boundary must be classified as `historical availability unavailable/unknown` (or an equivalent explicit state), not coerced to zero. If a required baseline was not migrated or independently preserved, the correct action is to use a verified alternate source, shorten/reframe the comparison, or downgrade confidence; do not fabricate continuity across a permanently unavailable source.

This adaptation remains connector-neutral and does not require private Amazon Ads interfaces or authorize live mutations.
