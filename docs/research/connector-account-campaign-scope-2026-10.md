# Exact advertiser-account and campaign connector scope — 2026-10-26

## Verified non-duplicate gap

The generic `scripts/evaluate_connector_capability_gate.py` accepted `expected_scope` for region, marketplace, ad product and account type but not exact advertiser account or campaign. A Verified US Sponsored Products report binding could not be constrained to the caller's actual advertiser/campaign. This differs from the already implemented Global SP post-write readback identity check, which is not a general connector capability preflight.

## Read-only contract and minimal change

Add optional `expected_scope.advertiser_account_id` and `expected_scope.campaign_id` mapped to `scope.advertiser_account_ids` and `scope.campaign_ids` at both capability and Verified binding levels. These are repository-normalized, concrete, unpadded opaque IDs, **case-sensitive** to avoid false identity matches. Existing marketplace/region/ad-product/account-type case-insensitive semantics remain unchanged. Missing bounded scope blocks at capability level; unmatched concrete scope blocks; a present but unmatched scope with Unknown/Partial members degrades; a binding that does not verify the requested account/campaign cannot support high confidence. Existing calls omitting exact identities remain backward compatible.

This does **not** infer advertiser/campaign enrollment, Amazon Business eligibility, API permission, retail readiness, source authenticity, actual ad delivery, causal lift or live write authorization. Read-only/Suggest/Shadow remain default; an authorized external Executor owns writes, retries, idempotency and reconciliation. Missing/unsupported/partial/unknown never becomes zero.

## Deterministic RED → GREEN

- Baseline main: `af0299cb530480cbe97bd9b67411cfe07b747947`; no open PRs. Relevant old branches had zero commits ahead.
- Test commits: `f3b4c62493bf1c86bebd87da123d650ec517bf80`, `06696562cdaf134c986a66faa4be72c79fffecb2`.
- [RED Actions 40223225257](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40223225257): 1495 unit tests, 3 FAIL + 16 ERROR, because the old gate rejected all exact identity scope keys.
- Minimum code/schema commit: `20d4473c5105d9524f39250892906f47984fe01a`.
- [GREEN Actions 40223291984](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40223291984): 1495/1495 PASS, Skill Validator 15 PASS, Eval Validator 55 PASS.
- Twenty synthetic tests cover exact matches, wrong account/campaign, absent and unknown membership, valid alternative binding, case sensitivity, placeholders, legacy scope compatibility and never-zero policy. No real Amazon Ads account touched.

## Source, license and decision boundaries

Amazon Ads [MCP account context](https://advertising.amazon.com/API/docs/en-us/mcp/get-started), [Global SP campaign guide](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns), [advertiser product-group eligibility query](https://advertising.amazon.com/API/docs/en-us/mcp/advertiser-product-group-eligibility) and [Amazon Business exclusive SP announcement](https://advertising.amazon.com/en-gb/resources/whats-new/amazon-business-exclusive-campaign-for-sponsored-product) motivate independently preserving account, campaign, marketplace and eligibility evidence. They do not define the new internal schema or establish eligibility for a particular campaign. Open-source metadata, activity, sampled CI, PRs, license and rejection reasons are recorded in `docs/SOURCES.md`; no external implementation copied. Reddit practitioner discussion is hypothesis-generation only.

## Next falsifiable gap

Independently sourced, dated, account/campaign/marketplace-specific **feature eligibility** joined to connector capability and actual delivery; do not confuse this identity gate with enrollment. Other gaps: continuous rule activation intervals, adapter raw HTTP provenance, and cross-control/retail/profitability confounders.
