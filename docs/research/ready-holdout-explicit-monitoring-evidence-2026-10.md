# Ready holdout explicit monitoring evidence boundary — 2026-10-26

## Confirmed gap and scope

Initial main `4767baaef5ef33b661b02ecf334db0109fb6bebd` (v1.85.0); no open PR and related historical branches zero ahead. `scripts/validate_experiment_plan.py` treated any non-object `comparison.boundary_monitoring` as absent, even when the field was explicitly provided with `null`, `Unknown`, `[]`, `false`, or `0`. Within a valid monitoring object, explicit `launch_verified_at: null` was skipped and a null/string `material_scope_changes` was treated like an empty list. This can promote unresolved monitoring evidence into `Ready`.

## Reproducible RED → GREEN

- RED test commit `bf292aa59a1b0e41f515c401fc2f6cb0ea3a2f62`, [Actions #40352431603](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40352431603): 1744 tests, 9 failures. Fourteen deterministic synthetic cases include missing-vs-null, invalid supplied types, explicit null optional fields, valid empty list, and Shadow-only compatibility.
- GREEN code commit `9db9ae89691b126b4085b457d75ed62ffd498d1e`, [Actions #40352546029](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40352546029): 1744/1744 pass; repository Skills and Eval fixture validators pass.
- Minimal behavior: only absent monitoring skips validation; supplied monitoring must be an object. Optional launch timestamp, when explicitly supplied, is parsed and must be timezone-aware. Material changes, when explicitly supplied, must be a list; an empty list is valid. Exploratory statuses retain unknowns. No new fields or dependencies.

## Source hierarchy and rejected imports

- [Amazon Ads budget/bidding rules](https://advertising.amazon.com/library/guides/budget-rules/) and [event-based bid rules, 2025-01-02](https://advertising.amazon.com/resources/whats-new/event-based-bid-rules-for-sponsored-products-advertisers) support that bid/budget control may vary over time. They do not define our `boundary_monitoring` field or certify continuous experiment isolation.
- [Amazon Attribution and campaign reporting](https://advertising.amazon.com/library/guides/intro-attribution-campaign-reporting) distinguishes reporting contexts; it is not an external attestation of our synthetic plan.
- Public candidates checked on 2026-10-26: KuudoAI/amazon_ads_mcp (74 stars, MIT, non-fork), OpenLineage/OpenLineage (2,724 stars, Apache-2.0, non-fork), langchain-ai/openevals (1,232 stars, MIT, non-fork). Checked recent push activity, open PR samples and recent public Actions, not exhaustive source/dependency/issue/security review. All rejected for import: stdlib suffices, adding dependencies would not prove source authenticity. No third-party code, prompts, schemas, workflows or templates copied. Unlicensed/restricted materials are principles-only.
- Practitioner discussion is hypothesis-generating only, not a platform rule or causal guarantee.

## Remaining boundary

A well-typed `Clean` monitoring claim still does not authenticate Amazon-native delivery or prove continuous rule execution across a comparison window. Requires authorized external source/readback lineage; this repository remains read-only/Suggest/Shadow, with all live writes delegated to an explicitly authorized Executor. Fifteen Skills unchanged.
