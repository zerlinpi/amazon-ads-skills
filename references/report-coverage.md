# Report coverage, row inclusion and selection effects

Load this shared reference when a decision assumes that rows returned by an Amazon Ads report represent the full underlying entity/query population, or when totals from reports with different inclusion rules are compared.

The goal is to prevent **report selection rules** from being mistaken for business behavior.

## 1. A valid report can still be population-incomplete by design

A report may be complete according to its own contract while intentionally omitting rows that do not satisfy an eligibility condition.

Examples from current Amazon Ads public documentation include:

- Sponsored Products Search Term reports include only search terms that generated at least one ad click for the requested period;
- Sponsored Products Targeting reports cover targets in campaigns that received at least one impression;
- other report types may have their own campaign/ad-product/account eligibility, lookback, grain, status or metric-availability contracts.

Therefore:

```text
report generation completed successfully
!= every logical entity/query appears as a row
```

Do not treat a missing row as zero until the report contract proves that zero-valued members are represented.

## 2. Track row-inclusion semantics explicitly

When coverage matters, capture when available:

- `report_type` / dataset identity;
- `row_inclusion_rule` — e.g. clicked-only, impression-qualified, delivered-only, active-only, unknown;
- `eligibility_scope` — campaign/ad product/account/profile/marketplace constraints;
- `lookback_limit`;
- requested date range and supported time grain;
- pagination/completion state;
- filters and selected dimensions;
- whether zero-activity entities can appear;
- whether report totals are expected to reconcile to a parent/canonical total;
- known metric availability or attribution differences.

If the inclusion rule is unknown and a conclusion depends on population completeness, downgrade confidence rather than infer completeness.

## 3. Search-term report selection effect

A clicked-only search-term report is useful for query conversion, spend, harvest and negative analysis among **observed clicked queries**. It is not, by itself, a complete census of every query impression opportunity.

Consequences:

- missing search terms cannot be labeled `0 impressions` or `0 clicks` merely because they are absent;
- summed search-term impressions may differ from Campaign Manager / campaign-level impressions because no-click search-term rows are not represented;
- account/query-level CTR denominators cannot be reconstructed from clicked-only rows unless a compatible complete impression denominator is supplied;
- “top/bottom search terms” means top/bottom **within the represented clicked population**, unless another source establishes full query coverage;
- absence from the report is not evidence that a query never served.

This does **not** make the report unusable for negatives or harvesting. It changes what population-level claims are justified.

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

- row-inclusion / eligibility rules;
- account/profile/marketplace scope;
- ad-product coverage;
- dimensions/grain;
- attribution and metric semantics;
- lookback/time boundaries;
- pagination/completeness state.

Two reports generated from the same console or API are not automatically population-equivalent.

When material, route these differences through `data-lineage.md` and classify the comparison as `Comparable / Reconcilable / Directional / Not Comparable / Unknown`.

## 8. Action gate

When an action depends on rows that the report contract may systematically omit:

- do not manufacture zero rows;
- do not make full-population rankings from a selected subset;
- do not infer no-delivery configuration state from performance-report absence alone;
- request/reconcile the source needed for the missing population dimension;
- or keep the recommendation explicitly bounded to the represented rows.

This is especially important for account audits, query coverage claims, CTR/impression diagnostics, pruning decisions and “all waste / all opportunities” language.

## 9. Safety boundary

This reference governs evidence coverage only. It does not authorize Amazon Ads writes. Any eventual mutation remains subject to the repository's `Read-only / Suggest / Shadow / Execute` boundary and an external authorized Connector/Executor.
