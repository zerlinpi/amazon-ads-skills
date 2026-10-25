# Sponsored Products rule activation transition-time evidence — 2026-10-25

## Evidence-backed gap

A normalized rule member can contain a valid `activation_status` and a repeated invalid/future `activation_effective_at`, yet the previous comparator treated the rule as stable. A timestamp without an associated status, or only present on one side of a shared rule identity, similarly cannot prove comparable controls.

The field is optional, repository-owned read-side transition evidence, **not** an Amazon Ads API field, execution instruction or continuous-time history. The canonical snapshot observation is a distinct timestamp. A status plus last-transition time cannot rule out intervening toggles, event triggers or missing marketplace/connector eligibility.

## Deterministic validation

- RED: commit `9bf16235fc6b10d3f847faed29e8428382f78189`, Actions 40156028288, 1251 tests / 15 FAIL.
- GREEN: commit `ccac3a78031a7bbf3d9fcb01720bd8a69d90c7fd`, Actions 40156066387, 1251/1251 PASS, 15 Skills and 55 eval fixtures.
- No new Skill, Amazon Ads write, retry, idempotency, or external Executor behavior.

## Platform and reuse boundary

Amazon Ads official schedule-based bid-rule launch (2023-11-06) and event-based bid-rule launch (2025-01-02) establish time/event-dependent bid controls, but not this normalized schema or full execution proof. GitHub candidates KuudoAI/amazon_ads_mcp, promptfoo/promptfoo, OpenLineage/OpenLineage and Deltologic/datadoe-mcp were assessed for license, stars, recent activity and sampled CI. None solves this source-bound rule timeline problem without adding unverified dependency complexity. No third-party code, prompts, schemas, templates or workflows reused.

## Next falsifiable gaps

1. Complete source-supported rule execution history and comparison-window trigger/timezone coverage.
2. Amazon Business exclusive campaign marketplace/advertiser eligibility and connector capability binding.
3. Independent raw HTTP response authenticity for external readback adapters.
