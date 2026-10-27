# Intervening Sponsored Products budget and routing event-state integrity — 2026-10-27

## Gap and evidence boundary

Starting main `ff7b82ed6cf0edcbc9dc371c9bd1a0c718a7cd24` (v1.103.0, push Actions #40476161466 SUCCESS) had no open PR. Four sampled historical branches were zero commits ahead. The comparator validated event identity/time/source and bid/video/placement/audience/strategy semantics, but still accepted malformed budget amounts/policy and invalid site/retailer routing as observed mid-window changes. Synthetic examples returned `Confounded` or `Treatment Isolated` rather than `Unknown`.

The fix is a **read-side normalized event-value consistency check**, not an Amazon-native event payload, authenticated event capture, actual rule-trigger history, or permission to write Amazon Ads.

## Deterministic RED → GREEN

- Tests-only RED `4076b1fe06d202437ec13483c5d1f3a1e2e0fc50`, [Actions #40482958315](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40482958315): 2029 tests, 10 FAIL; four new compatibility cases PASS.
- First minimal GREEN `0ef6014bd1c80ed55dc0d67c4b8063a705b2d7ee`, [Actions #40483041208](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40483041208): 2029 PASS, Skills/Evals PASS.
- Additional type-safety RED `96674486cf6dbcf84f5cbff990929eb8b4bd0e94`, [Actions #40483075939](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40483075939): 2031 tests, 2 ERROR on non-hashable routing labels.
- Type-safety GREEN `ca024abd07ebe448b87d032be8ae77441da021da`, [Actions #40483095636](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40483095636): 2031 PASS, Skills/Evals PASS.

Sixteen deterministic synthetic tests. Budget-change event sides require base/effective daily budgets, active rules and policy; bid-change event sides preserve optional partial budget shape while rejecting invalid explicit values. Routing events require known site restriction, optional mapped retailer scope and no across-retailer/Business-exclusive contradiction. One-sided retailer scope fails closed. No schema field, dependency or Skill added.

## Sources, licensing and non-adoption

Amazon official [budget rules](https://advertising.amazon.com/library/guides/sponsored-products-budget-best-practices), [daily budget policy](https://advertising.amazon.com/resources/whats-new/sponsored-ads-daily-budgeting-policy-and-options), [Amazon Business exclusive campaign launch](https://advertising.amazon.com/en-gb/resources/whats-new/amazon-business-exclusive-campaign-for-sponsored-product), [across-retailers Sponsored Products](https://advertising.amazon.com/solutions/products/sponsored-products-across-retailers) and [Marketing Stream v2 FAQ](https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/faq) support preserving budget/routing and source-time evidence. They do not define this repository's event schema or prove full-window completeness.

Sampled 2026-10-27 GitHub metadata: OpenLineage 2726 stars/Apache-2.0, OpenEvals 1233/MIT, KuudoAI amazon_ads_mcp 74/MIT, Promptfoo 26486/MIT, MetricFlow 1849/Apache-2.0, Agent Skills 26684/Apache-2.0, MCP Servers 91597/NOASSERTION, Langfuse 36579/NOASSERTION. All nonfork in sampled metadata; recent pushes and selected Actions/open PRs inspected. This is not an exhaustive code, CI, issue, security, dependency-license or fork/mirror audit. Reject external imports: standard-library deterministic guards suffice; none authenticates continuous Amazon Ads control events. No third-party code, prompts, schemas, workflows or templates copied. NOASSERTION and restrictive sources are principles-only. October 2026 Reddit PPC campaign-structure anecdotes are unverified hypotheses, not Amazon rules.

## Remaining risks

Omitted/empty `control_events` cannot establish full-window stability. Event-side rule activation, collection completeness, event restatement, authenticated capture gaps, platform-specific capability/eligibility and cross-control site/placement consistency remain separate work. Preserve source/metric/date/grain/identity/connector capability, attribution, retail confounders, causal boundaries and marginal economics. Unknown/partial/unsupported are never zero. All live Ads writes/retries/idempotency/reconciliation remain with an authorized external Executor.
