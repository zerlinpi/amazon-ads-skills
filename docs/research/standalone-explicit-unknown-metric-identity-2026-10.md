# Explicit unresolved standalone aggregation metric identity — 2026-10-27

## Fresh baseline and independent gap

Initial main `745ee62cd488713e7e076a0ef64952b853999b02`, v1.86.0, main Actions #40353209318 SUCCESS; no open PR. Relevant historical aggregation branches were zero ahead. All 15 Skills retained. The standalone gate returned `Allowed` for `additive` and `disjoint` with an **explicitly supplied** `metric_name` of null, blank, whole-label Unknown/Partial/Unsupported/Not Available/N/A or non-string. This is separate from the previously repaired known-ratio name contradiction.

## RED → GREEN

- RED `ae3ef9647afd3dba7104725609d468521625c8ee`: [Actions #40362141223](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40362141223), 1763 tests, 12 FAIL; seven new compatibility cases passed.
- Initial minimal fix `ef404a8ce3e096d5ec489f9c9d916bb423f95c28`: two placeholder separator normalization failures (Actions #40362273634). Corrected regex `381d2d79d86ffa586e1f54f36e0cdd348f615941`: [Actions #40362301091](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40362301091), 1763 PASS, Skills/Evals PASS.
- Explicit unresolved additive identity returns `Unknown`, never direct-sum Allowed. Omitted legacy name, valid concrete Spend/Impressions, known ratio blocking, overlapping rows, unknown semantics, and placeholder substrings in concrete names remain compatible. No source authentication or aggregation is performed.

## Sources, open-source and licensing

- [Amazon Ads metric glossary](https://advertising.amazon.com/en-us/library/guides/basics-of-success-understanding-amazon-advertising) and [reporting overview](https://advertising.amazon.com/library/guides/intro-attribution-campaign-reporting) define public advertising metrics, not the internal `metric_name` validation contract.
- Public GitHub metadata review: dbt-labs/metricflow (Apache-2.0 metadata, ~1,848 stars, non-fork, pushed 2026-10-13, active PRs, latest sampled Actions `action_required`), OpenLineage/OpenLineage (Apache-2.0, ~2,724 stars), langchain-ai/openevals (MIT, ~1,232 stars, sampled workflow success), KuudoAI/amazon_ads_mcp (MIT, 74 stars), modelcontextprotocol/servers (NOASSERTION, ~91,588 stars). No dependency adopted or third-party code/prompt/schema/workflow/template copied. This was not a full code, dependency-license, issue or security audit.
- [Public Reddit PPC discussion](https://www.reddit.com/r/FulfillmentByAmazon/comments/1jemras) is an anecdotal hypothesis source, not a platform specification or proof of incrementality.

## Safety and next gap

No new Skills, schemas, dependencies or Amazon Ads writes. Unknown/Partial/Missing/Unsupported never become zero. The check cannot prove authenticated metric identity, row disjointness, source component completeness, date/grain/currency/attribution compatibility or causal profit. External authorized Executor retains write/retry/idempotency/reconciliation authority. Next prioritize external provenance, continuous schedule/event/budget rule history and cross-campaign control interference.
