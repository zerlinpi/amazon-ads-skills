# Optimization Memory Contract

Load this shared reference when a decision touches an entity with prior optimization activity, when a previous action may still be maturing, or when the user asks for historical context.

The goal is not to create a generic long-term memory system. Preserve enough decision lineage to prevent duplicate, contradictory, stale, cross-scope, or falsely attributed Amazon Ads optimizations. Use `schemas/optimization-event.json` for event records, `schemas/entity-history.json` for derived history, `references/data-lineage.md` for measurement comparability, and `references/realized-ad-identity.md` when shopper-facing realization can confound attribution.

## Core model

Treat memory as an append-first event ledger plus derived summaries. Events record proposed, approved, applied, readback, evaluated, failed, rolled-back, corrected, or unknown states. Summaries are retrieval aids, not source of truth. Never overwrite an old event because a later dataset or conclusion changed; append a linked correction/re-evaluation.

## Read-before-recommend gate

Before a material bid, budget, placement, negative, state, or structural recommendation, retrieve when available: latest same-control event; pending validation; recent failed/unknown events; latest trusted readback and outcome; rollback conditions; overlapping parent/child actions or experiments; material evidence restatements; and relevant realization snapshots. If history cannot be retrieved, say `history unavailable`; do not infer no prior action.

## Collision-safe identity

Preferred identity is:

```text
marketplace + profile/account scope + entity type + entity id + control dimension
```

Names and locally normalized IDs alone are not collision-safe. When marketplace/profile scope is incomplete, ambiguous, or colliding, do not merge histories or transfer outcomes/readbacks; downgrade to Hold, Directional, or Manual Review until scope resolves.

Verified predecessor/successor migration can preserve bounded lineage, but predecessor live state is never successor current state. Cross-marketplace predecessor performance is directional by default: do not directly transfer bids, CPC/CVR/CTR/ACOS/ROAS baselines, budgets, placement multipliers, profitability thresholds, sample thresholds, or validation clocks without successor-market calibration.

## Lifecycle and anti-thrashing

Typical lifecycle:

```text
proposed → approved(optional) → applied|failed|unknown → readback → evaluated → keep|monitor|rollback_proposed|follow-up
```

Keep these distinctions explicit: proposed ≠ applied; applied ≠ readback-confirmed; readback-confirmed ≠ worked; worked ≠ proven causal; rollback-proposed ≠ rolled-back.

While a material action is still attribution/sample-maturity pending, avoid contradictory or large overlapping edits unless a safety guardrail requires intervention. Flag oscillation, unknown application, overlapping experiments, and parent-level confounding. Do not use a universal waiting period.

## Decision-time evidence identity

Mutable reporting history creates two separate questions: what evidence was available when the decision was made, and what the latest/restated history says now. Preserve both.

For material evaluated/corrected events, `evidence_snapshot` should preserve available decision-relevant measurement identity rather than only a dataset label. Canonical fields are defined in `schemas/optimization-event.json`; capture when known:

- snapshot identity and capture timestamp;
- `source_system` and `source_dataset`;
- `acquisition_channel`;
- `reporting_generation`;
- `semantic_version`;
- `date_attribution_semantics`;
- `historical_availability_status`;
- `comparability_status`;
- `available_through` and attribution/backfill maturity;
- compact evidence hash or immutable artifact reference.

These fields are nullable because an older connector or artifact may not expose them. Missing lineage is uncertainty, not permission to guess. In particular, `historical_availability_status = unavailable|retired_or_deleted|unknown` must never be interpreted as a zero historical metric or no historical activity.

When reporting generation, date attribution, acquisition channel, semantic version, or historical availability differs across replay windows, apply `references/data-lineage.md` before reusing the old outcome. A stored `Worked` result does not become action-safe evidence under a new measurement identity merely because campaign/entity IDs match.

If history later restates enough to change an outcome, append a correction/re-evaluation linked to the original event and preserve both evidence identities. Reconcile before using the changed conclusion for another aggressive optimization.

## Realization-aware memory

When platform-managed surface/product/creative/message realization can affect causal interpretation, preserve the bounded `realization_snapshot` defined in `schemas/optimization-event.json`. Missing realization fields are not evidence that realization was unchanged or zero.

Keep separate:

```text
control readback confirmed?
realization comparable?
outcome moved as expected?
```

If realization comparability is Directional, Not Comparable, or Unknown, do not upgrade to strong single-action causal attribution solely because the advertiser control applied.

## Partial-memory warnings

Expose incomplete-history conditions such as local-only history, external executor history unavailable, missing readback, unknown write result, event gap, identity-scope ambiguity, migration mapping partial, historical evidence restated, retired/deleted historical source, or realization comparability unresolved. Never treat a partial ledger as complete account history.

## Retrieval order

Resolve marketplace/profile scope first; retrieve same entity + same control newest-first; then verified predecessor history; overlapping other controls; parent changes; active experiments; account/portfolio constraints; and relevant realization snapshots. Keep the slice bounded rather than dumping account history into context.

## Output contract

When memory materially affects a decision, report history status, identity scope, latest relevant action/time, application/readback status, validation maturity, latest outcome, decision-time evidence identity, latest restatement status, realization comparability when relevant, unresolved warnings, and next decision point.

## Safety boundary

This memory contract stores decision evidence and state. It does not authorize live Amazon Ads mutation. Write/retry/idempotency/reconciliation/executor mechanics remain outside this repository in an explicitly authorized Connector/Executor.
