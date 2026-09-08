# Optimization Memory Contract

Load this shared reference when a decision touches an entity with prior optimization activity, when a previous action may still be maturing, or when the user asks for historical context.

The goal is not to create a generic long-term memory system. It is to preserve enough decision lineage to prevent duplicate, contradictory, stale, cross-scope, or falsely attributed Amazon Ads optimizations.

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

Memory must be scoped tightly enough to avoid cross-account and cross-marketplace collisions.

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

## Identity-scope safety gate

Treat `marketplace` and `profile/account scope` as part of optimization identity whenever memory can contain more than one account/profile/marketplace.

A matching entity ID, keyword text, campaign name, ASIN label, or display name is **not sufficient** to establish same-entity history across scopes.

Classify identity scope when useful as:

- `Complete` — marketplace and profile/account scope are present and match the requested entity;
- `Incomplete` — one or more required scope dimensions are missing;
- `Ambiguous` — multiple plausible histories remain after available scope filtering;
- `Collision Detected` — records with the same local entity key/name resolve to different marketplace/profile scopes.

### Fail-closed rules

When identity scope is `Incomplete`, `Ambiguous`, or `Collision Detected`:

- do not merge histories across candidate scopes;
- do not transfer `Worked / Keep`, `Rollback Candidate`, pending validation, or prior action outcomes from another scope;
- do not infer identity from display-name similarity;
- do not use a foreign-scope readback as current state;
- downgrade the memory-dependent decision to `Hold`, `Directional`, or `Manual Review` until the requested scope is resolved.

If the current request explicitly identifies marketplace/profile scope, filter memory to that scope before ranking recency or semantic similarity.

### Connector-normalized or local IDs

Some connectors, exports, test fixtures, caches, or intermediate stores may expose locally normalized IDs rather than globally collision-proof identifiers.

Therefore:

```text
entity type + entity id alone
≠ collision-safe optimization identity
```

The storage/retrieval layer should preserve scope fields alongside the local entity key. Public examples should use synthetic profile IDs and never rely on customer-identifying data.

## Verified migration lineage

A deliberate restructure can replace an entity with a new ID or move it to another profile/marketplace while preserving some business intent. This is different from assuming that two similarly named entities are the same.

History may cross an ID, profile, or marketplace boundary only when there is explicit migration evidence such as a trusted bulk-operation record, migration manifest, connector event, or another auditable mapping that links predecessor and successor.

A migration record should capture when available:

- predecessor entity type/id and marketplace/profile scope;
- successor entity type/id and marketplace/profile scope;
- migration timestamp and reason;
- verification source;
- scope-transition type;
- whether targeting semantics/match type were preserved;
- whether advertised-ASIN/product equivalence was preserved;
- whether business role/objective was preserved;
- continuity status: `Verified`, `Partial`, `Rejected`, or `Unknown`;
- evidence-portability status and constraints.

### Scope-transition types

Use when helpful:

- `same_scope` — predecessor/successor remain in the same marketplace/profile scope;
- `cross_profile_same_marketplace` — profile/account scope changed inside the same marketplace;
- `cross_marketplace` — marketplace changed;
- `unknown` — transition scope is not reliably known.

A cross-profile mapping is **not** a collision when it is explicit, audited and attached to the successor as lineage. However, it does not make the predecessor's live state current in the successor profile.

### Cross-marketplace portability limits

For `cross_marketplace` transitions, default continuity to `Partial` and `predecessor_evidence_portability` to `Directional Only` unless successor-market evidence proves a narrower fact is portable.

Potentially useful as bounded directional context:

- semantic query/product relevance;
- business intent and taxonomy;
- prior hypotheses worth retesting;
- known failure modes and safety pitfalls;
- structural lessons that do not depend on auction economics.

Do **not** transfer as action-safe performance evidence without successor-market calibration:

- bid magnitude or bid-change percentage;
- CPC, CVR, CTR, ACOS, ROAS or CPA baselines;
- budget size or pacing thresholds;
- placement multipliers;
- profitability thresholds or target economics;
- traffic/sample thresholds;
- validation clocks or expected response magnitude.

Why: currency, auction density, query demand, competitor set, retail price position, tax/fee economics, conversion behavior, logistics, promotion norms, attribution/reporting context, and product assortment can differ materially by marketplace.

Therefore:

```text
verified cross-marketplace mapping
≠ portable performance conclusion
```

A predecessor `Worked / Keep` outcome can justify a hypothesis or experiment in the successor marketplace, not a direct copy of the old action.

### What may transfer

When continuity is `Verified`, mature historical evidence may be used as bounded context, for example:

- historical relevance;
- mature profitability/efficiency patterns only when marketplace economics and measurement context are demonstrably compatible;
- prior hypotheses and tested actions;
- known failure modes;
- predecessor relationship for audit lineage.

For a verified `cross_profile_same_marketplace` migration, the above context may be retrieved after current-scope history and clearly labeled as predecessor evidence.

For `cross_marketplace`, prefer semantic/qualitative evidence first and require successor-specific observations before performance-based action.

### What must not transfer as current truth

Even with verified lineage, do not copy the predecessor's last known:

- bid;
- budget;
- state;
- placement modifier;
- negative attachment;
- pending mutation;
- readback status;
- active experiment assignment;
- validation clock.

The successor's current state must come from successor-specific trusted readback or source data.

If targeting semantics, ASIN/product scope, objective, route, marketplace, or important economics changed materially, downgrade continuity to `Partial` or `Rejected`. Preserve lineage for auditability without treating the predecessor and successor as literally identical entities.

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
- `event gap detected`;
- `identity scope incomplete`;
- `cross-profile collision detected`;
- `migration mapping partial`;
- `cross-marketplace portability limited`.

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

1. resolve marketplace + profile/account scope and reject accidental cross-scope collisions;
2. same entity + same control, most recent first;
3. verified predecessor history only when an explicit migration mapping links it to the requested successor;
4. same entity, other controls in the overlapping window;
5. parent campaign/ad-group/product-ad changes;
6. active experiments containing the entity;
7. recent account-wide or portfolio controls that materially affect delivery.

For cross-profile/cross-marketplace migrations, keep predecessor events labeled with their original scope. Do not rewrite them as if they originated in the successor scope.

Keep the returned slice bounded. Do not dump the whole account history into context.

## Compact entity summary

A derived summary should answer:

- What marketplace/profile scope does this history belong to?
- Is the identity scope complete and collision-free?
- What is the latest known control state?
- What was the last material action and why?
- Did it actually apply?
- Is evaluation complete?
- What was the outcome?
- Is a rollback condition active?
- Is there a verified predecessor/successor lineage or scope transition?
- If marketplace changed, which predecessor facts are actually portable?
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
- identity-scope status and warnings;
- marketplace/profile scope used for current-entity retrieval;
- latest relevant action and timestamp;
- application/readback status;
- validation maturity;
- latest outcome;
- identity-lineage and scope-transition status when migration is relevant;
- predecessor scope and portability status when predecessor evidence is used;
- unresolved conflicts or warnings;
- whether the new proposal is `Allowed`, `Hold`, `Experiment Only`, or `Manual Review`;
- the event IDs supporting the decision when available.

## Privacy and storage safety

Do not store credentials, refresh tokens, client secrets, access tokens or unnecessary customer-identifying data in optimization memory.

Use the minimum marketplace/account/profile scope required for collision-safe entity identity. Public examples should use synthetic identifiers.
