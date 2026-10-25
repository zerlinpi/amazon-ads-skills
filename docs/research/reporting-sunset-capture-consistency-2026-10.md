# Reporting sunset capture-time consistency — 2026-10-26

## Verified defect

A required reporting generation with a concrete, matching identity and Verified read binding could return high-confidence Pass even when the connector snapshot's `captured_at` was later than the generation's own declared `sunset_at`, while `reporting_generation_status` still claimed `active` or `sunset_scheduled`. That is unreconciled source evidence, not proof of current availability or retirement.

## Minimal read-only fix

When a generation is required, parse `sunset_at` and snapshot capture as offset-aware instants. If the sunset predates capture and status remains active/sunset_scheduled, set `data_contract_effect=unknown` and degrade high confidence. Do not advance the lifecycle to retired merely because a planned date passed. Preserve future/equal sunset, explicit retired blocks, no-generation requests and all other connector safety boundaries.

## Deterministic RED → GREEN

- RED commit `597329a99a6ef14c156f0541ab0aeb36f0714ab2`: 8 synthetic tests; 1457 tests / 3 FAIL ([Actions 40213666049](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40213666049)).
- GREEN commit `e4ed8e6bb5edac71cff49e4aca63114522a6c48c`: 1457/1457 PASS, 15 Skill validators, 55 eval fixture validators ([Actions 40213715351](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40213715351)).
- No Amazon Ads account write, retry, idempotency, new Skill or executor modification.

## Sources and copyright

Amazon Ads [unified reporting GA (2026-06-08)](https://advertising.amazon.com/resources/whats-new/streamline-campaign-analysis-with-unified-reporting) and [report migration help (updated 2026-10-12)](https://advertising.amazon.com/help/GK3JZZE5QLTF8U8A) document planned, changeable reporting lifecycle dates. These do not define the repository's timestamp gate. Open-source candidate metadata, sampled CI, licenses and rejection rationale are recorded in `docs/SOURCES.md`. No external code, prompt, schema, template or workflow copied. Practitioner posts are hypothesis generators only, not platform rules.

## Next evidence gaps

P0 independently sourced Amazon Business marketplace/advertiser/campaign eligibility plus connector capability binding; P1 continuous rule activation evidence; P2 authenticated raw HTTP readback; P3 causal control interactions and marginal profitability.
