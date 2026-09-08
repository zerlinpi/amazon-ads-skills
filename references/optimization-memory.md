# Optimization Memory Contract

Load this shared reference when a decision touches an entity with prior optimization activity, when a previous action may still be maturing, or when the user asks for historical context.

The goal is not to create a generic long-term memory system. It is to preserve enough decision lineage to prevent duplicate, contradictory, stale, or falsely attributed Amazon Ads optimizations.

## Core principle

Treat optimization memory as an append-first event ledger plus derived entity summaries.

- Events record what was proposed, approved, applied, read back, evaluated, failed, rolled back, or became unknown.
- Entity summaries are derived views for fast retrieval. They are not the source of truth.
- Never overwrite historical events merely because a later conclusion changed.
- A new event may supersede or correct an earlier interpretation while preserving the original record.

Use `schemas/optimization-event.json` for event records and `schemas/entity-history.json` for the derived entity-history view.

## Read-before-recommend gate

Before recommending a new bid, budget, placement, negative, target-state, campaign-state, or structural action on an entity, retrieve when available:

1. the latest relevant event for the same entity/control;
2. any pending evaluation or still-open validation window;
3. recent applied/failed/unknown events;
4. the latest readback state;
5. the latest outcome classification;
6. active rollback/stop conditions;
7. concurrent actions on parent/child entities that can contaminate attribution.

If no memory source exists, say `history unavailable` rather than assuming there was no prior action.

## Entity identity

Memory must be scoped tightly enough to avoid cross-account collisions.

Preferred identity tuple:

```text
marketplace + profile/account scope + entity type + entity id + control dimension
```

Examples of `control dimension`:

- bid;
- daily budget;
- placement modifier;
- campaign state;
- keyword/target state;
- negative keyword;
- negative product target;
- match type / structure.

Do not merge two entities because their names match. Use stable IDs when available.

## Event lifecycle

A common lifecycle is:

```text
proposed
→ approved (optional)
→ applied OR failed OR unknown
→ readback
→ evaluated
→ keep / monitor / rollback_proposed / follow-up experiment
→ rolled_back (if externally applied)
```

Not every event needs every stage. Preserve uncertainty explicitly.

### Important distinctions

- `proposed` is not `applied`.
- `applied` is not `readback confirmed`.
- `readback confirmed` is not `worked`.
- `worked` is not proof of causality if important concurrent changes remain unresolved.
- `rollback_proposed` is not `rolled_back`.

## Pending evaluation

An action is `pending evaluation` when its intended validation window is not mature or required post-change evidence has not arrived.

While a material action is pending:

- do not stack a contradictory edit on the same control unless a safety guardrail triggered;
- avoid another large edit that makes the first action uninterpretable;
- prefer `Hold`, `Keep Monitoring`, or a separately scoped experiment;
- record why an emergency override was necessary when one occurs.

Validation maturity should consider attribution lag, order volume, seasonality, promotions and retail-readiness changes. Do not use a fixed universal waiting period.

## Anti-thrashing rules

Flag a new proposal for manual review or hold when any of the following is true:

- it reverses the latest applied action before evaluation maturity;
- the same control has oscillated repeatedly without stable evidence;
- multiple actions are being layered faster than their effects can be separated;
- an earlier action has application status `Unknown` or `Drifted`;
- the entity is already inside an active experiment where the new edit would contaminate treatment/control;
- a parent-level change can explain the child-level movement under review.

An exception is allowed for triggered safety conditions such as severe overspend, loss of purchasability, listing suppression, inventory risk, or another explicit guardrail. Record the override reason.

## Staleness and freshness

Historical memory is context, not current truth.

Every derived entity summary should include:

- `as_of` timestamp;
- latest source event timestamp;
- latest trusted readback timestamp;
- unresolved/pending event count;
- source completeness or warnings.

Before presenting a stored state as current, refresh from a trusted live/exported source when the decision depends on current state.

A stale memory item may explain why an action happened, but it cannot prove the entity is still configured that way.

## Local-only / partial-memory warnings

If the runtime has multiple machines, agents, connectors, or write paths, memory can be incomplete.

Expose warnings such as:

- `local-only history`;
- `external executor history unavailable`;
- `missing readback`;
- `unknown write result`;
- `legacy changelog only`;
- `event gap detected`.

Do not silently treat a partial ledger as complete account history.

## Conflict and supersession

When newer evidence changes the interpretation of an older event:

- keep the old event immutable;
- append a new evaluation/correction event;
- link it through `parent_action_id` or related event IDs;
- mark the derived entity summary with the newest decision state.

For mutually conflicting events, prefer current trusted readback for state, but preserve historical intent and outcome separately.

## Retrieval order

For a new optimization decision, retrieve in this order:

1. same entity + same control, most recent first;
2. same entity, other controls in the overlapping window;
3. parent campaign/ad-group/product-ad changes;
4. active experiments containing the entity;
5. recent account-wide or portfolio controls that materially affect delivery.

Keep the returned slice bounded. Do not dump the whole account history into context.

## Compact entity summary

A derived summary should answer:

- What is the latest known control state?
- What was the last material action and why?
- Did it actually apply?
- Is evaluation complete?
- What was the outcome?
- Is a rollback condition active?
- Are there unresolved events or memory-quality warnings?
- When is the next decision point?

Prefer a compact summary plus the few source events needed for evidence.

## Suggested decision states

Use these derived states when useful:

- `No Recent Action`
- `Proposed Only`
- `Awaiting Application`
- `Application Unknown`
- `Pending Readback`
- `Pending Evaluation`
- `Worked / Keep`
- `Monitoring`
- `Rollback Candidate`
- `Rolled Back`
- `Failed Application`
- `Drifted`
- `Conflicted / Manual Review`

## Output contract for memory-aware decisions

When memory materially affects a recommendation, include:

- `history_status`;
- latest relevant action and timestamp;
- application/readback status;
- validation maturity;
- latest outcome;
- unresolved conflicts or warnings;
- whether the new proposal is `Allowed`, `Hold`, `Experiment Only`, or `Manual Review`;
- the event IDs supporting the decision when available.

## Privacy and storage safety

Do not store credentials, refresh tokens, client secrets, access tokens or unnecessary customer-identifying data in optimization memory.

Use the minimum account/profile scope required for collision-safe entity identity. Public examples should use synthetic identifiers.
