---
name: experiment-planner
description: Design guarded Amazon Ads experiments when an optimization hypothesis is promising but not yet action-safe. Use for bid, budget, placement, targeting, search-term, campaign-structure, launch, retail-readiness or growth tests that need a clear hypothesis, comparable baseline/control, primary metric, guardrails, validation window and stop/rollback criteria before external execution.
---

# Amazon Ads Experiment Planner

Use this Skill when evidence is insufficient for a confident direct optimization but strong enough to justify a controlled test.

Default mode: `Shadow` for design/simulation, otherwise `Suggest`. This Skill never executes live Amazon Ads mutations.

## Explicit material-change re-verification chronology (v1.95.0)

For a Ready holdout, `boundary_monitoring.material_scope_changes[].reverified` must still be positively true. When an optional `reverified_at` is explicitly supplied, it must be a known-offset RFC3339 instant at or after the material change and at or before `latest_verified_at`, compared in UTC with exact fractional precision. Do not silently treat null/Unknown or contradictory time as omitted evidence. Omitted legacy timestamps, valid equal/offset times and Shadow/Hold/Redesign remain compatible. This is internal consistency, not source authentication or continuous rule-history proof; no live Ads writes.

## Exact fractional-second Ready holdout chronology (v1.94.0)

When a Ready holdout supplies known-offset RFC3339 verification timestamps, compare UTC instants at their **full supplied fractional precision**, including seven or more digits. Python `datetime.fromisoformat` truncates past microseconds; a later isolation verification, launch verification or material scope change cannot be hidden by that truncation. Preserve valid high-precision timestamps, offsets, omitted optional legacy evidence and exploratory statuses. Validate with `../../scripts/validate_experiment_plan.py`. This is internal consistency, not continuous-control proof, source authentication or live Ads write permission.

## Ready holdout latest verification chronology (v1.93.0)

If a Ready holdout supplies `comparison.boundary_monitoring`, its `latest_verified_at` cannot predate a valid, positively verified `comparison.isolation_evidence[].verified_at`. Compare UTC instants across offsets and fractional seconds; preserve optional legacy omissions, unverified items and exploratory states. This checks internal chronology, not external Ads source authenticity or complete control history. Validate with `../../scripts/validate_experiment_plan.py`.

## Ready combined metric identity whitespace normalization (v1.92.0)

Before marking a combined readout `Ready`, reject whole-label `Not Applicable` even when its words are separated by repeated spaces, tabs, newlines or nonbreaking spaces. The validator normalizes real whitespace, hyphens and underscores for this exact placeholder only; a concrete metric label containing those words is not automatically unresolved. Apply to primary and guardrail metrics, preserve non-combined and exploratory compatibility, and never infer a missing measurement is zero. This is a repository-owned read-only identity check, not Amazon-native reporting authentication or write authority.

## Ready holdout verification timestamps (v1.91.0)

Ready holdouts require known-offset RFC3339 verification instants (T separator, optional fractional seconds, Z or ±HH:MM) for supplied boundary latest/launch verification, material-change timestamps and verified isolation timestamps. Reject -00:00, space separators and second-resolution timezone offsets. Preserve valid offset chronology, optional legacy omissions and exploratory plans. This is internal evidence consistency, not external authentication, continuous-control proof or live Ads write permission. Validate with ../../scripts/validate_experiment_plan.py before Ready classification.

## Ready combined-readout metric identity (v1.89.0)

Before marking a combined readout `Ready`, confirm the primary metric and every decision-driving guardrail have concrete, unpadded metric names. Whole-label `Unknown`, `Partial`, `Missing`, `Unsupported`, `Unavailable`, `Not Available`, `Not Supported`, `Not Applicable`, `N/A`, blank or non-string names cannot be promoted to resolved identities by an `additive` or `ratio_or_derived` declaration. Concrete names containing these words as substrings are not placeholders. Non-combined Ready and exploratory plans retain their prior compatibility. Use `../../scripts/validate_experiment_plan.py` for the deterministic readiness gate. This does not prove reporting provenance, compatible base components, row disjointness, attribution, experiment isolation or permission to mutate Amazon Ads.

## Official benchmark derived-rate readout safety (v1.90.0)

For a `Ready` combined readout, Amazon Ads benchmark Purchase rate, Add to cart rate, Detail page view rate, Branded search rate, Cost per purchase, Cost per detail page view, and Percent of purchases new to brand are derived measures. Do not declare them `additive` or `non_additive_deduplicated`. The standalone sum gate also blocks their direct summation when the name is supplied. `ratio_or_derived` is necessary for these named metrics but not sufficient: require trustworthy, compatible source numerators, denominators, attribution, currency, date, grain, and overlap evidence before any actual recomputation. Keep missing/unknown distinct from zero; no live Amazon Ads mutation.

## Connector capability gate

When a conclusion depends on live MCP/API/connector data, load `../../references/connector-capability.md` before interpreting missing or empty fields. If a machine-readable capability snapshot is available, identify the exact required capability IDs and run `../../scripts/evaluate_connector_capability_gate.py` **before metric interpretation**.

- `Pass` — continue with the Skill's normal evidence, sufficiency, lineage and safety checks.
- `Degraded` — do not make a high-confidence dependent recommendation; keep the result to `Directional`, `Hold`, `Alternate Source`, `Missing Data`, or `Manual Review`.
- `Blocked` — do not treat the dependent observation as action-safe until the capability is resolved or an allowed alternate source is verified.
- `missing_evidence_policy = never_zero` — `Partial`, `Unsupported`, `Unknown`, or absent connector capability is never a numeric zero, unchanged state, or proof that the platform lacks the feature.

This gate is read-only and does not authorize live Amazon Ads mutation.

## Core workflow

1. State the decision the experiment is meant to resolve.
2. Write one falsifiable hypothesis with an expected mechanism.
3. Define treatment scope and the cleanest feasible comparison: holdout/control, matched historical baseline, phased rollout, or switchback.
4. Choose one primary success metric and a small set of diagnostic/guardrail metrics.
5. Check sample sufficiency, attribution maturity, seasonality, promotions, stock, price, Buy Box / Featured Offer, mixed-ASIN and concurrent-change risk.
6. Check whether treatment/control can interfere through shared queries, ASIN demand, budgets, routing, placements, auctions, automation, or platform-managed realization.
7. If an AI-managed campaign uses an audience signal or another optimization signal, verify whether it is a hard eligibility/exclusion control or merely a model input before treating it as a cohort/holdout boundary.
8. For long-running tests, re-verify control boundaries after material keyword/target/negative, audience-signal, automation, migration, budget-pool, variation-family or retail-scope changes; launch-time cleanliness is not permanent proof.
9. Estimate the minimum decision-useful effect or practical business threshold when the economics support it; do not invent statistical precision from missing inputs.
10. Define pre-test state, test window, observation window, stop conditions and rollback triggers before any mutation.
11. Output a machine-readable experiment plan when needed using `../../schemas/experiment-plan.json`. A `Ready` conversion primary metric or decision-driving conversion guardrail must carry explicit `metric_semantics.metric_family`, `metric_semantics.attribution_family`, and `metric_semantics.semantic_version`. When `comparison.requires_combined_readout = true`, the primary metric and every decision-driving guardrail must also carry explicit `metric_semantics.aggregation_semantics`; canonical ratio KPIs (ROAS, ACOS, TACOS, CVR, CTR, CPC, CPA, CPM, vCPM, ROI) in a `Ready` combined readout require `ratio_or_derived`, not `additive` or `non_additive_deduplicated`, for both primary and guardrail metrics; TACOS is distinct from ad-attributed ACOS. This is a narrow consistency check, not proof of compatible source components. If a combined readout would directly sum rows, use `../../scripts/evaluate_metric_aggregation_gate.py`, pass the known metric display name as optional `metric_name` to catch contradictory additive ratio labels, and do not infer `unknown` as additive. An explicitly supplied null/placeholder/non-string `metric_name` in the standalone gate is unresolved and cannot authorize direct summation; omitted legacy names remain compatible. `non_additive_deduplicated` metrics require a source-provided aggregate for the intended scope, while `ratio_or_derived` metrics should be recomputed from compatible base components when defined; unresolved measurement identity belongs in `Shadow Only`, `Redesign`, or `Hold`. A plan marked `Ready` must resolve collision-safe scope: marketplace, profile/account scope, entity type and non-empty entity IDs. Whole-label unavailable placeholders or whitespace-padded identities are not concrete scope; duplicate treatment entity IDs, and any explicitly supplied duplicate/placeholder control IDs or treatment/control ID overlap, must fail readiness. Opaque IDs containing placeholder words as substrings remain valid, and control IDs are not mandatory when a separate verified holdout mechanism exists. A `Ready` holdout must also set `comparison.control_integrity = Clean` and carry at least one verified `comparison.isolation_evidence` item. A positive `verified` flag is insufficient when the evidence text is a whole-label unavailable placeholder or padded; explicitly supplied optional `source` and `verified_at` must be concrete and timezone-aware. Do not invent provenance or timestamps to reach Ready. Valid isolation mechanisms are platform randomization, a verified hard control, a verified routing partition, or a verified delivery partition; `optimization_signal` is not an isolation mechanism. If a `Ready` holdout supplies `comparison.boundary_monitoring`, require explicit `current_status = Clean` and a valid timezone-aware `latest_verified_at` even when no material changes are listed; an optional `launch_verified_at` must be valid and no later than `latest_verified_at`. A supplied incomplete monitoring record is not positive boundary evidence. Explicit `boundary_monitoring: null` or another non-object is unresolved, not equivalent to omission; explicitly supplied `launch_verified_at: null` or non-array `material_scope_changes` likewise fails `Ready`. An omitted monitoring record or omitted optional fields remain compatible. When material scope changes occur, record the latest trustworthy check in `comparison.boundary_monitoring.latest_verified_at` and the changes in `comparison.boundary_monitoring.material_scope_changes`; a boundary verification older than a material change is stale and cannot support `Ready`. Each recorded material scope change must also explicitly carry boolean `reverified: true`; missing, null, false, numeric or string values are unresolved even when the latest check is later. When repository scripts are available, validate these readiness gates with `../../scripts/validate_experiment_plan.py`; unresolved identity or boundary evidence belongs in `Shadow Only`, `Redesign`, or `Hold` rather than fabricated scope/evidence.
12. After an externally applied test, route outcome evaluation to `post-change-review` rather than judging success inside this planner.

## Progressive loading

- Detailed design, control selection, windows and general contamination: `references/experiment-design.md`
- Shared query/ASIN/budget/auction/control leakage, interference, or long-test boundary drift: `references/interference-and-leakage.md`
- AI-managed surface/product/creative realization or optimization-signal semantics: `../../references/realized-ad-identity.md`

Load only the reference required by the experiment. Ordinary short, low-overlap tests should not load the interference or realization references.

## Experiment validity gates

For a `Ready` plan, `comparison.requires_combined_readout` is optional for legacy compatibility, but if explicitly supplied it must be a JSON boolean. Null/Unknown/Partial/non-boolean evidence is unresolved, not equivalent to a verified `false`; keep the plan in `Shadow Only`, `Redesign`, or `Hold` until the need for a combined readout is established. A true flag still activates the existing ratio/derived metric guard for primary and guardrail KPIs. This is not independent authentication of source, date, grain, attribution, or denominator completeness.

Do not conflate non-ad retail metrics with ad-attributed conversions: exact `Total Retail Sales`, `Retail Sales`, `Organic Sales`, and `Sales Rank` may use their own retail/rank semantic family; unrelated `Wholesale Traffic` must not trigger conversion checks because it contains "sale". This is a bounded name guard, not an automatic retail data-quality pass. Bare `Sales`/`Total Sales` remain ambiguous and fail closed as conversions unless fully identified; `Ad-Attributed Sales` and `Purchases` still require attribution identity. Explicit `metric_family=conversion` always requires a concrete attribution family and version. Preserve source, metric, date, grain, marketplace and profile identity before any causal claim.

For `Ready` conversion metrics, the declared `metric_family` cannot override an obvious conversion name (Purchases, Sales, ROAS, ACOS, CVR, attributed orders/units, units sold) to bypass attribution checks. Match ACOS/CVR as whole metric tokens, not as substrings of TACOS or unrelated names; TACOS uses total retail sales and must not be silently treated as attributed ACOS. Require `metric_family = conversion`, a concrete `attribution_family`, and a concrete `semantic_version` for the primary metric and conversion guardrails. Whole-label Unknown/Partial/Missing/Unsupported/Not Applicable values are unresolved even when non-empty; non-conversion and Shadow/Hold designs retain their distinct semantics. These checks do not independently authenticate Amazon reporting.

Do not call an experiment decision-ready when any material issue remains unresolved:

- marketplace/profile scope or the actual experiment entity identity is unresolved for a plan that would otherwise be marked `Ready`;
- a proposed `Ready` holdout lacks `control_integrity = Clean` or lacks verified `isolation_evidence` for the actual treatment/control boundary;
- the hypothesis changes multiple independent controls without a way to separate effects;
- baseline and treatment periods differ materially in promotion, stock, price, listing state or attribution maturity;
- treatment and control share traffic or resources in a way that causes substantial leakage, displacement, or interference;
- the proposed cohort boundary relies on an audience signal / `optimization_signal` whose product semantics do not prove hard targeting or exclusion and no separate verified isolation boundary exists;
- a material scope-changing event occurred after `boundary_monitoring.latest_verified_at`, or any `boundary_monitoring.material_scope_changes` item lacks explicit boolean `reverified: true` (including missing/null/non-boolean evidence);
- realized treatment/control allocation materially departs from the declared design without an explanation;
- the test entity is mixed-ASIN and the proposed conclusion requires ASIN-level attribution that is not reliable;
- a `Ready` conversion primary metric or conversion guardrail lacks explicit metric family, attribution family, or semantic version;
- a `Ready` plan that requires a combined readout lacks explicit aggregation semantics for the primary metric or a decision-driving guardrail, or treats unknown/non-additive/derived semantics as permission for direct summation;
- the primary metric can improve while profitability or a critical guardrail deteriorates;
- sample size or traffic is too small to distinguish a useful business effect;
- another recent optimization on the same entity is still inside its validation window.

When blocked, return `Shadow Only`, `Redesign`, or `Hold` instead of forcing a test.

## Status semantics

- `Ready` — the experiment is decision-ready for **external execution review**, with collision-safe entity scope resolved and, for holdouts, a clean evidence-backed and sufficiently fresh isolation boundary. It is not permission to mutate Amazon Ads.
- `Shadow Only` — the design is useful for simulation/replay, but one or more action-safety, identity, or boundary prerequisites are not resolved.
- `Redesign` — the current comparison/treatment structure cannot answer the declared question credibly without changing the design.
- `Hold` — required evidence, retail/data state, validation maturity, or another prerequisite is not yet available.

A plan must never upgrade itself from `Shadow Only`/`Redesign`/`Hold` to `Ready` by inventing marketplace, profile/account scope, entity IDs, audience semantics, `isolation_evidence`, boundary verification time, sample sufficiency, or control integrity.

## Design principles

- Change the fewest controls needed to test the hypothesis.
- Prefer reversible treatments.
- Predeclare the primary metric and decision rule; do not select the winner after seeing whichever KPI improved.
- Keep efficiency and volume together. A lower ACOS with collapsed qualified demand is not automatically a win.
- Separate platform-attributed outcomes from business profitability and incrementality claims.
- When cohorts interact, inspect combined/pool outcomes before calling a treatment incremental.
- Treat control integrity as time-varying during long tests; revalidate after material scope changes.
- Treat configured audience/model signals as optimization inputs unless the relevant Amazon Ads product contract proves they are hard eligibility or exclusion boundaries.
- Use account-specific economics and comparable history before generic benchmarks.
- Never treat a fixed click/order count as a universal Amazon requirement.

## Output

Return:

1. **Decision question** — what uncertainty this test should resolve.
2. **Hypothesis** — treatment → mechanism → expected outcome.
3. **Scope** — marketplace, profile/account scope, ad type, entity IDs/ASINs, audience/optimization-signal semantics, and exclusions.
4. **Design** — treatment, comparison method, baseline/control, allocation integrity, `control_integrity`, holdout `isolation_evidence`, `boundary_monitoring.latest_verified_at`, `boundary_monitoring.material_scope_changes`, and interference risk.
5. **Metrics** — one primary metric, diagnostics and guardrails.
6. **Readiness** — data quality, sample sufficiency, attribution maturity, overlap/interference and confounders.
7. **Windows** — pre-test baseline, treatment period, conversion-lag/observation period and next review point.
8. **Decision rules** — Keep/Test winner, Extend, Inconclusive, Stop, Rollback Candidate or Redesign.
9. **Execution boundary** — `Suggest`/`Shadow`; external executor required for any live write.

Every experiment should preserve enough before/after state to support later `post-change-review` and `optimization-event` history.
