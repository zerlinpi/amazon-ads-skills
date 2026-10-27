# Control readback observation provenance integrity — 2026-10-27

## Fresh state and nonduplicate gap

Initial main: `67f5bfeaeeda833dfa44051a48021b36f68d72f0` (v1.96.0), main Actions [#40434752649](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40434752649) SUCCESS, no open PR. Reviewed 15 canonical Skills, AGENTS/CLAUDE/README, SOURCES/research, relevant comparator/tests/schema/references, runtime manifests and Actions; broader paths inventoried, not every file deeply audited. Five sampled historical control branches were zero commits ahead of main.

The prior v1.96.0 guard rejected **one reused non-null readback ID with different material states**. It did **not** check whether an explicitly supplied ID was a placeholder or malformed. For example, baseline `source.readback_id="Unknown"`, post `"post-1"` and a changed bid could be classified `Treatment Isolated`. Even with unchanged controls, two different `observed_at` instants under one identical readback ID could be classified `Comparable`. Both are source-observation identity contradictions, independent of earlier changed-state collision protection.

## Deterministic RED → GREEN

- Tests-first commit `daa1b8b53f9a9b0d8c655a56dcf45971bdab1fdc`: [RED Actions #40440704449](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40440704449), 1910 tests, **12 FAIL**. 19 new tests cover explicit unknown/partial/not-available/not-supported/not-applicable/N/A, blank/padded/non-string IDs, identical ID with different observation instants including one nanosecond, and compatibility.
- Production change `9beb1259b741dc6d4cb1955d196f3821c313662f` plus focused regex correction `763cf684410688387cdde53d2647a978f277799e`: [GREEN Actions #40440800591](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40440800591), **1910/1910 PASS**, repository Skills and Eval validators PASS.
- Minimal behavior: when a non-null readback ID is explicitly supplied, reject unresolved/invalid labels before any causal classification; when both valid IDs are identical, their exact UTC `observed_at` instants must also agree. Omitted/null optional legacy IDs, different concrete IDs, valid IDs containing placeholder substrings, unchanged same-time observations and offset-equivalent instants remain compatible. No schema addition, new Skill, dependency, Ads write, retry or executor change.

## Sources and boundaries

- [Amazon Marketing Stream](https://advertising.amazon.com/solutions/products/amazon-marketing-stream) describes near-real-time hourly metrics and campaign messages, not this repository's `readback_id` or independently authenticated readback events.
- [Amazon Ads Global Sponsored Products API](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns) distinguishes account/campaign/marketplace configuration identities; it does not define this internal observation-ID contract.
- [RFC3339](https://datatracker.ietf.org/doc/html/rfc3339) supplies a timestamp interchange syntax; normalized exact UTC comparison is repository-owned evidence consistency, not proof of continuous delivery.

### External candidate review, 2026-10-27

GitHub repository metadata and sampled PR/Actions (not exhaustive code, test, issue, dependency or security audits):

| Candidate | Stars | License | Non-fork / recent push | Sampled CI / PR | Decision |
| --- | ---: | --- | --- | --- | --- |
| [OpenLineage](https://github.com/OpenLineage/OpenLineage) | 2726 | Apache-2.0 | yes / Oct 25 | Oct 26 success and failure; PRs #5105/#5104 | Reject integration: generic lineage events do not authenticate this readback ID. |
| [MetricFlow](https://github.com/dbt-labs/metricflow) | 1848 | Apache-2.0 | yes / Oct 13 | not fully audited this run | Reject: semantic layer unrelated to narrow identity collision. |
| [OpenEvals](https://github.com/langchain-ai/openevals) | 1232 | MIT | yes / Oct 22 | Oct 25 success/action_required; PRs #291/#283 | Reject: deterministic stdlib tests suffice. |
| [Amazon Ads MCP](https://github.com/KuudoAI/amazon_ads_mcp) | 74 | MIT | yes / Oct 14 | Oct 25–26 successes; PRs #104/#101 | Reject: connector availability does not certify source observations. |
| [Agent Skills](https://github.com/agentskills/agentskills) | 26672 | Apache-2.0 | yes / Aug 9 | not fully audited this run | Reject: existing 15 canonical Skills already meet the task boundary. |

All candidates were previously considered in SOURCES/research; no imports or copied third-party code, prompts, schema, templates or workflows. Sources without an explicit compatible license are principles-only. A [September 2026 Reddit CPC/placement discussion](https://www.reddit.com/r/AmazonFBA/comments/1w6hdwl/amazon_ppc_is_this_normal_20_cpc_for_one_click/) suggests a testable bid-rule/placement interaction, **not** an Amazon specification or verified causal case.

## Residual gaps

Different plausible IDs are not external response authentication; no pair of snapshots proves uninterrupted Schedule/Event/Budget Rules history. Require externally authenticated connector capture, complete time-window coverage, attribution/metric/source/grain comparability, retail confounders and marginal contribution economics before causal claims. Preserve Missing/Unsupported/Partial/Unknown distinctly from numeric zero. Default Suggest/Shadow; live writes, retries, idempotency and reconciliation remain with an authorized external Executor.
