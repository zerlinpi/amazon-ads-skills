# Sponsored Products causal campaign identity — 2026-10-26

## Fresh-read and prioritized gap

At main `2db5c486344979d3d844257ffa5fccdaf8a6730e` (v1.70.0), no open PR and successful main Actions #40241884989, the read-only `compare_control_state` comparator checked optional campaign IDs only when they differed. For registered SP bid/budget causal comparisons, two snapshots with the same profile/marketplace but both omitting `scope.campaign_id` could return `Treatment Isolated`. A shared profile cannot prove that a campaign-specific bid/budget treatment belongs to the same campaign.

Existing branches `automation/bid-rule-lineage-20260920`, `automation/control-observability-binding-20260921`, `automation/experiment-aggregation-semantics-20260919` and the prior feature-eligibility branch were all 0 commits ahead of main. An earlier candidate rule-id placeholder test was rejected: PR #183 (closed, not merged), Actions #40246631610 passed unchanged production code because recursive material-state validation already rejects those placeholders. This avoids duplicate development.

## Deterministic RED→GREEN

- RED commit `d2a58cb88d5420a53c6c4d72e274b0e3b61a0465`: [Actions #40246750015](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40246750015), 1558 unit tests, 4 FAIL. Both-absent and explicit-null campaign IDs, including an entity-scoped pair, were incorrectly classified as isolated.
- Minimal code commit `49d49d3fbbaf59bb27315d61d8578b99e2276399`: [Actions #40246791399](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40246791399), 1558/1558 unit PASS, 15 Skills PASS, 55 eval fixtures PASS. Seven synthetic tests include valid opaque IDs, one-sided missing and existing compatibility.
- The fix is restricted to registered `sponsored_products_bid_change` and `sponsored_products_budget_change`; it reuses the existing concrete-identity helper, adds no external dependencies, Skills, schema fields, live Ads writes, retries, idempotency or Executor behavior.

## Platform facts, candidate review, copyright

Amazon Ads [Global Sponsored Products campaign API](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns) documents campaign identity, marketplace-specific configurations and distinct account context; [MCP account context](https://advertising.amazon.com/API/docs/en-us/mcp/get-started) distinguishes profile/advertiser/manager IDs. [Schedule bid rules (2023-11-06)](https://advertising.amazon.com/resources/whats-new/schedule-based-bid-rules-available-for-sponsored-products), [event bid rules (2025-01-02)](https://advertising.amazon.com/resources/whats-new/event-based-bid-rules-for-sponsored-products-advertisers), and [budget rules (2021-08-12)](https://advertising.amazon.com/resources/whats-new/dynamic-budget-control) establish time-varying campaign controls, not this repository's evidence schema. No Amazon native `campaign_id` validation grammar or rule-execution guarantee is inferred.

GitHub metadata sampled 2026-10-26: `KuudoAI/amazon_ads_mcp` 74 stars / MIT / non-fork / pushed 2026-10-14 / tests and recent successful CI / open PRs; `OpenLineage/OpenLineage` 2722 / Apache-2.0 / non-fork / pushed 2026-10-25 / active CI; `agentskills/agentskills` 26616 / Apache-2.0 / non-fork / pushed 2026-08-09; `ppcprophet/amazon-ads-mcp` 5 / GitHub MIT code / non-fork / pushed 2026-02-04 / no sampled Actions (its hosted service describes proprietary access); `cprice70/amazonads-mcp` 3 / no GitHub license / non-fork / pushed 2026-03-03 / sampled CI successful. Stars, tests and CI do not prove account data authenticity. This is not a complete security/dependency/issue audit. No third-party code, prompt, schema, workflow or template copied. An absent license is not a reuse grant; an open-source client does not license its hosted service.

[Reddit PPC campaign-structure discussion (2026-10-20)](https://www.reddit.com/r/AmazonFBA/comments/1xayhyy/the_campaign_structure_id_use_at_310kmonth_ad/) was treated only as an operator hypothesis about overlapping campaign traffic, not platform policy or causal proof. The narrow identity fix is repository-authored and evidence-backed.

## Next gaps

1. Authenticated, externally authorized feature-eligibility raw-response reconciliation requires a real trust root; distinct normalized source labels cannot provide it.
2. Continuous rule activation and trigger/timezone coverage over comparison windows remain unproven by two endpoint snapshots.
3. Cross-campaign control interactions, retail readiness, and marginal-profit/attribution confounders still require independent evidence.
