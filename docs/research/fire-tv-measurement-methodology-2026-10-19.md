# Fire TV display measurement methodology cutover — 2026-10-08

Reviewed: 2026-10-19  
Status: official-source measurement-comparability watch; no API/connector implementation.

## Official evidence and scope

The Amazon Ads support-center notice announces a **Fire TV display-supply measurement-methodology change effective 2026-10-08**. Impressions and clicks that fail the revised criteria are excluded from reported totals. Amazon estimates an **approximately 15% impression and 11% click impact across Fire TV display supply**; individual advertiser effects vary by campaign, marketplace and placement mix. Amazon says forecasts were updated and the new methodology aligns with MRC standards.

Source: https://advertising.amazon.com/help/ref=ams_head_help (support-center notice visible during 2026-10-19 review; a stable detail-page URL was not established).

These are **aggregate platform estimates, not campaign-level adjustment factors**. The notice alone does not establish a metric-specific API schema, whether historical rows were restated, or how an individual advertiser was affected.

## Decision consequence

When a comparison crosses 2026-10-08 and includes Fire TV display supply, preserve the reporting source, metric definition/version, marketplace, placement/supply mix, report extraction time, observed date grain and available methodology evidence. A raw pre/post decrease in reported impressions or clicks is not sufficient proof of delivery deterioration, bid inefficiency, creative fatigue or a causal effect from an advertiser action.

If methodology equivalence or any historical restatement is not verified, classify affected before/after metric comparisons as **Not Comparable** or at most **Directional**, and hold causal claims and automated sizing based on those metrics. Preserve the underlying observed values; do **not** impute missing observations as zero, and do **not** multiply campaign data by 1/0.85 or 1/0.89 to manufacture a normalized series. Separate unaffected ad products/supply only where verified segmentation permits.

This is already covered in principle by `references/data-lineage.md`, `references/report-coverage.md` and the post-change causal-confounder gates. No new Skill, connector capability ID, schema field, runtime permission or live write is justified by this notice alone.

## Conditional deterministic test

Only after an actual versioned Fire TV reporting envelope is available: construct a synthetic before/after fixture crossing the cutover with identical campaign controls but unresolved measurement-methodology identity. RED should demonstrate that the current evaluator incorrectly treats it as comparable, if that behavior actually exists. GREEN must hold causal/action conclusions without changing raw metrics. Run full unit, Skill and Eval validation before any behavior change.

## Adoption, rejection and rights

**Adopt:** independently expressed, date- and supply-scoped comparability warning grounded in Amazon's public notice.  
**Reject:** treating the aggregate 15%/11% figures as per-account correction multipliers; asserting a universal API schema, retroactive restatement, or cross-product applicability; introducing an unverified behavior change.

Amazon's notice is copyrighted vendor material; only facts and independent safety reasoning are recorded. No Amazon prose, API schema, code, prompt, template or workflow was copied.
