# Contextual benchmark policy

Amazon Ads benchmarks are comparison evidence, not universal authorization thresholds.

Load this reference when a recommendation materially uses Amazon Ads Benchmark reporting, another platform benchmark, an industry benchmark, or a third-party cohort comparison.

## Comparison priority

Use the narrowest defensible baseline in this order:

1. Same account, same objective, same attribution definition, prior comparable period.
2. Same account experiment or holdout.
3. Same ASIN/campaign historical cohort with comparable promotion and inventory state.
4. Comparable external cohort with disclosed methodology.
5. Broad platform/industry benchmark, directional only.

A peer benchmark can add context to an internal baseline. It does not replace the account's own economics, causal evidence, or historical response.

## Amazon Ads Benchmark reporting contract

Amazon's current public Benchmark reporting documentation describes a standardized peer comparison available for eligible brand owners/representatives across supported Sponsored Ads and Amazon DSP campaigns.

For current Amazon benchmark data, preserve these semantics when they matter:

- the comparison is against a **peer group**, not the whole category or all advertisers;
- Amazon describes peer matching using characteristics such as campaign country/marketplace, average sales-price range, category classification for endemic advertisers, and ad product/format usage;
- peer groups require a **minimum of 5 brands** for privacy;
- Campaign Manager may show the peer median (50th percentile), while API/downloadable reporting can expose the 25th and 75th percentile values;
- benchmark availability is eligibility-dependent, so not every campaign/account is guaranteed to have a benchmark row;
- current benchmark metrics include selected acquisition, traffic and video metrics such as new-to-brand purchase measures, CTR, CPC, video completion measures and CPM; metric availability can vary by ad product/format and should be read from the active report contract rather than assumed;
- Amazon exposes benchmark insights through Ads Console and API/reporting surfaces, but acquisition-channel capability still needs to be verified for the active connector.

Treat these as current vendor-report characteristics, not permanent constants for every marketplace, ad product, API generation or future methodology.

## Before using an external benchmark

Record or state when known:

- source and retrieval date;
- geography and marketplace;
- ad type / campaign type / format;
- objective;
- industry/category;
- peer-group identity or available peer-group descriptors;
- sample size/population or disclosed peer-group size range;
- mean/median/percentile/case-study status;
- attribution and conversion definition;
- observation window and seasonality;
- currency/tax treatment where relevant;
- acquisition channel and report generation when relevant;
- why the cohort is comparable;
- known methodology limitations.

If a missing field could materially change the decision, mark the benchmark `provisional`.

For Amazon Benchmark reporting specifically, do not assume that two benchmark observations from different dates have an identical peer population unless the available methodology/peer-group descriptors support that assumption.

## Missing benchmark handling

A **missing benchmark** is not evidence of zero peer performance, zero account performance, poor performance, or no opportunity.

Possible explanations include eligibility, insufficient peer-group population, unsupported marketplace/ad product/format, report configuration, acquisition-channel capability, or unavailable dimensions/metrics.

Therefore:

```text
missing benchmark
!= benchmark value = 0
!= account underperformance
!= automatic Hold/Critical classification
```

When the active connector does not expose a benchmark that Amazon documents elsewhere, record the capability gap and keep the comparison unavailable rather than fabricating a zero.

## Interpretation rules

- A benchmark gap is an observation, not a root cause.
- Below-median or below-25th-percentile performance does not by itself prove a campaign is unhealthy or that a specific control should change.
- Above-median or above-75th-percentile performance does not by itself prove profitable incremental headroom or justify scaling.
- Do not convert a peer percentile into a bid, budget, placement, targeting or negative-action magnitude.
- Do not replace a low-volume account segment with an industry average just to produce a number.
- Do not mix ROAS/TACOS/ACOS from incompatible attribution or revenue definitions.
- Platform-published uplift claims are evidence from the platform, not expected outcomes for this account.
- Fixed click, conversion, budget, CVR, CTR, ACOS or scaling thresholds may be used as optional heuristics only when explicitly labeled and bounded by account evidence.
- A peer benchmark can help prioritize investigation, but action safety still requires account economics, retail readiness, measurement comparability, and a plausible binding control/mechanism.

## Safe use patterns

### Contextualize

Use the benchmark to say that the account/campaign is above, near, or below a comparable peer distribution for a compatible metric.

### Prioritize investigation

A persistent peer gap can justify checking the relevant mechanism: creative/relevance for CTR, auction cost/competition for CPC, or acquisition strategy for new-to-brand measures.

### Avoid target substitution

Do not make "reach the peer median" the optimization objective unless the business explicitly adopts that target and it is compatible with profitability, incrementality and other guardrails.

### Avoid causal substitution

A category-wide benchmark movement can be a market-context clue, but it does not prove why this account changed. Internal time-series, control history and retail/market evidence remain necessary for causal claims.

## Required output

When a benchmark materially influences a recommendation, include:

- account value;
- comparison value and percentile/statistic;
- comparison source/type;
- peer/cohort fit;
- benchmark eligibility/availability status;
- retrieval window/date when relevant;
- confidence;
- what decision the comparison informs;
- what the benchmark does **not** prove;
- what additional account evidence supports the recommendation.

This reference never authorizes a live Amazon Ads write.
