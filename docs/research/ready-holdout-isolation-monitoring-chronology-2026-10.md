# Ready holdout latest monitoring / isolation verification chronology — 2026-10-27

## Verified gap and scope
Fresh main 03f1ee5ae0e9edf1cfcd22b299347364c4513b9e, v1.92.0, Actions #40407574049 SUCCESS; no open PR. Inventoried 446 paths, all 15 Skills, relevant tests/scripts/schema/references/research/runtime manifests; eight relevant old branches had zero commits ahead. A Ready holdout with latest clean monitoring 10:00Z and verified isolation evidence 11:00Z incorrectly passed. This is independent of RFC3339 syntax validation.

## RED → GREEN
- RED 1ffd1edf70f27a9f54cf5ca66e42d907e690ed40, [Actions #40414421617](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40414421617): 1854 tests, 5 FAIL, 0 ERROR; six compatibility cases passed.
- GREEN 57c998ae97e706f79a253fe58045a23ad754401c, [Actions #40414491229](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40414491229): 1854/1854 PASS; Skill/Eval validators PASS.
- Minimal fix collects valid positively verified isolation instants, then compares to supplied latest monitoring in UTC. No extra parsing errors, optional legacy requirements, new Skill/schema/dependency, or Ads writes.

## Sources and rights
[Amazon Ads budget/bidding rules](https://advertising.amazon.com/library/guides/budget-rules/), [event-based rules (2025-01-02)](https://advertising.amazon.com/resources/whats-new/event-based-bid-rules-for-sponsored-products-advertisers), and [Marketing Stream guide](https://advertising.amazon.com/library/guides/amazon-marketing-stream) establish time-varying controls and hourly data, not this internal contract or continuous control proof. Re-reviewed KuudoAI/amazon_ads_mcp (74, MIT), MetricFlow (1848, Apache-2.0), OpenLineage (2726, Apache-2.0), OpenEvals (1232, MIT), Agent Skills (26665, Apache-2.0), googleads/google-ads-mcp (1078, Apache-2.0, different platform), jhrendon/amazon-mcp (2, no detected SPDX license). Sampled metadata and CI/PRs, not full security, issues or dependency-license audit. Rejected all imports; no third-party code, prompts, schemas, workflows or templates copied. Reddit anecdotes are not standards.

## Next falsifiable gaps
P0 authenticated, interval-complete schedule/event/budget-rule and placement control history with gaps/trigger/timezone coverage. P1 source/metric/date/grain/identity/currency/attribution/denominator comparability. P2 cross-campaign budget/auction interference and marginal contribution economics. Two timestamps do not prove continuous control; default Read-only/Suggest/Shadow, authorized external Executor only for writes.
