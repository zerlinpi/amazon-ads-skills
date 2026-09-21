# Cross-ad-product attribution competition — 2026-09

## Gap found

The repository already models attribution variant, date attribution, maturity and reporting-generation drift, but performance-drop diagnosis did not explicitly require a cross-ad-product credit-allocation check before interpreting a product-level attributed-conversion decline as shopper conversion deterioration.

## Fresh official evidence

Amazon Ads Help, **Conversion attribution**, updated August 5, 2026, states that eligible Amazon ad products for brands compete for attribution. When a shopper interacts with multiple eligible ads, attribution considers relevance to the sold product and uses a last-touch hierarchy that prioritizes clicks over views. The same help page also documents that Amazon DSP conversions are reported on conversion date, reinforcing the need to preserve date-attribution semantics separately from credit-allocation logic.

Source: https://advertising.amazon.com/help/G3BB9TWP5KC375TJ

Amazon Ads' January 1, 2026 Store-ads attribution launch remains relevant for a different boundary: standard conversion metrics for eligible view-attributed inventory changed methodology while `all views` metrics remained separately available. That is an attribution-variant cutover, not the same thing as cross-product credit competition.

Source: https://advertising.amazon.com/resources/whats-new/view-attribution-updates-for-amazon-store-ads

## Decision implication

A Sponsored Products campaign can show stable traffic but fewer attributed purchases after Sponsored Brands, Sponsored Display or DSP activity changes. That observation alone does not prove shopper conversion propensity fell. Cross-product attribution competition is a competing measurement/credit-allocation hypothesis that should be checked before aggressive bid suppression.

This does **not** mean every product-level decline is caused by attribution competition. The safe sequence is:

1. observe the attributed conversion change;
2. verify comparable windows, attribution maturity and metric semantics;
3. inspect material activity changes in other eligible ad products when evidence is available;
4. keep `Observation` separate from the attribution-competition `Hypothesis`;
5. downgrade to `Directional`/`Hold` when the required cross-product evidence is unavailable and the distinction could change the action;
6. only assign a cause after competing retail, traffic, control and measurement explanations are reconciled.

## Implementation boundary

Adopted only as a decision-safety rule in `performance-drop-diagnosis` plus an eval fixture. No Amazon API implementation, attribution algorithm, ranking formula or write behavior is copied or implemented. Live writes remain outside the repository.
