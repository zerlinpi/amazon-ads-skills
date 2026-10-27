# Nested null material-control evidence — 2026-10-27

## Verified gap and RED→GREEN

Fresh main `3f91fe2abaffc35da3a9091e51667f9632709a02`, successful main Actions #40491907842, no open PR. The recursive `_explicit_material_state_problem` rejected placeholder strings and nonfinite values but silently accepted Python `None` / JSON `null` at nested object/list leaves. Two observed Complete endpoints could return `Treatment Isolated` despite the same unknown nested material value; a positive mid-window event with null could return `Confounded`.

Tests-only `f15065538febbac1293774bc629fd6b413493fdf`, Actions #40499231832: 2050 tests, 4 FAIL. Minimal fix `da257cb33ef0a5b42732a9f74b0d709b6c2fb8e9`, Actions #40499291654: 2050 PASS, Skill/Eval validators PASS. Seven synthetic tests: two endpoint nested-null, two event-side nested-null, and three compatibility cases for observed zero/false, omitted optional field, and null provenance outside material state. No Amazon Ads calls or writes.

## Sources, limits and copyright

[Amazon Marketing Stream v2 FAQ](https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/faq) distinguishes metric null from measured zero, record grain from delivery cadence, and versioned restatements. This does **not** define this repository's normalized control-state schema. [Amazon Sponsored Products best practices](https://advertising.amazon.com/library/guides/sponsored-products-best-practices) describes separately managed bids, budgets and placements. Neither authenticates an event stream or proves full-window coverage. [Oct 26 2026 Reddit PPC data-ownership anecdote](https://www.reddit.com/r/AmazonFBA/comments/1xfzdeb/) is an unverified hypothesis about the value of change logs, not platform policy or measured ROI.

Sampled GitHub metadata Oct 27: OpenLineage/OpenLineage 2727 stars, Apache-2.0, nonfork, pushed Oct 25 (recent Actions success/open PRs); langchain-ai/openevals 1233, MIT, nonfork, pushed Oct 22 (recent PR Actions action_required/open PRs); KuudoAI/amazon_ads_mcp 74, MIT, nonfork, pushed Oct 14 (recent Actions success/open PRs); agentskills/agentskills 26689, Apache-2.0, nonfork, pushed Aug 9; langfuse/langfuse 36584, NOASSERTION, nonfork, pushed Oct 27. This is a metadata and selected CI/PR sample, not an exhaustive code, tests, issues, security, fork/mirror or transitive-license audit. Adopt abstract lineage and deterministic regression-testing principles only. Reject dependencies: existing Python stdlib is sufficient and none independently authenticates Amazon Ads events. NOASSERTION is not permission to copy. No third-party code, prompts, schemas, workflows, templates or protected prose reused.

## Safety

15 Skills unchanged. Null/unknown/unsupported/partial never become zero. Preserve source/metric/date/grain/identity/connector capability, Observation/Hypothesis/Cause/Action/Outcome, confounders, control interaction and marginal economics. Default Read-only/Suggest/Shadow; external authorized Executor owns live Ads writes, retries, idempotency and reconciliation. Omitted/empty events never prove complete history.
