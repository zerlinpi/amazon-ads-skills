# Control-state comparability

Load this shared reference when a baseline/post-change, period-over-period, experiment, placement, bid, or budget conclusion depends on causal interpretation rather than descriptive movement alone.

Measurement comparability is necessary but not sufficient for causal comparability. Two windows can use the same source, reporting generation, metric definitions, attribution semantics, grain, and mature data while the active advertiser controls differ materially.

## Control-state comparability gate

For each decision-relevant window, capture when supported and relevant:

- base/default/target bid state;
- campaign bidding strategy, including fixed, dynamic, rule-based, or unknown;
- placement bid adjustments;
- audience bid adjustment state;
- schedule/event bid rules and active windows;
- campaign/portfolio/account budget and pacing controls;
- targeting/negative/routing state that can change traffic ownership;
- experiment/treatment assignment when applicable;
- effective timestamps for material control changes.

When control evidence is exchanged between a Skill, connector, replay fixture, or reviewer, use `schemas/control-state-snapshot.json` as the machine-readable evidence envelope. Preserve marketplace/profile scope, observation time, source/acquisition provenance, each material control's effective timestamp, and its evidence status. A missing, unsupported, or stale control remains `unknown`; it must not be synthesized as zero, false, absent, or unchanged.

The schema is an evidence contract, not an Amazon API response schema and not an execution payload. It does not require a connector to expose controls it cannot read.

When two schema-valid snapshots are available, `scripts/compare_control_state.py` provides a deterministic, read-only first-pass classification. It fails closed to `Unknown` for marketplace/profile mismatch, missing material controls, stale/unsupported/unknown evidence, or changed controls without effective timestamps. With an explicitly named intended treatment, it returns `Treatment Isolated` only when that treatment changed and no other evidenced material control changed; overlapping evidenced changes are `Confounded`. Without an intended treatment, stable evidenced controls are `Comparable` and changed controls are only `Directional`. The comparator does not prove causality and does not override stronger experiment/reconciliation evidence.

Do not invent an auction-level composition formula from configured controls. Treat them as a control graph whose realized effect is observed through delivery, CPC, traffic mix, placement/audience mix, conversion, and economic outcomes.

## States

Classify control-state comparability as:

- `Comparable` — no decision-material control difference outside the intended treatment/change;
- `Treatment Isolated` — the intended control changed and other material controls are sufficiently stable for bounded attribution;
- `Directional` — overlapping control changes exist, but broad directional learning remains useful;
- `Confounded` — one or more overlapping material controls can plausibly explain the observed effect;
- `Unknown` — required control state or change timestamps are unavailable, stale, or unsupported by the active connector.

`Unknown` is not unchanged state. Missing connector support is not evidence that a control was absent.

## Causal rule

A post-change or experiment conclusion must not be more causal than the weaker of:

1. measurement comparability; and
2. control-state comparability.

If baseline and post-change windows differ in placement adjustment, audience bid adjustment, bidding strategy, schedule/event rule, budget/pacing state, or traffic-routing controls beyond the intended treatment, downgrade a single-control causal claim to `Directional`, `Confounded`, or `Unknown` unless a valid design or reconciliation separates the effects.

Examples:

```text
same ROAS definition + same reporting generation
+ placement modifier changed as intended
+ audience bid adjustment also changed
=> metric comparison may be valid, placement causal attribution is confounded
```

```text
same mature metrics
+ bid changed as intended
+ budget became binding in the post window
=> observed delivery response cannot be attributed to bid alone
```

## Unified reporting boundary

Amazon Ads Unified Reporting can combine dimensions such as campaign, placement, and audience and standardize metrics across ad products. That improves measurement access; it does not prove that advertiser control state was stable between compared windows. Standardized labels and multi-dimensional reporting must not be used as a substitute for control-state history.

## Decision use

Before `Worked`, `Failed`, aggressive scale, rollback, or precise marginal-effect claims:

1. verify the intended change/readback;
2. verify measurement comparability using `data-lineage.md` when needed;
3. reconstruct the material control timeline, preserving source and effective timestamps in `schemas/control-state-snapshot.json` when machine-readable evidence is available;
4. use `scripts/compare_control_state.py` for deterministic first-pass classification when two snapshots are available;
5. identify binding controls and overlapping changes;
6. check whether traffic/product/query/target/placement/audience mix changed consistently with those controls;
7. downgrade causal language when isolation is not supported;
8. prefer a follow-up experiment or clean validation window when the action is important and confounding remains material.

This reference is read-only. It does not authorize Amazon Ads writes; execution, retry, idempotency, and reconciliation remain external Connector/Executor concerns.
