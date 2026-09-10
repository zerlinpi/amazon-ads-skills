# Data lineage and comparability

Load this shared reference only when a decision compares, joins, or reconciles metrics from different exports, APIs, MCPs, warehouses, dashboards, caches, refresh schedules, metric-definition versions, report row-inclusion rules, or snapshots with different backfill maturity.

The goal is to prevent a source, measurement-definition, coverage-selection, or historical-restatement change from being mistaken for a business change.

If a decision depends on whether returned rows represent the full logical population, load `report-coverage.md` for row-inclusion / eligibility handling.

## 1. Same metric name does not guarantee the same measurement

Two fields both named `orders`, `sales`, `spend`, `ACOS`, or `ROAS` may differ because of:

- attribution window or attribution maturity;
- event-time vs ingestion-time cutoffs;
- timezone/day boundary;
- currency conversion timing;
- aggregation grain;
- filters, entity scope, status inclusion, or report row-inclusion / eligibility rules;
- deduplication/backfill behavior;
- data availability lag;
- semantic/model version;
- partial-day or incomplete partition state.

Do not compare them as one continuous series until these dimensions are compatible or reconciled.

A useful metric identity is:

```text
metric name
+ metric definition ID
+ semantic/report version
+ attribution definition
+ aggregation grain
+ scope/filter contract
+ row-inclusion / eligibility contract
```

The table path or dashboard label alone is not metric identity.

## 2. Minimum source metadata

When lineage matters, capture when available:

- `source_system` — Amazon Ads API, MCP, CSV, warehouse, BI export, connector, etc.;
- `source_dataset` / report identity;
- `extracted_at` or `observed_at`;
- `ingested_at` when a downstream store is involved;
- `available_through` — latest event/report date believed complete;
- marketplace, profile/account scope, currency and timezone;
- attribution window/model or `unknown`;
- aggregation grain and filters;
- report `row_inclusion_rule` / eligibility contract when returned rows are selected by clicks, impressions, delivery, state or another condition;
- semantic/report version when known;
- per-metric definition/version when a dataset can evolve individual metrics independently;
- completeness/backfill status;
- `backfill_age` or snapshot maturity when historical partitions can restate;
- transformation lineage or upstream source when a derived dataset is used.

Missing lineage is not proof that two sources are equivalent.

## 3. Comparability states

Classify a comparison as:

- `Comparable` — material definitions, scope, coverage, maturity and time boundaries align;
- `Reconcilable` — differences exist but can be calibrated or normalized with evidence;
- `Directional` — useful for broad direction only; exact deltas/causal claims are unsafe;
- `Not Comparable` — measurement or population-selection differences can plausibly explain the apparent movement;
- `Unknown` — required lineage is missing.

A recommendation must not be more confident than the comparability state.

These states apply even when both windows come from the **same** source system or table.

## 4. Detect source-lineage drift

Flag lineage drift when the baseline and comparison window do not share a stable measurement path.

Examples:

- baseline uses a direct API report while decline uses a D-2 warehouse table;
- one window is final/backfilled while the other is provisional;
- a connector changes attribution/report definition mid-series;
- historical rows were recomputed under a new semantic version but recent rows were not;
- one source excludes paused/archived entities while another includes them;
- one report is clicked-only while another includes impression-qualified rows;
- source timezone or currency treatment changes between windows.

Treat a source or row-eligibility switch near the apparent break point as a competing cause until reconciled.

## 5. Detect semantic metric-version drift

A stable source path can still contain a discontinuous metric definition.

Flag semantic drift when the same metric name changes materially in any of these ways:

- attribution rule or maturity rule;
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

Do not invent a conversion factor from one noisy day or infer semantic equivalence because the source URI did not change.

## 6. Reconciliation workflow

When a source or semantic change is unavoidable:

1. identify the canonical decision metric and required population/scope;
2. identify the metric definition/version and row-inclusion rule used in each window;
3. find an overlap window where both measurement paths report the same dates/entities when possible;
4. compare totals and key components, not only ratios;
5. explain systematic lag, filtering, selection, attribution or semantic differences;
6. normalize only when the transformation is explicit and defensible;
7. label unresolved differences and downgrade actionability;
8. prefer one stable source, one stable semantic version and one stable coverage contract for both windows when possible.

For a semantic-version cutover, prefer replaying history under the current definition over splicing pre-cutover and post-cutover values into one trend.

## 7. Freshness vs event coverage

`extracted_at` is not the same as `available_through`.

A warehouse refreshed today may still contain complete data only through two days ago. Likewise, a current API response may include recent dates whose conversions are not attribution-mature.

Track separately:

- when the dataset was fetched;
- which event dates are complete;
- which conversion dates are mature enough for the decision.

Population completeness is separate again: a report can be fresh and complete for its own clicked-only/impression-qualified contract while still not enumerate every logical entity/query. Use `report-coverage.md` when that distinction matters.

## 8. Backfill parity and mutable history

Historical rows may change after their event date because conversions, attribution, refunds, deduplication, late-arriving events, or upstream corrections are backfilled.

Therefore:

```text
same source + same semantic version
≠ comparable snapshots
```

when baseline and comparison were captured at materially different backfill maturity.

Common failure pattern:

```text
baseline window frozen at D+1
post window read at D+7
source and metric version are identical
late conversions continue to backfill
apparent post-change lift
```

The apparent lift may be a snapshot-maturity artifact rather than an optimization effect.

For post-change reviews and historical comparisons, prefer one of:

1. re-extract both windows at a comparable maturity age;
2. freeze both windows under the same snapshot policy;
3. retain revision metadata and reconcile the amount of historical restatement;
4. use a source-provided finalization/completeness state when it is trustworthy.

Track when useful:

- snapshot capture timestamp;
- event-window end date;
- backfill age or maturity label;
- whether historical partitions are mutable;
- last restatement timestamp;
- revision/backfill status;
- whether both windows were re-read under the same policy.

Do not call a post-change result `Worked` merely because the later window had more time to accumulate attributed conversions than the frozen baseline.

## 9. Derived metrics

Ratios inherit the weakest lineage of their components and denominator coverage.

For example:

```text
ROAS = sales / spend
```

If sales and spend come from different source definitions, semantic versions, snapshot maturities, attribution states, or incompatible selected populations, the resulting ROAS should not be treated as clean even when the arithmetic is correct.

Prefer recomputing derived metrics from compatible components rather than mixing precomputed ratios from different systems, versions, maturity states, or row-inclusion contracts.

## 10. Source precedence

Do not hard-code a universal rule that API always beats warehouse, or warehouse always beats MCP.

Prefer the measurement path that is:

1. correctly scoped to the requested marketplace/profile/entity and population;
2. definitionally compatible with the decision;
3. complete for the required dates and explicit about row eligibility;
4. attribution-mature enough;
5. auditable and reproducible;
6. stable across the compared windows;
7. explicit about metric semantic version when definitions can change;
8. comparable in historical-restatement/backfill maturity when snapshots are mutable.

If two trusted paths disagree materially, expose the disagreement rather than silently choosing the more favorable result.

## 11. Action gate

When a material performance break or post-change lift aligns with unresolved source-lineage, row-eligibility, semantic-version, or asymmetric-backfill drift:

- do not call the movement `Confirmed` business deterioration or `Worked` optimization outcome;
- do not generate aggressive bid, budget, negative, pause, scaling, or rollback actions from the disputed delta;
- return `Directional`, `Missing Data`, `Hold`, or `Manual Review` as appropriate;
- request a same-source/same-version/same-coverage replay, compatible population denominator, matched-maturity snapshot, or overlap reconciliation.

## 12. Safety boundary

This reference governs evidence quality only. It does not authorize live Amazon Ads writes and does not require any private connector implementation.
