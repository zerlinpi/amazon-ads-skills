# Observed SP rule events: extra sibling arrays — 2026-10-28

## Verified gap

Starting main HEAD `9ca0feaece1e3c352354bedcd743a3aefb31e513`, v1.114.0, no open PR. Prior changes already guarded outer rule collections, nested descendants and non-rule routing/audience arrays. The separate remaining gap: an additional direct array beside `schedule_rules`/`event_rules` or `active_budget_rules` in a positive mid-window Sponsored Products rule `control_events` state could bypass the outer proof and descendant-list walker. Even an empty `unmapped_targets: []` could be classified `Confounded`. This is a synthetic normalized read-side evidence defect, not an assertion about live Amazon Ads API behavior.

## RED → GREEN

- Branch `fix/intervening-sp-rule-extra-direct-list-20261028`, PR #228.
- RED test-only commit `38480f18c1e0e2a2e523ed8c96b4cb9f8f29552e`, [Actions #40597911676](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40597911676): 2139 tests, 5 expected failures (incorrect `Confounded` instead of `Unknown`), no errors; 4 new compatibility cases passed.
- GREEN production commit `08730525aab90660f5a01dfee33e372fbd480616`, [Actions #40597993016](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40597993016): 2139/2139 unit PASS, 15 Skills PASS, 55 Evals PASS.
- Test `tests/test_intervening_rule_extra_direct_list_proof.py`: nine deterministic cases. Minimal fix in `scripts/compare_control_state.py`: reject extra list-valued sibling fields outside registered rule lists on both event phases. Valid registered lists, scalar metadata and flat legacy events remain compatible. No schema field, new Skill, dependency or Ads write.

## Sources and license boundary

- [Amazon Sponsored Products schedule-based bid rules](https://advertising.amazon.com/resources/whats-new/schedule-based-bid-rules-available-for-sponsored-products), published 2023-11-06, establishes time-varying bid rules; [Marketing Stream v2 FAQ](https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/faq), checked 2026-10-28, distinguishes record identity, delivery parts, restatements and null versus measured zero. Neither source defines this repository's normalized event schema or certifies full-window event coverage.
- Revisited GitHub OpenLineage (Apache-2.0, approximately 2.7k stars), OpenEvals (MIT, approximately 1.2k), KuudoAI Amazon Ads MCP (MIT, about 74 previously observed), Agent Skills (Apache-2.0, approximately 26.7k), MCP Servers (GitHub SPDX NOASSERTION and a licensing transition, approximately 91.6k). Read LICENSE files, sampled recent commits and open PRs; star counts are approximate or last-observed, not live GitHub API counts. This is not a complete fork/mirror, issue, CI, dependency-license or security audit. Reject imports: standard-library guard suffices, none authenticates Amazon Ads event history. No third-party code, prompts, schema, workflows or templates copied.
- Public PPC expert and Reddit anecdotes remain testable hypotheses, not Amazon platform rules or causal proof.

## Limits and next gaps

The optional outer proof does not authenticate raw Connector evidence or prove the whole experimental event window was captured. Next: source-supported event capture windows, endpoint/event version association, and independently proven complex non-rule collections if needed. Preserve source/metric/date/grain/identity/connector capability, missing/unsupported/partial/unknown not zero, Observation/Hypothesis/Cause/Action/Outcome, confounders and marginal economics. Default Read-only/Suggest/Shadow; external authorized Executor owns all Ads writes/retries/idempotency/reconciliation.
