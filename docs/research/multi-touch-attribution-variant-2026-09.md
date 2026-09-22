# Amazon Ads multi-touch attribution variant review — 2026-09

Reviewed: 2026-09-23.

## Fresh official evidence

Amazon Ads' public multi-touch attribution launch material says multi-touch attribution distributes credit for Amazon purchase conversions across multiple Amazon Ads touchpoints according to estimated contribution, while familiar standard attribution is last-touch. It exposes separately designated multi-touch Orders, Sales and ROAS alongside standard metrics.

The same Amazon source states that multi-touch metrics are available for United States advertisers across the ad console, Amazon DSP campaign manager, sponsored-ads downloadable reports, Amazon DSP downloadable custom reports, most Amazon Ads API v3 report types, and Amazon Marketing Stream conversion datasets for Amazon DSP, Sponsored Products, Sponsored Brands and Sponsored Display.

These are point-in-time product/capability facts, not a universal guarantee for every marketplace, report type, dimension or connector.

## Gap found

The repository already treats attribution variant as first-class measurement identity for standard/default versus `all views`, but it had no explicit multi-touch contract. A connector can therefore expose generic Orders/Sales/ROAS fields while stripping or mixing the MTA designation, or two comparison windows can silently use last-touch versus multi-touch credit allocation.

That can create a false performance break even when shopper behavior did not change.

## Adoption

Adopt only the generic measurement-safety invariant in `references/multi-touch-attribution.md`:

- preserve `attribution_variant` explicitly;
- last-touch and multi-touch metrics are not interchangeable;
- verify marketplace, report/dataset and connector capability rather than assuming global availability;
- missing MTA is an observability/capability gap, not zero;
- an unreconciled variant shift is a measurement hypothesis, not a confirmed business cause;
- do not base aggressive bid/budget/pause/negative/scaling actions solely on an unreconciled MTA-vs-last-touch delta.

No Amazon prose, schema, API implementation, prompt or workflow is copied. Amazon documentation is proprietary; only factual behavior and an independently written generic safety policy are recorded.

## GitHub / open-source review boundary

Fresh searches also rechecked Amazon's `amzn/amazon-marketing-stream-examples` (MIT-0, non-fork, active reference implementation) for Stream dataset engineering. It remains useful for dataset/subscription evidence but does not define the business semantics of multi-touch attribution more authoritatively than Amazon Ads' product announcement. No code is adopted.

Forks/mirrors of the Amazon Stream sample and low-evidence wrappers are not counted as independent evidence. High stars alone would not justify adoption; no newly discovered open-source project supplied stronger, current MTA semantics plus a clearer license/engineering basis than the first-party Amazon source.
