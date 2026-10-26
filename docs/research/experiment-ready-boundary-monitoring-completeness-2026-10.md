# Complete optional Ready holdout monitoring (v1.78.0)

Reviewed 2026-10-26. Adopted: narrow semantic safety fix, MINOR. No Amazon Ads account writes.

## Reproducible gap

A supplied `comparison.boundary_monitoring` on a `Ready` holdout was ignored when `material_scope_changes` was empty or omitted. This permitted `current_status` and `latest_verified_at` to be absent, null, malformed or timezone-naive while still returning Ready. A supplied `launch_verified_at` after `latest_verified_at` also passed. The earlier v1.77.0 positive re-verification guard only ran for recorded material changes, so this is distinct.

## RED → GREEN

Starting main `867bbfd573b1962358c2401a433cebfbd658ef55`, no open PR. Sampled old experiment/rule branches had no commits ahead of main. RED test commit `6983ef9dcc136206d89bcddc46ba50b78ca045b1`: [Actions #40281384600](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40281384600), 1627 tests / 9 FAIL, five compatibility cases passed. Minimal production commit `209584832e0dc89f92a076e29d3c43a92d428f52`: [Actions #40281435606](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40281435606), 1627/1627 PASS, 15 Skills and 55 eval fixtures PASS. Fourteen synthetic tests.

When a Ready holdout explicitly supplies monitoring, require `current_status = Clean`, a valid timezone-aware `latest_verified_at`, and a valid optional `launch_verified_at <= latest_verified_at`, regardless of material-change list length. Existing positive `reverified: true` and per-change chronology still apply. Monitoring remains optional for legacy Ready, and exploratory Shadow/Hold/Redesign may retain unknowns. This is not remote source attestation or a complete schema validator.

## Source and rights assessment

Official Amazon Ads schedule bid rules (2023-11-06), event-based bid rules (2025-01-02), and Amazon Brand Lift methodology (updated 2025-05-02) establish time-varying controls or product-specific exposed/control design. None defines the repository's monitoring fields, a fixed verification TTL, or authenticates Ads delivery. See `docs/SOURCES.md` for exact official links.

New candidate ferrants/amazon-seller-agent-claude-code (8 stars, non-fork, SPDX NOASSERTION, two sampled successful Actions) and AlchemyCollectives/amazon-seller-agent (0 stars, fork, SPDX NOASSERTION, no sampled Actions) rejected for code import. Marketplace Ad Pros bundled Skills have separate licensing statements, and neither offers independent evidence for this guard. Re-reviewed KuudoAI/amazon_ads_mcp (MIT), promptfoo (MIT), OpenLineage (Apache-2.0), Agent Skills (Apache-2.0); no dependency adoption justified. No third-party code, prompts, schemas, templates or workflows copied.

## Residual gaps

P0 external authentication of holdout isolation and delivery requires an authorized provider with source evidence, not new self-declared flags. P1 continuous schedule/event/budget rule execution history over the comparison window. P2 auction/budget/ASIN interference and marginal contribution-profit causality. Maintain Read-only/Suggest/Shadow, never-zero unknowns and external authorized Executor for all live writes/retries/reconciliation.
