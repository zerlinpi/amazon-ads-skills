# Amazon Marketing Stream dataset-level coverage review — 2026-09

Reviewed: 2026-09-23.

## Fresh evidence

Amazon Ads describes Amazon Marketing Stream as a push-based system delivering hourly campaign metrics and campaign-change information in near real time through the Amazon Ads API. This establishes Marketing Stream as a distinct acquisition path from pull-based reporting, not merely another label for an hourly report.

Amazon's `amzn/amazon-marketing-stream-examples` reference implementation exposes separate subscriptions for `sp-traffic`, `sp-conversion`, `budget-usage`, `sd-traffic`, `sd-conversion`, `sb-traffic`, `sb-conversion`, plus entity/change and recommendation datasets. Point-in-time GitHub review on 2026-09-23: non-fork, non-archived, MIT-0, 20 stars / 16 forks, last push 2026-04-13. Stars are context only; the adoption reason is that this is an Amazon-owned reference implementation with concrete dataset/subscription engineering evidence.

## Gap found

The repository already distinguishes source system, acquisition channel, freshness, `available_through`, attribution maturity and backfill state. It did not explicitly prevent a healthy Stream dataset from being used as evidence that a sibling Stream dataset was subscribed and complete.

That matters for intraday ratios and decisions. For example, observed Sponsored Products traffic for an hour does not prove the separate conversion dataset was delivered for that hour. Treating an absent conversion sibling as zero can create a false CVR/ROAS collapse and unsafe bid/budget advice.

## Adoption

Adopt only the generic dataset-level completeness invariant:

- preserve exact Stream dataset identity;
- verify subscription and delivery state independently per required dataset;
- missing/delayed/unknown sibling dataset is an observability gap, not metric zero;
- do not silently coarsen an intraday question to daily reporting merely to bypass missing Stream coverage.

No Amazon sample code, CDK implementation, schema, workflow or subscription CLI is copied. The repository remains measurement/advice only; Stream ingestion/execution stays outside this repository.

## Rejected / deferred

- Building an Amazon Marketing Stream consumer: rejected as connector/executor infrastructure outside this repository's boundary.
- Adding a generic machine-readable stream subscription schema: deferred until a real downstream consumer demonstrates need; the policy/reference plus deterministic regression is sufficient for the current gap.
- AWS advertising/marketing sample repositories unrelated to Amazon Ads Stream dataset semantics: rejected as lower relevance even when licenses are permissive.
