# Intervening material-control events and endpoint reversion — 2026-10-27

## Verified gap and decision value

Main `e9289762f2e0e74212bdc1c02a5dc5ef22a3565a` had a successful validation run and no open PR. The comparator compared two complete readbacks, but did not inspect positively observed intervening control transitions. Synthetic Sponsored Products bid-test fixtures with unchanged schedule/budget/placement endpoint states and a mid-window change followed by reversion returned `Treatment Isolated`. This is not covered by previous readback identity, effective-time or placeholder guards.

## Contract and RED→GREEN

- New **optional** post-owned `control_events` list, with event identity, exact known-offset RFC3339 time, matching scope/source, registered control type, positive observed evidence and before/after material states. For rule events, require usable member IDs and modifiers. Independent source readback identities cannot be reused.
- Positively observed competing events return `Confounded` even if net endpoint control state is unchanged. Malformed/unknown/partial/derived, mismatched, duplicate, outside-window or no-op records return `Unknown`. Treatment endpoint proof remains mandatory. Omitted/empty event lists retain old endpoint-only classification and cannot prove continuous stability.
- RED tests-only `02d082dcb7f9bce5f4961352443e0e661cf05dfc`, Actions #40469314324: 1990 tests, 17 FAIL. Initial GREEN `a2cb16ff682c5ebf15ab2c0631e1362a55fb8044`, Actions #40469412526: 1990 PASS. Further regression cases cover source-readback collision and absent intended treatment. Final PR validation must pass before merge.
- Tests are synthetic, deterministic and read-only; no Amazon Ads account credentials, mutations or API calls.

## Official evidence, candidate evaluation and limitations

Amazon schedule-based bid rules (2023-11-06) and hours-of-day budget rules (2023-11-30) show that material controls can change during a comparison window. Marketing Stream describes near-real-time campaign messages, but Stream v2 FAQ distinguishes batch delivery frequency from underlying hourly/daily grain and documents restatements. None guarantees that a connector has captured every transition or defines this repository-owned event shape.

Sampled 2026-10-27 GitHub metadata, open PRs and Actions for OpenLineage (Apache-2.0), OpenEvals (MIT), KuudoAI Amazon Ads MCP (MIT), Promptfoo (MIT), Langfuse (NOASSERTION) and Agent Skills (Apache-2.0). Previously reviewed in SOURCES except new Promptfoo/Langfuse comparisons. No full source/security/transitive-license audit; no third-party code, prompt, schema, workflow or template imported. No-license/NOASSERTION sources yield abstract principles only. Public Reddit PPC anecdotes are hypotheses, not platform norms.

## Next genuine gaps

A positively observed event proves a potential confounder, **not** a complete event log. A future independently authenticated, coverage-verified continuous control timeline must handle missing intervals, rule triggers, time zones, stream version/restatement identity and external source authenticity. Source/metric/date/grain/currency/attribution and marginal-profit confounders remain separate. Maintain 15 Skills, Suggest/Shadow and external authorized Executor.
