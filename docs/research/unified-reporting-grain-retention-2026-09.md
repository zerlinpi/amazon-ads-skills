# Unified Reporting time-grain retention — 2026-09

## Gap

The repository already treated historical availability as a first-class evidence dimension, but its shared report-coverage contract did not explicitly encode that Amazon Unified Reporting history differs by requested time grain. That omission can turn unavailable older hourly rows into an apparent zero-activity interval or encourage silent coarsening from hourly to daily data.

## Amazon official evidence

Reviewed 2026-09-23.

Amazon Ads, **Streamline campaign analysis with the new unified reporting** (unBoxed 2025 launch material), states that Unified Reporting supports date ranges extending back **two weeks for hourly reporting**, **15 months for daily or weekly reporting**, and **up to six years for monthly, yearly, or summary-grain reporting**. It also describes standardized campaign metrics and flexible dimensions across Amazon Ads products.

Source: https://advertising.amazon.com/resources/whats-new/unboxed-2025-campaign-analysis-with-unified-reporting

Amazon Ads, **Campaign analysis with unified reporting, now available**, published 2026-06-08, confirms Unified Reporting general availability and cross-account, cross-ad-product, cross-country reporting with standardized metrics and dimensions.

Source: https://advertising.amazon.com/resources/whats-new/streamline-campaign-analysis-with-unified-reporting

## Decision consequence

Historical availability must be bound to the requested grain, not represented as one generic Unified Reporting retention value. A six-month daily report does not prove six months of hourly observability. Missing hourly rows outside the verified hourly window are unavailable/unknown evidence, not numeric zero. If intraday behavior is decision-critical, silently replacing hourly data with daily or weekly data changes the question and can hide within-day effects.

The shared contract therefore requires either a supported interval at the required grain, a lineage-compatible retained alternate source, or an explicit `Alternate Source` / `Missing Data` / `Hold` / `Manual Review` outcome.

## GitHub / implementation scan

Fresh searches for Amazon Ads reporting wrappers, MCP connectors, agent/evaluation frameworks and reporting systems did not produce a third-party source with stronger authority over current Amazon Unified Reporting retention semantics than Amazon's own documentation. Existing reviewed connector/runtime projects remain useful for transport and agent-engineering patterns, but they do not override Amazon's platform capability contract. No third-party code, prompt, schema, workflow or template was copied for this change.

## Adoption boundary

Adopt only the abstract fail-closed rule and the dated official capability evidence. Do not hard-code these windows as eternal platform constants; revalidate current official/API/account evidence when the exact retention limit materially affects a decision.
