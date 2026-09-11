# Data lineage and comparability

Load this shared reference only when a decision compares, joins, or reconciles metrics from different exports, APIs, MCPs, warehouses, dashboards, caches, refresh schedules, metric-definition versions, report row-inclusion rules, reporting generations, date-attribution semantics, acquisition channels, or snapshots with different backfill maturity.

The goal is to prevent a source, measurement-definition, coverage-selection, reporting-generation, date-attribution, acquisition-path, or historical-restatement change from being mistaken for a business change.

If a decision depends on whether returned rows represent the full logical population, load `report-coverage.md` for row-inclusion / eligibility handling.

## 1. Same metric name does not guarantee the same measurement

Two fields both named `orders`, `sales`, `spend`, `ACOS`, or `ROAS` may differ because of:

- attribution window or attribution maturity;
- traffic-date vs conversion-date allocation;
- event-time vs ingestion-time cutoffs;
- timezone/day boundary;
- currency conversion timing;
- aggregation grain;
- filters, entity scope, status inclusion, or report row-inclusion / eligibility rules;
- reporting generation or standardized terminology changes;
- acquisition channel or connector capability differences;
- deduplication/backfill behavior;
- data availability lag or historical-range limits;
- semantic/model version;
- partial-day or incomplete partition state.

Do not compare them as one continuous series until these dimensions are compatible or reconciled.

A useful metric identity is:

```text
metric name
+ metric definition ID
+ semantic/report version or reporting generation
+ attribution definition
+ date-attribution semantics
+ aggregation grain
+ scope/filter contract
+ row-inclusion / eligibility contract
+ acquisition channel when it can alter availability or transformation
```

The table path, dashboard label, standardized metric name, or vendor name alone is not metric identity.

## 2. Minimum source metadata

When lineage matters, capture when available:

- `source_system` — Amazon Ads, warehouse, BI system, connector vendor, etc.;
- `source_dataset` / report identity;
- `acquisition_channel` — advertising-console export, Amazon Ads API, MCP/connector, warehouse import, scheduled delivery, manual export, etc.;
- `channel_capability_status` — verified available, unavailable, unsupported, transformed, or unknown for the decision-relevant metric/dimension;
- `reporting_generation` — legacy Sponsored Ads/DSP report, Unified Reporting, warehouse transform, etc.;
- `extracted_at` or `observed_at`;
- `ingested_at` when a downstream store is involved;
- `available_through` — latest event/report date believed complete;
- marketplace, profile/account scope, currency and timezone;
- attribution window/model or `unknown`;
- `date_attribution_semantics` — traffic date, conversion date, event date, or `unknown` when conversions can move across dates;
- aggregation grain and filters;
- report `row_inclusion_rule` / eligibility contract when returned rows are selected by clicks, impressions, delivery, state or another condition;
- semantic/report version when known;
- per-metric definition/version when a dataset can evolve individual metrics independently;
- completeness/backfill status;
- maximum historical range and metric/dimension-specific availability limits when relevant;
- `backfill_age` or snapshot maturity when historical partitions can restate;
- transformation lineage or upstream source when a derived dataset is used.

Missing lineage is not proof that two sources are equivalent.

### Product availability vs active-channel availability

Keep these questions separate:

```text
Is the metric available in the product/reporting surface?
Is the metric available through the active connector/API/export path?
Does the active path preserve the same semantics and scope?
```

A metric can be available in the product but unavailable through the active connector. Likewise, a warehouse or MCP can expose a transformed field that is not identical to the original reporting field.

Therefore:

- `missing from active connector` ≠ metric value is zero;
- `unsupported by current API path` ≠ feature absent from Amazon Ads;
- `available in the product` ≠ automatically available through the active connector;
- `field present in connector` ≠ semantics verified.

When a decision materially depends on a field that the current acquisition channel cannot provide, classify it as a capability/data-availability gap, use a verified alternate acquisition path when allowed, or downgrade the decision. Do not invent the missing measurement.

## 3. Comparability states

Classify a comparison as:

- `Comparable` — material definitions, scope, coverage, date semantics, acquisition path, maturity and time boundaries align;
- `Reconcilable` — differences exist but can be calibrated or normalized with evidence;
- `Directional` — useful for broad direction only; exact deltas/causal claims are unsafe;
- `Not Comparable` — measurement, reporting-generation, date-allocation, acquisition-path or population-selection differences can plausibly explain the apparent movement;
- `Unknown` — required lineage is missing.

A recommendation must not be more confident than the comparability state. These states apply even when both windows ultimately come from Amazon Ads.

## 4. Detect source-lineage drift

Flag lineage drift when the baseline and comparison window do not share a stable measurement path.

Examples:

- baseline uses a direct API report while decline uses a D-2 warehouse table;
- one window is final/backfilled while the other is provisional;
- a connector changes attribution/report definition mid-series;
- the acquisition path changes from console export to connector/API and the available metric set or transformations change;
- historical rows were recomputed under a new semantic version but recent rows were not;
- one source excludes paused/archived entities while another includes them;
- one report is clicked-only while another includes impression-qualified rows;
- a reporting platform migration changes terminology, date attribution, history limits or dimension behavior;
- source timezone or currency treatment changes between windows.

Treat a source, acquisition-channel, reporting-generation, row-eligibility or date-attribution switch near the apparent break point as a competing cause until reconciled.

## 5. Detect semantic metric-version drift

A stable source path can still contain a discontinuous metric definition.

Flag semantic drift when the same metric name changes materially in any of these ways:

- attribution rule or maturity rule;
- traffic-date vs conversion-date allocation;
- included/excluded entity states;
- order/sales deduplication logic;
- purchased-ASIN or halo inclusion;
- currency or timezone normalization;
- aggregation, filtering, or row-inclusion contract;
- backfill behavior;
- business-semantic transformation;
- calculation formula for a derived metric.

Warning pattern:

```text
same dataset
same column name
semantic_version v2 → v3
historical backfill = false
apparent KPI break occurs at version cutover
```

Do not interpret the break as a confirmed Amazon Ads change until one of the following is available:

1. both windows recomputed under one semantic version;
2. an overlap period computed under both definitions with a defensible bridge;
3. a documented, deterministic transformation proving comparability.

Do not invent a conversion factor from one noisy day or infer semantic equivalence because the source URI or metric label did not change.

## 6. Reporting-generation migrations

Treat a move between reporting generations as a first-class measurement migration, not a cosmetic UI change.

A current Amazon Ads example is the transition from legacy Sponsored Ads / Amazon DSP reports to Unified Reporting. Public Amazon Ads documentation states that Unified Reporting standardizes metric names and terminology and reports conversion metrics on **traffic date**; legacy Amazon DSP and legacy Sponsored Brands workflows could report conversions on **conversion date**. Amazon also documents history limits that vary by time grain, metric and dimension, and plans to decommission the legacy report centers on December 31, 2026.

Generic rules:

- record the reporting generation on every decision-relevant export during a migration period;
- never splice daily/weekly series across a traffic-date / conversion-date boundary as if date buckets had identical meaning;
- matching total mature conversions over a broad window does not prove daily ROAS/CVR patterns are comparable;
- standardized names do not prove standardized historical meaning;
- verify the requested historical range is actually available for the chosen grain, metric and dimensions before replaying a baseline;
- prefer recreating both baseline and comparison under one reporting generation/definition when possible;
- otherwise build an overlap bridge and keep unresolved deltas `Directional`.

Do not use an apparent lift or drop that coincides with an unreconciled reporting migration as the sole basis for aggressive bid, budget, negative, pause, scaling or rollback actions.

## 7. Reconciliation workflow

When a source, acquisition channel, reporting generation or semantic change is unavoidable:

1. identify the canonical decision metric and required population/scope;
2. identify the metric definition/version, acquisition channel, reporting generation, date-attribution semantics and row-inclusion rule used in each window;
3. verify both windows are available and complete at the requested grain;
4. verify the active acquisition path actually exposes the needed metrics/dimensions without undocumented transformation;
5. find an overlap window where both measurement paths report the same dates/entities when possible;
6. compare totals and key components, not only ratios or daily timing shapes;
7. explain systematic lag, filtering, selection, date-allocation, attribution or semantic differences;
8. normalize only when the transformation is explicit and defensible;
9. label unresolved differences and downgrade actionability;
10. prefer one stable source, acquisition path, reporting generation, semantic version and coverage contract for both windows when possible.

For a semantic/reporting cutover, prefer replaying history under the current definition over splicing incompatible pre-cutover and post-cutover values into one trend.

## 8. Freshness vs event coverage

`extracted_at` is not the same as `available_through`.

A warehouse refreshed today may still contain complete data only through two days ago. Likewise, a current API response may include recent dates whose conversions are not attribution-mature.

Track separately:

- when the dataset was fetched;
- which event/traffic dates are complete;
- which conversion outcomes are mature enough for the decision;
- whether the requested historical range exists for the selected grain/dimensions;
- whether the active acquisition channel supports every metric needed for the decision.

Population completeness is separate again: a report can be fresh and complete for its own clicked-only/impression-qualified contract while still not enumerate every logical entity/query. Use `report-coverage.md` when that distinction matters.

## 9. Backfill parity and mutable history

Historical rows may change after their event date because conversions, attribution, refunds, invalid-traffic filtering, deduplication, late-arriving events, or upstream corrections are backfilled.

Therefore:

```text
same source + same semantic version
≠ comparable snapshots
```

when baseline and comparison were captured at materially different backfill maturity.

For post-change reviews and historical comparisons, prefer one of:

1. re-extract both windows at a comparable maturity age;
2. freeze both windows under the same snapshot policy;
3. retain revision metadata and reconcile the amount of historical restatement;
4. use a source-provided finalization/completeness state when it is trustworthy.

Track snapshot capture time, event-window end, backfill age/maturity, mutability, last restatement, revision status, and whether both windows were re-read under the same policy.

Do not call a post-change result `Worked` merely because the later window had more time to accumulate attributed conversions than the frozen baseline.

## 10. Derived metrics

Ratios inherit the weakest lineage of their components, date allocation and denominator coverage.

For example, ROAS should not be treated as clean when sales and spend come from incompatible source definitions, acquisition paths, reporting generations, semantic versions, snapshot maturities, attribution states, date semantics or selected populations.

Prefer recomputing derived metrics from compatible components rather than mixing precomputed ratios from different systems, versions, maturity states, reporting generations, acquisition paths or row-inclusion contracts.

## 11. Source precedence

Do not hard-code a universal rule that API always beats warehouse, console export always beats connector data, legacy reports always beat Unified Reporting, or vice versa.

Prefer the measurement path that is:

1. correctly scoped to the requested marketplace/profile/entity and population;
2. definitionally compatible with the decision;
3. available through a verified acquisition channel for the required metrics/dimensions;
4. explicit about reporting generation and date-attribution semantics;
5. complete for the required dates and explicit about row eligibility/history limits;
6. attribution-mature enough;
7. auditable and reproducible;
8. stable across the compared windows;
9. explicit about metric semantic version when definitions can change;
10. comparable in historical-restatement/backfill maturity when snapshots are mutable.

If two trusted paths disagree materially, expose the disagreement rather than silently choosing the more favorable result.

## 12. Action gate

When a material performance break or post-change lift aligns with unresolved source-lineage, acquisition-channel, reporting-generation, date-attribution, row-eligibility, semantic-version or asymmetric-backfill drift:

- do not call the movement `Confirmed` business deterioration or `Worked` optimization outcome;
- do not generate aggressive bid, budget, negative, pause, scaling or rollback actions from the disputed delta;
- return `Directional`, `Missing Data`, `Hold` or `Manual Review` as appropriate;
- request a verified acquisition path, same-source/same-generation/same-version/same-coverage replay, compatible population denominator, matched-maturity snapshot, or overlap reconciliation.

## 13. Safety boundary

This reference governs evidence quality only. It does not authorize live Amazon Ads writes and does not require any private connector implementation.
