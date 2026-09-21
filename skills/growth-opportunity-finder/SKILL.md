---
name: growth-opportunity-finder
description: Find and prioritize commercially actionable Amazon Ads growth opportunities across ASINs, campaigns, search terms, targets, placements and budgets. Use when the user asks where to scale, where more spend could profitably grow sales, which winners deserve investment, or what growth opportunities exist beyond fixing waste.
---

# Amazon Ads Growth Opportunity Finder

Use this Skill to answer **where growth is worth pursuing**, not merely where metrics look good.

Default mode: `Suggest`. Use `Shadow` for scenario modeling when useful. This Skill never performs live Amazon Ads mutations by itself.

## Connector capability gate

When a conclusion depends on live MCP/API/connector data, load `../../references/connector-capability.md` before interpreting missing or empty fields. If a machine-readable capability snapshot is available, identify the exact required capability IDs and run `../../scripts/evaluate_connector_capability_gate.py` **before metric interpretation**.

- `Pass` — continue with the Skill's normal evidence, sufficiency, lineage and safety checks.
- `Degraded` — do not make a high-confidence dependent recommendation; keep the result to `Directional`, `Hold`, `Alternate Source`, `Missing Data`, or `Manual Review`.
- `Blocked` — do not treat the dependent observation as action-safe until the capability is resolved or an allowed alternate source is verified.
- `missing_evidence_policy = never_zero` — `Partial`, `Unsupported`, `Unknown`, or absent connector capability is never a numeric zero, unchanged state, or proof that the platform lacks the feature.

This gate is read-only and does not authorize live Amazon Ads mutation.

## Campaign objective gate

Load `../../references/campaign-objective.md` before qualifying campaign-level growth or interpreting efficiency as success/failure. Use the shared bounded roles `Discovery`, `Control`, `Growth`, `Profit`, `Defense`, `Experiment`, and `Unknown` rather than inventing a local objective taxonomy.

- Preserve the declared `primary_metric` and `guardrail_metrics`; do not silently replace them with ACOS/ROAS because those metrics are available.
- `Growth` may make marginal headroom and incremental volume central, but it still requires economics and retail-readiness guardrails.
- `Profit` requires positive marginal economics before scale; historical average profitability is not enough.
- `Discovery` may tolerate bounded learning cost, but exploratory spend is not proof of scalable demand.
- `Defense` must distinguish strategic coverage from incremental acquisition and expose opportunity cost/cannibalization.
- `Experiment` must preserve treatment integrity and the declared experiment metric before recommending expansion.
- `Control` should not be scaled merely because it looks efficient; first determine what stable role it is intended to hold.
- `Unknown` is a real state. Do not infer campaign objective from name, ACOS/TACOS, match type, spend pattern, organic rank movement, or a short performance window. Keep objective-dependent recommendations `Directional` or `Hold` until intent is verified.

Campaign objective changes how evidence is interpreted; it never bypasses connector, retail, economic, incrementality, attribution, or binding-control gates.

## Progressive loading

Start here. Read `references/opportunity-evaluation.md` only when ranking or sizing concrete opportunities. Load shared repository references only when they affect the decision:

- `../../references/campaign-objective.md` for campaign mission and success/guardrail semantics;
- `../../references/benchmark-policy.md` for external comparisons;
- `../../references/decision-boundaries.md` for action permissions;
- `../../references/amazon-ads-metrics.md` for metric definitions;
- `../../references/search-term-impression-share.md` when query headroom, share-of-voice, SIS or Impression Rank affects a growth decision;
- `../performance-drop-diagnosis/references/causal-drop-diagnosis.md` only when a growth candidate is entangled with a recent decline.

## Required decision context

Gather what is available and explicitly mark missing inputs:

- marketplace, currency, timezone and date window;
- campaign objective/role from the shared objective contract, including source, confidence, `primary_metric` and `guardrail_metrics` when available;
- ASIN/product scope and ad types;
- spend, sales, orders, impressions, clicks, CPC, CTR, CVR, ACoS/ROAS;
- total sales/TACoS when available;
- margin or target economics when available;
- inventory/days of supply, Featured Offer/Buy Box, price, promotion and listing state;
- campaign budget usage, serving constraints and placement/search-term/target evidence;
- Search Term Impression Share / Impression Rank and its window/scope when share headroom matters;
- advertised-ASIN and purchased-ASIN scope where mixed-ASIN or halo effects matter.

Do not invent missing economics, inventory, rank, total-sales data, or campaign objective.

## Workflow

1. **Resolve campaign objective.** Load the shared objective contract, preserve explicit intent and success/guardrail metrics, and retain `Unknown` when intent is not verified.
2. **Map available evidence.** Record report grain, date windows, attribution maturity and missing fields before ranking opportunities.
3. **Find proven demand.** Identify entities with repeatable conversion evidence, business relevance and enough data to distinguish signal from noise.
4. **Find headroom.** Look for constrained winners, under-covered high-quality queries/targets, efficient placements, profitable ASINs with insufficient support, or traffic routes that can be expanded without merely moving spend internally. SIS may strengthen a query-level visibility-headroom hypothesis, but low SIS alone is not growth proof.
5. **Run retail-readiness gates.** Inventory, Featured Offer/Buy Box, price, reviews, listing quality, delivery promise, suppression and conversion problems can block otherwise attractive scale.
6. **Check incrementality and cannibalization risk.** Separate branded defense, own-ASIN traffic, generic discovery, competitor conquesting and sibling-ASIN halo where the data allows it.
7. **Resolve the binding control.** Before choosing bid, budget, placement or routing, determine whether that control plausibly limits the opportunity. Do not map low SIS mechanically to a bid or budget increase.
8. **Classify the opportunity.** Use one of the opportunity types below.
9. **Rank and size.** Use the opportunity reference to compare expected impact, evidence quality, headroom, readiness, risk, reversibility and confidence. Do not rank by low ACoS or low SIS alone.
10. **Produce controlled next actions.** Prefer small, measurable, reversible steps with explicit validation and rollback conditions.

## Opportunity types

- `scale-proven-winner` — validated campaign/target/search term/placement with business headroom;
- `budget-release` — profitable demand appears constrained by campaign/portfolio budget;
- `query-harvest` — validated search term deserves cleaner Exact or dedicated routing;
- `share-headroom-candidate` — high-value query has compatible SIS evidence suggesting additional paid-impression share may be available, with the actual binding control still resolved separately;
- `share-defense` — strategically important query has a meaningful share/rank deterioration worth monitoring or testing;
- `target-expansion` — productive keyword/product/category target suggests adjacent expansion;
- `placement-opportunity` — a placement has credible incremental headroom;
- `asin-investment` — a retail-ready ASIN deserves more paid support;
- `listing-before-spend` — demand exists but conversion/retail readiness should be fixed before scale;
- `defense-or-protection` — proven demand/rank/brand position should be protected rather than aggressively expanded;
- `experiment` — promising but uncertain opportunity should be tested instead of treated as proven;
- `hold` — evidence or readiness is insufficient for additional spend.

## Safety gates

Do not present a scale action as `Action-safe` when any material blocker remains unresolved:

- campaign objective is `Unknown` and the recommendation depends on the intended campaign trade-off;
- insufficient or attribution-immature evidence;
- structural loss against known economics without an explicit strategic exception;
- inventory or Featured Offer/Buy Box risk;
- listing/price/review issue that plausibly suppresses conversion;
- mixed-ASIN or purchased-ASIN ambiguity that could move spend away from another profitable product;
- branded cannibalization or defense traffic mistaken for incremental acquisition;
- promotion/seasonality creating a temporary winner;
- budget increase with no evidence of demand headroom;
- low SIS without compatible economics, routing, budget/headroom and retail evidence;
- SIS joined to a performance report with unresolved scope/window/report-contract mismatch.

Classify recommendations as `Action-safe`, `Directional`, or `Blocked`.

## Output

Return:

1. **Campaign objective and evidence coverage** — exact role/intent, objective source/confidence, primary/guardrail metrics, scope, windows and missing inputs.
2. **Opportunity map** — where growth appears possible and where it is blocked.
3. **Ranked opportunities** — entity, opportunity type, evidence, headroom, economics/readiness, risk, confidence and actionability.
4. **Controlled action plan** — proposed action, expected mechanism, validation metric/window and rollback condition.
5. **Do-not-scale list** — attractive-looking entities that fail objective, economics, incrementality, readiness or evidence gates.
6. **Next evidence to collect** — what would upgrade `Directional` opportunities into `Action-safe` decisions.

Do not use fixed universal click/order/ACoS thresholds. Prefer account-specific economics, comparable historical baselines, declared campaign objective and explicit uncertainty.
