# Sponsored Brands multi-ad-group reporting coverage — 2026-10-19

Status: official-source research; no connector implementation or live Ads mutation.

## Version-scoped evidence

Amazon Ads' Sponsored Brands v4 migration guide states that legacy v3 campaign reads may expose only the first ad group/ad in a multi-ad-group campaign. Complete enumeration requires the appropriate v4 listing surfaces. For the legacy Sponsored Brands Reporting API v2, a report request needs `creativeType: all` to include multi-ad-group campaign performance. The v2 report reference separately documents that omission can exclude these campaigns.

Official references:
- https://advertising.amazon.com/API/docs/en-us/sponsored-brands/v4-migration-guide
- https://advertising.amazon.com/API/docs/en-us/reference/sponsored-brands/2/reports

The requirement is specific to the documented legacy report surface; it must **not** be blindly applied to Reporting API v3, Unified Reporting, or unrelated endpoints.

## Decision consequence

A successful response is not proof of complete campaign/ad-group population coverage. Preserve the exact API generation, report type, actual request filters, row inclusion, profile/marketplace, date window, grain, pagination, freshness and metric identity. If a required inclusion filter or full entity inventory is unverified, classify the dependent population evidence as Unknown/Partial and hold any full-population claim. Missing entities/rows must not become measured zero.

The repository already has generic request-compatibility and population-completeness gates in `references/report-coverage.md` and `references/connector-capability.md`. This source alone does not warrant a new Skill, capability ID, schema, automatic request rewrite, or advertising write permission.

## Conditional test candidate

If an actual connector emits version-tagged request envelopes, add deterministic synthetic tests for the v2 surface: missing `creativeType: all` must not yield a full-population Pass or zero inference; a verified inclusive request may proceed only to separate extraction/pagination/metric gates. A v3 entity response returning one ad group must not be considered complete without independent inventory evidence.

Do not implement this until the exact connector request and current data contract are confirmed. For behavior changes, require RED→GREEN and full unit/Skill/Eval validation.

## Source decision and rights

Adopt: narrowly scoped, falsifiable official interface facts and independent conservative decision-safety implications. Reject: universalizing the legacy filter, importing provider schemas or SDKs, introducing a sixteenth Skill, or assuming runtime connector coverage. No vendor prose, code, templates, API schema, or third-party prompts/workflows were copied.
