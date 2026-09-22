# Report coverage, row inclusion and selection effects

Load this shared reference when a decision assumes that rows returned by an Amazon Ads report represent the full underlying entity/query population, or when totals from reports with different inclusion rules are compared.

The goal is to prevent **report selection rules and incomplete extraction** from being mistaken for business behavior.

## 1. Separate generation, extraction and population coverage

A report can be valid according to its own row contract and still be population-incomplete by design. Separately, a successfully generated report can be only partially acquired by a connector/client because pagination stopped early, a response was truncated, a download was incomplete, or a downstream ingestion omitted pages.

Keep these states distinct:

- `generation_status` — whether the upstream report job/artifact completed successfully;
- `pagination_status` — complete, partial, not_applicable, or unknown for the acquisition path;
- `truncation_status` — not_truncated, truncated, suspected, or unknown;
- `row_inclusion_rule` — clicked-only, impression-qualified, delivered-only, active-only, full-enumeration, or unknown;
- `population_coverage` — whether the returned rows can answer the logical population question being asked.

Therefore:

```text
report generation completed successfully
!= extraction completed successfully
!= every logical entity/query appears as a row
```

A partial/truncated extraction is not evidence of zero for omitted members and is not evidence of full population coverage. Do not treat a missing row as zero until both acquisition completeness and the report contract prove that zero-valued members are represented.

## 2. Track row-inclusion and extraction semantics explicitly

When coverage matters, capture when available:

- `report_type` / dataset identity;
- `generation_status`;
- `row_inclusion_rule` — e.g. clicked-only, impression-qualified, delivered-only, active-only, unknown;
- `eligibility_scope` — campaign/ad product/account/profile/marketplace constraints;
- `lookback_limit`;
- requested date range and supported time grain;
- `pagination_status`, including whether every expected page/token/chunk was consumed;
- `truncation_status`, including connector/client row caps or incomplete downloads when known;
- filters and selected dimensions;
- whether zero-activity entities can appear;
- whether report totals are expected to reconcile to a parent/canonical total;
- known metric availability or attribution differences.

If generation succeeded but pagination/truncation is unknown, do not promote that success to extraction completeness. If the inclusion rule is unknown and a conclusion depends on population completeness, downgrade confidence rather than infer completeness.

## 3. Search-term report selection effect

A clicked-only search-term report is useful for query conversion, spend, harvest and negative analysis among **observed clicked queries**. It is not, by itself, a complete census of every query impression opportunity.

Consequences:

- missing search terms cannot be labeled `0 impressions` or `0 clicks` merely because they are absent;
- summed search-term impressions may differ from Campaign Manager / campaign-level impressions because no-click search-term rows are not represented;
- account/query-level CTR denominators cannot be reconstructed from clicked-only rows unless a compatible complete impression denominator is supplied;
- “top/bottom search terms” means top/bottom **within the represented clicked population**, unless another source establishes full query coverage;
- absence from the report is not evidence that a query never served.

This does **not** make the report unusable for negatives or harvesting. It changes what population-level claims are justified.

### Sponsored Products historical-availability boundary

Historical availability is **acquisition-channel and reporting-generation scoped**, not a single Sponsored Products Search Term constant. Current Amazon official evidence reviewed on 2026-09-22 exposes two different boundaries:

- the Sponsored Products Search Term **console/help** surface, updated May 18, 2026, documents a **65-day lookback window** and `summary` / `daily` time units;
- the current Sponsored Ads **Reporting API v3** report-type reference lists `spSearchTerm` with **95-day data retention**, a **31-day maximum request period**, and `SUMMARY` / `DAILY` time units.

These values are not interchangeable. A 31-day maximum request period is not the same concept as 95-day historical retention, and console/help availability must not be silently imposed on Reporting API v3 (or vice versa). Treat both as dated platform-capability evidence, not eternal repository constants. When an exact current limit matters, bind the evidence to `source_system + acquisition_channel + reporting_generation + report_type`, then reconcile it through `platform-capability-lineage.md` against current official/API/account evidence. **Do not silently choose** 65 or 95 merely because one number is more convenient for the requested window.

When the requested Sponsored Products search-term window extends beyond the historical availability verified for the **actual acquisition channel**:

- mark the unsupported portion as `historical-availability = unavailable` or `unknown` according to the evidence; do not fabricate coverage;
- missing older search-term rows are **not zero clicks, zero spend, zero orders, or proof that the term did not exist**;
- bound rankings, harvest/negative conclusions, trend claims, and denominators to the verified available interval;
- if the older interval is decision-critical, request a verified alternate source such as a retained historical export/warehouse snapshot with compatible lineage, or return `Alternate Source`, `Missing Data`, `Hold`, or `Manual Review` rather than silently shortening the requested history;
- do not splice an alternate source into the current report without checking source system, acquisition channel, reporting generation, metric/date-attribution semantics, row eligibility, grain, marketplace/profile identity, freshness and backfill maturity through `data-lineage.md`.

A connector successfully returning the newest interval does not prove it can answer a longer search-term question. Connector capability, acquisition channel, reporting generation and upstream historical availability are separate evidence dimensions.

## 4. Targeting and other delivered-only views

An impression-qualified target report can support performance analysis for targets that actually delivered. It cannot, alone, distinguish among all possible reasons why another configured target is absent, such as:

- zero delivery;
- state/status exclusions;
- date/filter mismatch;
- campaign/ad-product eligibility;
- report contract differences;
- missing or incomplete source extraction.

For configured-but-not-delivering diagnostics, reconcile with a trusted entity/configuration inventory when available rather than inferring configuration state from the performance report alone.

## 5. Reconciliation by purpose

Choose a denominator/source that matches the question.

### Query efficiency among clicked traffic

A clicked-only Search Term report can be appropriate when the decision is explicitly limited to observed clicked search terms.

### Total campaign/account impressions or CTR

Use a compatible campaign/account total or another source whose inclusion contract covers the required population. Do not force clicked-only search-term rows to reproduce the parent impression total.

### Search-term share of voice / impression competition

Use the Search Term Impression Share report or another compatible source when the question specifically depends on impression share/rank. Do not assume ordinary Search Term report coverage is equivalent to SIS coverage.

### Configured target inventory / zero-delivery analysis

Use trusted entity/configuration state plus an eligible performance view. Performance-report row absence alone is insufficient.

## 6. Selection-aware ranking

Population rank claims require population coverage.

If rows are selected by clicks, impressions, delivery, status or another outcome-related condition, state the ranking universe explicitly, for example:

- `highest spend among clicked search terms represented in this report`;
- `lowest CVR among impression-qualified delivered targets`;
- `top opportunity within returned rows; full population rank unavailable`.

Do not silently shorten those labels to `worst search term in the account` or `all non-performing targets`.

## 7. Cross-report comparisons

Before joining or reconciling two reports, compare their:

- report generation status;
- pagination/truncation/acquisition completeness;
- row-inclusion / eligibility rules;
- account/profile/marketplace scope;
- ad-product coverage;
- dimensions/grain;
- attribution and metric semantics;
- lookback/time boundaries.

Two reports generated from the same console or API are not automatically population-equivalent, and two successful report jobs are not automatically equally complete extractions.

When material, route these differences through `data-lineage.md` and classify the comparison as `Comparable / Reconcilable / Directional / Not Comparable / Unknown`.

## 8. Action gate

When an action depends on rows that the report contract may systematically omit, or when extraction completeness is not verified:

- do not manufacture zero rows;
- do not make full-population rankings from a selected or partially acquired subset;
- do not infer no-delivery configuration state from performance-report absence alone;
- do not equate upstream report-job success with complete connector/client acquisition;
- request/reconcile the source or remaining pages needed for the missing population dimension;
- or keep the recommendation explicitly bounded to the represented and verified-acquired rows.

This is especially important for account audits, query coverage claims, CTR/impression diagnostics, pruning decisions and “all waste / all opportunities” language.

## 9. Safety boundary

This reference governs evidence coverage only. It does not authorize Amazon Ads writes. Any eventual mutation remains subject to the repository's `Read-only / Suggest / Shadow / Execute` boundary and an external authorized Connector/Executor.
