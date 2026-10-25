# Connector scope placeholder and exclusion evidence — 2026-10-25

## Fresh-read baseline and gap

At main `65a666da49b766c06f3e168a9f260780515203f6` (v1.58.0), no open PR existed; sampled historical branches were behind main. The connector gate accepted `expected_scope.marketplace="Unknown"` when a capability and binding both listed `"Unknown"`, potentially returning high-confidence Pass. It also treated an unmatched observed list such as `["US", "Unknown"]` as definitive proof that `JP` was unsupported, rather than preserving uncertainty. This is distinct from previous snapshot connector ID, binding identity, access mode, and timestamp repairs.

## RED → GREEN

Test commit `50500f991d8f92fe7f45d66f872d5eb5fcc33838` before production repair: [Actions 40190109725](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40190109725), 1397 tests, 12 FAIL. Minimal code commit `f4fabf40499d5b71f323792d8638758f9925a254`: [Actions 40190166935](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40190166935), 1397 PASS, 15 Skills PASS, 55 eval fixtures PASS. Seventeen deterministic synthetic cases; no live Amazon Ads reads or writes.

## Decision boundary

A requested connector decision scope must be a concrete identity, not a repeated Unknown/Unsupported/Partial/Missing/Unavailable/Not Available/Not Supported label or whitespace-padded string. For a capability or verified binding scope, a matching concrete member proves only that bounded connector surface; an unmatched list containing an unavailable/malformed member is Unknown, not proof of marketplace, ad-product, region or account-type exclusion. A fully concrete unmatched list remains blocked. No scope list alone establishes Amazon Business advertiser/campaign eligibility, account entitlement, actual delivery, or authority to write.

The repair reuses the existing whole-label identity check. It rejects unusable caller-requested scope values, distinguishes an observed concrete match from an unknown unmatched list, and preserves definitive exclusion only for a fully concrete mismatch. It does not assert Amazon-native API enum equivalence, full scope-list completeness, marketplace entitlement, advertiser enrollment, campaign eligibility, or actual placement delivery. An unmatched unknown list is not zero or an affirmative exclusion.

## Source, adoption and copyright review

Official [Amazon Ads MCP account context](https://advertising.amazon.com/API/docs/en-us/mcp/get-started) distinguishes marketplace/account selection. Official [advertiser product-group eligibility](https://advertising.amazon.com/API/docs/en-us/mcp/advertiser-product-group-eligibility) exposes advertiser-scoped eligibility checks. Official [Amazon Business exclusive Sponsored Products launch, 2025-05-05](https://advertising.amazon.com/en-gb/resources/whats-new/amazon-business-exclusive-campaign-for-sponsored-product) distinguishes marketplace availability from advertiser eligibility. None defines the internal normalized scope label contract.

Sampled GitHub on 2026-10-25: denisneuf/python-amazon-ad-api (203 stars, MIT, non-fork, recent successful Actions and tests, PRs #297/#296); agentskills/agentskills (26,592 stars, Apache-2.0, non-fork, validator tests, sampled failed older Actions, PRs #613/#609); KuudoAI/amazon_ads_mcp (74 stars, MIT, non-fork, tests and recent successful Actions, PRs #104/#101). Rejected integration because none authenticates live advertiser/campaign eligibility and a small local guard addresses the observed bug. Stars, issue/PR samples, tests, licenses and Actions are metadata, not a full code/security audit. No third-party code, prompts, schemas, workflows or templates copied. [Practitioner discussion on Amazon and Beyond vs Amazon Business (2025-05-12)](https://www.reddit.com/r/FulfillmentByAmazon/comments/1kl1zod/) is a hypothesis source, not normative platform evidence.

## Next genuine gaps

P0 time-scoped advertiser/campaign/marketplace eligibility bound to a verified connector surface and specific account identity; P1 continuous activation history of schedule/event/budget rules; P2 trusted raw Adapter HTTP response authenticity; P3 cross-control causal and marginal-economics confounders.
