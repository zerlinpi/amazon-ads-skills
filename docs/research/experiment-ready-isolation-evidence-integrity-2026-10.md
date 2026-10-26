# Ready holdout isolation evidence integrity (v1.79.0)

Reviewed 2026-10-26. **Adopted:** narrow, deterministic repository-owned Ready gate; MINOR. No Amazon Ads account reads/writes, no new Skill, schema or dependency.

## Confirmed independent gap

Starting main `e1c27402c660268f0b81c4f33c2506ba9160025f` (v1.78.0; Actions #40281766923 success; no open PR), the semantic validator accepted a Ready holdout with `comparison.isolation_evidence[0].verified=true` and the entire `evidence` value `Unknown`, `Not Supported`, or a padded placeholder. When supplied, `source=Unavailable` or whitespace-padded source, and `verified_at=null`, invalid or timezone-naive, were also accepted. This was not covered by the previous Ready identity and boundary-monitoring chronology fixes. Historical experiment branches sampled were behind main with zero ahead.

A verified boolean is a claim, not a substitute for concrete supporting evidence. The fix rejects whole-label unavailable/placeholder or padded evidence; optional source and verification timestamp, **if supplied**, must be concrete and timezone-aware. Omission of these optional fields remains legacy-compatible. Valid narrative evidence containing a word such as "unknown" is not a placeholder. Shadow/Hold/Redesign retain unresolved evidence for analysis. No fixed TTL or invented remote attestation is introduced.

## Deterministic RED → GREEN

- RED test commit `4ae7cd51a0807bb2d42684a5e1a1e1a4acf2cc89`, [Actions #40294180163](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40294180163): **1639 tests, 8 FAIL**. Four compatibility tests passed.
- Minimal production fix `a28cc1c9e50f771b9defb6c35ebdd6f8fe3ab03f`, [Actions #40294279133](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40294279133): **1639/1639 PASS**, 15 Skills and 55 eval fixtures pass.
- Test file: `tests/test_experiment_ready_isolation_evidence_integrity.py`, 12 synthetic deterministic cases. No external Ads API calls.

## Source and copyright boundary

Official [Amazon Ads API eligibility tools](https://advertising.amazon.com/API/docs/en-us/mcp/eligibility) distinguish advertiser program/product eligibility, not repository holdout allocation. [Amazon Attribution API onboarding](https://advertising.amazon.com/API/docs/en-us/amazon-attribution/get-started) requires authorized advertiser access; it does not authenticate these local evidence strings. [Amazon event bid rules (2025-01-02)](https://advertising.amazon.com/resources/whats-new/event-based-bid-rules-for-sponsored-products-advertisers) and [budget rules (2021-08-12)](https://advertising.amazon.com/resources/whats-new/dynamic-budget-control) demonstrate potential time-varying competing controls. None defines the `isolation_evidence` schema, a universal verification TTL or proof of Sponsored Products holdout isolation.

Re-reviewed previously catalogued projects on 2026-10-26: [KuudoAI/amazon_ads_mcp](https://github.com/KuudoAI/amazon_ads_mcp) (74 stars, MIT, non-fork, pushed 2026-10-14, two sampled successful CI runs, PR #104/#101), [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) (26,446 stars, MIT, non-fork, pushed 2026-10-26, two sampled successful CI runs, PR #11992/#11991), [OpenLineage/OpenLineage](https://github.com/OpenLineage/OpenLineage) (2,722 stars, Apache-2.0, non-fork, pushed 2026-10-25, sampled action_required runs, PR #5107/#5105), [agentskills/agentskills](https://github.com/agentskills/agentskills) (26,638 stars, Apache-2.0, non-fork, pushed 2026-08-09), [evidentlyai/evidently](https://github.com/evidentlyai/evidently) (8,011 stars, Apache-2.0, non-fork, pushed 2026-09-29). Stars and sampled CI/PR metadata do not constitute a full code, security, dependency-license or issue audit. All rejected as dependencies: the confirmed local invariant needs no external framework and none independently authenticates Amazon Ads holdout allocation. No third-party code, prompts, schemas, templates or workflows copied. Unlicensed or restricted content remains abstract-principles-only.

[Public Amazon DSP audience holdout discussion (2025-08-29)](https://www.reddit.com/r/datascience/comments/1n3jnpw) describes overlap concerns; [PPC placement discussion (2026-09-20)](https://www.reddit.com/r/PPC/comments/1wldrkt/amazon_ppc_too_much_impression_on_product_pages/) raises placement-distribution questions. Both are uncontrolled community reports, **not** Amazon policy or causal evidence.

## Residual gaps

P0: External independent verification of actual holdout assignment/delivery and source authenticity requires an authorized provider, not another self-declared field. P1: Full-window Schedule/Event/Budget rule execution and trigger history. P2: Auction/budget/ASIN overlap and marginal contribution-profit inference. Maintain source/metric/date/grain/identity/connector capability, Observation/Hypothesis/Cause/Action/Outcome, never-zero missing values, and Read-only/Suggest/Shadow with authorized external Executor for all writes, retries and reconciliation.
