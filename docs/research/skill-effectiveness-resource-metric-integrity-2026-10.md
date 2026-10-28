# Skill-effectiveness optional resource measurement integrity — 2026-10-28

## Reproduced gap and prioritization

Fresh main `14fbf8b70c6d419c9d838b0e17d8449d8c00a786` (v2.3.0), no open PR and last main push CI SUCCESS. Existing `schemas/skill-effectiveness-benchmark.json` constrains `tokens` to a non-negative integer and `latency_ms` to a non-negative number, but the direct CLI summarizer did not validate those optional fields. `_mean_optional` included negative, boolean and non-finite values, and silently skipped present malformed strings. This could fabricate negative resource usage or output non-standard `NaN`/`Infinity`. No real account/model incident is claimed. Existing v2.3.0 trial-ID uniqueness and v2.2.0 measurement-identity guards do not cover resource measurement validity.

Prioritized gaps: (P0) malformed actual resource observations distort evaluation outputs (deterministic, fixable without external trust); (P1) external harness run identity/authenticity and independent trials; (P2) Amazon dataset/account/subscription/window binding; (P3) control event/readback version linkage and causal profitability.

## Deterministic RED → GREEN

- Test-only `36ab94d2be4fe8156f1150413c59159cac91f8f8` ([RED Actions #40634376428](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40634376428)): 2219 unit tests, 14 expected FAIL and 3 new compatibility PASS. Includes negative/fractional/boolean/string/NaN/Infinity tokens, negative/boolean/string/nonfinite latency, and excluded-pair integrity.
- Minimal production fix `42bef5d18faaae4a5b2c19dcf3faf09994588681` ([GREEN Actions #40634431673](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40634431673)): 2219 unit tests PASS, Skill and eval validators PASS. `_validate_resource_metrics` checks each supplied optional metric before paired counting/averaging; absent and explicit null remain null. No schema change, Skill, dependency or Ads write.
- Final PR HEAD must re-pass required `validate` after release/docs changes; do not infer merged-main CI from PR success.

## Source / license boundary

Amazon Ads [Stream v2 overview](https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/overview) and [FAQ](https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/faq) confirm null is not measured zero and versioned delivery requires correct record identity; they do not define this internal Skill-eval metric schema. Existing repository schema and failing tests are the direct evidence. Previously reviewed OpenLineage (Apache-2.0), OpenEvals (MIT), SkillsBench (Apache-2.0), Amazon Ads MCP (MIT) were rechecked for public metadata, recent Actions and PRs. No code/prompt/schema/workflow/template copied; no full security or transitive-license audit; no need to import a dependency. Practitioner anecdotes are not normative rules or statistical significance.

## Limits / next gap

This check cannot prove external model execution authenticity, trial independence, resource-metering accuracy, or statistically significant Skill improvement. Read-only evaluation; external authorized Executor exclusively owns live Amazon Ads mutations, retries and reconciliation.
