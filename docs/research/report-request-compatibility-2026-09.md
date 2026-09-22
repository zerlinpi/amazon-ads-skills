# Reporting request compatibility — 2026-09

Reviewed: 2026-09-22

## Highest-value gap

The repository already separated reporting generation, extraction completeness, row eligibility, historical availability, metric semantics and connector capability. It did not yet make the validity of the **requested report configuration** an explicit evidence state. That matters because an absent/rejected metric can be caused by an incompatible `reportTypeId × groupBy × columns × timeUnit × filters` request rather than zero advertiser activity.

## Amazon official evidence

The current Sponsored Ads Reporting API v3 getting-started documentation states that:

- every report request requires `groupBy`, whose supported values are report-type specific;
- `timeUnit=DAILY` requires `date` in `columns`;
- `timeUnit=SUMMARY` may use `startDate` and `endDate`;
- filters are constrained by the requested grouping, and only filters supported by every requested `groupBy` may be used.

Source: https://d3a0d0y2hgofx6.cloudfront.net/ja-jp/guides/reporting/v3/get-started.html

The current Sponsored Ads report-type reference separately enumerates report-specific `groupBy`, columns/metrics, filters, time units, maximum periods and retention. For example, `spSearchTerm` uses `searchTerm` grouping while `spCampaigns` supports campaign/ad-group/placement groupings; a column or grouping exposed by one report type must not be silently assumed for another.

Source: https://d3a0d0y2hgofx6.cloudfront.net/ja-jp/guides/reporting/v3/report-types.html

Amazon's Unified Reporting GA announcement (June 8, 2026) confirms that standardized metrics/dimensions and multi-dimensional combinations are expanding across products/accounts. This strengthens the need to carry reporting-generation and exact request compatibility rather than assuming one universal metric/dimension matrix.

Source: https://advertising.amazon.com/resources/whats-new/streamline-campaign-analysis-with-unified-reporting

## Repository adaptation

Add a shared fail-closed `request_compatibility_status` to the report-coverage decision contract. Validate the exact report type, grouping, columns, time unit and filters before interpreting an absent/rejected field. `incompatible`, `partial`, or `unknown` compatibility is missing/unsupported evidence, **not metric zero**. Successful report generation remains separate from population coverage and extraction completeness.

No Amazon prose, API schema, request example, SDK code or proprietary implementation was copied. Only factual platform semantics were independently expressed as repository-owned decision rules.

## Incremental GitHub discovery / de-duplication

This round used multiple Amazon Ads reporting/API/MCP and Agent Skills/evaluation searches.

- `Imsamiullah09/amazon-ads-mcp` surfaced as a current Amazon Ads MCP implementation and independently demonstrates that report requests expose `reportTypeId`, `groupBy`, `columns` and `timeUnit`. It is discovery/engineering context only; Amazon official documentation remains semantic authority. No code or request templates were copied.
- `JonasSchroeder/amazon-ads-api-report-downloader` and several same-name forks/mirrors surfaced in reporting searches. Mirrors/forks were de-duplicated and not counted as independent evidence; downloader mechanics do not improve this repository's decision contract beyond current official request semantics.
- `aws-solutions/amazon-marketing-cloud-insights-on-aws` surfaced but is archived and concerns AMC rather than Sponsored Ads request compatibility; rejected for this change.
- High-adoption Agent Skills/evaluation projects including `benchflow-ai/skillsbench`, `google/agents-cli`, `alibaba/skill-up`, `evalstate/fast-agent` and `huggingface/upskill` were re-discovered. They are runtime/evaluation evidence, not stronger authority for this Amazon reporting gap, and previously reviewed concepts already cover progressive loading/evaluation. No additional runtime feature was adopted.

Stars/activity are discovery context only. Forks, mirrors, archived projects, marketing shells and already-reviewed projects are not independent evidence and do not justify duplicate functionality.

## Decision

Strengthen the existing `references/report-coverage.md` contract rather than adding a Skill, connector implementation or executor behavior. The decision layer should fail closed before metric interpretation when the requested report configuration is not proven compatible, while keeping all live Amazon Ads writes external.
