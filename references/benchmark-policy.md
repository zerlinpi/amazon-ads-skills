# Contextual benchmark policy

Amazon Ads benchmarks are comparison evidence, not universal authorization thresholds.

## Comparison priority

Use the narrowest defensible baseline in this order:

1. Same account, same objective, same attribution definition, prior comparable period.
2. Same account experiment or holdout.
3. Same ASIN/campaign historical cohort with comparable promotion and inventory state.
4. Comparable external cohort with disclosed methodology.
5. Broad platform/industry benchmark, directional only.

## Before using an external benchmark

Record or state when known:

- source and retrieval date;
- geography and marketplace;
- ad type / campaign type;
- objective;
- industry/category;
- sample size/population;
- mean/median/percentile/case-study status;
- attribution and conversion definition;
- observation window and seasonality;
- currency/tax treatment where relevant;
- why the cohort is comparable;
- known methodology limitations.

If a missing field could materially change the decision, mark the benchmark `provisional`.

## Interpretation rules

- A benchmark gap is an observation, not a root cause.
- Do not replace a low-volume account segment with an industry average just to produce a number.
- Do not mix ROAS/TACOS/ACOS from incompatible attribution or revenue definitions.
- Platform-published uplift claims are evidence from the platform, not expected outcomes for this account.
- Fixed click, conversion, budget, CVR, CTR, ACOS or scaling thresholds may be used as optional heuristics only when explicitly labeled and bounded by account evidence.

## Required output

When a benchmark materially influences a recommendation, include:

- account value;
- comparison value;
- comparison source/type;
- cohort fit;
- confidence;
- what decision the comparison informs;
- what additional account evidence supports the recommendation.
