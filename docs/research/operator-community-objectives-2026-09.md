# Operator/community review: campaign mission before KPI judgment — 2026-09

## Why this review

GitHub engineering sources are useful for packaging, connectors and evaluation, but mature PPC operating practice also appears in seller/operator communities. Community evidence is treated as hypothesis/failure-mode discovery, not normative authority.

## Higher-authority Amazon evidence

Amazon Ads' current Sponsored Products Search Term documentation says search-term rows can be used to identify high-performing searches and negative candidates relative to advertiser goals, while the report only includes terms with at least one ad click. Amazon's Sponsored Brands goal-based campaign documentation explicitly ties campaign goals to different success metrics. Amazon's 2026 benchmark reporting also supports filtering by campaign goals. These sources support the general principle that optimization should be goal-aware rather than one universal KPI threshold.

## Community signals reviewed

Recent/representative r/FulfillmentByAmazon threads repeatedly expose the same operational tension: launch/ranking campaigns may intentionally accept short-run inefficiency, profit campaigns require unit economics, and reducing TACOS/ACOS without preserving the campaign's mission can destroy ranking/volume. Other operator threads emphasize inventory/listing readiness and the Search Term Report rather than bid-only tuning.

Adoption boundary: these posts are anecdotes. The repository does **not** adopt their fixed ACOS/TACOS targets, bid percentages, click thresholds, keyword counts, ranking promises, or claims of causal organic lift.

## Adopted invariant

Before role-specific optimization, preserve an explicit campaign-objective context. Use bounded roles (`Discovery`, `Control`, `Growth`, `Profit`, `Defense`, `Experiment`, `Unknown`) and allow `Unknown`. Do not infer mission from one performance ratio or campaign name. Role-specific tolerance never bypasses economics, retail readiness, evidence quality, safety guardrails or measurement comparability.

## Quora and other platforms

Public-platform discovery is allowed, but inaccessible/robots-blocked or unverifiable content is not converted into repository policy. A source must be inspectable enough to document what was learned and what was rejected.