# Intervening SP rule activation metadata parity — 2026-10-27

## Fresh gap and priority

Main `40b62ffeb00b6e0e6261f86909ea54d13a5c2f29` had a successful push Actions #40516198444 and zero open PRs. Three relevant historical branches had zero commits ahead. The endpoint comparator already required optional activation metadata parity on shared rule IDs, but the newly introduced mid-window event path did not call the same guard. An event could show a common rule with `activation_status` or `activation_effective_at` present on only one side and still return `Confounded` for an otherwise isolated bid change. A missing value is not a verified activation transition.

## Deterministic RED → GREEN

- Tests-only `5690d1fe5720f5302328cbab65e6e7ccb3af3295`: [Actions #40523992555](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40523992555) — 2078 tests, 6 FAIL, five new compatibility cases passed. Cases cover both directions of status and effective-time one-sidedness across schedule/event bid rules and active budget rules.
- Minimal implementation `b092b4481cdc703197e2b17007f917d2bebeac09`: [Actions #40524098654](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40524098654) — 2078/2078 PASS; Skill validator 15 PASS; Eval validator 55 PASS. Reuses `_rule_activation_presence_problem` on paired event states only for registered Sponsored Products bid/budget surfaces. No new schema field or dependency.
- Valid status/effective-time changes, both-absent metadata, and genuinely new rule IDs remain compatible. The event log is optional and non-exhaustive; this fix cannot certify full-window control stability or source authenticity.

## Evidence and licensing

Amazon official announcements: [schedule bid rules, 2023-11-06](https://advertising.amazon.com/resources/whats-new/schedule-based-bid-rules-available-for-sponsored-products), [event bid rules, 2025-01-02](https://advertising.amazon.com/resources/whats-new/event-based-bid-rules-for-sponsored-products-advertisers), [hour-of-day budget rules, 2023-11-30](https://advertising.amazon.com/resources/whats-new/hours-of-day-available-for-schedule-based-budget-rules). They establish time-varying platform controls, not this repository-owned normalization. [Marketing Stream v2 FAQ](https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/faq) warns that delivery cadence, record grain, multipart delivery and restatement versions must be distinguished; it does not certify a complete rule transition log.

Sampled GitHub metadata on 2026-10-27: OpenLineage 2727 stars/Apache-2.0, OpenEvals 1233/MIT, KuudoAI Amazon Ads MCP 74/MIT, Agent Skills 26693/Apache-2.0, Promptfoo 26495/MIT. All nonfork; recent commit/PR and selected Actions checked, not full security, issues, code, CI, mirror or transitive-license audits. Previously researched; no third-party code, prompt, schema, workflow or template imported. The stdlib parity helper suffices, and these projects do not authenticate Amazon event evidence. Restrictive/no-license sources are abstract-principles only. Low-vote Reddit PPC dayparting anecdotes are hypotheses, not platform standards or causality proof.

## Next real gaps

P0 remains authenticated complete time-window control history (missing intervals, source event provenance, rule trigger/actual effective time, restatements). P1 is further cross-control and partial collection evidence; P2 is connector source/metric/date/grain/currency/attribution identity; P3 is cross-campaign interaction and incremental contribution profit. Do not fabricate completeness from empty event lists or coerce missing/partial/unsupported/unknown into zero. Keep 15 Skills, Suggest/Shadow default and external authorized Executor for live writes/retries/idempotency/reconciliation.
