# Ready combined-readout requirement identity — 2026-10-27

## Fresh baseline and independently reproduced gap

Main `2e6c95755d6a5617a9d44f025cabd5461b30bddc` (v1.87.0), main Actions #40362826294 SUCCESS, no open PR, 15 canonical Skills. Historical aggregation branches inspected and zero commits ahead. Existing `_validate_ready_combined_readout_semantics` only gated when `comparison.get("requires_combined_readout") is True`, so explicitly null, Unknown, Partial, numeric, list and object values bypassed the ratio KPI checks while `Ready`. This is a new readout-requirement identity gap, distinct from known-ratio classification and explicit unknown metric names.

## Deterministic RED→GREEN

- RED `f9646ea99d354aa21c705be0b98abac5cf81bb1d`, [Actions #40371547946](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40371547946): 1775 tests, 8 FAIL, four new compatibility cases passed.
- GREEN `472dc5c7e3ee8edbca2af96ff358f568c0a2387b`, [Actions #40371654073](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40371654073): 1775 PASS; Skill and Eval validators PASS.
- Minimal fix checks explicit presence and exact bool type before returning for false or omission. True still enforces ratio/derived semantics. Explicit false and omitted legacy fields remain compatible; exploratory plans retain unknown evidence. No new Skill, schema, dependency, or live Ads writes.

## Source and license decisions

- [Amazon Ads campaign reporting](https://advertising.amazon.com/library/guides/intro-attribution-campaign-reporting), [multi-touch attribution](https://advertising.amazon.com/resources/whats-new/uncover-ad-value-across-funnel-with-multi-touch-attribution), and [2026 view-attribution update](https://advertising.amazon.com/resources/whats-new/view-attribution-updates-for-amazon-store-ads/) confirm changing and distinct metric semantics; they do not define internal JSON boolean fields or validate data source comparability.
- GitHub metadata re-review: dbt-labs/metricflow (1,848 stars, Apache-2.0, non-fork, pushed 2026-10-13), OpenLineage/OpenLineage (2,724, Apache-2.0, non-fork, pushed 2026-10-25), langchain-ai/openevals (1,232, MIT, non-fork, pushed 2026-10-22), KuudoAI/amazon_ads_mcp (74, MIT, non-fork, pushed 2026-10-14), modelcontextprotocol/servers (91,588, NOASSERTION, non-fork, pushed 2026-10-25). These are already reviewed in SOURCES; no additional dependency or third-party code/prompt/schema/workflow/template reused. Stars and sampled metadata are not a full code, CI, issue, security or transitive license audit.
- Operator/community claims remain hypotheses, not Amazon policy or causal proof.

## Remaining boundaries

Internal boolean identity does not prove a combined readout is actually required, authenticate data source, metric/date/grain/attribution/currency, verify row disjointness or denominator completeness, establish experiment isolation or authorize writes. Next inspect source-provenance attestation, continuous bid/budget-rule history and cross-campaign causal interaction; do not turn unknowns into zero.
