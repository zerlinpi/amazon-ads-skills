# Sponsored Products Search Term historical availability — 2026-09

Reviewed: 2026-09-22

## Highest-value gap

The repository already handled the Sponsored Products Search Term report's clicked-row selection effect, but did not explicitly bind a requested historical search-term window to the report's upstream lookback availability. That left a narrow but material failure mode: an agent could receive a valid recent report, silently treat older unavailable rows as absent/zero, and overstate a 90-day or year-over-year search-term conclusion.

## Amazon official evidence

Amazon Ads Help, **Search term report for Sponsored Products**, updated May 18, 2026, states that:

- the report contains only search terms that resulted in at least one ad click;
- the report supports `summary` and `daily` time units;
- the lookback window is 65 days;
- search-term rows can also represent inferred best matches in non-search contexts, so row text is not automatically a literal shopper query.

Source: https://advertising.amazon.com/help/G3HEFZYWZF84NPS9

Adoption: factual platform/report semantics only. No Amazon prose, UI assets, API schema, examples, or proprietary implementation were copied. The repository-authored contract treats the 65-day value as dated platform-capability evidence, requires re-verification when an exact current limit matters, and never converts unavailable older history to zero.

## Incremental GitHub discovery / de-duplication

This round used multiple Amazon Ads/PPC/API/MCP and Agent Skills/evaluation/multi-agent queries rather than a fixed shortlist.

- `benchflow-ai/skillsbench` — ~1.8k stars observed; Apache-2.0; non-fork/non-archived; pushed through 2026-07-23. Re-discovered and de-duplicated because it is already reviewed in this repository for paired Skill-effectiveness evaluation. No implementation imported.
- `alibaba/skill-up` — ~1.0k stars observed; Apache-2.0; non-fork/non-archived; active on 2026-09-22. Re-discovered and de-duplicated because the repository already reviewed it for Skill evaluation/evolution infrastructure. No runtime, harness, prompt, schema, workflow, or code imported.
- `google/agents-cli` — high-adoption Apache-2.0 agent tooling, re-discovered in the >1k-star active Agent Skills/evaluation scan and already reviewed here. Its explicit evaluation lifecycle overlaps existing deterministic tests and paired-effectiveness contracts, so no CLI/runtime dependency was added.
- `openai/openai-agents-python` and `microsoft/agent-framework` — high-adoption MIT agent frameworks re-discovered in the active multi-agent scan and already reviewed. Their execution/runtime machinery remains outside this portable decision library and does not solve the specific Amazon report-history gap.
- `KuudoAI/amazon_ads_mcp` — MIT Amazon Ads MCP implementation re-discovered in the domain scan and already reviewed. Connector engineering does not override Amazon's upstream report-history availability, so no connector code/schema was imported.
- `MarketplaceAdPros/amazon-ads-mcp-server`, `ppcprophet/amazon-ads-mcp`, `zach22-1999/lingxing-mcp` and other lower-adoption Amazon/MCP results were reviewed as discovery context only. None supplied stronger authoritative semantics than Amazon's current Help contract; hosted/proprietary or connector-specific behavior was not adopted.

Stars/activity are discovery context only, not authority. Forks/mirrors and previously reviewed projects were not counted as independent new evidence.

## Decision

Adopt the Amazon official historical-availability boundary in the shared `report-coverage.md` contract instead of adding a 16th Skill or hard-coding a new executor/connector behavior. The Search Term Skill already progressively loads this reference when missing rows/population coverage affect the conclusion.

When requested history exceeds the currently verified upstream report availability, bound the conclusion to the available interval or require a lineage-compatible retained export/warehouse snapshot. Missing older rows are not zero.
