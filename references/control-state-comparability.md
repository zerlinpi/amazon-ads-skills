# Control-state comparability

Load this shared reference when a baseline/post-change, period-over-period, experiment, placement, bid, or budget conclusion depends on causal interpretation rather than descriptive movement alone.

Measurement comparability is necessary but not sufficient for causal comparability. Two windows can use the same source, reporting generation, metric definitions, attribution semantics, grain, and mature data while the active advertiser controls differ materially.

## Control-state comparability gate

For each decision-relevant window, capture when supported and relevant: base/default/target bid state; campaign bidding strategy; placement bid adjustments; audience bid adjustment state; schedule/event bid rules; campaign/portfolio/account budget and pacing controls; targeting/negative/routing state; experiment/treatment assignment; and effective timestamps for material control changes.

When control evidence is exchanged between a Skill, connector, replay fixture, or reviewer, use `schemas/control-state-snapshot.json` as the machine-readable evidence envelope. A missing, unsupported, or stale control remains `unknown`; it must not be synthesized as zero, false, absent, or unchanged.

The snapshot must declare the decision-material control types expected and a coverage status. `Complete` is allowed only when every required control is represented by source-supported evidence. `Partial` or `Unknown` coverage is not evidence that omitted controls were absent.

### Collection-valued control evidence

When a registry-required control is represented as a top-level list, the list contents alone do not prove that the control state is complete. This applies to both empty and non-empty lists: one returned row/page is still partial evidence when additional rows may exist.

A list-valued required control is decision-complete only when its machine-readable `collection_evidence` establishes all three conditions:

- `enumeration_status=Complete` — the source/connector completed the decision-relevant enumeration;
- `pagination_status=Complete` — no unresolved continuation, row cap, or truncation remains;
- `capability_status=Supported` — the active acquisition path supports that control collection at the required scope.

`Partial`, `Truncated`, `Unsupported`, `Unknown`, or missing collection evidence fails closed to `Unknown`, even when the returned list is non-empty. A verified empty list is therefore distinct from an unknown empty list, and a non-empty partial list is distinct from a complete collection.

This generic gate applies to top-level list-valued controls. Lists embedded inside structured controls, such as schedule/event rule surfaces or budget-rule state, retain their surface-specific completeness requirements; do not infer that a parent object is complete merely because an embedded list exists.

For structured controls that contain decision-material nested lists, completeness is recorded separately in `nested_collection_evidence`, keyed by the nested state field. Sponsored Products causal comparisons currently require this for:

- `schedule_or_event_rule.state.schedule_rules`;
- `schedule_or_event_rule.state.event_rules`;
- `budget_or_pacing.state.active_budget_rules` when evaluating Sponsored Products budget changes.

Each required nested list must independently prove `enumeration_status=Complete`, `pagination_status=Complete`, and `capability_status=Supported`. One nested surface cannot launder another: complete event-rule evidence does not prove schedule-rule completeness, and a non-empty budget-rule list does not prove that all active rules were observed. Missing, partial, truncated, unsupported, or unknown nested evidence fails closed to `Unknown`.

### Versioned requirement provenance

`references/control-requirement-registry.json` is the repository-owned, versioned authority for `decision_surface -> required_control_types`. A snapshot with `derivation_status=Verified` must name its `requirement_registry_id`, and that identity plus the decision surface must resolve to the exact required set in the registry. An unknown/stale registry identity, an unregistered decision surface, or a snapshot-required set that differs from the registry fails closed to `Unknown`.

Connector capability is deliberately separate. Capability evidence answers whether a required control can be observed; it never decides whether the control is required. Connector non-support therefore reduces coverage rather than shrinking the registry-derived requirement set. This prevents a connector or agent from manufacturing `Complete` by omitting a control it cannot read.

The registry should remain narrow and evidence-backed. Add production decision surfaces only when Amazon official semantics or equivalent high-confidence evidence show that the listed controls are decision-material. Unknown surfaces remain `Unknown`; do not infer a nearest surface. Registry changes require regression evidence because they alter the causal proof boundary.

The schema is an evidence contract, not an Amazon API response schema and not an execution payload. It does not require a connector to expose controls it cannot read; unsupported controls instead prevent a false completeness claim.

Optimization identity is type-bound as well as ID-bound. When `scope.entity_id` is populated, `scope.entity_type` must identify the semantic namespace/kind represented by that ID. This matters when reporting surfaces normalize distinct targeting entities into a shared identifier field; the same identifier value without its entity type is not sufficient evidence of the same optimization entity. Baseline/post snapshots with a missing or changed entity type must fail closed to `Unknown`.

When two schema-valid snapshots are available, `scripts/compare_control_state.py` provides a deterministic, read-only first-pass classification. It fails closed to `Unknown` for marketplace/profile mismatch, incomplete/unknown material-control coverage, unverified requirement provenance, missing/unknown/stale registry identity, unregistered decision surface, registry mismatch, required controls absent from either snapshot, changed expected-control sets or decision surfaces, stale/unsupported/unknown evidence, or changed controls without effective timestamps. With an explicitly named intended treatment, it returns `Treatment Isolated` only when that treatment changed inside a complete, registry-verified material-control set and no other evidenced material control changed; overlapping evidenced changes are `Confounded`. Without an intended treatment, stable evidenced controls are `Comparable` and changed controls are only `Directional`.

Do not invent an auction-level composition formula from configured controls. Treat them as a control graph whose realized effect is observed through delivery, CPC, traffic mix, placement/audience mix, conversion, and economic outcomes.

## Sponsored Products budget-change state

For `decision_surface=sponsored_products_budget_change`, generic evidence that a campaign has a budget is not enough. The repository-owned `budget_or_pacing.state` must preserve at least:

- `base_average_daily_budget` — the source-supported configured average daily budget;
- `effective_daily_budget` — the budget actually in force for the decision window after applicable automated budget rules;
- `active_budget_rules` — source-supported rule evidence for that window. An empty list means the source positively observed no active rules; connector non-support or missing rule evidence remains unknown and must not be encoded as `[]`.

Amazon currently documents schedule-based and performance-based Sponsored Ads budget rules that can automatically raise daily budgets, with multiple applicable rules able to combine. Amazon also documents Sponsored Ads daily budgets as average daily budgets whose day-level spend can vary under the account policy. Therefore configured budget, effective budget, observed spend, and rule state are distinct evidence. A day where spend exceeds the configured average daily budget is not by itself proof of a manual budget edit, policy breach, or executor action.

The deterministic comparator applies this stronger structured-state check only to the registered Sponsored Products budget-change surface. If base/effective budget or active-rule evidence is missing, the comparison fails closed to `Unknown`. This does not model Amazon's budget-rule implementation and does not authorize any write.

## States

- `Comparable` — no decision-material control difference outside the intended treatment/change.
- `Treatment Isolated` — intended control changed and other registry-required controls are sufficiently stable.
- `Directional` — material controls changed without an identified isolated treatment.
- `Confounded` — overlapping material controls can plausibly explain the observed effect.
- `Unknown` — required state, coverage, requirement provenance, registry resolution, or timestamps are unavailable, stale, unverified, or unsupported.

`Unknown` is not unchanged state. Missing connector support is not evidence that a control was absent.

## Causal rule

A post-change or experiment conclusion must not be more causal than the weaker of measurement comparability and control-state comparability. If baseline and post-change windows differ in placement adjustment, audience bid adjustment, bidding strategy, schedule/event rule, budget/pacing state, or traffic-routing controls beyond the intended treatment, downgrade a single-control causal claim unless a valid design or reconciliation separates the effects.

## Unified reporting boundary

Amazon Ads Unified Reporting can combine dimensions such as campaign, placement, and audience and standardize metrics across ad products. That improves measurement access; it does not prove that advertiser control state was stable between compared windows.

## Decision use

Before `Worked`, `Failed`, aggressive scale, rollback, or precise marginal-effect claims: verify intended change/readback; verify measurement comparability; resolve the decision surface against `references/control-requirement-registry.json`; use connector capability only to determine observability; reconstruct material control timelines with source/effective timestamps; run `scripts/compare_control_state.py` when two snapshots exist; identify binding/overlapping controls; inspect traffic and economic outcomes; downgrade causal language when isolation is unsupported; and prefer a clean validation window when confounding remains material.

This reference is read-only. It does not authorize Amazon Ads writes; execution, retry, idempotency, and reconciliation remain external Connector/Executor concerns.
