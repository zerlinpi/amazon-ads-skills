# Sponsored Products retailer-scope/B2B control evidence — 2026-10-25

## Verified gap
The existing comparator validated Amazon Business placement values and Business-only site restriction independently, but repeated `ACROSS_RETAILERS` with a B2B placement modifier (even `0`) or exclusive routing could return `Treatment Isolated`. One-sided retailer-scope evidence was misclassified as an observed change rather than `Unknown`.

## Source boundaries
Amazon Ads across-retailers page (reviewed 2026-10-25): https://advertising.amazon.com/solutions/products/sponsored-products-across-retailers
Amazon Business-exclusive campaign launch (2025-10-31): https://advertising.amazon.com/en-us/resources/whats-new/amazon-business-exclusive-campaign-for-sponsored-product/
Placement help (prior dated review 2026-09-28): https://advertising.amazon.com/help/GYYZVM7LGSRYGWV5
Reddit reports are anecdotal, not causal evidence or platform bidding policy. Third-party licensing/acceptance details are in docs/SOURCES.md.

## Contract
Optional normalized `targeting_or_routing.state.retailer_scope` accepts only `AMAZON_STORE` and `ACROSS_RETAILERS`; one-sided presence is `Unknown`. Across-retailers conflicts with a B2B placement modifier (including numeric zero) or `site_restriction=AMAZON_BUSINESS`. Valid observed retailer changes remain confounders. Both-absent legacy evidence remains compatible without retailer or B2B eligibility proof. Mixed retailer/ad-group scope requires a separately verified adapter contract. No Amazon-native enum mapping, account/marketplace eligibility, connector authentication, actual delivery or causal effect is inferred.

## RED -> GREEN
RED test commit `f885a296538f2ae4c2a1bf07d6387f5c6b08aa22`: 21 deterministic cases; 1315 total tests, 15 failed (Actions 40166608309).
Production fix `c7f9fcd1573572e81a9459b943d7f6d11c89b781`: 1315/1315 unit tests and both validators passed (Actions 40166648485).
No live Ads writes, new Skill, external Executor, retry/idempotency behavior or third-party code reuse.

## Next gaps
P0 independently sourced marketplace/campaign eligibility and connector capability binding; P1 continuous rule activation/window coverage; P2 authentic raw HTTP provenance; P3 cross-control marginal/causal inference.
