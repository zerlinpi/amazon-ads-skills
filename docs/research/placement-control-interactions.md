# Placement control interaction research

Reviewed 2026-09-10 for the `placement-optimization` hardening pass.

## Public Amazon Ads references

The following public vendor documentation was used only to verify factual Sponsored Products control behavior:

- Amazon Ads, **Improve your campaign performance on rest of search placements using Sponsored Products rest of search bid adjustment control** (January 9, 2024): placement adjustments are available for Top of Search, Product Pages, and Rest of Search, and the Rest of Search control is available with both fixed and dynamic bidding strategies.
  - https://advertising.amazon.com/resources/whats-new/improve-campaign-performance
- Amazon Ads, **Guide to dynamic bidding - up and down with Sponsored Products**: dynamic up/down changes bids in real time based on predicted conversion likelihood and Amazon recommends limiting overlapping changes when testing so performance differences remain interpretable.
  - https://advertising.amazon.com/library/guides/dynamic-bidding-sponsored-products
- Amazon Ads, **Events for schedule bid rules, now available for Sponsored Products advertisers** (January 2, 2025): event-based rules can automatically increase campaign bids during selected traffic events.
  - https://advertising.amazon.com/resources/whats-new/event-based-bid-rules-for-sponsored-products-advertisers
- Amazon Ads, **Schedule based bid rules now available for Sponsored Products** (November 6, 2023): bid rules can change bids by time/day/date range, adding another time-varying bidding control.
  - https://advertising.amazon.com/resources/whats-new/schedule-based-bid-rules-available-for-sponsored-products

## Adopted generic method

The repository does **not** copy Amazon documentation prose, UI assets, formulas, API examples, or proprietary implementation. Public vendor documentation is not treated as open-source code.

Only these factual/control-design implications were independently rewritten:

1. placement modifiers do not operate in isolation when campaign bidding strategy and other bid rules are active;
2. configured bid controls should be separated from realized placement delivery/CPC evidence;
3. material control changes require an effective-time timeline before causal attribution;
4. when exact control-composition/order is not documented for the active configuration, the Skill must not invent a deterministic auction-level effective-bid formula;
5. historical placement ROAS/CVR is evidence about realized past traffic, not a guarantee of marginal efficiency after another modifier increase;
6. overlapping control changes should downgrade causal attribution and favor Hold/Shadow/Experiment over another immediate material change.

## Repository adaptation

Implemented as:

- `skills/placement-optimization/references/realized-bid-exposure.md`;
- a thinner routing contract in `skills/placement-optimization/SKILL.md`;
- `evals/fixtures/placement-coupled-controls-confounded-lift.json`.

Safety remains `Read-only / Suggest / Shadow` by default. Live writes, retry, idempotency, and authoritative readback remain external Connector/Executor concerns.
