# Single-run Skill-effectiveness summary identity integrity — 2026-10-28

## Verified gap and priority

Fresh main `40685b588da744e7eb46a6e73323a2f687bc32fe` (v2.4.0), zero open PRs, latest main Actions success. All 15 Skills and runtime manifests inspected, with focused review of `schemas/skill-effectiveness-benchmark.json`, paired summarizer, longitudinal comparator and existing tests/research. Four relevant historical Skill branches were behind main and had zero unique commits. A summary with missing `skill`, `fixture_id`, `mode`, `harness.model_version`, or an explicit `Unknown` model version could still report `Measured`. The longitudinal comparator had already rejected unresolved identity, so this is a distinct single-run input-validation gap rather than duplicate work. A malformed list-valued mode also caused an unhandled TypeError during the first fix.

Priority: P0 internal benchmark identity integrity (reproducible, local fix); P1 external harness execution/trial independence proof (cannot be authenticated here); P2 external Amazon account/dataset/subscription/time-window binding; P3 control event/readback version association and causal profit interpretation.

## Deterministic RED→GREEN

- Tests-only `a34d6e6178dfbab9bdd2262c4ec46e8a82c4b822`: [RED Actions #40639471528](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40639471528), 2241 tests / 18 expected FAIL / 4 compatibility PASS.
- Initial code `2b9df331f7e6f9ca42f6e6fd46ec6afef8ec1cf8`: [GREEN Actions #40639535046](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40639535046), 2241 PASS.
- Extra list-mode test `dfd79dc4919e4d5b3625edeee6d93daea11a9124`: [RED Actions #40639552609](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40639552609), 2242 tests / 1 ERROR (unhandled list-valued mode).
- Final minimal code `767c12de1126c82419e9574f9a93ff6d906d7a76`: [GREEN Actions #40639597102](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40639597102), 2242/2242 PASS, 15 Skills and 55 Evals PASS. Latest PR HEAD and merged main must be checked separately after release changes.

The read-only summarizer now validates required core identities and allowed mode, rejects whole-label placeholders/padded/malformed supplied strings, and validates optional hashes when non-null. Explicit null rubric and omitted/null optional hashes remain compatible. No Schema expansion, Skill, dependency, actual model call, Ads write, retry or executor logic.

## Sources, licenses, rejected alternatives

Official Amazon [Stream v2 overview](https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/overview), [FAQ](https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/faq) and [unified reporting announcement June 8 2026](https://advertising.amazon.com/resources/whats-new/streamline-campaign-analysis-with-unified-reporting) are platform context only, not the source of this internal benchmark rule. Existing schema, comparator and deterministic failing tests are the direct evidence.

Public GitHub metadata sampled 2026-10-28: OpenLineage (Apache-2.0; 2729 stars; active), OpenEvals (MIT; 1234 stars; recent sampled CI `action_required`), SkillsBench (Apache-2.0; 1877 stars; sampled CI success), Amazon Ads MCP (MIT; 74 stars). Nonfork status and activity sampled, not full code/security/issue or transitive-license audits. No third-party source code, prompts, schemas, workflow templates or copyrighted text reused. These projects do not prove that synthetic harness IDs correspond to distinct real executions, so adding a framework would be scope expansion without proven value. Reddit PPC practitioner claims are hypotheses only.

## Limits / next gap

A concrete declared identity is necessary but does not authenticate a real model run or prove independent paired samples, statistical significance, external Amazon Ads data completeness, or causal profitability. Keep 15 Skills and default Read-only/Suggest/Shadow; external authorized Executor alone owns live account writes, retries, idempotency and reconciliation.
