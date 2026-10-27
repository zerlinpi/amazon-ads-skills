# Explicit material-change re-verification chronology — 2026-10-27

## Evidence and independent gap

Fresh main `3dcae025753006b38ccab5f927b7aa6361e7f2cf` (v1.94.0), main Actions #40421995788 SUCCESS; zero open PR. Read recent commits, 450-path tree, all 15 canonical Skills, relevant validator/tests/schema/references/research and Codex/Claude Code/WorkBuddy manifests. Eight sampled old feature branches were zero commits ahead of main. Other repository areas inventoried, not claimed as fully line-audited.

Ready holdout monitoring already requires a material change's `reverified: true` and checks the change timestamp against the latest clean boundary check. But an explicitly supplied `material_scope_changes[].reverified_at` was ignored. A record could claim re-verification *before* the change, *after* the latest clean check, or provide null/Unknown/unknown-offset time and still pass Ready. This is a distinct contradiction from the prior exact-fractional timestamp fixes.

The backward-compatible contract checks only explicitly supplied `reverified_at`: known-offset RFC3339, `change.timestamp <= reverified_at <= latest_verified_at` using exact UTC fractional ordering. Omitted legacy timestamps remain optional; the existing positive `reverified` boolean remains required. This does not establish external authenticity or interval-complete control stability.

## Deterministic RED → GREEN

- Tests-only commit `5bbbfed737c56b4a391cbb098f1afc44fd5385d7`, [RED Actions #40428169436](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40428169436): 1882 tests, 8 FAIL, 0 ERROR; six valid/legacy/Shadow compatibility cases passed.
- Minimal code commit `d41bb195eb1c2d8377e3ee781a4e58342db9644a`, [GREEN Actions #40428221122](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40428221122): 1882 PASS; Skill and Eval validators PASS.
- Explicit null, Unknown, numeric, unknown-offset, before-change, after-latest and nanosecond contradictions are rejected. Equal bounds, valid offset-equivalent times, omitted optional evidence, unrelated Ready and exploratory plans stay compatible.
- No new Skill, third-party dependency, Amazon Ads write/retry/idempotency capability, or claim of causality.

## Source provenance, external review, rights

- [Amazon Marketing Stream official guide](https://advertising.amazon.com/library/guides/amazon-marketing-stream): hourly near-real-time campaign metrics and campaign-change messages make time-varying control evidence operationally relevant, but do not attest this repository's re-verification record.
- [Amazon Ads Budget/Bidding Rules](https://advertising.amazon.com/library/guides/budget-rules/): automated rules can change effective controls; not an internal schema specification.
- [RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339) and [Python 3.12 datetime](https://docs.python.org/3.12/library/datetime.html): timestamp syntax and precision constraints; internal exact-fraction ordering uses standard-library Decimal.
- [Amazon Ads view-attribution update, 2026-01-01](https://advertising.amazon.com/resources/whats-new/view-attribution-updates-for-amazon-store-ads/) and [ad campaign attribution help, updated 2026-08-27](https://advertising.amazon.com/help/GX7KDKHMWQYMJ385): conversion measurement can change with model/report scope; not evidence of causal isolation.
- Public Reddit Amazon PPC examples about budget/placement interaction are unverified case hypotheses, not platform rules or safe numerical defaults.
- GitHub candidate metadata sampled 2026-10-27: MetricFlow 1848 stars, Apache-2.0, nonfork, last push Oct 13 (sampled Actions action_required); OpenLineage 2726, Apache-2.0, nonfork, Oct 25 (sampled Actions success); OpenEvals 1232, MIT, nonfork, Oct 22 (sampled Actions success); KuudoAI amazon_ads_mcp 74, MIT, nonfork, Oct 14 (sampled Actions success); Agent Skills 26668, Apache-2.0, nonfork, Aug 9 (sampled Actions failure); MCP Servers 91593, GitHub SPDX NOASSERTION, nonfork, Oct 25 (sampled Actions skipped); Google Ads MCP 1078, Apache-2.0, nonfork, Oct 26 (sampled Actions success). Each had a sampled open PR. Already in SOURCES; **reject all imports** for this narrow stdlib-only gap. NOASSERTION is not a blanket code-reuse grant. These samples are not complete security/issue/PR/dependency-license audits. No third-party code, prompts, schemas, templates or workflows copied.

## Remaining gaps

P0 full-window, source-bound Schedule/Event/Budget/Placement rule history with gap detection and verified effective-time identity; P1 connector/report/source/date/grain/currency/attribution/denominator comparability; P2 cross-campaign interference and marginal contribution-profit causality. Read-only/Suggest/Shadow by default; actual Ads writes remain with a separately authorized external Executor.
