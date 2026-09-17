# Platform Capability Lineage

Load this reference when an Amazon Ads recommendation depends on a time-varying platform capability or exact platform rule rather than only advertiser performance data. Typical examples include bidding-strategy behavior, maximum/minimum control ranges, placement/audience modifiers, rule eligibility, console/API availability, supported ad products, advertiser types, or marketplace rollout.

The purpose is to prevent an older but still-live guide, a launch announcement, a different ad product, or a different control surface from silently becoming current action-safe platform behavior.

## Capability identity

For every platform fact that materially affects a recommendation, preserve enough identity to answer what the source actually proves:

```text
capability_name
source_url / source_id
source_kind
published_or_updated_at
retrieved_at
ad_product
control_surface
marketplace / region
advertiser_type / eligibility
capability_scope
value_or_behavior_claim
conflict_status
```

`source_kind` should distinguish at least current product/help documentation, API/reference documentation, launch/what's-new announcement, general/evergreen guide, and observed connector/account capability.

`capability_scope` is the bounded set for which the fact is evidenced: for example Sponsored Products vs Sponsored Brands, console vs API, a named placement/control, advertiser eligibility, and stated marketplaces. A fact verified for one scope is not automatically portable to another.

Use `published_or_updated_at` when the source exposes it and always record `retrieved_at` for volatile platform facts. Missing publication/update metadata is itself evidence uncertainty; do not invent a date.

## Source reconciliation policy

There is no repository-wide rule that "newer always wins" or that one documentation class always overrides every other source. Reconcile in this order:

1. Confirm the sources describe the same ad product, control, surface, eligibility and marketplace scope.
2. Prefer a directly applicable, explicitly current product/help or API/reference statement over a generic example only when the scopes truly overlap and the newer source clearly supersedes the older behavior.
3. Treat launch announcements as evidence that a capability existed for the announced release/scope, not proof that its limits and eligibility are unchanged today.
4. Treat console and API evidence separately unless current documentation proves parity.
5. Keep older or broader evidence as historical/contextual rather than deleting it when it explains why a conflicting rule may still appear in live documentation.

If scope, date, or supersession cannot be established, do not silently choose one source.

## Conflict states

Use one of these states when the capability fact matters:

- `Supported` — current, directly applicable evidence is sufficient for the requested scope; any older conflicting source has been reconciled as superseded or out of scope.
- `Conflicted` — two or more credible sources materially disagree and the difference cannot be reconciled by scope, date, surface or eligibility.
- `Unknown` — required capability evidence is missing, stale, inaccessible, or too generic for the requested scope.
- `Historical` — the fact is useful for explaining a prior period but is not trusted as current behavior.

When `conflict_status = Conflicted` or `Unknown`, an exact numeric platform rule is not action-safe. Preserve the direction or decision logic that does not depend on the disputed number, request/verify the current account capability when possible, or output `Hold`, `Directional`, `Experiment`, or `Manual Review`. **Do not silently choose** the most convenient percentage, limit or formula.

## Numeric-rule safety

Platform limits and automatic bid multipliers are not account sizing policy. Even when a platform rule is `Supported`, it defines what Amazon may allow/do; it does not prove that the advertiser should use the maximum or any particular percentage.

Keep these layers separate:

```text
verified platform capability / allowed range
≠ advertiser-specific action magnitude
≠ guaranteed realized auction exposure
```

Use `references/action-sizing.md` for advertiser-specific magnitude and realized-delivery evidence for outcome interpretation.

## Current motivating failure mode

Amazon can leave multiple official pages live while platform behavior evolves. As reviewed in September 2026, current Sponsored Products documentation includes a dynamic-bidding statement that differs from still-live broader guidance about placement-specific upward adjustment limits. That is exactly the class of drift this contract is designed to contain: first reconcile source date + exact scope; if the discrepancy remains unresolved for the requested decision, mark it `Conflicted` rather than importing the older or newer percentage by convenience.

Do not copy the example percentage into another Skill as a permanent repository constant. Re-verify current Amazon documentation or account/API capability whenever the exact rule materially affects a decision.

## Output when capability lineage matters

Include, at minimum:

- capability name and requested scope;
- selected source(s) and `source_kind`;
- `published_or_updated_at` when known and `retrieved_at`;
- `capability_scope` / eligibility;
- `conflict_status`;
- which conclusion remains safe if the platform fact is unresolved;
- whether account/API/console readback is required before an exact action.

This reference governs decision evidence only. It does not authorize live Amazon Ads mutation or replace external Connector/Executor readback.
