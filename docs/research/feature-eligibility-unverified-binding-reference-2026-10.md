# Feature eligibility source-reference collision with unverified connector probes — 2026-10-26

## Highest-value verified gap

The v1.70.0 source-independence guard compared a feature eligibility `source_reference` only with **Verified** bindings of required connector capabilities. A capability may have a legitimate Verified binding for read-side access **and** an Unverified probe. Reusing that probe's ID, surface ID or evidence reference as allegedly independent feature-specific entitlement evidence was accepted. The same collision could turn a synthetic Ineligible assertion into Blocked without independent proof. The fix compares reference identities across every binding on required capabilities, regardless of verification status. It does not change which bindings qualify for capability access.

## RED → GREEN

- Branch: `fix/feature-eligibility-unverified-binding-reference-20261026`; PR #185.
- RED `438bfd3395c68bafc232b581aa206375443aa719`, [Actions #40250988299](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40250988299): 1564 tests, four failures, two control tests passing.
- GREEN `96ecd664f08a69bcfd238fc3e22ad4c0e6b40840`, [Actions #40251036262](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40251036262): 1564/1564 tests PASS, 15 Skill validators and 55 eval fixtures PASS.
- Minimal change: remove the Verified-only filter in the source-reference collision guard. No changes to feature eligibility status validation, connector binding verification, schema, Skill count, execution modes or Amazon Ads write/retry/idempotency.

## Source and copyright boundary

Amazon Ads official announcements for [schedule-based bid rules](https://advertising.amazon.com/resources/whats-new/schedule-based-bid-rules-available-for-sponsored-products), [event-based bid rules](https://advertising.amazon.com/resources/whats-new/event-based-bid-rules-for-sponsored-products-advertisers) and [budget rules](https://advertising.amazon.com/resources/whats-new/dynamic-budget-control) establish control interactions, not this internal reference rule. GitHub candidates KuudoAI/amazon_ads_mcp (MIT), promptfoo/promptfoo (MIT), OpenLineage/OpenLineage (Apache-2.0), agentskills/agentskills (Apache-2.0) and coaxon/amazon-mcp (MIT) were sampled for stars, fork status, push activity and public CI. None adds an independently authenticated Amazon eligibility source for this narrow fix. No third-party code, prompt, schema, workflow or template copied; license metadata does not cover full transitive audit.

## Remaining boundaries

A distinct `source_reference` still does **not** authenticate raw HTTP, prove Amazon advertiser/campaign entitlement or establish continuous schedule/event/budget rule activation. The next high-value work needs externally authorized evidence and complete source-supported rule event history; avoid simulated cryptographic assurances or default-zero substitutions.
