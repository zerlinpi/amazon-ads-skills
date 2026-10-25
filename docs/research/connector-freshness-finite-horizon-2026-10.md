# Connector freshness finite-horizon validation — 2026-10-25

## Verified defect
scripts/evaluate_connector_capability_gate.py accepted Python float NaN and positive infinity for freshness_requirement.max_age_seconds. Since age > NaN and age > Infinity both evaluate false for finite ages, stale snapshot and binding evidence could be classified as current, producing high-confidence Pass. Python JSON parsing may also produce infinity from an overflowing numeric literal such as 1e309. This is a repository-side numerical safety defect, not an Amazon Ads API rule.

## Contract and tests
Require a finite non-negative numeric freshness horizon before comparing snapshot/binding/supporting-evidence timestamps. Reject NaN, infinity and overflow. Preserve zero and finite positive horizons, legacy omitted freshness requirements, and the existing chronological proof rules. Eight synthetic deterministic cases; RED Actions 40174166525: 1336 tests, three failures; GREEN Actions 40174214895: 1336/1336 plus Skill and eval validators.

## Platform and open-source boundary
Amazon Ads unified reporting launch (2026-06-08): https://advertising.amazon.com/resources/whats-new/streamline-campaign-analysis-with-unified-reporting ; Marketing Stream v2 overview: https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/overview . These are reporting context, not definitions of our TTL. Candidate repositories, sampled licenses/activity and rejection rationale are recorded in docs/SOURCES.md. No third-party code or restricted assets reused.

## Remaining gaps
P0 marketplace/advertiser/campaign eligibility joined to exact connector capability, scope and timestamp; P1 continuous rule-activation interval evidence; P2 authenticated raw HTTP provenance; P3 cross-control causal attribution and marginal profitability. Do not treat any of these as resolved by a finite freshness horizon.
