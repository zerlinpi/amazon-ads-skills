# Feature-specific eligibility joined to exact connector scope — 2026-10-26

## Reproduced non-duplicate gap

Baseline main: `8747be4cf4259ba26ab787ac06d212da5c636a81`. No open PRs. Relevant prior feature/connector branches had zero commits ahead. Existing exact account/campaign connector capability checks (v1.66) and canonical observation access (v1.67) prove only read-side coverage; they cannot establish advertiser, campaign, or marketplace feature enrollment. A high-confidence connector Pass was possible without any independently supplied feature-specific eligibility evidence.

## Minimal optional evidence join

When a decision explicitly depends on feature eligibility, callers can supply `feature_eligibility_requirement` containing a concrete feature ID, marketplace, exact advertiser-account and campaign IDs, `as_of` and a finite `max_age_seconds`. The account/campaign/marketplace MUST match the caller's `expected_scope` (opaque IDs case-sensitive). A separately supplied `feature_eligibility_evidence` record must match the same feature and identities, declare `evidence_type=feature-specific`, `verification_status=Verified`, a concrete source system/reference, and a valid known-offset observation within the requested horizon.

Verified `Eligible` allows the *eligibility subgate* to pass subject to the independently existing connector capability gate. Verified `Ineligible` blocks; missing, partial, unknown, stale, future, generic advertiser-product-group, unverified, mismatched, or source-ambiguous evidence degrades. No evidence is coerced to zero. No feature requirement means legacy connector behavior is unchanged. This is a repository-owned normalized read-side **evidence consistency** check, not a live Amazon entitlement query, proof of enrollment, API permission, authenticated raw response, or write authority. A `Verified` label and source reference remain adapter-supplied claims; external authentication and authorized execution are out of scope. For new campaigns without a campaign ID, do not invent one or claim campaign-level eligibility.

## Deterministic RED → GREEN

- RED test commit `e426200e49ab7172832a9ae3f38ac11e6653feb0`: 22 synthetic tests. [Actions #40232208710](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40232208710) ran 1531 tests with **20 FAIL + 1 ERROR** because the old gate ignored the eligibility requirement and did not emit its subgate effect.
- Minimal code commit `59af08746c112ac516ff454749a64c423f75780a`: [Actions #40232275602](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40232275602) **1531/1531 PASS**, 15 Skill validations PASS, 55 Eval fixtures PASS.
- No Amazon Ads account writes, retries, idempotency, external Executor, third-party code reuse, or new Skills.

## Sources and licensing

[Amazon Ads MCP account context](https://advertising.amazon.com/API/docs/en-us/mcp/get-started) distinguishes profile, manager and advertiser account IDs. [Advertiser product-group eligibility](https://advertising.amazon.com/API/docs/en-us/mcp/advertiser-product-group-eligibility) describes a separate product-group query and is **not** proof of Amazon Business exclusive campaign enrollment. [Amazon Business exclusive SP launch](https://advertising.amazon.com/resources/whats-new/amazon-business-exclusive-campaign-for-sponsored-product) (2025-10-31) explicitly limits creation to eligible advertisers in supported marketplaces. [Global SP guide](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns) distinguishes global campaign and per-marketplace context. These vendor facts motivate a separate eligibility gate; none defines this repository's normalized fields or independently verifies the caller's source record.

Candidate open-source metadata, sampled CI/PRs and rejection reasons are recorded in `docs/SOURCES.md`. No external code, prompts, schemas, templates or workflows copied. Public PPC/Reddit anecdotes are hypothesis discovery only, not platform entitlement evidence.

## Next falsifiable gaps

P0: source-authenticated eligibility provenance / external live entitlement reconciliation, without equating generic product-group eligibility to B2B enrollment. P1: continuous schedule/event/budget-rule activation evidence across a comparison window. P2: authenticated raw HTTP adapter responses. P3: control interaction, marginal economics and causal confounders.
