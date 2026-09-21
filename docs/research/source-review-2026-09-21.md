# Source review — 2026-09-21

Point-in-time discovery pass for Amazon Ads decision quality plus agent/MCP/evaluation engineering. Stars are discovery metadata only, never an adoption criterion.

## Adopted evidence

### Amazon Ads Help — Conversion attribution

- Type: first-party official documentation.
- Freshness observed: updated August 5, 2026.
- License/copyright: Amazon proprietary documentation; factual behavior only, no prose copied.
- Adoption: **yes, abstract factual semantics only**.
- Why: directly closes a decision-safety gap. Amazon documents cross-ad-product competition for attribution, so a product-level attributed-conversion decline can reflect credit reallocation rather than an equivalent shopper-demand decline.
- Implementation: independently written guard in `performance-drop-diagnosis` and a deterministic replay fixture; no API implementation or Amazon prose copied.
- URL: https://advertising.amazon.com/help/G3BB9TWP5KC375TJ

### Amazon Ads — View Attribution Updates for Amazon Store ads

- Type: first-party launch announcement, January 1, 2026.
- License/copyright: Amazon proprietary documentation; factual behavior only.
- Adoption this pass: **no new implementation**; already represented in `references/data-lineage.md` as attribution-variant/cutover semantics.
- Why retained: confirms that methodology cutover and cross-product credit competition are distinct attribution risks and should not be collapsed into one field.
- URL: https://advertising.amazon.com/resources/whats-new/view-attribution-updates-for-amazon-store-ads

### Amazon Ads — Unified reporting generally available

- Type: first-party launch announcement, June 8, 2026.
- License/copyright: Amazon proprietary documentation; factual behavior only.
- Adoption this pass: **rejected as duplicate**. Reporting-generation and unified-reporting migration semantics already have dedicated research, lineage contracts, schemas and evals.
- URL: https://advertising.amazon.com/resources/whats-new/streamline-campaign-analysis-with-unified-reporting

## GitHub discovery / rejection log

### KuudoAI/amazon_ads_mcp

- License: MIT (previously reviewed).
- Activity: active public Amazon Ads MCP; current discovery still exposes broad reporting/API-v1 coverage.
- Adoption this pass: **rejected as duplicate**.
- Reason: connector capability taxonomy, async reporting, progressive tool disclosure and API-v1 beta caution are already represented in connector-capability research/contracts. No new decision-quality gap justified more code.
- URL: https://github.com/KuudoAI/amazon_ads_mcp

### deeppavlov/mcp-evals

- Stars observed: 1 at review time; active history with 271 commits surfaced by discovery.
- License: Apache-2.0.
- Engineering evidence: code-first tasks, domains, evaluators, tests/CI-oriented repository structure.
- Adoption this pass: **rejected**.
- Reason: useful evidence that tool-using agents benefit from task/evaluator separation, but this repository already has deterministic eval fixtures, contract validators and Skill-effectiveness measurement. Importing its framework would add dependencies and runtime surface without closing the attribution gap.
- URL: https://github.com/deeppavlov/mcp-evals

### jeffmichaeljohnson-tech/claude-code-toolkit

- License signal surfaced by public discovery: MIT.
- Engineering themes: agent orchestration, on-demand MCP loading, progressive disclosure, session intelligence, quality feedback loops.
- Adoption this pass: **rejected**.
- Reason: progressive loading, runtime-neutral Skills, memory boundaries and evaluation loops already exist here; the toolkit is broad runtime infrastructure rather than Amazon Ads decision semantics. No code/prompt/template copied.
- URL: https://github.com/jeffmichaeljohnson-tech/claude-code-toolkit

### di37/EvalSurfer

- License: not relied on in this pass; no implementation reused.
- Engineering theme: agent-native evaluation with deterministic measurement tools.
- Adoption this pass: **rejected pending stronger need/evidence**.
- Reason: current eval stack already separates deterministic measurement from judgment sufficiently for the identified gap; adding another evaluation protocol would be architecture churn.
- URL: https://github.com/di37/EvalSurfer

### vaibuep/amazon-ads-mcp

- Discovery result substantially mirrored the capability/package description of `KuudoAI/amazon_ads_mcp`.
- Adoption this pass: **rejected as likely duplicate/fork/mirror evidence**; not counted as an independent source.
- URL: https://github.com/vaibuep/amazon-ads-mcp

## Priority decision

The attribution-competition guard was prioritized over runtime/MCP/eval expansion because it changes a real Amazon Ads decision: without it, stable Sponsored Products traffic plus lower attributed purchases could trigger an unsafe bid cut even when credit shifted after activity increased in another eligible ad product. Runtime candidates did not expose a comparably direct, non-duplicate action-safety gap.
