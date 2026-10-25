# Feature eligibility source-reference independence — 2026-10-26

## Evidence-backed, non-duplicate gap

At main `96d326e4ae06a96a20347ee2ec6cc21a219fb055` (v1.69.0), the optional feature-specific eligibility gate validated exact feature/marketplace/advertiser/campaign identities, time, and a non-placeholder `source_reference`, but did not reject **the same reference as its required connector capability binding**. A single normalized connector probe could therefore be echoed as a separate self-described Verified Eligible entitlement, yielding high-confidence Pass. A self-referential Ineligible claim could be treated as verified exclusion. Neither establishes independently sourced feature eligibility.

This change checks only exact opaque reference collisions against Verified bindings of **required** capabilities: `binding_id`, `surface_id`, and `evidence[].reference`. Collision makes `feature_source_independence_effect=unknown` and `feature_eligibility_effect=unknown`; the overall decision degrades unless another independent requirement blocks. Unrelated capability references are not compared. Distinct references remain compatible, but distinct labels alone cannot authenticate original API responses, prove enrollment, or establish real advertising outcomes.

## Deterministic RED→GREEN

- RED `ef887fedffc413f5baa9498e9ae259e1cf5a929f`: [Actions #40241663063](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40241663063), 1551 tests, 4 FAIL. Old state incorrectly accepted matching binding reference, surface ID, binding ID, and self-referential Ineligible.
- Initial GREEN `47dc61a042084f7b808ed7589ed78f88b912dd8d`: [Actions #40241697745](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40241697745), 1551 PASS, 15 Skills and 55 eval fixtures PASS. A follow-up removes contradictory Ineligible warning text when its provenance is unproven.
- No new Skill, new external dependency, Amazon Ads account write, executor retry, idempotency or reconciliation.

## Platform and reuse boundaries

Amazon Ads [MCP account context](https://advertising.amazon.com/API/docs/en-us/mcp/get-started) requires authorized account selection; [product-group eligibility](https://advertising.amazon.com/API/docs/en-us/mcp/advertiser-product-group-eligibility) is not the same as named feature enrollment; [Amazon Business exclusive SP](https://advertising.amazon.com/en-gb/resources/whats-new/amazon-business-exclusive-campaign-for-sponsored-product) is only available to eligible advertisers. These are platform distinctions, **not** vendor definitions of this repository-owned collision check.

Metadata, test and sampled CI review of KuudoAI/amazon_ads_mcp, denisneuf/python-amazon-ad-api, promptfoo/promptfoo, OpenLineage/OpenLineage, agentskills/agentskills, modelcontextprotocol/servers, and the adapted vaibuep/amazon-ads-mcp fork found no demonstrated reason to add a dependency for this narrow guard. License and activity observations are in `docs/SOURCES.md`. No external code, prompts, schemas, templates or workflows copied. Unlicensed/NOASSERTION sources confer no reuse permission. Reddit PPC reports are only hypotheses, never entitlement or causal proof.

## Next falsifiable gaps

1. Authenticated raw source evidence and externally authorized reconciliation of feature eligibility, with a trust root and concrete account/feature scope; no self-declared Verified flag can substitute.
2. Complete rule-activation interval coverage across bid, event and budget rules; endpoint snapshots alone cannot prove uninterrupted activation.
3. Causal confounders and marginal-profit decision boundaries under simultaneous control changes.
