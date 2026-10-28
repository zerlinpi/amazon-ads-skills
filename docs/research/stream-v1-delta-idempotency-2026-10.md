# Stream v1 delta idempotency and delivery-window evidence — 2026-10-28

## Reproducible problem

Initial main `36b0ebba60c1f87471b35d9f5849536e001a13b4` (v1.116.0), zero open PR, main Actions #40604546053 SUCCESS. The standalone `scripts/evaluate_metric_aggregation_gate.py` allowed additive/disjoint Stream v1 summation without evidence that incremental messages were deduplicated or that the requested window was completely delivered. Repeated deltas can inflate sums; lost deltas can understate them. This is a synthetic internal gate defect, not a claim of real account data corruption.

## RED→GREEN

Tests-only `5a33aa85cf390d5f4e3f7999bbf7a547e41c383d`: [RED Actions #40611132056](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40611132056), 2163 tests / 10 expected failures, four compatibility passes. Production `f8846a21c1565c746e0cef917c06781c25d69e89` and legacy test expectation adjustments `0e8fb144390e4534be82bd321c5766a2c0dd16c7`, `948e7e33571e72ab367b2c8d955818d66e0c8e41`: [GREEN Actions #40611237705](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40611237705), 2163 PASS, 15 Skill and 55 Eval validators PASS.

## Contract and migration

For resolved v1, require `stream_delta_reconciliation` with exactly `idempotency_id_coverage`, `idempotency_id_deduplication`, and `delivery_window_coverage`, all `Verified`. Missing, Partial, Unknown, malformed or wrong-generation proof returns `Unknown`, not Allowed or zero. Verified proof permits additive/disjoint summation only subject to separate source, metric, account, date, grain, subscription and attribution checks. No schema, Skill, dependency, ingestion implementation or Ads write was added. V1 `stream_reconciliation_status` changes from `Not Applicable` to `Unknown` or `Verified`; existing callers must migrate, so AGENTS.md MAJOR policy applies (v2.0.0).

## Official sources and IP boundary

[Amazon Stream v2 Overview](https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/overview) explicitly contrasts deprecated v1 incremental values and client `idempotency_id` deduplication with v2 per-window totals and record-key/version selection. [Stream v2 FAQ](https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/faq) discusses delta loss, ordering, retries and duplicates. Checked 2026-10-28. Our normalized proof fields are repository-defined, not Amazon-native and not independent source authentication.

Previously reviewed OpenLineage, OpenEvals, Amazon Ads MCP, Agent Skills, MCP Servers and Amazon MIT-0 Stream examples were not imported; no third-party code, prompts, schemas, templates or workflows copied. GitHub metadata is sampled, not a full security/license/issue/CI audit. Public operator anecdotes remain hypotheses.

## Next genuine gaps

P0: source-authenticated full-window delivery and account/dataset/subscription binding. P1: event/endpoint version alignment and backfill/restatement. P2: cross-campaign controls and incrementality/profitability. External authorized Connector/Executor owns actual deduplication, retries, reconciliation and live Ads writes.
