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

Do not invent an auction-level composition formula from these configured controls. Treat them as a control graph whose realized effect is observed through delivery, CPC, traffic mix, placement/audience mix, conversion, and economic outcomes.

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
3. reconstruct the material control timeline;
4. identify binding controls and overlapping changes;
5. check whether traffic/product/query/target/placement/audience mix changed consistently with those controls;
6. downgrade causal language when isolation is not supported;
7. prefer a follow-up experiment or clean validation window when the action is important and confounding remains material.

This reference is read-only. It does not authorize Amazon Ads writes; execution, retry, idempotency, and reconciliation remain external Connector/Executor concerns.
