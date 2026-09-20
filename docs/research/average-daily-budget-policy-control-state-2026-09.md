# Average daily budget policy as control state — 2026-09

## Gap

The repository already distinguished configured campaign budget, effective budget, active budget rules and realized spend. The remaining causal gap was the account/platform average-daily-budget policy or setting that can permit realized daily spend above the configured average daily budget. Without preserving that state, a before/after budget comparison can incorrectly attribute a one-day spend increase to a manual campaign budget edit.

## Official evidence reviewed

Amazon Ads, **New sponsored ads daily budgeting policy and options** (May 9, 2023): Sponsored Products, Sponsored Brands and Sponsored Display daily budgets are average daily budgets; Amazon documents daily spend flexibility and an account setting/API for additional spend from leftover amounts. This is first-party product behavior, not copied implementation text.

Source: https://advertising.amazon.com/resources/whats-new/sponsored-ads-daily-budgeting-policy-and-options

Amazon Ads, **Budget rules now available in Amazon advertising console globally** (August 12, 2021) and the current **budget rules** guide: schedule- and performance-based rules can automatically increase campaign budgets. These remain distinct from the average-daily-budget policy state.

Sources:
- https://advertising.amazon.com/resources/whats-new/dynamic-budget-control
- https://advertising.amazon.com/library/guides/budget-rules

## Adoption boundary

No Amazon API schema, request payload, proprietary implementation, examples, thresholds or prose are copied. The repository independently records the generic safety requirement as `average_daily_budget_policy` inside the existing `budget_or_pacing` causal state. This is an evidence label, not an assertion that every connector exposes the setting under that field name.

If the active connector/export cannot observe the applicable policy/setting, causal coverage remains incomplete/unknown. Missing policy evidence is not interpreted as disabled, zero, or unchanged.

## Why this outranks broader feature additions

This closes a false-causality path in an existing high-impact Skill without adding a Skill, executor, write path or speculative optimization heuristic. It directly improves decision quality and action safety while preserving the repository's read-only/Suggest default.
