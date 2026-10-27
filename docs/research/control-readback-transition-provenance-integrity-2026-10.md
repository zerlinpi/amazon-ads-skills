# Reused readback transition provenance integrity — 2026-10-27

## Evidence and priority

Starting main `7c8297e8e11c0d603b40fd836f7a5aa8e3d9fea7` v1.99.0; main Actions #40451757569 SUCCESS, zero open PR, five sampled historical branches zero ahead. Repository inventory and targeted content review covered README, AGENTS, CLAUDE, 15 Skills, references, schemas, scripts, tests, evals, playbooks, SOURCES/research and three runtime manifests.

**P0 confirmed:** same concrete `source.readback_id`, same control state, effective time and evidence status, but contradictory optional `transition_provenance` could return `Comparable`. This is a separate actor/transition evidence consistency flaw from v1.96–v1.98 readback guards.

## RED → GREEN

- Tests-only `bc3c7949fa53b463de96c6d6de1153193d8861a9`; [RED #40457523558](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40457523558): 1953 tests, 9 FAIL. Six new compatibility tests passed.
- Minimal fix `185a77312dee0a6e686ee2e5ea840b768bda8378`; [GREEN #40457609259](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40457609259): 1953 PASS, Skill 15 PASS, Eval 55 PASS.
- For same readback ID, compare supplied actor, management mode, actor-evidence status, reason, and exact UTC transition instant; one-sided provenance is Unknown. Distinct IDs, omitted/null legacy fields, offset-equivalent instants are compatible. No new Skill, schema, dependency, or Ads mutation.

## Sources, licensing and rejection

- [Amazon Marketing Stream](https://advertising.amazon.com/library/guides/amazon-marketing-stream), [SP bidding strategies updated 2026-09-28](https://advertising.amazon.com/help/GCU2BUWJH2W3A8Z7), [Full-Funnel Campaigns 2026-09-29](https://advertising.amazon.com/resources/whats-new/full-funnel-campaigns-from-discovery-to-sales) and [RFC3339](https://datatracker.ietf.org/doc/html/rfc3339) support attention to time-varying controls, not the repository's `readback_id` or authenticated transition authorship. [Reddit July 2026](https://www.reddit.com/r/FulfillmentByAmazon/comments/1v8abo9/127_acos_on_amazons_automated_bidding_rules_this/) is a hypothesis only.
- OpenLineage (2726 stars/Apache-2.0), MetricFlow (1848/Apache-2.0), OpenEvals (1232/MIT), KuudoAI amazon_ads_mcp (74/MIT), Agent Skills (26675/Apache-2.0), Google Ads MCP (1078/Apache-2.0) are nonfork and recently sampled on 2026-10-27. CI and open PRs sampled for several; previous SOURCES entries already cover them. **Reject code integration**: Python standard library suffices and none authenticates raw Ads actors. Full source/security/issues/dependency-license/mirror audit not claimed. No third-party code, prompt, schema, workflow or template copied; unlicensed/restrictive material is principles-only.

## Remaining gaps

Full-window Schedule/Event/Budget Rules execution, missing observation intervals, connector/raw-response authenticity, attribution/grain/currency and marginal-profit causal interactions remain unproven. No missing/partial/unsupported/unknown to zero. Default Read-only/Suggest/Shadow; live Ads writes and retries/idempotency/reconciliation require an external authorized Executor.
