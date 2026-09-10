# Account audit framework

Load this only after `amazon-ads-audit/SKILL.md` routes here for a full account review.

The audit should explain the account result, identify the largest evidence-backed risks/opportunities, and preserve data/aggregation safety. It is not a bulk-edit recipe.

## 1. Scope and reliability gate

Resolve before grading performance:

- marketplace and profile/account scope;
- currency and timezone;
- exact current/comparison windows;
- attribution definition and maturity;
- source freshness/completeness;
- promotion/event context;
- retail readiness where conversion is material to the conclusion;
- truncation, pagination state, missing entity levels, or partial coverage.

If multiple source paths or metric versions are involved, load `../../../references/data-lineage.md`.

Do not infer missing rows as zero. A missing entity can mean no delivery, filtering, truncation, unavailable coverage, omitted zero-impression data, or an unfetched page depending on the source.

### Pagination and truncation gate

A page of rows is not automatically a population. When a source exposes `nextToken`, cursor, page number, row limit, total-count metadata, truncation warnings, or equivalent continuation state, preserve that metadata with the extracted slice.

Before calling an entity-level dataset complete for an account audit:

1. exhaust the continuation path, or use a trusted equivalent complete export;
2. record pages/rows fetched and whether a continuation token remains;
3. detect hard row caps or tool/context truncation independently of API pagination;
4. reconcile the completed additive aggregate to the canonical parent/profile total when one exists;
5. explain material residual gaps before population-wide ranking or grading.

A response-level `truncated=false` does not prove population completeness if a non-empty continuation token still exists. Likewise, `100 rows returned` is not evidence that only 100 rows exist.

If coverage is incomplete, local observations about returned rows may still be useful, but label them `Partial / Directional`. Do not claim `top`, `bottom`, concentration share, long-tail coverage, account-wide waste, or whole-population rank unless the relevant population is complete or the ranking guarantee is explicit and trustworthy.

## 2. Canonical totals and aggregation integrity

Choose one canonical additive grain for account totals, preferably a trusted profile/account total or a complete campaign aggregation for the exact same scope/window.

Entity levels such as campaign, keyword/target, search term, placement and advertised product are usually **overlapping decompositions** of the same traffic. Do not sum them together as separate pools of spend, sales or orders.

Reconcile when possible:

```text
trusted profile total
↔ complete campaign aggregate
```

If they disagree materially, investigate before grading the account:

- source/refresh mismatch;
- date or timezone mismatch;
- state/filter inclusion differences;
- incomplete pagination, truncation, or hard row caps;
- partial ad-product coverage;
- attribution/semantic differences.

Do not hide the mismatch by choosing the more favorable number.

## 3. Aggregate base metrics, then derive ratios

Base additive metrics include, when definitions align:

- impressions;
- clicks;
- spend;
- orders;
- sales;
- units.

Recompute ratios from aggregate numerators/denominators:

```text
CTR  = clicks / impressions
CPC  = spend / clicks
CVR  = orders / clicks
ACOS = spend / sales
ROAS = sales / spend
CPA  = spend / orders
```

Do not simple-average row-level ACOS, ROAS, CTR, CVR or CPC to produce an account result. Ratio averages are distorted by different row weights.

## 4. Establish the business result

Start broad:

- spend, attributed sales, orders and units;
- CTR, CPC, CVR, ACOS/ROAS;
- TACOS only when compatible total retail sales exists;
- contribution profit/break-even only when sufficient cost/economic inputs exist.

Use the requested objective: profitability, growth, launch, defense, efficiency, share, or another stated goal. Do not replace it with a universal target.

When a prior comparable period exists, report current, prior, absolute delta and relative delta. Separate data-quality uncertainty from business movement.

## 5. Explain drivers before recommending actions

Trace the result through:

```text
impressions → clicks/CTR → CPC/spend → CVR/orders → AOV/sales → efficiency/profit
```

Rank contributors by material absolute impact on spend, sales/orders, or profit rather than the most extreme percentage on tiny volume.

Useful decompositions include:

- ad product;
- campaign;
- advertised ASIN/product family;
- keyword/target;
- search term;
- placement;
- budget/serving constraint.

A lower-grain view diagnoses the canonical total; it does not create extra account spend.

## 6. Structure and routing audit

Check for:

- campaigns carrying conflicting business intents;
- auto/manual or brand/generic/competitor/category intent that cannot be controlled cleanly;
- query/target routes that cannot be traced;
- duplicate reach or unexplained self-competition;
- excessive fragmentation or long-term no-delivery entities;
- mixed-ASIN scopes that make target-level conclusions unsafe;
- negative/harvest routing whose attachment scope is unclear;
- budget pools or portfolio constraints that make campaigns interdependent.

Route specialized findings to the matching Skill rather than duplicating its full logic here.

## 7. Waste and protection

Waste candidates should be evidence-backed and scoped. Consider:

- sustained spend with weak sales/profit contribution;
- CPC inflation plus weak conversion;
- poor query relevance;
- placement inefficiency;
- budget consumed by routes with weak marginal value.

Do not equate zero orders or high ACOS with an automatic negative/pause. Check attribution maturity, prior-winner history, brand/strategic value, retail readiness, Mixed-ASIN effects and negative attachment scope.

Use `search-term-analysis`, `negative-targeting`, `bid-optimization` or `placement-optimization` for the detailed decision.

## 8. Growth and headroom

Growth candidates require more than good historical ROAS/ACOS. Look for compatible evidence across:

- demand/relevance;
- profitability/objective fit;
- marginal headroom;
- budget/serving constraints;
- inventory and retail readiness;
- promotion/event dependence;
- reversibility and measurement quality.

Route qualified candidates to `growth-opportunity-finder` or `budget-optimization`.

## 9. Retail and economics gate

Before calling a conversion-led issue an ad problem, consider:

- inventory/purchasability;
- Featured Offer / Buy Box;
- price and promotions;
- listing suppression/content changes;
- delivery promise;
- reviews/ratings;
- parent/variation-family changes.

Before calling an efficiency improvement profitable, distinguish attributed revenue metrics from contribution economics.

## 10. Audit prioritization

Prioritize by business impact and action safety:

1. data/scope/retail blockers;
2. material risk or severe waste;
3. budget/serving constraints;
4. high-confidence efficiency opportunities;
5. qualified growth opportunities;
6. longer-term structural improvements.

Include an explicit Hold/Need-more-data set. A useful audit does not force an action for every finding.

## 11. Output contract

A full audit should contain:

1. scope and data confidence, including coverage/pagination status when relevant;
2. executive verdict;
3. canonical account scorecard;
4. driver/contribution analysis;
5. structure/routing findings;
6. retail/economic confounders;
7. prioritized issues/opportunities with evidence and confidence;
8. proposals routed to specialist Skills when appropriate;
9. Hold / Need more data;
10. next review/measurement.

Default mode remains `Suggest`. No live Amazon Ads mutation is performed by this repository.
