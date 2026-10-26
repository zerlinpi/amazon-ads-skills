# Ready experiment identity and control-arm collision guard

Reviewed: 2026-10-26. Decision surface: `scripts/validate_experiment_plan.py` Ready-only semantic gate. Status: adopted, MINOR v1.76.0.

## Gap and priority

P0 internal: the validator accepted syntactically nonempty but semantically unavailable scope identities, duplicate treatment units, and explicitly overlapping or placeholder control-arm identities while reporting `Ready`. This could promote an unresolved or contaminated experiment into external execution review. The JSON Schema intentionally allows exploratory incomplete plans, so a Ready-only semantic gate is the narrowest safe change.

P1 external: independently verified holdout allocation, complete rule-activation intervals, source-authenticated feature eligibility and cross-campaign interference remain unproven. P2: marginal economics and attribution maturity require live, account-specific evidence. Do not invent missing metrics or convert unknown to zero.

## Deterministic reproduction and repair

- RED: `a6152af0b3f7dc26968e0b0eee1fe102f95e72f4`, [Actions #40271192479](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40271192479), 1603 tests / 10 FAIL; 3 compatibility cases passed. The 10 failures demonstrate the old Ready gate's acceptance of placeholder/padded/duplicate/colliding identities.
- Minimal production fix: `854e0ddbace1ac2d467b603b7e8449dd3d5b27bb`. Corrected the whitespace normalization character class in `be860dd7958742a76a4ca42ff78555d2b42a1cbe` after an intermediate failed CI run.
- GREEN: [Actions #40271281809](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40271281809), 1603/1603 PASS, 15 Skills and 55 eval fixtures PASS.
- Ready identity uses case-sensitive opaque IDs, whole-label placeholder rejection (not substring rejection), no padding, unique treatment IDs, and optional control IDs that must be concrete, unique and disjoint. Exploratory `Shadow Only`/`Hold`/`Redesign` are not tightened. No Amazon Ads API call, write, retry, idempotency or Executor logic.

## Source and copyright decision

Amazon Ads [MCP account context](https://advertising.amazon.com/API/docs/en-us/mcp/get-started) and [Brand Lift](https://advertising.amazon.com/resources/whats-new/measure-brand-marketing-impact-using-amazon-brand-lift) establish that authorization/account and measurement context are distinct; neither specifies our normalized ID strings or proves experiment randomization. Public GitHub projects and current metadata are recorded in `docs/SOURCES.md`; none supplies authenticated evidence for this internal semantic gap, so no code, dependency, prompt, schema, template or workflow is imported. No-license/NOASSERTION sources are ideas-only. [2026-10-20 operator PPC anecdote](https://www.reddit.com/r/AmazonFBA/comments/1xan7qv/) is a hypothesis source only.

## Next falsifiable gap

An explicit `verified: true` holdout isolation assertion can still be a self-reported claim without independent raw source authentication or longitudinal control integrity. This requires a real authorized adapter/trust root rather than another invented local status field. Investigate only if a non-duplicative deterministic evidence contract can be demonstrated; otherwise leave unchanged.
