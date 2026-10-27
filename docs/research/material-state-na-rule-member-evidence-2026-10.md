# N/A material-state and rule/audience member evidence — 2026-10-27

## Reproducible gap

At main `1daa3992190480c382db5105ae74b1168c280b06`, the generic material-state sentinel gate rejected Unknown, Missing, Unsupported and Partial, but not N/A or Not Applicable. Complete/observed nested states and Sponsored Products schedule/event/budget rule or audience member IDs with those exact labels could be treated as unchanged controls, incorrectly returning `Treatment Isolated`. This is distinct from the v1.99 scope/source identity check.

## Deterministic verification

PR #214, branch `fix/material-state-na-rule-member-evidence-20261027`.
- RED commit `7b66c043256d95376c3d3c0f9e00f3e1eeb887eb`: 1970 tests / 12 FAIL, [Actions #40463277508](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40463277508).
- GREEN commit `d0ccfd996b1d3c28d252b7add1fdcd9b6cd4682b`: 1970 tests PASS and Skill/Eval validators PASS, [Actions #40463362413](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40463362413).
- Seventeen synthetic cases cover exact labels, hyphen/underscore/tab variants, nested and complete list states, schedule/event/budget rule IDs, audience IDs, genuine zero/false, valid opaque substrings and confounding changes.
- Minimal fix extends the existing recursive reserved-state labels; no schema, dependency, new Skill or Ads write.

## Sources, licensing and boundaries

Amazon Ads official budget/bidding rule and Marketing Stream guides describe automatic, time-varying controls and hourly reporting, but do not define this repository's normalized sentinel labels or certify continuous rule execution. July 2026 Reddit anecdote is a hypothesis only. OpenLineage, MetricFlow, OpenEvals, KuudoAI Amazon Ads MCP, Agent Skills and Google Ads MCP were sampled for license, fork, stars and recent activity; selected Actions and open PRs sampled. They were rejected as unnecessary dependencies for a deterministic local guard. No external implementation copied. See `docs/SOURCES.md` for URLs, review limitations and copyright boundaries.

## Next gap

Continuous Schedule/Event/Budget Rules time-window coverage, authenticated source readbacks, complete reporting lineage and incremental contribution-profit causal checks remain unresolved. Keep Read-only/Suggest/Shadow and external authorized Executor.
