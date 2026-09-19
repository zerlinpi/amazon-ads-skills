# Metric aggregation semantics review — 2026-09-19

## Decision gap

Amazon Ads now exposes measurement surfaces where some metrics are intentionally de-duplicated across campaigns, advertiser accounts, manager accounts, supply sources, and custom time periods. A metric identity that records only name/family/attribution/version is therefore insufficient for safe downstream aggregation.

The repository policy is:

- preserve aggregation semantics as lineage, never infer it from the display name;
- `unknown` is not `additive`;
- de-duplicated/non-additive and ratio/derived metrics must not be treated as ordinary roll-up-safe sums without an explicit source contract;
- this repository records the semantic identity but does not implement a generic BI aggregation engine.

## Primary Amazon evidence

### Amazon Ads dynamic reach and frequency reporting — official

Amazon Ads announced dynamic reach and frequency reporting on April 2, 2026. The reporting surface provides de-duplicated reach/frequency across custom campaign combinations and can span advertiser accounts, manager accounts, supply sources, and frequency groups.

Adoption: factual measurement semantics only. No Amazon page text, API schema, report template, field table, or implementation is copied. The generic lesson is that metric additivity is part of metric identity and must travel with lineage.

### Amazon Ads Frequency Group / advertiser-level reach reporting — official

Earlier Amazon DSP reach/frequency releases explicitly describe consolidated de-duplicated measurement designed to eliminate audience double-counting across orders, publishers, channels, and devices.

Adoption: corroborating evidence that direct summation can be invalid for distinct/de-duplicated audience metrics. No implementation material copied.

## Open-source semantic-layer review

### dbt-labs/metricflow — ~1.8k stars; Apache-2.0; active

MetricFlow is a mature semantic-layer project with real Python implementation, tests, issues, and continued 2026 maintenance. Its generic engineering value is that metric semantics belong in a modeled contract and are preserved through query planning rather than inferred at the final presentation layer.

Adoption decision: method-level only. No code, query planner, schema, metric definitions, SQL generation, prompts, or workflows are copied. The repository needs only a small connector/measurement-lineage semantic flag, not a semantic query engine.

### semanticdatalayer/SML — ~175 stars; Apache-2.0; active

SML explicitly distinguishes additive, non-additive, and semi-additive metric behavior and documents that distinct-count-style metrics cannot be safely combined by basic addition.

Adoption decision: use the generic taxonomy insight only, independently rewritten into repository-specific values such as `additive`, `non_additive_deduplicated`, `ratio_or_derived`, and `unknown`. No SML schema, YAML, prose, examples, calculation-method tables, or engine behavior is copied.

### apache/superset — ~74.8k stars; Apache-2.0; very active

Superset is a large, actively maintained BI project. Recent engineering discussion around non-additive totals reinforces a conservative pattern: aggregation safety should come from explicit metric semantics rather than guessing from rendered totals or metric labels.

Adoption decision: corroborating engineering evidence only. No Superset implementation, semantic-layer types, query strategy, issue text, or UI logic is copied.

### OpenSemanticLayer/OpenSemanticLayer — 7 stars; AGPL-3.0; fork

This repository is a fork of dbt-labs/metricflow and therefore is not counted as independent evidence. Its AGPL license also makes implementation reuse inappropriate for this repository's current scope.

Adoption decision: excluded as duplicate/fork evidence; no code or schema reused.

## Why this is prioritized

This gap directly affects decision quality because an unsafe roll-up can fabricate scale, reach, or efficiency conclusions even when every source row is individually correct. It therefore ranks above adding another Skill or importing a general semantic-layer framework.

The minimal repository change is to preserve aggregation semantics end-to-end through optimization-event evidence and derived measurement memory. A separate deterministic decision gate is required before using the field to block cross-scope aggregation; recording the field alone is not treated as proof that downstream reasoning is already safe.
