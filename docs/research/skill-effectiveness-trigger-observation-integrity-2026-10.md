# Skill-effectiveness trigger observation integrity — 2026-10-28

## Verified gap and priority

At main `bfc4ac082fc670c81ef2ace78c155da0dcd5e7d4`, the paired effectiveness summarizer filtered optional `triggered` fields to booleans without validating malformed supplied values. As a result, `"false"`, `0`, arrays and unknown placeholders disappeared silently from the rate denominator. A reported 100% trigger rate could be based on one observed boolean with other comparable trials unmeasured. This is a local data-integrity issue, not evidence of a real advertising-account or agent-harness incident.

Priority: P0 for the existing Skill-eval reporting surface because malformed values can distort a safety/activation metric without any warning. Independent model execution identity and complete source delivery remain higher-level unproven external boundaries, but cannot be fixed by adding invented local `Verified` flags.

## Existing contracts and scope

- `schemas/skill-effectiveness-benchmark.json` already defines optional `triggered` as boolean or null.
- `evals/SKILL-EFFECTIVENESS.md` already separates discovery, negative controls, forced invocation, paired effectiveness, scorer/harness errors and measured outcomes.
- The summarizer computes comparable pairs only when both arms are measured. Non-measured pairs remain excluded; their malformed supplied trigger telemetry must still be rejected.
- Missing and explicit null are unmeasured, never coerced to false/zero. A valid boolean zero-rate is not the same as no observed booleans.

## RED → GREEN

- Test-only commit: `81b3eb4a73cd503e98667554a73117bfa0f89584`. [RED #40645366608](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40645366608): 2258 tests, 12 FAIL, 3 ERROR, one new compatibility test passed.
- Minimal production fix: `86a33d549bb5b32047e075a959e41c15ac46bc1a`. [GREEN #40645433397](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40645433397): 2258/2258 PASS, 15 Skill directories and 55 eval fixtures validated.
- Sixteen new synthetic deterministic tests cover malformed supplied values on measured and excluded trials; valid boolean rate; missing/null; partial coverage; excluded-pair denominator.
- Fix: reject non-null non-boolean `triggered` for every trial and expose `trigger_observed_count` beside `trigger_rate` and `trial_count` in each comparable variant summary. No new Skill, dependency, schema field, live model run or Ads write.

## Public evidence and copyright boundary

Amazon Marketing Stream v2 FAQ (official): https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/faq — source and null-vs-zero distinction, not the Skill-eval schema. Unified reporting GA (June 8, 2026): https://advertising.amazon.com/resources/whats-new/streamline-campaign-analysis-with-unified-reporting — reporting semantic drift, not proof of agent activation. Official placement/schedule controls remain context for Ads confounders, not trigger rates.

Public open-source candidates checked 2026-10-28: adewale/skill-eval-harness (78 stars, MIT), langchain-ai/openevals (1234, MIT), benchflow-ai/skillsbench (1877, Apache-2.0), KuudoAI/amazon_ads_mcp (74, MIT). Nonfork metadata, last activity, sampled Actions and open PRs reviewed; complete dependency/license/security/issue review not performed. Existing SOURCES/research already discusses similar evaluation methods. No third-party implementation, prompt, schema, template or workflow copied. Reject new framework: no demonstrated incremental value for a standard-library boolean validator.

Public practitioner/Reddit bid and budget examples are hypotheses subject to confounders and do not establish Amazon Ads platform norms. Source/metric/date/grain/identity/connector capability, Observation/Hypothesis/Cause/Action/Outcome, marginal profit, control interactions and external authorized Executor remain unchanged.

## Remaining gaps

1. External harness must prove declared `trial_id` values correspond to distinct actual model runs and that trigger observations are complete; `trigger_observed_count` only reports internal declared coverage.
2. External Amazon Ads connector must bind advertiser account, dataset, subscription, delivery window, readback and source version to trustworthy raw records.
3. Repeated paired real-harness experiments with stable measurement identity are required before claiming statistically reliable Skill lift.
