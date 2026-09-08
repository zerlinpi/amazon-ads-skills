---
name: growth-opportunity-finder
description: Find and prioritize commercially actionable Amazon Ads growth opportunities across ASINs, campaigns, search terms, targets, placements and budgets. Use when the user asks where to scale, where more spend could profitably grow sales, which winners deserve investment, or what growth opportunities exist beyond fixing waste.
---

# Amazon Ads Growth Opportunity Finder

Use this Skill to answer **where growth is worth pursuing**, not merely where metrics look good.

Default mode: `Suggest`. Use `Shadow` for scenario modeling when useful. This Skill never performs live Amazon Ads mutations by itself.

## Progressive loading

Start here. Read `references/opportunity-evaluation.md` only when ranking or sizing concrete opportunities. Load shared repository references only when they affect the decision:

- `../../references/benchmark-policy.md` for external comparisons;
- `../../references/decision-boundaries.md` for action permissions;
- `../../references/amazon-ads-metrics.md` for metric definitions;
- `../performance-drop-diagnosis/references/causal-drop-diagnosis.md` only when a growth candidate is entangled with a recent decline.

## Required decision context

Gather what is available and explicitly mark missing inputs:

- marketplace, currency, timezone and date window;
- business objective: profit, revenue, rank/launch, defense, market share, clearance, or balanced growth;
- ASIN/product scope and ad types;
- spend, sales, orders, impressions, clicks, CPC, CTR, CVR, ACoS/ROAS;
- total sales/TACoS when available;
- margin or target economics when available;
- inventory/days of supply, Featured Offer/Buy Box, price, promotion and listing state;
- campaign budget usage, serving constraints and placement/search-term/target evidence;
- advertised-ASIN and purchased-ASIN scope where mixed-ASIN or halo effects matter.

Do not invent missing economics, inventory, rank or total-sales data.

## Workflow

1. **Define growth objective.** Distinguish profitable scale, launch/rank investment, defense, market-share growth and clearance. The same ACoS can mean different things under different objectives.
2. **Map available evidence.** Record report grain, date windows, attribution maturity and missing fields before ranking opportunities.
3. **Find proven demand.** Identify entities with repeatable conversion evidence, business relevance and enough data to distinguish signal from noise.
4. **Find headroom.** Look for constrained winners, under-covered high-quality queries/targets, efficient placements, profitable ASINs with insufficient support, or traffic routes that can be expanded without merely moving spend internally.
5. **Run retail-readiness gates.** Inventory, Featured Offer/Buy Box, price, reviews, listing quality, delivery promise, suppression and conversion problems can block otherwise attractive scale.
6. **Check incrementality and cannibalization risk.** Separate branded defense, own-ASIN traffic, generic discovery, competitor conquesting and sibling-ASIN halo where the data allows it.
7. **Classify the opportunity.** Use one of the opportunity types below.
8. **Rank and size.** Use the opportunity reference to compare expected impact, evidence quality, headroom, readiness, risk, reversibility and confidence. Do not rank by low ACoS alone.
9. **Produce controlled next actions.** Prefer small, measurable, reversible steps with explicit validation and rollback conditions.

## Opportunity types

- `scale-proven-winner` — validated campaign/target/search term/placement with business headroom;
- `budget-release` — profitable demand appears constrained by campaign/portfolio budget;
- `query-harvest` — validated search term deserves cleaner Exact or dedicated routing;
- `target-expansion` — productive keyword/product/category target suggests adjacent expansion;
- `placement-opportunity` — a placement has credible incremental headroom;
- `asin-investment` — a retail-ready ASIN deserves more paid support;
- `listing-before-spend` — demand exists but conversion/retail readiness should be fixed before scale;
- `defense-or-protection` — proven demand/rank/brand position should be protected rather than aggressively expanded;
- `experiment` — promising but uncertain opportunity should be tested instead of treated as proven;
- `hold` — evidence or readiness is insufficient for additional spend.

## Safety gates

Do not present a scale action as `Action-safe` when any material blocker remains unresolved:

- insufficient or attribution-immature evidence;
- structural loss against known economics without an explicit strategic exception;
- inventory or Featured Offer/Buy Box risk;
- listing/price/review issue that plausibly suppresses conversion;
- mixed-ASIN or purchased-ASIN ambiguity that could move spend away from another profitable product;
- branded cannibalization or defense traffic mistaken for incremental acquisition;
- promotion/seasonality creating a temporary winner;
- budget increase with no evidence of demand headroom.

Classify recommendations as `Action-safe`, `Directional`, or `Blocked`.

## Output

Return:

1. **Growth objective and evidence coverage** — exact scope, windows and missing inputs.
2. **Opportunity map** — where growth appears possible and where it is blocked.
3. **Ranked opportunities** — entity, opportunity type, evidence, headroom, economics/readiness, risk, confidence and actionability.
4. **Controlled action plan** — proposed action, expected mechanism, validation metric/window and rollback condition.
5. **Do-not-scale list** — attractive-looking entities that fail economics, incrementality, readiness or evidence gates.
6. **Next evidence to collect** — what would upgrade `Directional` opportunities into `Action-safe` decisions.

Do not use fixed universal click/order/ACoS thresholds. Prefer account-specific economics, comparable historical baselines and explicit uncertainty.