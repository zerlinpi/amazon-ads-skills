# Ready experiment retail metric name boundary — 2026-10-26

## Confirmed gap and baseline

Fresh main HEAD `ffd33c8abaa8f9fe4b8070eaf4642f5a1268c6d7` (v1.82.0); no open PR. Three older experiment branches were behind main with zero ahead commits. `_is_conversion_metric()` matched `sale` as a substring, so a Ready experiment using Total Retail Sales, Retail Sales, Organic Sales, Sales Rank or Wholesale Traffic was incorrectly required to claim an ad-attributed conversion family and attribution version. This is distinct from earlier changes that stopped genuinely attributed Sales, Purchases, ACOS and ROAS from hiding behind non-conversion families.

## RED → GREEN

- RED commit `958827676f9c9613f3c22c7b2681e93eea01cdcd`, [Actions #40327402552](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40327402552): 1696 tests, 6 expected FAIL; 8 new safety/compatibility tests PASS.
- Minimal code change `5e9dcb9a8baf88734f303a2cca1be639abdc909b`, regex escape correction `4251870e93e694e3acc8e846c14a1adf9fb9d6e7`, [GREEN Actions #40327563792](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40327563792): 1696/1696 PASS, Skill validator PASS, Eval validator PASS.
- Use bounded whole-label exceptions for explicitly non-ad retail/rank names, and token boundaries for Sales. Preserve the conversion gate for ambiguous Sales/Total Sales, Ad-Attributed Sales, Purchases, and any explicitly declared conversion family. Apply to primary and guardrail metrics. No change to 15 Skills, schema, mode or Executor.

## Official source evidence and limits

- [Amazon Ads attribution versus retail sales](https://advertising.amazon.com/help/GX7KDKHMWQYMJ385): attributed campaign sales and retail sales differ in timing/definitions.
- [Amazon Ads TACOS guide](https://advertising.amazon.com/en-ca/library/guides/common-holiday-advertising-myths): total sales include organic and paid, distinct from ad-attributed ACOS sales.
- [Amazon Seller BSR, published 2025-09-03](https://sell.amazon.com/blog/amazon-best-sellers-rank): Best Sellers Rank is a category-relative rank, not an attributed order count.
- This is only internal semantic-name consistency. It cannot validate retail/ads source authenticity, currency, date, grain, attribution maturity, total-sales coverage, holdout isolation or causality.

## Open-source adoption/rejection and copyright

GitHub metadata observed 2026-10-26: KuudoAI/amazon_ads_mcp (74 stars, MIT), denisneuf/python-amazon-ad-api (203, MIT), langchain-ai/openevals (1,231, MIT), OpenLineage/OpenLineage (2,724, Apache-2.0), agentskills/agentskills (26,643, Apache-2.0), modelcontextprotocol/servers (91,578, NOASSERTION). Sampled fork flags, push recency, Actions and open PRs; not a full code, CI, issues, dependency, security or license audit. Reject runtime/framework imports because a local deterministic check resolves this narrow defect. No code, prompts, schemas, workflows or templates copied; unclear licenses are not permission to reuse. Practitioner anecdotes are hypotheses, not platform specifications.

## Next real gaps

1. External authenticated measurement/retail-source lineage and component-level ratio recomputation.
2. Full-window schedule/event/budget-rule execution evidence.
3. Cross-campaign control interaction, overlap and marginal-profit causality.
