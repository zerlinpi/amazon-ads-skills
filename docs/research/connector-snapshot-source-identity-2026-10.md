# Connector snapshot/source identity evidence — 2026-10-25

## Fresh main and verified gap

At main `09698986a0103d74910221a391c05d77827365b8` (v1.57.0), `scripts/evaluate_connector_capability_gate.py` accepted a Supported/Verified read capability with a missing, placeholder, null or whitespace-padded `snapshot.connector_id` and returned high-confidence Pass. Explicitly unusable optional `source_system` or `acquisition_channel` was also ignored. Valid bindings do not prove which connector supplied a snapshot. This is independent of the previously fixed binding identity and access-mode checks.

## RED → GREEN

Tests committed first: `f5dd802ffbe4bda3470454fd88f6fb72f8824b85` (registered-capability fixture correction `6e4e6d301d12b48653d2435c78b744efa2ce70b3`), followed by minimal repair `627bbf53d01586485162a81049ba43a6adafa716`. RED [Actions 40186241773](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40186241773): 1380 tests, 11 FAIL. GREEN [Actions 40186288201](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40186288201): 1380/1380 PASS, 15 Skill and 55 eval fixture validators PASS. Fourteen deterministic cases, eleven previously failing. Synthetic inputs only; no Amazon Ads live reads/writes.

## Decision boundary

A `Supported`/`Verified` read capability must also have a concrete snapshot-level `connector_id`. A missing, blank, placeholder (`Unknown`/`Unsupported`/`Partial`/`Missing`/`Unavailable`/`Not Available`/`Not Supported`) or whitespace-padded connector identity degrades the entire decision, even with multiple valid bindings. Optional `source_system` and `acquisition_channel` may be omitted for legacy snapshots, but when explicitly provided they must be concrete identities, not null/placeholder/whitespace-padded values. This is a repository-owned read-side provenance check, not authentication of remote API responses, proof of account eligibility, or permission to write.

The change uses the existing `_verified_identity` whole-label validator and caps the overall gate to Degraded for invalid snapshot provenance. A valid alternate binding cannot rehabilitate an unidentified snapshot; a valid connector ID containing the substring `unknown` is not rejected. A legitimate explicit source identity passes; legacy omitted optional source fields remain compatible. No API-native enum, cryptographic provenance, advertiser/campaign entitlement, or Executor function is claimed.

## Source and licensing review

Official platform context: [Amazon Ads MCP account selection](https://advertising.amazon.com/API/docs/en-us/mcp/get-started) distinguishes dynamic/fixed account IDs and marketplace/profile selection; [MCP eligibility](https://advertising.amazon.com/API/docs/en-us/mcp/eligibility) describes advertiser program and product eligibility checks; [Amazon Business exclusive Sponsored Products announcement, 2025-05-05](https://advertising.amazon.com/en-gb/resources/whats-new/amazon-business-exclusive-campaign-for-sponsored-product) distinguishes supported marketplaces from actual advertiser enrollment. None specifies this repository-owned snapshot identity validator.

Sampled public GitHub metadata 2026-10-25: [KuudoAI/amazon_ads_mcp](https://github.com/KuudoAI/amazon_ads_mcp), 74 stars, MIT, non-fork, pushed 2026-10-14, tests and successful sampled Actions, open PRs #104/#101; [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo), 26,401 stars, MIT, non-fork, active 2026-10-25, test tree and successful sampled Actions, open PRs #11978/#11977; [OpenLineage/OpenLineage](https://github.com/OpenLineage/OpenLineage), 2,721 stars, Apache-2.0, non-fork, active 2026-10-25, sampled Actions success, open PRs #5105/#5104; [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers), 91,547 stars, repository license metadata NOASSERTION, non-fork, active 2026-10-25, sampled Actions success, open PRs #4817/#4803. All rejected for code integration: deterministic internal provenance guard suffices, and these sources do not authenticate this connector's live response. Stars, sampled CI, issue/PR status, and license metadata are not full code/security audits. No third-party code, prompts, schema, workflows or templates copied. The no-assertion license source supplies abstract risk ideas only.

## Next evidence gaps

P0 independent time-scoped marketplace/advertiser/campaign eligibility and connector capability proof; P1 continuous rule activation history; P2 externally trusted raw Adapter HTTP provenance; P3 cross-control causality and marginal economic confounders.
