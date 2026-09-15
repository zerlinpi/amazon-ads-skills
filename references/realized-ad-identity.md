# Realized ad identity and platform-managed realization

Load this shared reference when Amazon can change the **realized ad experience** without a corresponding advertiser edit to the campaign's ordinary bid, budget, targeting, placement, state, or structure controls.

The goal is to keep configured intent separate from what shoppers were actually shown.

## Core distinction

Treat these as different layers:

```text
configured controls
→ eligibility / selection logic
→ realized delivery surface
→ realized product mix
→ realized creative/message
→ observed traffic and outcomes
```

A stable campaign configuration does not prove that the realized ad identity stayed stable.

Examples of platform-managed realization can include:

- auto-enrolled delivery surfaces or ad experiences;
- AI-selected product groups from an eligible catalog;
- dynamically assembled product combinations;
- platform-generated or platform-selected creative/message variants;
- shopper-context-dependent realization that varies while campaign targets remain unchanged.

Do not assume every ad product supports every layer. Record only what the relevant Amazon Ads product/report actually exposes.

## Realized identity dimensions

When realization can affect a decision, capture when available:

- `ad_product` / format;
- marketplace + profile/account scope;
- campaign/ad-group/ad IDs where exposed;
- configured targeting and control state;
- realization mode: `manual`, `platform_managed`, `hybrid`, or `unknown`;
- delivery surface / placement / experience;
- advertised ASIN(s) or realized product group when reportable;
- creative/message/prompt identity when reportable;
- eligibility/rollout state;
- measurement window and acquisition channel;
- source/report identity, row eligibility, freshness and completeness.

`unknown` is a valid state. A connector that does not expose realized product, creative, prompt, or surface dimensions is **not evidence** that those dimensions were unchanged or zero.

## Optimization signals are not automatically hard targeting constraints

For AI-managed campaigns, distinguish **optimization signals** from **hard targeting constraints**.

An audience signal, conversion signal, catalog signal, or other advertiser-provided model input can guide optimization without defining the full set of shoppers who are eligible to receive the ad. A configured audience signal therefore does not by itself prove that actual delivery was restricted to that audience.

Current Amazon Ads examples include Brand+ and Performance+ Audience Signals. Amazon describes advertiser audiences added to these campaigns as AI optimization inputs; for Brand+ Prospecting, Amazon explicitly describes retaining full reach discovery while the signal guides optimization. Treat that as product-specific evidence for this semantic distinction, not a universal rule for every Amazon Ads audience control.

Therefore:

```text
audience signal configured
!= hard audience targeting constraint
!= verified delivery only to signal members
!= valid experiment holdout boundary
```

Before using a configured signal as a targeting or experiment boundary, verify the product's actual control semantics and, when the conclusion depends on realized exposure, inspect delivery/reporting evidence at the closest available scope.

For diagnosis and post-change review:

- record whether the changed item is a hard eligibility/exclusion control or an optimization input;
- do not attribute a traffic-mix change to a narrow audience restriction merely because a signal was added;
- do not infer that users outside the signal were excluded unless the product contract proves it;
- when the active connector exposes only configured signals but not realized audience/delivery composition, keep audience-composition conclusions `Directional` or `Unknown`.

For experiments, an optimization signal is **not a holdout boundary**. If treatment/control separation depends on audience isolation, require an actual exclusion/eligibility mechanism or realized delivery evidence that proves the cohorts are sufficiently separated.

## Causal safety

Before attributing a performance change to an advertiser action, check whether realized ad identity also changed during the same window.

Examples:

```text
same bid + same targeting
+ different realized product mix
→ conversion/ROAS change may be composition-driven
```

```text
same campaign controls
+ newly eligible platform-managed surface
→ traffic mix may change without advertiser edit
```

```text
same campaign + same products eligible
+ unknown realized creative/message mix
→ creative-level causality is not established
```

A platform rollout announcement establishes a possible mechanism, not account-level exposure. Require account/campaign eligibility plus realized delivery evidence before calling it causal.

## Product-mix safety

When Amazon dynamically selects products from a catalog or eligible set:

- do not treat the configured catalog/eligible-ASIN set as the realized advertised-product mix;
- do not assign all campaign outcomes equally to every eligible ASIN;
- do not infer that a product was shown merely because it was eligible;
- do not interpret a campaign-level lift/drop as proof that a specific product became stronger/weaker unless product-level exposure/outcomes support it;
- when product realization is unavailable, keep ASIN-specific conclusions `Directional`, `Unknown`, or `Manual Review`.

This is especially important when product economics, retail readiness, price, inventory, Featured Offer status, or conversion rate differ materially across the eligible catalog.

## Post-change evaluation

For a post-change review, distinguish:

1. **control readback** — was the intended advertiser control applied?
2. **realization stability** — did surface/product/creative realization remain sufficiently comparable?
3. **outcome movement** — did delivery and business outcomes move as expected?

`control readback confirmed` does not prove that the evaluated outcome was generated under an otherwise stable ad realization.

If a material platform-managed realization shift overlaps the validation window:

- downgrade single-action causal attribution;
- prefer a narrower comparable slice if available;
- reconcile surface/product/creative-level evidence where reportable;
- otherwise classify the result `Directional`, `Confounded`, `Keep Monitoring`, or `Manual Review` rather than inventing certainty.

## Derived-history projection semantics

A compact entity-history view must distinguish **what was last observed** from **whether realization is observable now**.

Keep these concepts separate:

- `last observed realization` — the most recent bounded realization state for which material shopper-facing dimensions were actually observed;
- `observed_at` — when that known realization was captured;
- `observation freshness` — whether that observation is recent enough for the current decision, based on the decision horizon and source behavior rather than a repository-wide fixed age threshold;
- `current observability` — whether the latest acquisition attempt can currently observe the material realization dimensions;
- `comparability status` — whether the last observed realization can safely be compared with the decision/evaluation window.

The projection is intentionally not simple last-write-wins.

Example:

```text
t1: realization observed, coverage = Complete, identity = A
t2: newer acquisition attempt, coverage = Unavailable
```

The newer unavailable observation **must not erase** the bounded evidence captured at `t1`. Preserve `t1` as the last observed realization and separately record that current observability became `Unavailable` at `t2`.

At the same time, the last observed realization **must not be presented as current truth** merely because no newer known identity is available. Its timestamp/freshness and the newer observability result must travel with the derived summary.

Therefore:

```text
newer Unknown/Unavailable
!= realized identity became null/zero
!= prior observed identity still current
```

Projection rules:

1. Advance `last_observed_realization` only from an event/snapshot that contains bounded observed realization evidence; an observability failure does not replace it with null/zero.
2. Advance `current_realization_observability` from the newest relevant observation attempt, including `Complete`, `Partial`, `Unavailable`, or `Unknown`.
3. Preserve separate timestamps for the last observed identity and the latest observability check. Event recency is not the same as realization observation recency.
4. Do not label the last observed identity `Current` solely because it is the newest known identity. Derive observation freshness from the current decision horizon, acquisition cadence, platform behavior, and explicit warnings.
5. When current observability is `Unavailable`/`Unknown`, or the last observed identity is stale for the decision, downgrade current-state claims and causal attribution to `Directional`, `Hold`, or `Manual Review` as appropriate.
6. Historical replay may still use the older bounded snapshot for the historical window it actually represents; lack of current observability does not retroactively invalidate valid historical evidence.

These rules are designed for deterministic derived summaries while keeping the append-first event ledger as the source of truth.

### Scope-bound replay

Realization projection must also remain bound to one collision-safe optimization identity. A matching local campaign/ad-group/entity ID is not sufficient when multiple profiles or marketplaces can exist.

For production replay, resolve the requested scope before projection and bind the reducer to the complete expected tuple:

```text
marketplace
+ profile/account scope
+ entity type
+ entity id
```

Then require every realization-bearing event in the replay slice to match that tuple. If a relevant event is missing one of those dimensions, or resolves to a different marketplace/profile/entity, fail closed rather than guessing that it belongs to the requested history.

Therefore:

```text
same entity id + missing profile scope
!= verified same optimization identity
```

and:

```text
mixed or incomplete scope
→ reject replay / Manual Review
not
→ silently merge or assume same entity
```

The repository projector accepts an optional `expected_scope` input for this purpose. Lightweight historical fixtures can omit it, but production memory retrieval should provide it whenever the ledger can contain more than one marketplace/profile scope. This keeps the projector backward-compatible without weakening the optimization-memory identity gate.

## Acquisition-channel safety

A realization dimension may exist in Ads Console or a specialized report while being unavailable through the active API/MCP/connector.

Therefore:

```text
missing from active connector
!= zero exposure
!= unchanged realization
!= feature absent from Amazon Ads
```

Use `data-lineage.md` when acquisition-channel or reporting availability affects the decision.

## Action gate

Platform-managed realization evidence can change which control is worth investigating, but it never directly authorizes a live mutation.

Do not react to a realization shift by mechanically cutting bids, budgets, placements, products, or targets. First determine whether the realized mix is harmful, beneficial, merely different, or still unknown, and whether the actual advertiser-controllable binding lever is known.

Default actionability under unresolved realization identity is `Directional`, `Experiment`, `Hold`, or `Manual Review`.

## Current Amazon Ads evidence motivating this policy

Current public examples demonstrate why this shared layer is necessary:

- Sponsored Products / Sponsored Brands prompts can introduce an additional platform-managed ad experience for eligible existing campaigns without an ordinary manual campaign-control edit.
- Sponsored Brands collections can use automatic control in which Amazon AI dynamically curates product groupings from the advertiser catalog based on campaign targets and shopping signals; manual product selection remains a separate mode.
- Brand+ / Performance+ Audience Signals can act as AI optimization inputs rather than hard audience-only targeting boundaries; product-specific documentation must determine the exact semantics before an Agent treats a signal as an eligibility or experiment boundary.

These are examples of the general realization problem, not hard-coded assumptions that every account, marketplace, ad product, or future format behaves the same way.

## Safety boundary

This reference governs evidence identity and causal interpretation only. It does not authorize Amazon Ads writes. Mutation, retry, idempotency and reconciliation remain external Connector / Executor responsibilities.
