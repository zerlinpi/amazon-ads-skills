# Amazon Ads report row-eligibility and coverage research

Reviewed: 2026-09-10

This note records public Amazon Ads reporting behavior used to harden repository coverage logic. It does not copy Amazon documentation prose and does not import private APIs, account data, UI assets, or proprietary implementation details.

## Public sources reviewed

### Sponsored Products Search Term report

Amazon Ads help page, updated May 18, 2026:

- https://advertising.amazon.com/help/G3HEFZYWZF84NPS9

Relevant factual behavior independently summarized for this repository:

- the report is useful for customer search-term performance, harvesting and negative-targeting analysis;
- returned search-term rows are subject to a click-based inclusion rule: search terms represented in the report generated at least one ad click;
- because no-click search-term rows are not represented, summed report impressions need not match Campaign Manager impressions;
- absence from this report is therefore not proof of zero impressions or no serving.

Repository adaptation: treat `row_inclusion_rule` / eligibility as measurement metadata, bound search-term conclusions to the represented clicked population, and require another compatible source for full query-impression or zero-click-query claims.

### Sponsored Products Targeting report

Amazon Ads help page, updated February 24, 2026:

- https://advertising.amazon.com/help/GPDYPV4AAYCAJFKP

Relevant factual behavior independently summarized:

- targeting performance reporting is scoped to targets in campaigns that received at least one impression.

Repository adaptation: performance-report absence alone is insufficient proof that a configured target does not exist, is paused, or had an explicit zero state. For configured inventory / zero-delivery diagnostics, reconcile against trusted entity/configuration state.

### Downloadable reports in sponsored ads

Amazon Ads help page, updated August 19, 2026:

- https://advertising.amazon.com/help/GBYSPTSLR337JMLH

Relevant factual behavior independently summarized:

- downloadable report availability and row semantics vary by report type and ad product;
- report/campaign-manager metrics may change as invalid traffic is removed;
- account time zone is material to report interpretation.

Repository adaptation: report type, eligibility, time window/grain, source freshness and row-inclusion semantics belong in evidence lineage rather than being assumed from a generic `Amazon Ads report` label.

### Search Term Impression Share report

Amazon Ads help page, updated February 24, 2026:

- https://advertising.amazon.com/help/G7AQQUSFVZPAAXEU

Relevant factual behavior independently summarized:

- SIS reports account-wide impression share and rank for represented search terms and have their own report/time-window contract.

Repository adaptation: ordinary Search Term report coverage must not be silently treated as equivalent to Search Term Impression Share coverage. Use the report whose population and metric contract matches the decision question.

### Unified reporting

Amazon Ads launch announcement, June 8, 2026:

- https://advertising.amazon.com/resources/whats-new/streamline-campaign-analysis-with-unified-reporting

Relevant factual behavior independently summarized:

- unified reporting can combine multiple advertiser/manager accounts, countries, ad products, metrics and dimensions.

Repository adaptation: a unified interface does not eliminate the need to preserve scope, dimension, row-eligibility and metric-definition metadata. Cross-account/ad-product consolidation should remain explicit in lineage and aggregation logic.

## Adoption method and copyright boundary

Amazon Ads help/announcement pages are public vendor documentation, not source code licensed for wholesale reuse by this repository. This repository therefore adopts only factual platform/reporting behaviors needed for safe analysis, then independently rewrites the methodology as:

- `references/report-coverage.md`;
- coverage-aware routing in `skills/search-term-analysis/SKILL.md`;
- row-inclusion identity in `references/data-lineage.md`;
- synthetic regression coverage in `evals/fixtures/search-term-clicked-only-coverage-bias.json`.

No substantial Amazon prose, screenshots, UI copy, API contracts, or private implementation are copied.

## Why this is high value

Without this distinction, an agent can make several materially wrong decisions while using a technically successful report:

1. infer nonexistent zero rows from absent search terms;
2. calculate population CTR from a selected denominator;
3. call a clicked-only subset the entire account query population;
4. misdiagnose parent/report impression mismatch as corruption;
5. prune or rank entities using an incomplete selection universe.

The corrective rule is generic and connector-neutral:

```text
successful report completion
!= complete logical population
```

Population-sensitive decisions require the report's row-inclusion / eligibility contract or an explicit downgrade in actionability.
