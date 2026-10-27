# Intervening SP optional budget evidence parity — 2026-10-27

## Verified nonduplicate gap

Initial main: `dec76412b9852433099eb558a615413397ce6b06`; main Actions #40483293494 SUCCESS, zero open PR, four sampled historical branches with zero ahead. Existing v1.104 budget-event validation checks supplied values but does not check before/after presence parity for optional base/effective budget or policy on Sponsored Products bid reviews. Synthetic positive budget-rule change events with a missing field on only one side incorrectly returned `Confounded` instead of `Unknown`. The defect is distinct from negative numeric values, invalid routing labels and prior event identity checks.

## Deterministic RED→GREEN and compatibility

- Tests-only commit `57fd389bf8fa90c5a344256237742611e8bcd8bd`; [RED Actions #40491508793](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40491508793): 2043 tests, 8 FAIL. Six cases exercise one-sided budget amount/policy; two initially proposed Amazon Business placement parity checks.
- First production fix `02aba1491c353665266283704e1ffae85c05b090`; [Actions #40491584220](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40491584220): 1 FAIL from an existing valid Amazon Business placement confounder test. One-sided placement presence can be a positively observed addition, so this blanket restriction was rejected.
- Corrected code and tests `33b4be37d1e4be9095c81702510238c39b66d787`; [GREEN Actions #40491683393](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40491683393): 2043 PASS, Skill/Eval validators PASS. Six negative budget-parity tests plus six compatibility cases. No live Amazon Ads API, mutation, or third-party dependency.
- Minimal implementation: on registered SP bid/budget event surfaces, require presence parity for `base_average_daily_budget`, `effective_daily_budget`, and `average_daily_budget_policy` in event before/after state. Budget-change surfaces already require all fields. On bid surfaces, both-absent optional fields remain compatible. Amazon Business placement addition/removal remains a confounder.

## Primary context and limits

Amazon Ads [schedule bid rules (Nov 6 2023)](https://advertising.amazon.com/resources/whats-new/schedule-based-bid-rules-available-for-sponsored-products), [hours-of-day budget rules (Nov 30 2023)](https://advertising.amazon.com/resources/whats-new/hours-of-day-available-for-schedule-based-budget-rules) and [Marketing Stream](https://advertising.amazon.com/library/guides/amazon-marketing-stream) support time-varying control observation. [Marketing Stream v2 FAQ](https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/faq) warns that delivery cadence is not data grain and that deliveries/restatements require reconciliation. None defines normalized `control_events` or certifies complete, independently authenticated event history. [Sep 8 2026 Reddit PPC change-logging anecdote](https://www.reddit.com/r/FulfillmentByAmazon/comments/1wap6f2/) suggests an operator logging hypothesis, not platform policy.

2026-10-27 sampled GitHub OpenLineage, OpenEvals, KuudoAI amazon_ads_mcp, MetricFlow, Agent Skills and MCP Servers: stars, nonfork status, last push and SPDX license, plus selected CI/PRs for the first three. All were previously reviewed in SOURCES; reject direct integration because no candidate authenticates this Ads event stream or improves this narrow stdlib check. NOASSERTION sources are abstract-principles only. No third-party code, prompts, schemas, templates or workflows copied. No full security/dependency-license/issue/mirror audit claimed.

## Remaining gaps

The optional event list cannot establish continuous Schedule/Event/Budget Rule history or completeness. Independent source authentication, missing interval detection, activation chronology, cross-control/retailer/placement consistency, measurement lineage and marginal profit causal confounders remain. Keep 15 Skills, no missing-to-zero, default Suggest/Shadow, and external authorized Executor for all writes/retries/idempotency/reconciliation.
