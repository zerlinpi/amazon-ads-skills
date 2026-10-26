# Ready combined metric identity: whitespace-obfuscated Not Applicable — 2026-10-27

## Baseline and verified nonduplicate gap

Fresh main: `c963b60bc507e2f4a7b5584399935b3ca32b6a8d` (v1.91.0); zero open PRs at start. Checked recent commits, Actions, full file tree, all 15 canonical SKILL.md files, AGENTS/CLAUDE/runtime manifests, SOURCES/research, scripts/tests/schemas and selected legacy branches. Relevant sampled branches were all behind main, not reusable unmerged work. No `knowledge/` directory. The existing `_unresolved_combined_metric_name` normalized hyphens/underscores but, because its character class escaped `\\s` incorrectly, failed to collapse repeated spaces, tabs, newlines and nonbreaking spaces. `Not  Applicable` and `Not\\tApplicable` could therefore pass a Ready combined readout as concrete metric identities. This is an internal placeholder-normalization defect, not an Amazon Ads platform contract.

## Deterministic RED → GREEN

- RED: test commit `b1b031f4ec9009d4e34c70cdd4079acbce1aceaa`, [Actions #40407197848](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40407197848): 1843 tests, **7 FAIL**, 0 ERROR. Seven failures were the newly added primary/guardrail placeholder cases; six compatibility tests passed.
- GREEN: minimal production fix `95e5e5381f43d763a04fc3633699c25c8f2ab0fb`, [Actions #40407278247](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40407278247): 1843 tests PASS, Skill validator PASS, Eval validator PASS.
- The single production change corrects the regular-expression character class from a literal backslash/s class to a real whitespace class. No schema change, new Skill, runtime dependency, metric computation or Amazon Ads write. Non-combined Ready, exploratory Shadow Only, real metric names containing the words, and existing single-space/hyphen placeholders retain behavior.

## Official and practitioner evidence boundary

- [Amazon Ads campaign reporting](https://advertising.amazon.com/library/guides/intro-attribution-campaign-reporting) and [2026 view-attribution change](https://advertising.amazon.com/resources/whats-new/view-attribution-updates-for-amazon-store-ads/) support preserving precise metric and attribution identity before comparing campaign results. They do **not** define the repository's placeholder strings or validate raw connector reports.
- [Amazon Ads budget and bidding rules](https://advertising.amazon.com/library/guides/budget-rules) documents automatically changing campaign controls. That motivates continuous-window control evidence but does not prove such evidence exists here.
- Reddit PPC anecdotes about budget pacing and bids are operator hypotheses only; no platform normative or causal claims derived from them.

## GitHub candidate and license decisions (metadata sampled 2026-10-27)

| Candidate | Stars | License | Activity / sampled CI | Decision |
| --- | ---: | --- | --- | --- |
| dbt-labs/metricflow | 1848 | Apache-2.0 | pushed 2026-10-13; sampled Actions action_required | Reject dependency: semantic layer does not fix this local regex |
| OpenLineage/OpenLineage | 2726 | Apache-2.0 | pushed 2026-10-25; sampled success/failure | Reject: no external provenance authentication in scope |
| langchain-ai/openevals | 1232 | MIT | pushed 2026-10-22; sampled success/action_required | Reject: deterministic stdlib tests suffice |
| KuudoAI/amazon_ads_mcp | 74 | MIT | pushed 2026-10-14; sampled success | Reject: no connector or write needed |
| agentskills/agentskills | 26663 | Apache-2.0 | pushed 2026-08-09 | Reject: 15 canonical Skills unchanged |
| modelcontextprotocol/servers | 91593 | NOASSERTION | pushed 2026-10-25 | Reject: license ambiguity, no blanket reuse |

Sampled stars, non-fork flags, open PR and Actions metadata are not exhaustive security, code, issue, dependency-license or CI audits. All candidates were previously listed in SOURCES. No external code, prompts, schemas, workflows, templates or copyrighted prose copied; abstract principles only.

## Residual gaps

P0 full-window schedule/event/budget-rule control histories and independent source authentication; P1 numerator/denominator, currency, date, grain, attribution-version and overlap compatibility; P2 cross-campaign interference and marginal contribution profit. Keep Missing/Unknown/Unsupported/Partial distinct from measured zero; default Read-only/Suggest/Shadow. All live Ads writes, retries, idempotency and reconciliation remain with an authorized external Executor.
