# Reused readback effective-time and evidence-status integrity — 2026-10-27

## Observed gap and priority

Starting main: `0ca02300acd3c64db0f8e9b4245b3973826bee56` (v1.97.0). PRs: none open. Recent main CI: [#40441020608](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40441020608) SUCCESS. Five relevant historical branches sampled, all zero ahead.

**P0 confirmed:** the comparator already rejects same `readback_id` with changed `observed_at` or changed material control `state`. However, one observation ID and one observation time could be reused to assert different control `effective_at` instants or contradictory `evidence_status` values while still producing `Comparable`. These are mutually incompatible provenance assertions for one readback. This defect is independent of previously fixed observation-time/state identity contradictions.

**P1 unresolved:** complete window-level schedule/event/budget rule execution and gaps in observation coverage. **P2 unresolved:** independent source authentication, metric/date/grain/attribution/currency comparability. **P3 unresolved:** bid/placement/budget interference and marginal profit causality.

## RED → GREEN

- Tests-only commit: `077767d6dcd9db6109d7d9e21e4013652442d52d`; [RED Actions #40445576097](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40445576097): 1921 unit tests, 5 FAIL, no new baseline errors. New deterministic cases cover bid/budget effective time mismatch, nanosecond mismatch, one-sided missing time, observed/derived status mismatch, equivalent timezone representations, distinct IDs, omitted legacy IDs, unchanged evidence and isolated bid treatment.
- Minimal production fix: `0bb42f303c9a8b00654fa008600403672f53ea1d`; [GREEN Actions #40445622542](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40445622542): 1921 PASS, Skill and Eval validators PASS.
- A reused non-null readback ID now requires identical effective UTC instants and evidence statuses for each shared control, in addition to pre-existing observation-time and state checks. One-sided null/missing effective time is not treated as unchanged. Distinct valid IDs, omitted/null IDs and offset-equivalent instants remain compatible.
- 15 Skills, no new schema, external dependency or Amazon Ads write surface. Classification change is MINOR because it strengthens decision safety.

## Source/implementation boundaries

[Amazon Marketing Stream](https://advertising.amazon.com/solutions/products/amazon-marketing-stream) documents hourly metrics and near-real-time campaign changes. [Sponsored Products budget best practices](https://advertising.amazon.com/library/guides/sponsored-products-budget-best-practices) documents automatic schedule/performance budget rules. [Global SP API](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns) illustrates marketplace-specific controls. [RFC3339](https://datatracker.ietf.org/doc/html/rfc3339) is the time syntax basis. None defines `source.readback_id` or proves that a snapshot came from Amazon; the ID contract is repository-owned.

[Public PPC anecdote, July 27 2026](https://www.reddit.com/r/FulfillmentByAmazon/comments/1v8abo9/127_acos_on_amazons_automated_bidding_rules_this/) suggests checking rule/placement interactions but is not verified platform behavior or a causal finding.

Reviewed prior SOURCES entries for OpenLineage (Apache-2.0), MetricFlow (Apache-2.0), OpenEvals (MIT), KuudoAI amazon_ads_mcp (MIT), Agent Skills (Apache-2.0) and Google Ads MCP (Apache-2.0). Fresh GitHub metadata confirms nonfork status and recent activity; full code, CI, issue/PR, security and dependency-license review is **not** claimed for this run. No integration: this deterministic comparison needs only Python standard library. No third-party code, prompts, schemas, workflows or templates copied; restricted or unlicensed material is not reused.

## Remaining limitation

Even perfect internal provenance consistency cannot prove continuous budget/bid/placement control states, full-window schedule-rule triggers, authentic API observations, or incremental economic outcomes. Keep Read-only/Suggest/Shadow; live mutation/retry/idempotency/reconciliation remains external to this repository.
