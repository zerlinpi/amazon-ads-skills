# Reused control-state readback identity — 2026-10-27

Initial main `d3a3efbd115154958bae6a56c7e0c3ffe8e3c394`, v1.95.0; main Actions #40428378491 SUCCESS; no open PR. Read all 15 Skills, relevant comparator/schema/tests/references, repository instructions, manifests, SOURCES/research; inventoried 412 files, 20 scripts, 160 tests, 12 schemas, 89 research entries, 27 references, 58 eval paths, one playbook, no knowledge directory. Six sampled old branches were zero ahead. Inventory is not a line-by-line audit.

## Gap and deterministic RED → GREEN

The existing `source.readback_id` denotes one observed readback, not a reusable campaign/connector identity. Baseline/post snapshots could reuse the same explicit non-null ID with different material bid/budget/rule/placement states, yet the comparator could claim `Treatment Isolated` or `Confounded`. This is a source-identity contradiction, not the previous holdout chronology issue.

- RED `a45f2530f23fd0de54157a79b527e4bf345f977e` ([Actions #40434390981](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40434390981)): 1891 tests, 4 FAIL, 0 ERROR; five compatibility tests passed.
- GREEN `1e68bda948ddbc6a4b960b187e9153c67fc5b455` ([Actions #40434481521](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40434481521)): 1891 PASS, Skill/Eval validators PASS.
- Both-supplied same non-null readback ID plus changed material states => `Unknown`. Distinct IDs, omitted/one-sided legacy IDs, unchanged states retain behavior. No new schema, dependency, Skill, API authentication or Ads writes.

## Sources and rights

Official [budget and bidding rules](https://advertising.amazon.com/library/guides/budget-rules), [schedule bid rules](https://advertising.amazon.com/resources/whats-new/schedule-based-bid-rules-available-for-sponsored-products), [Marketing Stream v2](https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/overview) contextualize time-varying controls/report restatements, not internal readback identity. Sampled GitHub metadata 2026-10-27: OpenLineage 2726/Apache-2.0, MetricFlow 1848/Apache-2.0, OpenEvals 1232/MIT, KuudoAI amazon_ads_mcp 74/MIT, Agent Skills 26668/Apache-2.0; nonfork, sampled Actions and open PRs, not full security/license audits. No imports: stdlib check sufficient. No third-party code/prompts/schemas/workflows/templates copied. Public PPC cases are hypotheses, not platform norms.

## Next gaps

P0 complete, source-bound schedule/event/budget/placement execution intervals and gap detection; P1 authenticated connector/source, date/grain/currency/attribution/denominator comparability; P2 cross-campaign interference and marginal profit causality. Suggest/Shadow by default; external authorized Executor only.
