# Data lineage and comparability

Load this shared reference only when a decision compares, joins, or reconciles metrics from different exports, APIs, MCPs, warehouses, dashboards, caches, refresh schedules, metric-definition versions, report row-inclusion rules, reporting generations, date-attribution semantics, attribution variants, acquisition channels, or snapshots with different backfill maturity.

The goal is to prevent a source, measurement-definition, coverage-selection, reporting-generation, attribution-methodology, date-attribution, acquisition-path, historical-availability, or historical-restatement change from being mistaken for a business change.

If a decision depends on whether returned rows represent the full logical population, load `report-coverage.md` for row-inclusion / eligibility handling.

If a decision depends on whether the active MCP/connector can expose the required profile, report, metric, dimension, history, pagination, freshness, or semantic identity at all, load `connector-capability.md` first. When available, preserve a machine-readable observation using `../schemas/connector-capability-snapshot.json`. Connector `Unsupported`, `Partial`, or `Unknown` states are acquisition-path evidence gaps, not metric zeros or proof that the Amazon Ads product lacks the feature.

## 1. Same metric name does not guarantee the same measurement

Two fields both named `orders`, `sales`, `spend`, `ACOS`, or `ROAS` may differ because of:

- attribution window, model, variant, or attribution maturity;
- traffic-date vs conversion-date allocation;
- event-time vs ingestion-time cutoffs;
- timezone/day boundary;
- currency conversion timing;
- aggregation grain;
- filters, entity scope, status inclusion, or report row-inclusion / eligibility rules;
- reporting generation or standardized terminology changes;
- acquisition channel or connector capability differences;
- deduplication/backfill behavior;
- data availability lag, historical-range limits, or retired/deleted source history;
- semantic/model version;
- partial-day or incomplete partition state.

Do not compare them as one continuous series until these dimensions are compatible or reconciled.

A useful metric identity is:

```text
metric name
+ metric definition ID
+ semantic/report version or reporting generation
+ attribution definition
+ attribution_variant
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
- `attribution_variant` — standard/default, all-views, click-based, view-based, custom, or `unknown` when multiple variants can coexist;
- `date_attribution_semantics` — traffic date, conversion date, event date, or `unknown` when conversions can move across dates;
- aggregation grain and filters;
- report `row_inclusion_rule` / eligibility contract when returned rows are selected by clicks, impressions, delivery, state or another condition;
- semantic/report version when known;
- per-metric definition/version when a dataset can evolve individual metrics independently;
- completeness/backfill status;
- maximum historical range and metric/dimension-specific availability limits when relevant;
- `historical_availability_status` — available, partially available, retired/deleted, unsupported, or unknown when the requested baseline can disappear independently of metric value;
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

### Retired or deleted historical reporting surfaces

A source can stop exposing history because the reporting generation, saved report, schedule, UI surface, retention window, or underlying historical store has been retired or deleted. That is a historical availability state, not a metric observation.

Therefore:

```text
legacy source no longer returns historical rows
≠ historical metric value is zero
≠ historical entity had no delivery
```

When a documented retirement/deletion boundary can explain the missing baseline:

- set `historical_availability_status` to `retired/deleted` (or the nearest explicit connector-neutral equivalent), not `available` with zero values;
- do not backfill missing legacy history with zeros, empty aggregates, or a different reporting generation without proving semantic comparability;
- prefer a verified preserved export/warehouse snapshot or replay both windows under one compatible current generation when history exists there;
- if no compatible baseline remains, shorten or reframe the comparison and downgrade the conclusion to `Unknown`, `Directional`, `Missing Data`, or `Hold` as appropriate;
- when an exact retirement date matters, verify current vendor documentation because migration dates can change.

This rule is intentionally generic. A current Amazon Ads migration is documented in `docs/research/unified-reporting-migration.md`.

## 3. Comparability states

Classify a comparison as:

- `Comparable` — material definitions, attribution variant, scope, coverage, date semantics, acquisition path, maturity and time boundaries align;
- `Reconcilable` — differences exist but can be calibrated or normalized with evidence;
- `Directional` — useful for broad direction only; exact deltas/causal claims are unsafe;
- `Not Comparable` — measurement, attribution-methodology, reporting-generation, date-allocation, acquisition-path or population-selection differences can plausibly explain the apparent movement;
- `Unknown` — required lineage is missing.

A recommendation must not be more confident than the comparability state. These states apply even when both windows ultimately come from Amazon Ads.

### Machine comparison of measurement composition

When both windows expose the bounded `measurement_composition` envelope from the optimization evidence contract, use `../scripts/compare_measurement_composition.py` for a deterministic first-pass comparison. The helper is intentionally narrower than full metric comparability and returns:

- `Comparable` — every decision-relevant composition field is explicitly known and equal;
- `Directional` — direct/modeled split observability or lower-grain allocation coverage / `Unallocated` state changed;
- `Not Comparable` — modeled-conversion inclusion semantics or allocation grain changed;
- `Unknown` — either envelope is absent, a required field is missing/null/invalid, or a required string state is explicitly unknown/unavailable.

Missing evidence never becomes `false`, zero, complete allocation, direct-only measurement, or unchanged composition. The comparator does not decide whether a parent-level aggregate outside the affected allocation ambiguity can still be used; that remains a decision-specific reconciliation question. It also does not replace source/version/backfill, control-state, realization, retail or counterfactual checks.

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
- a reporting platform migration changes terminology, attribution methodology, date attribution, history limits or dimension behavior;
- a legacy reporting surface is retired/deleted so the requested baseline is no longer retrievable;
- source timezone or currency treatment changes between windows.

Treat a source, acquisition-channel, reporting-generation, attribution-variant, row-eligibility, historical-availability or date-attribution switch near the apparent break point as a competing cause until reconciled.

## 5. Detect semantic metric-version drift

A stable source path can still contain a discontinuous metric definition.

Flag semantic drift when the same metric name changes materially in any of these ways:

- attribution rule, variant or maturity rule;
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

### Attribution variants can coexist inside one reporting system

Do not assume that one reporting generation has only one conversion definition.

A current Amazon Ads example is the January 1, 2026 Amazon Store ads view-attribution update. Amazon introduced a **shopping-signal enhanced last-touch** attribution model for eligible view-attributed Sponsored Brands, viewable-impression Sponsored Display, and Amazon DSP Store inventory. Purchases, Sales, and ROAS under that methodology became the standard reported conversion metrics. Amazon simultaneously kept separate `all views` conversion metrics for eligible campaigns using all ad views within a 14-day window through Unified Reporting interfaces and APIs. Amazon states that click-based attribution was unchanged by this specific update.

This creates a first-class `attribution_variant` boundary even when source system, reporting generation, campaign ID and displayed metric family otherwise look compatible.

Therefore:

```text
same conversion metric family
+ standard/default attribution variant
≠ automatically comparable to
same conversion metric family
+ all views attribution variant
```

Rules:

- preserve the exact attribution variant for Purchases, Sales, ROAS and derived conversion metrics when more than one variant is available;
- do not splice pre-cutover values produced under a prior default methodology with post-cutover standard values unless the historical series has been recomputed under one compatible definition;
- do not substitute `Purchases (all views)` for standard `Purchases`, or vice versa, simply to avoid a gap;
- an apparent conversion/ROAS drop coincident with an attribution-methodology cutover is a measurement-lineage hypothesis before it is an advertising-performance diagnosis;
- when the specific platform change affects view attribution but click-based attribution is documented as unchanged, use compatible click-side metrics as supporting evidence where useful, while still respecting their own scope and maturity;
- campaign types/inventory outside the documented eligibility scope must not be assumed to have undergone the same methodology change;
- if a connector strips the variant label or cannot expose both variants, mark `attribution_variant = unknown` and downgrade comparison confidence rather than guessing.

This is not a universal claim that `all views` is more or less correct than the standard variant. The safe choice depends on the decision question; the requirement is to avoid silently mixing definitions.

## 6. Reporting-generation migrations

Treat a move between reporting generations as a first-class measurement migration, not a cosmetic UI change.

A current Amazon Ads example is the transition from legacy Sponsored Ads / Amazon DSP reports to Unified Reporting. Public Amazon Ads documentation states that Unified Reporting standardizes metric names and terminology and reports conversion metrics on **traffic date**; legacy Amazon DSP and legacy Sponsored Brands workflows could report conversions on **conversion date**. Amazon also documents history limits that vary by time grain, metric and dimension, and plans to decommission the legacy report centers on December 31, 2026. Migration guidance reviewed September 17, 2026 additionally says remaining saved/scheduled legacy reports and historical data on those legacy pages will be permanently deleted at shutdown.

Generic rules:

- record the reporting generation on every decision-relevant export during a migration period;
- never splice daily/weekly series across a traffic-date / conversion-date boundary as if date buckets had identical meaning;
- matching total mature conversions over a broad window does not prove daily ROAS/CVR patterns are comparable;
- standardized names do not prove standardized historical meaning;
- verify the requested historical range is actually available for the chosen grain, metric and dimensions before replaying a baseline;
- distinguish `history was zero` from `history is no longer available because the source was retired/deleted`;
- preserve decision-critical legacy baselines before a documented retirement when allowed by the user's data-governance policy, but do not require or implement private connector storage here;
- prefer recreating both baseline and comparison under one reporting generation/definition when possible;
- otherwise build an overlap bridge and keep unresolved deltas `Directional`.

Do not use an apparent lift or drop that coincides with an unreconciled reporting migration as the sole basis for aggressive bid, budget, negative, pause, scaling or rollback actions.

## 7. Reconciliation workflow

When a source, acquisition channel, reporting generation, attribution variant or semantic change is unavoidable:

1. identify the canonical decision metric and required population/scope;
2. identify the metric definition/version, attribution variant, acquisition channel, reporting generation, date-attribution semantics and row-inclusion rule used in each window;
3. verify both windows are available and complete at the requested grain, including whether either source crossed a retention/retirement boundary;
4. verify the active acquisition path actually exposes the needed metrics/dimensions without undocumented transformation;
5. find an overlap window where both measurement paths report the same dates/entities when possible;
6. compare totals and key components, not only ratios or daily timing shapes;
7. explain systematic lag, filtering, selection, date-allocation, attribution or semantic differences;
8. normalize only when the transformation is explicit and defensible;
9. label unresolved differences and downgrade actionability;
10. prefer one stable source, acquisition path, reporting generation, attribution variant, semantic version and coverage contract for both windows when possible.

For a semantic/reporting cutover, prefer replaying history under the current definition over splicing incompatible pre-cutover and post-cutover values into one trend. If the old source has been retired and no compatible replay or preserved baseline exists, do not synthesize one from zero-filled history.

## 8. Freshness vs event coverage

`extracted_at` is not the same as `available_through`.

A warehouse refreshed today may still contain complete data only through two days ago. Likewise, a current API response may include recent dates whose conversions are not attribution-mature.

Track separately:

- when the dataset was fetched;
- which event/traffic dates are complete;
- which conversion outcomes are mature enough for the decision;
- whether the requested historical range exists for the selected grain/dimensions;
- whether the historical source still exists or has crossed a retention/retirement boundary;
- whether the active acquisition channel supports every metric and attribution variant needed for the decision.

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

Ratios inherit the weakest lineage of their components, attribution variant, date allocation and denominator coverage.

For example, ROAS should not be treated as clean when sales and spend come from incompatible source definitions, attribution variants, acquisition paths, reporting generations, semantic versions, snapshot maturities, attribution states, date semantics or selected populations.

Prefer recomputing derived metrics from compatible components rather than mixing precomputed ratios from different systems, variants, versions, maturity states, reporting generations, acquisition paths or row-inclusion contracts.

## 11. Source precedence

Do not hard-code a universal rule that API always beats warehouse, console export always beats connector data, legacy reports always beat Unified Reporting, or standard attribution always beats `all views`.

Prefer the measurement path that is:

1. correctly scoped to the requested marketplace/profile/entity and population;
2. definitionally compatible with the decision;
3. explicit about attribution variant/model/window when alternatives coexist;
4. available through a verified acquisition channel for the required metrics/dimensions;
5. explicit about reporting generation and date-attribution semantics;
6. complete for the required dates and explicit about row eligibility/history limits/retirement state;
7. attribution-mature enough;
8. auditable and reproducible;
9. stable across the compared windows;
10. explicit about metric semantic version when definitions can change;
11. comparable in historical-restatement/backfill maturity when snapshots are mutable.

If two trusted paths disagree materially, expose the disagreement rather than silently choosing the more favorable result.

## 12. Action gate

When a material performance break or post-change lift aligns with unresolved source-lineage, attribution-variant, acquisition-channel, reporting-generation, date-attribution, row-eligibility, historical-availability, semantic-version or asymmetric-backfill drift:

- do not call the movement `Confirmed` business deterioration or `Worked` optimization outcome;
- do not generate aggressive bid, budget, negative, pause, scaling or rollback actions from the disputed delta;
- return `Directional`, `Missing Data`, `Hold` or `Manual Review` as appropriate;
- request a verified acquisition path, same-source/same-generation/same-attribution-variant/same-version/same-coverage replay, compatible population denominator, preserved compatible baseline, matched-maturity snapshot, or overlap reconciliation.

## 13. Safety boundary

This reference governs evidence quality only. It does not authorize live Amazon Ads writes and does not require any private connector implementation.
