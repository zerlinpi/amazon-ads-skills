# Sponsored Products Search Term historical availability — 2026-09

Reviewed: 2026-09-22

## Highest-value gap

The repository already handled the Sponsored Products Search Term report's clicked-row selection effect and, in PR #83, added an explicit historical-availability boundary. A fresh official-source reconciliation exposed a more important follow-up: **historical availability differs by acquisition channel/reporting generation**. Treating one surface's numeric limit as a universal Search Term limit can unnecessarily discard valid history or, in the opposite direction, claim history that the active path cannot retrieve.

## Amazon official evidence

### Console/help surface

Amazon Ads Help, **Search term report for Sponsored Products**, updated May 18, 2026, states that:

- the report contains only search terms that resulted in at least one ad click;
- the report supports `summary` and `daily` time units;
- the lookback window is **65 days**;
- search-term rows can also represent inferred best matches in non-search contexts, so row text is not automatically a literal shopper query.

Source: https://advertising.amazon.com/help/G3HEFZYWZF84NPS9

### Sponsored Ads Reporting API v3

The current Amazon Ads API Sponsored Ads report-type reference, retrieved September 22, 2026, lists the Sponsored Products `spSearchTerm` report with:

- **95-day data retention**;
- **31-day maximum report period per request**;
- `SUMMARY` or `DAILY` time units;
- `searchTerm` groupBy;
- the same clicked-impression selection warning for Search Term rows.

Source: https://d3a0d0y2hgofx6.cloudfront.net/ja-jp/guides/reporting/v3/report-types.html

The Reporting API v3 getting-started reference separately confirms that `timeUnit=DAILY` requires the `date` column, `SUMMARY` may use `startDate`/`endDate`, and report-type-specific `groupBy` support constrains valid requests.

Source: https://d3a0d0y2hgofx6.cloudfront.net/ja-jp/guides/reporting/v3/get-started.html

## Reconciliation

The 65-day console/help lookback and 95-day Reporting API v3 retention are both Amazon official evidence but are not safe to collapse into one repository-global constant. They describe different acquisition surfaces/reporting contracts. In addition, the API's 31-day maximum request period is a request-span constraint, not a historical-retention constraint: retrieving a longer eligible history may require multiple non-overlapping requests rather than declaring the older interval unavailable.

Decision contract:

```text
historical availability
= f(source system, acquisition channel, reporting generation, report type, time grain, current capability evidence)
```

When the active acquisition channel is unknown, or current official/account evidence conflicts, preserve `Unknown` / `Conflicted` and **do not silently choose** 65 or 95. Missing history remains missing evidence, never zero.

Adoption: factual platform/report semantics only. No Amazon prose, UI assets, API schema, examples, or proprietary implementation were copied. The repository-owned `report-coverage.md` contract independently expresses the acquisition-channel lineage rule.

## Incremental GitHub discovery / de-duplication

This round again used multiple Amazon Ads / Advertising API / reporting / MCP and Agent Skills / evaluation searches rather than a fixed shortlist.

- `KuudoAI/amazon_ads_mcp` — MIT; active Amazon Ads MCP implementation, re-discovered and already reviewed. Its async reporting/tooling remains useful connector-engineering context, but connector behavior cannot override Amazon's source-specific historical-availability contract. No code/schema imported.
- `ScaleLeap/amazon-advertising-api-sdk` — Amazon Advertising API SDK result re-discovered, but the repository is archived. Rejected as current semantic authority; current Amazon API documentation is stronger evidence.
- `amzn/amazon-advertising-api-php-sdk` — Amazon-owned historical SDK result, archived. Useful only as historical ecosystem context; rejected for current reporting semantics.
- `denisneuf/python-amazon-ad-api` and other lower-adoption API wrappers were discovery context only. Wrapper behavior is not stronger evidence than current Amazon Reporting API documentation and does not justify importing code.
- Previously reviewed high-adoption Agent Skills/runtime projects were de-duplicated because this gap is an Amazon reporting-source lineage problem, not a runtime/evaluation-framework deficiency.

Stars/activity are discovery context only, not authority. Forks, mirrors, archived SDKs and previously reviewed projects were not counted as independent implementation evidence.

## Decision

Strengthen the existing shared `report-coverage.md` contract instead of adding a Skill, connector implementation or executor behavior. Search Term decisions must bind historical availability to the actual acquisition channel/reporting generation. For Reporting API v3, do not confuse the 31-day maximum request period with the 95-day retention window. For console/help workflows, do not assume API retention automatically applies. When exact current capability is decision-critical, re-verify the active path through `platform-capability-lineage.md` and connector/account evidence.
