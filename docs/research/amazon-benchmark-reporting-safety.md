# Amazon Benchmark reporting safety review

Review date: 2026-09-14

## Primary public sources reviewed

1. Amazon Ads Help — **Benchmark reporting**, updated June 10, 2026  
   https://advertising.amazon.com/help/GXRC3X4EEPXH8NVE
2. Amazon Ads What's New — **Benchmarks reporting now generally available worldwide**, published May 18, 2026  
   https://advertising.amazon.com/resources/whats-new/benchmarks-reporting-now-generally-available-worldwide

## Factual platform behavior retained

Amazon's current public documentation describes Benchmark reporting as peer-context measurement for eligible brand owners/representatives across supported Sponsored Ads and Amazon DSP campaigns.

Relevant facts used by this repository:

- peer groups are matched using characteristics including marketplace/country, average sales-price range, category classification for endemic advertisers, and ad product/format usage;
- privacy rules require at least 5 brands in a peer group;
- Campaign Manager can show a 50th-percentile/median benchmark, while API/downloadable reports can expose 25th and 75th percentile values;
- benchmark availability depends on eligibility, so absence of a benchmark does not imply a zero value;
- current GA benchmark metrics include selected new-to-brand, CTR, CPC, video-completion and CPM measures;
- benchmark reporting is available through Amazon Ads Console and API/reporting surfaces for supported use cases.

These facts are treated as current report characteristics rather than timeless assumptions. Marketplace, ad-product, metric and acquisition-channel support must still be read from the active reporting contract.

## Independent adaptation

The repository already had `references/benchmark-policy.md`, so no new benchmark Skill or duplicate shared reference was created.

The current Amazon reporting behavior was independently adapted into four safety principles:

1. **Peer context is not an authorization threshold.** Below median/25th percentile can prioritize investigation but does not make a campaign unhealthy by itself.
2. **Percentile gap is not a causal diagnosis.** It does not identify whether bid, budget, placement, targeting, creative, retail state or market competition is the binding mechanism.
3. **Missing benchmark is not zero.** Eligibility, minimum peer population, report configuration, marketplace/ad-format support or connector capability can explain missing data.
4. **Peer performance is not account economics.** A campaign should not be forced toward a peer metric when doing so conflicts with its objective, profitability, incrementality or retail guardrails.

Deterministic policy tests guard the failure mode where peer percentiles are treated as universal health/action thresholds and require Campaign Health Monitor to route material peer comparisons through the shared benchmark policy. A separate regression fixture was intentionally not retained because these repository-contract invariants are mechanically testable without increasing the fixture pack solely for count.

## Copyright / license adoption boundary

Amazon Help and What's New pages are public vendor documentation, not source code offered under this repository's MIT license.

No Amazon prose, screenshots, UI assets, report templates, API schemas, examples or proprietary peer-matching implementation were copied. Only factual platform/report behavior was summarized, and the decision framework was independently written for this repository.

No third-party open-source implementation was adopted in this change, so no additional software license obligations were introduced.
