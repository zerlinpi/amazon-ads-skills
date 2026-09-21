# Modeled conversion allocation safety — 2026-09

## Gap

A lower-grain Amazon Ads report can appear to lose conversions even when parent-level attributed conversions remain present but cannot be allocated to that reporting dimension. Treating omitted or `Unallocated` conversion rows as zero can produce false target/search-term/placement waste diagnoses and unsafe bid suppression.

## Primary evidence

Amazon Ads, **Modeled conversions now reported for Sponsored Display campaigns** (July 1, 2024): Amazon states that modeled conversions are reported in the same conversion columns as directly attributed conversions. When meaningful estimates cannot be produced at a requested reporting breakdown, conversions can be reported on an `Unallocated` row (example: targeting clause level). This is first-party product/reporting documentation and is used as behavioral evidence, not copied implementation.

Source: https://advertising.amazon.com/resources/whats-new/modeled-conversions-for-sponsored-display-campaigns

Amazon Ads, **Amazon DSP provides modeled attribution for off-Amazon conversions for US advertisers** (August 16, 2024): directly measured and modeled off-Amazon conversions can be reported together as a combined campaign result. This reinforces that conversion metric identity can include modeled measurement and therefore must be preserved when comparing periods/sources.

Source: https://advertising.amazon.com/resources/whats-new/modeled-attribution-for-off-amazon-conversions-for-us-advertiser

## Adopted abstraction

- Preserve modeled-versus-direct measurement semantics when known.
- Preserve valid `Unallocated`/sentinel conversion rows in the parent-level total defined by the source contract.
- Do not redistribute unallocated conversions to lower-grain entities without supported allocation evidence.
- Separate parent-level conversion movement from allocation-to-dimension movement.
- If material conversions are unallocated, downgrade lower-grain causal/action claims rather than interpreting missing allocation as zero.

No Amazon text, code, schema, or proprietary workflow is copied into the repository; only the safety abstraction is encoded.

## GitHub candidates reviewed

- `coaxon/amazon-mcp` — MIT; public repository describes SP-API + Ads API read paths, dry-run defaults and security-oriented deployment material. Useful connector engineering evidence, but not adopted this round because the gap is Amazon reporting semantics rather than connector transport. Its README also says tests are being updated for a core/pro split, so it is not stronger evidence than first-party Amazon documentation for this behavior.
- `ppcprophet/amazon-ads-mcp` — proprietary and hosted; useful evidence that external MCPs expose reporting/diagnosis surfaces, but rejected for implementation reuse because the repository explicitly declares a proprietary license and depends on a hosted account/service.
- `KuudoAI/amazon_ads_mcp` — previously reviewed in this repository; broad Ads API surface, but no new non-duplicative decision-safety primitive was found for this gap. Not counted again as independent evidence.

Stars/activity are discovery signals only and were not used as adoption criteria. No third-party code, prompt, schema, or workflow was copied.
