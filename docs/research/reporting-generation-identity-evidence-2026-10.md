# Reporting-generation identity evidence — 2026-10-25

## Baseline and verified gap

At main `c39bf9ca190c7c0bdbaf9a3c0f80fdd936afc0e0` (v1.60.0), zero open PR; reviewed older reporting branches were behind main. The existing connector gate treated identical placeholder requested/observed `reporting_generation` strings as a valid match and treated unknown observed identity as a definitive mismatch. A padded observed string could match after trimming. This is distinct from prior Connector Scope and Binding evidence checks.

## RED → GREEN

RED `78e8072f56dc58e206bdcab6bd5e8eebaa887a13`: [Actions 40199527214](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40199527214), 1425 tests, 13 FAIL. GREEN `e354a59688f88a8104bbb77c2793bd2c7379b76c`: [Actions 40199576967](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40199576967), 1425/1425 PASS and both validators PASS. Eighteen deterministic synthetic tests exercise requested placeholders, observed placeholders/padding, valid matches, casefolded matches, real mismatches and no requirement. No live Ads reads or writes.

## Minimal behavior and boundary

The gate uses the existing `_verified_identity` predicate for required and observed reporting-generation identities. Caller placeholder or padded requirements raise `ValueError`; an observed unavailable/padded generation returns `data_contract_effect=unknown` and `Degraded` without high confidence. Real concrete mismatches still block. The rule does not prove data freshness, per-metric availability, source authenticity, account/campaign eligibility or actual advertising lift. Never convert missing/unsupported evidence to metric zero. External authorized Executor owns all live mutations.

## Sources and licensing

Official [Unified Reporting GA (2026-06-08)](https://advertising.amazon.com/resources/whats-new/streamline-campaign-analysis-with-unified-reporting) and [report migration help (updated 2026-10-12)](https://advertising.amazon.com/help/GK3JZZE5QLTF8U8A) establish that report generations and metric compatibility matter; neither supplies these repository-owned labels. GitHub public metadata rechecked for KuudoAI/amazon_ads_mcp (MIT, 74 stars), denisneuf/python-amazon-ad-api (MIT, 203), promptfoo/promptfoo (MIT, 26,406), OpenLineage/OpenLineage (Apache-2.0, 2,721), modelcontextprotocol/servers (NOASSERTION, 91,550); none needed for a local deterministic guard. Stars/CI are sampled and do not constitute complete security/issue/PR/license audit. No third-party code, prompts, schemas, templates or workflows copied. Community PPC anecdotes are hypotheses only.

## Next evidence gap

P0 independently bind Amazon Business marketplace/advertiser/campaign eligibility to account, campaign, time, source and Connector capability; P1 rule activation continuity; P2 Adapter raw HTTP provenance; P3 causal interaction and marginal economics.
