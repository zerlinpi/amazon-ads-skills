# Connector unknown-scope final gate classification — 2026-10-25

## Baseline and nonduplicate gap

At main `d00fd023c189d493496598b4829f725015dba5a4` (v1.59.0), zero open PRs; sampled old branches had no commits ahead of main. PR #171 correctly distinguished observed unknown scope members from fully concrete exclusions in `_scope_effect`, but the outer capability gate still returned `Blocked` for **all** non-pass scope effects. Thus `["US", "Unknown"]` with requested JP reported a definitive blocked capability rather than uncertainty. The old test asserted only `scope_effect=unknown` and no high confidence, so missed the final decision classification. This is distinct from earlier scope parsing and connector identity repairs.

## RED → GREEN

RED commit `1e8bbe031ee918cff0022d06d8c59fc19626e66f` [Actions 40194559495](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40194559495): 1407 tests, six failures, all new final-gate classification assertions. Minimal production fix `e94535bd29acadad70633cb33e6e63ff32f86328` [Actions 40194643701](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40194643701): 1407 tests PASS; Skill and Eval validators PASS. Ten synthetic cases cover unknown-only, mixed, null, blank, malformed, Partial, omitted scope, concrete mismatch/match and binding unknown. No live Ads reads/writes.

## Behavior boundary

Only a present nonempty scope with unmatched unknown/malformed members can degrade rather than assert verified exclusion. Missing/unbounded capability scope continues to block (never assume global access), as does a fully concrete mismatch or an Unsupported capability. The internal third return value of `_scope_effect` tracks whether uncertainty comes solely from observed unusable members, not from missing fields; the public `scope_effect` label remains unchanged. A Verified Binding still must match independently. Degraded is not proof of support, missing metrics are not zero, and nothing grants account entitlement or write authority.

## Sources and licensing

Official [Amazon Ads MCP account context](https://advertising.amazon.com/API/docs/en-us/mcp/get-started), [advertiser eligibility](https://advertising.amazon.com/API/docs/en-us/mcp/eligibility), [advertiser product-group eligibility](https://advertising.amazon.com/API/docs/en-us/mcp/advertiser-product-group-eligibility) and [Amazon Business exclusive SP launch (2025-05-05)](https://advertising.amazon.com/en-gb/resources/whats-new/amazon-business-exclusive-campaign-for-sponsored-product) establish account/marketplace-specific checks, not this repository's evidence enum. Reviewed GitHub metadata for KuudoAI/amazon_ads_mcp (MIT, 74 stars), denisneuf/python-amazon-ad-api (MIT, 203), promptfoo/promptfoo (MIT, 26,404) and OpenLineage/OpenLineage (Apache-2.0, 2,721): non-forks with sampled recent CI, but none is a necessary or sufficient dependency for this local classification. These are partial observations, not exhaustive security/PR/issue audits. No external code or prompt/schema/workflow copied. Reddit anecdotes about site routing are hypothesis sources only.

## Next evidence gap

P0 advertiser/marketplace/campaign eligibility must be bound to a specific account, campaign, connector, verified time and source; a connector scope list alone cannot prove entitlement. P1 continuous rule-activation evidence, P2 authenticated raw Adapter HTTP provenance, P3 causal control interaction and marginal economics.
