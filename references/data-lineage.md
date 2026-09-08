# Data lineage and comparability

Load this shared reference only when a decision compares, joins, or reconciles metrics from different exports, APIs, MCPs, warehouses, dashboards, caches, or refresh schedules.

The goal is to prevent a source change from being mistaken for a business change.

## 1. Same metric name does not guarantee the same measurement

Two fields both named `orders`, `sales`, `spend`, `ACOS`, or `ROAS` may differ because of:

- attribution window or attribution maturity;
- event-time vs ingestion-time cutoffs;
- timezone/day boundary;
- currency conversion timing;
- aggregation grain;
- filters, entity scope, or status inclusion;
- deduplication/backfill behavior;
- data availability lag;
- semantic/model version;
- partial-day or incomplete partition state.

Do not compare them as one continuous series until these dimensions are compatible or reconciled.

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
- semantic/report version when known;
- completeness/backfill status;
- transformation lineage or upstream source when a derived dataset is used.

Missing lineage is not proof that two sources are equivalent.

## 3. Comparability states

Classify a cross-source comparison as:

- `Comparable` — material definitions, scope, maturity and time boundaries align;
- `Reconcilable` — differences exist but can be calibrated or normalized with evidence;
- `Directional` — useful for broad direction only; exact deltas/causal claims are unsafe;
- `Not Comparable` — source differences can plausibly explain the apparent movement;
- `Unknown` — required lineage is missing.

A recommendation must not be more confident than the comparability state.

## 4. Detect source-lineage drift

Flag lineage drift when the baseline and comparison window do not share a stable measurement path.

Examples:

- baseline uses a direct API report while decline uses a D-2 warehouse table;
- one window is final/backfilled while the other is provisional;
- a connector changes attribution/report definition mid-series;
- historical rows were recomputed under a new semantic version but recent rows were not;
- one source excludes paused/archived entities while another includes them;
- source timezone or currency treatment changes between windows.

Treat a source switch near the apparent break point as a competing cause until reconciled.

## 5. Reconciliation workflow

When a source change is unavoidable:

1. identify the canonical decision metric and required scope;
2. find an overlap window where both sources report the same dates/entities;
3. compare totals and key components, not only ratios;
4. explain systematic lag, filtering, attribution or semantic differences;
5. normalize only when the transformation is explicit and defensible;
6. label unresolved differences and downgrade actionability;
7. prefer one stable source for both baseline and decline windows when possible.

Do not invent a conversion factor from one noisy day.

## 6. Freshness vs event coverage

`extracted_at` is not the same as `available_through`.

A warehouse refreshed today may still contain complete data only through two days ago. Likewise, a current API response may include recent dates whose conversions are not attribution-mature.

Track separately:

- when the dataset was fetched;
- which event dates are complete;
- which conversion dates are mature enough for the decision.

## 7. Derived metrics

Ratios inherit the weakest lineage of their components.

For example:

```text
ROAS = sales / spend
```

If sales and spend come from different source definitions or maturity states, the resulting ROAS should not be treated as clean even when the arithmetic is correct.

Prefer recomputing derived metrics from compatible components rather than mixing precomputed ratios from different systems.

## 8. Source precedence

Do not hard-code a universal rule that API always beats warehouse, or warehouse always beats MCP.

Prefer the source that is:

1. correctly scoped to the requested marketplace/profile/entity;
2. definitionally compatible with the decision;
3. complete for the required dates;
4. attribution-mature enough;
5. auditable and reproducible;
6. stable across the compared windows.

If two trusted sources disagree materially, expose the disagreement rather than silently choosing the more favorable result.

## 9. Action gate

When a material performance break aligns with unresolved lineage drift:

- do not call the break `Confirmed` business deterioration;
- do not generate aggressive bid, budget, negative, pause, or rollback actions from the disputed delta;
- return `Directional`, `Missing Data`, `Hold`, or `Manual Review` as appropriate;
- request a same-source replay or overlap reconciliation.

## 10. Safety boundary

This reference governs evidence quality only. It does not authorize live Amazon Ads writes and does not require any private connector implementation.