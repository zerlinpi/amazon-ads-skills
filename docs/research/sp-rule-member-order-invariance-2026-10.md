# Sponsored Products rule-member order invariance — 2026-10-26

## Fresh read and reproducible gap

Base main `1c880a61ffe98ea7d3b6ae127c453a66f38c42a3` (v1.74.0), successful main Actions #40261236294, no open PR at start. Relevant historical rule/control branches had no commits ahead of main. In the registered SP bid/budget causal comparator, source enumeration of the same unique `rule_id` members in a different order could be misclassified as a competing schedule/event/budget rule change. This is a false `Confounded` classification for a base-bid treatment, not evidence that any rule ran continuously.

## Deterministic RED → GREEN

- Branch `fix/sp-rule-member-order-invariance-20261026`, PR #188.
- RED test commit `f51b605bbe0aaef47f9819a57aaf98ca2e9c2895`, [Actions #40266042350](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40266042350): 1590 tests, 3 FAIL (schedule/event/active-budget rule reorder during base-bid change); 7 controls passed. Reordering active budget rules during a budget treatment already remained isolated because that list belongs to the intended budget control.
- Minimal production fix `63c7976d5ea23e1e72e9b7c9368786d1b44c6b2a`, [Actions #40266103247](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40266103247): 1590/1590 PASS, 15 Skill directories and 55 eval fixtures validators PASS.
- The change sorts only the three validated SP rule member collections by concrete, unique `rule_id` for equality comparison. It does not change input snapshots, collection completeness, member evidence, any other list order, rule activation status, timestamps, or the registry. Genuine modifier/activation/member changes remain confounded; malformed/duplicate/one-sided evidence remains Unknown. No new Skill, dependency, Amazon Ads write, retry, idempotency or Executor behavior.

## Official and community sources; copyright

- Amazon Ads [schedule-based bid rules](https://advertising.amazon.com/en-us/resources/whats-new/schedule-based-bid-rules-available-for-sponsored-products/) (2023-11-06), [event-based bid rules](https://advertising.amazon.com/resources/whats-new/event-based-bid-rules-for-sponsored-products-advertisers) (2025-01-02), and [budget rules](https://advertising.amazon.com/resources/whats-new/dynamic-budget-control) (2021-08-12) establish time/event-dependent campaign controls. They do not specify this repository-owned normalized collection ordering contract or prove full-window execution.
- GitHub metadata sampled 2026-10-26: KuudoAI/amazon_ads_mcp (74 stars, MIT, non-fork, pushed 2026-10-14, recent Actions success, PR #104); promptfoo/promptfoo (26,427, MIT, non-fork, pushed 2026-10-26, recent Actions success, PR #11987); OpenLineage/OpenLineage (2,722, Apache-2.0, non-fork, pushed 2026-10-25, recent Actions success, PR #5105); agentskills/agentskills (26,627, Apache-2.0, non-fork, pushed 2026-08-09, older sampled Actions failure, PR #613). These already appear in SOURCES/research. Public stars, sampled CI and PR metadata do not establish security, correctness, entitlement or full license-dependency review. No third-party code, prompt, schema, workflow or template copied.
- [Amazon seller discussion on budget scheduling](https://www.reddit.com/r/Amazonsellercentral/comments/1v96nqw/looking_to_allocate_budget_on_hourly_basis_in/) (July–October 2026) is an operator hypothesis source only, not Amazon policy or proof of rule continuity.

## Remaining gaps

P0: actual feature eligibility and raw response authenticity require an external authorized, independently verifiable source.
P1: two rule snapshots and normalized identity/order do not prove continuous execution or complete trigger/transition history.
P2: cross-campaign interference, retail shocks and marginal economics require additional causal/experiment evidence.
