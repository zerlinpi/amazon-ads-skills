# Intervening Sponsored Products event-state value integrity — 2026-10-27

## Evidence-backed gap

Starting main `8ade91c2e71d36f3b2b88d4afd0dbe292ee202f2` had no open PR and passing CI. The new optional `control_events` path accepted `evidence_status=observed` and two different generic before/after states as proof of a transition, even when those values would be rejected as unusable Sponsored Products control states at the endpoints. Synthetic invalid bids, negative video/placement modifiers, incomplete placement surfaces, duplicate/invalid audience boosts and unsupported bidding strategies returned `Confounded` or `Treatment Isolated` instead of `Unknown`.

This is an evidence-identity and value-semantics bug, not proof that Amazon Ads emitted such records. A complete event stream and source authenticity are separate, unresolved requirements.

## RED → GREEN and compatibility

- Initial RED test commit `a3ed449a99b36228cd6c8cb6d708e22bf3248a25`, [Actions #40475574154](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40475574154): 2012 tests, 14 FAIL, with six positive compatibility cases passing.
- Initial minimal fix `5761b7760e851bfaa8ca2f56560a9ea37e0bf2d3`, [Actions #40475654662](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40475654662): 2012/2012 PASS, Skill and Eval validators PASS.
- Additional compatibility RED `112fbc55e5df82efeb2efd5f350bd3762be9c939`, [Actions #40475833006](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40475833006): 2015 tests, 2 FAIL for supported `rule-based` and `RULE_BASED` aliases. Follow-up `a58c737bae6f2dcbe5f6c6dc29f0f4cb8432630f` aligns event aliases with the existing endpoint gate; final PR validation is required before merge.
- Scope is the registered Sponsored Products bid/budget causal surfaces; event-before/after base/video bid values, placement numeric modifiers and required surfaces, audience member identities/boosts, and bidding-strategy enum/ROAS guardrail are checked. The existing rule-member validator remains in place. No new Skill, external dependency or schema field.

## Source review and copyright boundary

Official [Sponsored Products bidding strategies (updated 2026-09-28)](https://advertising.amazon.com/help/GCU2BUWJH2W3A8Z7), [placement adjustments](https://advertising.amazon.com/resources/whats-new/improve-campaign-performance), [budget/bidding rules](https://advertising.amazon.com/library/guides/budget-rules/), and [Marketing Stream v2 FAQ](https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/faq) support treating bid/placement/strategy state as material, while warning that stream delivery cadence and data grain differ. None defines the repository's event payload or independently authenticates it.

Sampled 2026-10-27 GitHub metadata: OpenLineage 2726 stars/Apache-2.0/nonfork/Oct 25 push (Actions success/failure), OpenEvals 1233/MIT/nonfork/Oct 22 (success/action_required), KuudoAI amazon_ads_mcp 74/MIT/nonfork/Oct 14 (success), Agent Skills 26681/Apache-2.0/nonfork/Aug 9, Langfuse 36575/NOASSERTION/nonfork/Oct 27. No full security, dependency, issue or PR audit. Reject imports: Python stdlib and repository-owned guards suffice; NOASSERTION is not blanket reuse permission. No external code, prompts, schemas, workflows, templates or protected prose copied. Reddit PPC stories are hypotheses only, not Amazon platform rules.

## Remaining decision limits

Event arrays remain optional and cannot prove uninterrupted control stability. Event-side budget policy, targeting/routing, control activation, collection completeness and full-window coverage need separate evidence and deterministic tests. Missing/unsupported/partial/unknown must not be converted to zero. Preserve source, metric, date, grain, identity, connector capability, Observation/Hypothesis/Cause/Action/Outcome, causal confounders, marginal economics and control interactions. Default Suggest/Shadow; only an authorized external Executor can perform live writes.
