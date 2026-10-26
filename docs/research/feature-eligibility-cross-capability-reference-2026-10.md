# Cross-capability feature eligibility source-reference collision — 2026-10-26

## Falsifiable, non-duplicate gap

The v1.72.0 source-independence check scanned every binding, but only for required connector capability IDs. A connector snapshot may contain extra, non-required capability probes. A feature-specific eligibility `source_reference` repeating the extra capability's `binding_id`, `surface_id` or `evidence.reference` was accepted as independent, despite being the same normalized connector probe. A self-referential Ineligible record could falsely Blocked an account as well. No actual Amazon entitlement or remote API response was involved in the synthetic reproduction.

## Deterministic RED → GREEN

- Base main: `5481be597d02a2090a7afdee4ea2d94d1bfa2e84`. PR #186, branch `fix/feature-eligibility-cross-capability-reference-20261026`.
- RED `c971a41633c3fe2328909c5a2682bc64aed60da6`, [Actions #40256092116](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40256092116): 1573 tests, 6 FAIL. Three controls (distinct eligible/ineligible and legacy no-feature) passed.
- GREEN `83310e41df04a0ed15689556c7b283e67259ec27`, [Actions #40256160583](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40256160583): 1573/1573 tests PASS, 15 Skill validator and 55 eval fixture validator PASS.
- Minimal repair: iterate all observed capabilities only for source-reference collision detection. Required capability validation, scope/identity/time, verified binding qualification and read-only mode are unchanged. Nine new deterministic tests; no new Skill, schema, dependency or Amazon Ads write/retry/idempotency.

## Official source and copyright boundary

[Amazon Ads MCP account context](https://advertising.amazon.com/API/docs/en-us/mcp/get-started) separates profile, advertiser and manager identity. [Advertiser product-group eligibility](https://advertising.amazon.com/API/docs/en-us/mcp/advertiser-product-group-eligibility) cannot substitute for feature-specific campaign enrollment. [Amazon Business exclusive SP launch, 2025-05-05](https://advertising.amazon.com/en-gb/resources/whats-new/amazon-business-exclusive-campaign-for-sponsored-product) restricts creation to eligible advertisers. These sources support the distinction between connector read access and feature eligibility; none defines our normalized reference-collision rule.

GitHub samples KuudoAI/amazon_ads_mcp (MIT, 74 stars), promptfoo/promptfoo (MIT, 26,422), OpenLineage/OpenLineage (Apache-2.0, 2,722), agentskills/agentskills (Apache-2.0, 26,619), and modelcontextprotocol/servers (NOASSERTION, 91,560) were already covered in SOURCES and rechecked for mutable metadata, public activity and sampled CI/PRs. Reject importing any: a bounded stdlib guard needs no external runtime, and stars/CI do not authenticate Ads evidence. No third-party code, prompt, schema, workflow or template copied; NOASSERTION is not a reuse grant. No complete security/transitive-license audit claimed. Practitioner placement anecdotes are hypotheses only, not Amazon Ads platform rules.

## Remaining gaps

P0: distinct reference labels do not authenticate the external source or prove actual advertiser/campaign entitlement; authorized readback and reconciliation remain external.
P1: schedule/event/budget-rule snapshot and last transition do not prove continuous execution across the causal comparison window.
P2: cross-campaign bid/budget/placement and retail effects require source-specific causal confounder and marginal profit checks.
