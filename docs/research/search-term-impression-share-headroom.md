# Search Term Impression Share headroom research

Reviewed: 2026-09-19

## Primary public sources

### Amazon Ads — Search Term Impression Share (SIS) report for Sponsored Products

Amazon Ads Help page, updated February 24, 2026, plus Amazon's public Sponsored Products launch documentation.

Sources:

- https://advertising.amazon.com/help/G7AQQUSFVZPAAXEU
- https://advertising.amazon.com/resources/whats-new/search-term-impression-report-sponsored-products

Facts retained for methodology design:

- the report exposes search-term impression share and numeric impression rank relative to other advertisers;
- Amazon describes the measure at account level for the search term;
- Amazon recommends using it to observe the impact of bidding, targeting, and budget changes on share of impressions;
- the current help page documents summary/daily time units and a 90-day lookback for this report.

### Amazon Ads — Top-of-search impression share

Amazon Ads launch documentation dated September 22, 2021.

Source: https://advertising.amazon.com/resources/whats-new/top-of-search-impression-share-metric

Amazon defines top-of-search impression share as the percentage of top-of-search impressions a campaign received out of the total top-of-search impressions it was eligible to serve on. This is a different metric and scope from account-wide Search Term Impression Share.

**Semantic safety rule:** do not transfer the top-of-search metric's `eligible` denominator wording into Search Term Impression Share unless current Amazon documentation for the exact SIS surface explicitly establishes the same denominator. Similar metric labels are not evidence of identical measurement semantics.

### Amazon Ads — Search term report for Sponsored Products

Amazon Ads Help page, updated May 18, 2026.

Source: https://advertising.amazon.com/help/G3HEFZYWZF84NPS9

Used only to preserve the already-established distinction between a clicked-only Search Term performance report and other search-term reporting populations.

## Independent adaptation

This repository does not reproduce Amazon help-page prose, UI, report templates, or implementation details. Public vendor documentation is used only to establish factual platform/reporting behavior, then the decision method is independently written for this repository.

The adopted generic method is:

1. treat SIS as market-visibility/share evidence rather than conversion or incrementality proof;
2. preserve its account-level scope when considering campaign/target-level controls;
3. preserve exact metric identity and denominator semantics instead of treating every `impression share` field as interchangeable;
4. verify report window, ad product, search-term identity and population contract before joining SIS to performance data;
5. require economics, retail readiness, routing and actual binding-control evidence before turning low share into a growth action;
6. never infer guaranteed incremental clicks/sales/profit or a fixed bid/budget change from low SIS alone;
7. use Shadow/Experiment/Hold when the account-wide share signal cannot yet be mapped to a causal campaign/target control.

## License / copyright handling

Amazon Ads Help and What's New pages are public vendor documentation, not source code offered under this repository's MIT license. No substantial Amazon prose or proprietary implementation is copied. Only factual reporting behavior and independently rewritten analytical principles are retained.
