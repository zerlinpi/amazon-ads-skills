# Exact fractional-second Ready holdout chronology — 2026-10-27

## Scope and independent gap

Fresh main `a7a62fc3f9ab6ba436c171be1ccb4237b4c40ffc` (v1.93.0), latest main push Actions #40414819610 SUCCESS, no open PR. Reviewed recent commits, branch comparisons, Actions, 448-path tree, 15 Skills and relevant validators/tests/schemas/references/research/AGENTS/runtime manifests. Other directories inventoried, not claimed as exhaustively line-audited.

Ready holdout checks parsed RFC3339 timestamps with `datetime.fromisoformat` and compared Python datetimes. Python stores microseconds, truncating seven-plus fractional digits. Thus an isolation proof at `10:00:00.0000001Z` compared equal to a latest boundary check at `10:00:00Z`; the same defect affected launch verification and material scope change chronology. Existing `project_measurement_comparison_history.py` already preserves sub-microsecond ordering in a separate workflow, so this closes an independent parity gap, not a new time format restriction.

## RED → GREEN

- Initial tests-only `c7662fc7752c986fe312f38849624b4e8f13714f` demonstrated the parser limitation but over-constrained legitimate RFC3339 high precision; tests refined before final RED in `22e46b287532b9a05a6cf5a55e72a791324277c3`.
- Final RED: [Actions #40421697469](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40421697469) — 1868 tests, 6 FAIL, 0 ERROR; eight valid/legacy/exploratory cases PASS.
- Minimal GREEN `34bd6cbde493cf4e4dc6ad22f2ad62efae468458`: [Actions #40421775715](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40421775715) — 1868 PASS, Skill/Eval validators PASS. Regex captures the original arbitrary-length fraction, Python datetime normalizes whole seconds to UTC, and Decimal preserves exact fractional ordering. No external dependencies or changes to the Ready schema.
- Cases include seventh/ninth digits, offset-equivalent instants, later launch/isolation/material changes, valid high-precision equality, and omitted legacy/Shadow behavior.

## Sources, rights and rejected imports

[Python 3.12 datetime](https://docs.python.org/3.12/library/datetime.html) and [RFC3339](https://datatracker.ietf.org/doc/html/rfc3339) support the precision distinction. [Amazon budget/bidding rules](https://advertising.amazon.com/library/guides/budget-rules/) and [Marketing Stream v2 FAQ](https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/faq) support time-varying controls but do not authenticate this internal evidence. Source content is paraphrased, not copied.

New sampled projects: vanling1111/amazon-ads-api-python-sdk (3 stars, MIT, nonfork, last pushed 2026-05-30), dgerydp/amazon-ad-workbench (17, Apache-2.0, nonfork, 2026-03-23), saleweaver/python-amazon-sp-api (689, MIT, nonfork, 2026-10-26). Existing reviews: MetricFlow, OpenLineage, OpenEvals, Amazon Ads MCP, Agent Skills. No candidate supplies authenticated full-window control history or materially improves this dependency-free fix; none imported. Metadata sampling is not a full code/CI/issue/PR/security audit. No third-party code, prompts, schemas, workflows or templates reused. Reddit PPC anecdotes are hypotheses only.

## Limits and next gaps

This protects internal chronology, not external source authenticity or complete schedule/event/budget/placement-rule execution history. Prioritize (P0) bounded, source-bound, gap-detecting full-window control evidence; (P1) metric/source/date/grain/attribution/denominator comparability; (P2) cross-campaign control interactions and marginal contribution profit. Default Read-only/Suggest/Shadow, 15 Skills unchanged, external authorized Executor alone handles Ads writes.
