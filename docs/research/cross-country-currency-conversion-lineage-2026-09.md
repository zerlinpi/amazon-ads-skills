# Cross-country currency-conversion lineage review — 2026-09

## Decision

Adopt one narrow read-side guard: when cross-country reporting returns monetary metrics in a selected reporting currency, preserve native-vs-reporting currency and conversion provenance before treating monetary deltas as comparable. Do not implement FX conversion in this repository.

## Fresh Amazon evidence

- Amazon Ads, **“Generate a single sponsored ads campaign report for all countries at once with a currency of your choice”** (2023-09-28): the Ads Console can generate one sponsored-ads campaign report across multiple countries and apply a selected currency conversion to selected metrics. This proves that a returned monetary field can be report-converted rather than native-account currency.
- Amazon Ads, **“Streamline campaign analysis with unified reporting, now generally available”** (2026-06-08): Unified Reporting can combine multiple manager/advertiser accounts, ad products and countries in one report. This increases the practical likelihood that cross-country monetary metrics participate in one analysis.
- Amazon Ads, **“Register once and manage ads worldwide with a global seat”** (2025-02-20): DSP global seats preserve regional/profile boundaries even while enabling consolidated multi-country reporting. This supports keeping account/region identity separate from presentation-level aggregation.

Amazon documentation is proprietary. Only factual platform behavior was used; no Amazon prose, schema, workflow, or implementation was copied.

## Gap against current main

`references/data-lineage.md` already named currency conversion timing and `references/cross-account-identity.md` already required reconciling currency before cross-country aggregation. However, current main did not explicitly distinguish native account currency from selected reporting currency or require conversion provenance. That leaves a narrow failure mode: two rows can display the same reporting currency after conversion while having different native-currency / conversion treatment, and an agent can mistake the resulting monetary delta for an advertising-performance change.

The minimal implementation belongs in the existing cross-account identity policy rather than a new Skill or FX subsystem.

## GitHub / connector candidates reviewed this round

- **KuudoAI/amazon_ads_mcp** — Amazon Ads MCP/tool layer with workflow/approval concepts. Useful connector engineering context, but it does not supersede Amazon's official reporting semantics and importing its tool layer would duplicate the repository's connector-neutral boundary. No code, prompt, schema, or workflow reused.
- **ppcprophet/amazon-ads-mcp** — hosted Amazon Advertising MCP; repository states a proprietary license and hosted-account dependency. Rejected for implementation reuse; no protected implementation copied.
- **coaxon/amazon-mcp** — open-source SP-API/Ads API MCP discovered in the current scan. Useful as connector-surface context, but the present gap is measurement provenance rather than API transport. No implementation imported.
- **WaytoAIC/waytoaic-amazon-ads-skills** — low-adoption Amazon Ads Skills repository with recommendation-only write boundary. Its domain overlap is high but it provides no stronger evidence for currency-conversion semantics than Amazon's official reporting documentation. No implementation imported.

Popularity is discovery context only; none of these candidates justified a dependency or copied implementation for this gap.

## Safety boundary

This change does not authorize Amazon Ads writes, perform foreign-exchange conversion, invent exchange rates, or move retry/idempotency/reconciliation into the Skill library. Unknown conversion provenance stays unknown; affected monetary comparisons are downgraded until reconciled.
