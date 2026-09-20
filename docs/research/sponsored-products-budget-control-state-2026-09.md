# Sponsored Products budget control-state causality — 2026-09

Reviewed: 2026-09-20

## Highest-value gap

The repository already modeled `budget_or_pacing` as a material control and had strong upstream-cap, marginal-headroom and opportunity-cost rules. The machine-readable control requirement registry, however, had only one production surface: `sponsored_products_bid_change`.

That meant a post-change review for an intended Sponsored Products budget change could not establish a registry-verified material-control set. The deterministic comparator correctly failed closed to `Unknown`, but the budget workflow had no path to `Treatment Isolated` even when complete evidence existed.

A second, related semantic gap was that a generic `budget_or_pacing` value did not prove whether the evidence represented the configured average daily budget, an automated rule-adjusted effective budget, or only realized spend.

## RED evidence

The test-only commit added two deterministic expectations before implementation:

1. the versioned registry must contain `sponsored_products_budget_change` with an official-evidence-backed material-control set;
2. when only `budget_or_pacing` changes inside that complete set, the comparator should return `Treatment Isolated`, while a concurrent base-bid change should be `Confounded`.

GitHub Actions run 35492876970 failed exactly at this boundary: the registry lookup raised a missing-surface error and the comparator returned `Unknown` rather than `Treatment Isolated`.

## Current Amazon evidence

Amazon Ads Help, **Understand budget rules in Sponsored ads**, updated September 2, 2026, documents schedule-based and performance-based budget rules that automatically increase campaign daily budgets when their conditions are met. It also documents that multiple applicable rules can cumulatively affect the daily budget.

Source: https://advertising.amazon.com/help/GNSMLANWNF344YBE

Amazon Ads' sponsored ads daily budgeting policy announcement documents the campaign budget as an average daily budget and states that day-level spend can be higher than the average under the applicable policy/settings, with the amount averaged over the month.

Source: https://advertising.amazon.com/resources/whats-new/sponsored-ads-daily-budgeting-policy-and-options

Amazon Ads Help, **Bidding strategies for Sponsored Products**, updated September 14, 2026, documents dynamic, fixed and rule-based bidding and audience bid adjustments. Existing repository evidence separately covers placement adjustments and scheduled/event bid rules. Together, these surfaces justify keeping bid strategy, placement, audience, bid-rule and budget/pacing controls in the causal proof boundary for an intended budget change.

Source: https://advertising.amazon.com/help/GCU2BUWJH2W3A8Z7

These are product facts, not an Amazon API schema. The repository does not assume that every connector exposes every rule field or that the current product behavior is permanent across all marketplaces and generations.

## Independent implementation

The repository-authored change is deliberately narrow:

- register `sponsored_products_budget_change` in the existing control-requirement registry;
- require `budget_or_pacing.state` for that surface to preserve `base_average_daily_budget`, `effective_daily_budget`, and source-supported `active_budget_rules`;
- fail closed to `Unknown` when any of those budget-state facts are unavailable;
- route the existing budget Skill through the shared control-state comparator for causal post-change questions;
- add a synthetic eval where automatic budget rules change effective budget without a manual budget edit.

No live Amazon Ads mutation, retry, idempotency, reconciliation, credential handling, or connector implementation is added.

## GitHub discovery review

Fresh multi-query discovery also reviewed several newly surfaced projects. Stars are point-in-time discovery context only, not authority.

- **MarketplaceAdPros/amazon-ads-mcp-server** — about 29 stars; MIT; last code push observed 2025-05-21. It is a real TypeScript MCP wrapper, but no repository Actions workflow or test suite surfaced and much of the useful behavior depends on a hosted MarketplaceAdPros service. Rejected as implementation evidence for this gap; no code/tool schema/auth workflow was copied.
- **Xnurta/Xnurta-MCP** — about 14 stars; very active through 2026-09-18. The public repository exposes Skills/manifests/docs and documents live ad editing, but no root license file or license metadata surfaced. It therefore serves only as connector-domain context; no Skill text, prompt, manifest, workflow or write semantics were reused.
- **jshorwitz/awesome-agentic-advertising** — about 40 stars; no license surfaced; README-only curated index. Useful for discovery, not independent engineering evidence, so it is not counted as a separate implementation source.
- **elementary-data/elementary** — about 2.4k stars; Apache-2.0; actively maintained with substantial CI. Its data-observability/freshness engineering is strong generic corroboration, but the repository already has source/freshness/backfill/lineage contracts. Adding an observability runtime would duplicate infrastructure rather than close this Amazon control-state gap.
- **langfuse/langfuse** — about 34.8k stars; actively maintained; core is MIT while enterprise directories use a separate restricted license. Its trace/evaluation platform is useful external-runtime infrastructure, but this repository already has deterministic fixtures and effectiveness contracts. No dependency, evaluator, trace schema, prompt or enterprise code was adopted.

## Copyright and license boundary

Amazon Help/What's New pages are public vendor documentation, not open-source code. Only factual product behavior is paraphrased. MarketplaceAdPros is MIT, Elementary is Apache-2.0, Langfuse has a mixed open-core license boundary, and the other newly reviewed repositories above had no reusable license boundary established for this change. No third-party code, prompt, schema, workflow, template or substantial prose is copied.

## Remaining boundary

This closes the budget-specific registry/effective-state gap, not every causal confounder. A future high-value review should test whether production control surfaces need a stronger machine requirement for targeting/negative/routing stability, because a changed traffic-routing control can also invalidate single-control attribution.
