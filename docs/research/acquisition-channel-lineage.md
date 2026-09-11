# Acquisition-channel lineage for Amazon Ads evidence

## Why this matters

Amazon Ads exposes reporting through multiple surfaces and delivery paths, including the advertising console, downloadable reports, API-backed workflows, and downstream connectors or warehouses. Availability is not uniform across every report, ad product, marketplace, or integration path.

A decision system therefore needs to distinguish:

```text
metric exists in Amazon Ads
metric exists in a specific report/product surface
metric is exposed by the active API / MCP / connector
metric is preserved unchanged by a downstream warehouse transform
```

These are different claims.

## Reviewed public sources

### Amazon Ads — Search Term Impression Share report for Sponsored Products

Amazon's public help page documents SIS as an account-wide search-term metric and states that the report is accessible through downloadable reports in the reporting center. The current page is updated February 24, 2026 and documents summary/daily units and a 90-day lookback.

Source: https://advertising.amazon.com/help/G7AQQUSFVZPAAXEU

### Amazon Ads — Search term impression share launch announcement for Sponsored Products

The public launch announcement describes the Sponsored Products SIS report as available in the Report Center / advertising console.

Source: https://advertising.amazon.com/resources/whats-new/search-term-impression-report-sponsored-products

### Amazon Ads — Sponsored Brands search term impression rank/share announcement

Amazon's public announcement for the Sponsored Brands search-term impression report explicitly lists both Amazon Ads API and Advertising console as access channels. This is useful evidence that access-channel availability is a report/ad-product property rather than a universal assumption.

Source: https://advertising.amazon.com/resources/whats-new/search-term-rank-report

### Amazon Ads — Reports and metrics by product

Amazon's current reporting documentation lists reporting availability by campaign type and marks some reporting capabilities as API-only, reinforcing that reporting surfaces and acquisition channels differ by report/product.

Source: https://advertising.amazon.com/help/GBYSPTSLR337JMLH

## Generic method adopted

The repository independently adopts the following data-governance rule:

- Track `source_system` separately from `acquisition_channel`.
- Track whether the active channel is verified to expose the decision-relevant metric/dimension.
- Never convert a missing connector field into a metric value of zero.
- Never infer that a feature is absent from Amazon Ads merely because one connector or API path does not expose it.
- When a decision materially depends on a missing field, use a verified alternate source when permitted or downgrade actionability.

For SIS specifically, absence from an active connector must not become a fabricated `0% impression share` or `100% remaining headroom` signal.

## Copyright and license boundary

The Amazon Ads pages above are public vendor documentation, not source code offered under an open-source license for redistribution. This repository does not copy their prose, UI, report templates, examples, or implementation. It records factual platform-access behavior and independently rewrites the resulting data-lineage methodology.

No private Amazon interface, credential flow, customer data, or live mutation path is introduced by this research.
