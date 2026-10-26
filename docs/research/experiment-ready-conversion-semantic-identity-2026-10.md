# Ready experiment conversion metric semantic identity — 2026-10-26

## Fresh read and gap ranking

Initial main: `c4f8b86635bfaa4e0a2b79295512a9374d2c68b1`, initial main Actions #40294573100 SUCCESS, no open PR. Relevant experiment and freshness branches sampled 0 ahead; 15 canonical Skills, 55 eval fixtures, 12 schemas, 144 pre-change test files, and no `knowledge/` directory. Reviewed README, AGENTS/CLAUDE, three runtime manifests, source/research index, schema, semantic validator, related tests and experiment references. Other directories received a structural inventory, not a claim of line-by-line audit.

- **P0 confirmed and fixed:** a Ready primary Purchases/Sales/ROAS metric or conversion guardrail could declare `metric_family: traffic` (or `Unknown`) to bypass the conversion attribution gate. Even when declared `conversion`, placeholder `attribution_family` and `semantic_version` were accepted as non-empty.
- **P1 external proof:** attribution provenance and Amazon Ads API responses still require an authorized independent source. Distinct strings alone do not authenticate a source.
- **P2 causal continuity:** full-window bid/budget/event rule history, cross-campaign interference and contribution-profit incrementality remain unproven.

## Reproducible RED to GREEN

Synthetic tests: `tests/test_experiment_ready_conversion_semantic_identity.py`. RED commit `28abfc14c5af075973556045dd0dcb794911a6e7`, [Actions #40301701019](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40301701019): 1652 tests, 7 FAIL. The blank-family test and compatibility cases already passed. Minimal production fix `533a4dd76f2a4eedc52005334fe5ed747635c65e`; whitespace normalization correction `d10701ffd781281f82ef96bff89f6ffb6ae084f8`; positive not-applicable regression test `2c156db5e53e46171ea8051f74eec888d00be9dd`. [GREEN Actions #40301895414](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40301895414): 1653/1653 PASS, 15 Skills, 55 eval fixtures.

Behavior is intentionally narrow: detect obvious conversion names regardless of a contradictory declared family, require an actual `conversion` family and concrete unpadded attribution family and semantic version. Whole-label Unknown/Partial/Missing/Not Supported/Not Applicable fail closed; valid opaque versions containing these words as substrings, non-conversion metrics and exploratory Shadow/Hold remain compatible. No schema fields, dependency, Skill count, remote Ads write or Executor behavior changed.

## Public platform evidence (not an internal field specification)

- [Amazon Ads view attribution update, 2026-01-01](https://advertising.amazon.com/resources/whats-new/view-attribution-updates-for-amazon-store-ads/): standard Purchases, Sales and ROAS may use a changed view attribution method for specified inventory; eligible all-views metrics remain separate. This is not a universal change to all campaign types or click attribution.
- [Amazon Ads Unified Reporting, 2026-06-08](https://advertising.amazon.com/en-gb/resources/whats-new/streamline-campaign-analysis-with-unified-reporting): cross-account/product/dimension reporting increases the need for explicit metric identity, not license to mix attribution families.
- [Amazon Ads Marketing Stream v2 converted product dataset](https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/datasets/ads-converted-product): distinct purchases/sales and multi-touch metrics must not be silently treated as the same semantic identity.
- [Amazon Ads reporting account authorization](https://advertising.amazon.com/API/docs/en-us/guides/reporting/dsp/creating-reports): account/profile authorization context is distinct from internal semantic labels.
- [Amazon Ads event bid rules, 2025-01-02](https://advertising.amazon.com/resources/whats-new/event-based-bid-rules-for-sponsored-products-advertisers) and [budget rules, 2021-08-12](https://advertising.amazon.com/resources/whats-new/dynamic-budget-control) illustrate time-varying controls, not proof of experiment isolation.

## GitHub and community candidate disposition (sampled 2026-10-26)

- [langchain-ai/openevals](https://github.com/langchain-ai/openevals): 1,231 stars, MIT, non-fork, pushed 2026-10-22; sampled Actions SUCCESS / ACTION_REQUIRED, open PRs #291/#283 and issue #290. **Reject dependency/code import**: evaluation framework cannot resolve caller-supplied attribution identity.
- [braintrustdata/autoevals](https://github.com/braintrustdata/autoevals): 1,068 stars, MIT, non-fork, pushed 2026-10-22; sampled Actions ACTION_REQUIRED, open PRs #254/#252. **Reject**: no demonstrated improvement over deterministic local gate.
- [KuudoAI/amazon_ads_mcp](https://github.com/KuudoAI/amazon_ads_mcp): 74 stars, MIT, non-fork, pushed 2026-10-14; sampled Actions SUCCESS, open PRs #104/#101. **Reject**: connector implementation does not independently authenticate this repo's declared metric semantics.
- [OpenLineage/OpenLineage](https://github.com/OpenLineage/OpenLineage): 2,722 stars, Apache-2.0, non-fork, pushed 2026-10-25; large external framework unnecessary for this local invariant.
- [Imsamiullah09/amazon-ads-mcp](https://github.com/Imsamiullah09/amazon-ads-mcp): 0 stars, MIT, non-fork, pushed 2026-06-10; no demonstrated tested advantage. **Reject**.

Stars, issue/PR and two-run CI samples are metadata observations, not complete code, dependency-license, fork-mirror, security or correctness audits. All third-party code/prompts/schemas/workflows/templates are excluded; no-license/NOASSERTION sources are abstract-principles-only. [Public AmazonFBA PPC strategy discussion, 2026-09-29](https://www.reddit.com/r/AmazonFBA/comments/1wt55bx/my_ppc_strategy_what_is_yours/) suggests operator hypotheses, not Amazon Ads policy, universal thresholds or causal evidence.

## Safety

Maintain source, metric, date, grain, profile/campaign identity and connector capability; separate Observation, Hypothesis, Cause, Action and Outcome. Never turn Missing/Unknown/Partial/Unsupported into zero. Preserve confounders, marginal economics, control interactions and Read-only/Suggest/Shadow; any live Amazon Ads write, retry, idempotency and reconciliation belongs to an external explicitly authorized Executor.
