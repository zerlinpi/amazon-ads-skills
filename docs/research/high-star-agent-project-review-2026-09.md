# High-star agent / MCP / evaluation project review — 2026-09-18

## Purpose

This review supports one repository question:

> Which engineering ideas from widely adopted GitHub projects materially improve the current Amazon Ads Skills decision library without turning it into a framework-specific agent runtime?

GitHub stars are used only as a discovery signal. They are mutable, can be gamed, and do not prove correctness, license compatibility, Amazon Ads relevance, or decision quality.

Observed star counts below are a point-in-time snapshot from GitHub repository metadata on 2026-09-18.

## Reviewed high-star projects

| Project | Stars observed | License signal | Relevant engineering value | Repository decision |
|---|---:|---|---|---|
| `mem0ai/mem0` | ~65.5k | Apache-2.0 | persistent memory, append-oriented memory evolution, entity/time-aware retrieval | No SDK/runtime dependency. Existing append-first optimization ledger already captures the useful boundary; keep future retrieval ideas separate from authoritative event history. |
| `microsoft/autogen` | ~61.0k | GitHub metadata reported CC-BY-4.0 in this review; verify per-path licensing before reuse | multi-agent orchestration and agent runtime abstractions | Rejected as a repository dependency. Orchestration runtime is external to these portable Skills. |
| `crewAIInc/crewAI` | ~58.7k | MIT | explicit orchestration, flows, control-plane separation, observability | No framework dependency. The generic separation between domain decision logic and runtime/execution reinforces the current architecture. |
| `langchain-ai/langgraph` | ~41.9k | MIT | durable state, human-in-the-loop, long-running workflow recovery, memory | No dependency. Durable execution/recovery belongs to an external runner/executor, not the Skill knowledge layer. |
| `vercel-labs/agent-skills` | ~31.3k | no SPDX license surfaced in repository metadata during this review | large real-world Skill collection and ecosystem pressure toward progressive disclosure | No code/content adoption. Used only as ecosystem evidence; licensing must be checked before any future reuse. |
| `agentskills/agentskills` | ~25.5k | Apache-2.0 code; documentation states CC-BY-4.0 | normative Skill format, discovery/activation/resources progressive disclosure | Already aligned. This round further simplifies README and keeps detail in references/resources instead of expanding Skill bodies. |
| `promptfoo/promptfoo` | ~25.2k | MIT | repeatable LLM evals, CI integration, red-team/evaluation separation | No dependency added. Existing deterministic + capability replay + with/without-Skill contracts already cover the repository's immediate need. |
| `letta-ai/letta` | ~24.8k | Apache-2.0 metadata; README says current active source moved to `letta-code` | stateful agents and durable memory | Rejected for direct adoption: active implementation lives elsewhere and full agent-state runtime is outside this repository's scope. |
| `modelcontextprotocol/python-sdk` | ~24.3k | MIT | normative MCP client/server implementation and protocol tooling | No SDK dependency: this repository is not an MCP server. Protocol-facing concepts remain connector-neutral. |
| `confident-ai/deepeval` | ~18.3k | Apache-2.0 | end-to-end/trajectory/step evaluation | No dependency added. Useful as confirmation that trajectory/step evaluation belongs in an external evaluation harness rather than in `SKILL.md`. |
| `modelcontextprotocol/registry` | ~7.3k | repository license is in an MIT → Apache-2.0 transition; docs are CC-BY-4.0 | stable registry identity, namespace ownership/verification, validated catalog entries | Generic registry principle adopted independently: repository-owned canonical connector capability IDs and deterministic resolution. No registry API/schema/code copied. |

## Direct Amazon Ads / seller projects reviewed alongside the high-star scan

Direct Amazon Ads repositories remain much smaller than general agent-framework projects, so stars are not a sensible quality proxy in this niche.

- `KuudoAI/amazon_ads_mcp` — MIT, ~69 stars observed. Still the strongest direct open Amazon Ads MCP engineering reference reviewed here for profile/region binding, report lifecycle and progressive tool exposure.
- `nospicyplease/amazon-ppc-advanced-skills` — MIT, ~15 stars observed. Useful domain-level evidence for guarded preflight/readback and retail context; methods only, no implementation copied.
- `TrackIQ-HQ/amazon-seller-skills` — MIT, very new/low-star in this snapshot. Useful only as emerging adjacent-retail capability taxonomy, not load-bearing engineering evidence.

The repository therefore does not prefer a 60k-star generic agent framework over a 69-star Amazon Ads connector when the latter has more direct evidence for an Amazon-specific connector question.

## Highest-value new gap found

The connector capability runtime gate added previously expects exact `required_capabilities`, but those IDs were not canonicalized.

That creates an interoperability problem:

```text
Skill A asks for current-bid-readback
Skill B asks for bid-state-read
Connector publishes current_bid
→ semantically similar capability
→ incompatible string identity
→ false Unsupported / Unknown or ad hoc model guessing
```

The MCP Registry's registry/identity approach and the Agent Skills catalog/discovery model both reinforce a generic engineering principle:

> stable capability identity belongs in an explicit catalog, not in transient model wording.

This review therefore adds a repository-owned, connector-neutral catalog:

`references/connector-capability-catalog.json`

and a deterministic resolver:

`scripts/resolve_skill_capabilities.py`

The catalog maps the existing 15 Skills to bounded decision profiles such as:

- `live-analysis`;
- `action-safe-proposal`;
- `ready-experiment`;
- `outcome-review`.

Each profile returns registered required and optional read/report/observe/stream capabilities. Unknown Skill/profile names fail closed.

## Why no generic agent framework was imported

This repository's job is Amazon Ads decision logic and evidence safety.

Frameworks such as CrewAI, LangGraph, AutoGen, Letta and Mem0 solve broader runtime concerns:

- process orchestration;
- durable execution;
- human interrupts;
- provider/model routing;
- agent lifecycle;
- generic persistent memory;
- infrastructure-level tracing.

Embedding one of these frameworks would:

1. increase dependencies and runtime assumptions;
2. reduce Codex / Claude Code / WorkBuddy portability;
3. duplicate functionality intentionally kept in the external Connector / Executor / evaluation harness;
4. not improve an Amazon Ads decision by itself.

Therefore those projects are reviewed as architecture evidence, not dependencies.

## README restructuring lesson

The normative Agent Skills guidance recommends progressive disclosure: compact metadata, focused Skill instructions, and on-demand resources.

The old repository README had accumulated detailed rules for attribution variants, SIS, report eligibility, budget pools, action sizing, placement interactions, memory and individual regressions. Those details already have authoritative homes under `references/`, `evals/` and `docs/research/`.

This round rewrites README as a first-use navigation document rather than a duplicate reference manual.

## Copyright / license adoption boundary

No third-party code, prompt, schema, workflow, template, test implementation or long documentation passage is copied in this change.

Adopted content is limited to independently rewritten engineering principles:

- stable registry identity;
- progressive disclosure;
- explicit runtime/decision-layer separation;
- deterministic evaluation before semantic judgment;
- append-first authoritative memory vs derived retrieval state.

Where a repository had unclear/mixed licensing, it was used only as factual ecosystem evidence or excluded from implementation reuse.

## Sources

Repositories reviewed:

- https://github.com/modelcontextprotocol/registry
- https://github.com/modelcontextprotocol/python-sdk
- https://github.com/agentskills/agentskills
- https://github.com/vercel-labs/agent-skills
- https://github.com/microsoft/autogen
- https://github.com/crewAIInc/crewAI
- https://github.com/promptfoo/promptfoo
- https://github.com/confident-ai/deepeval
- https://github.com/langchain-ai/langgraph
- https://github.com/mem0ai/mem0
- https://github.com/letta-ai/letta
- https://github.com/KuudoAI/amazon_ads_mcp
- https://github.com/nospicyplease/amazon-ppc-advanced-skills
- https://github.com/TrackIQ-HQ/amazon-seller-skills

Normative/public documentation used for current behavior:

- Agent Skills specification and progressive disclosure: https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx
- MCP Registry project/documentation: https://github.com/modelcontextprotocol/registry
- Amazon Ads Unified Reporting GA: https://advertising.amazon.com/resources/whats-new/streamline-campaign-analysis-with-unified-reporting


## Incremental review — 2026-09-18

A second pass focused on official/runtime-adjacent repositories that are even closer to the connector-capability boundary:

| Project | Stars observed | License signal | Incremental finding | Decision |
|---|---:|---|---|---|
| `anthropics/skills` | ~176.9k | no SPDX license surfaced in repository metadata during this pass | strong ecosystem evidence that Skills should remain compact, composable, and resource-backed | No code/prose adoption. The normative `agentskills/agentskills` specification remains the implementation reference. |
| `anthropics/claude-code` | ~146.0k | no open-source SPDX license surfaced; prior review treats current repository content as proprietary/all-rights-reserved | runtime discovery/workspace behavior only | No implementation reuse. Existing Claude onboarding remains factual-interface documentation only. |
| `openai/codex` | ~125.0k | Apache-2.0 | durable repository instructions and Skill/runtime integration continue to support a repository-root, progressive-loading workflow | No new runtime dependency or copied implementation. |
| `punkpeye/awesome-mcp-servers` | ~95.2k | MIT | broad ecosystem discovery only; popularity lists are not capability evidence | Rejected as a load-bearing source. A curated list cannot prove that a particular connector tool satisfies an Amazon Ads capability contract. |
| `modelcontextprotocol/servers` | ~90.4k | mixed/no single SPDX signal surfaced at repository metadata level | official MCP examples reinforce that server/tool identity and implementation-specific surfaces vary across integrations | No source copying. Connector-specific tool names remain outside the canonical capability catalog. |
| `mcp-use/mcp-use` | ~10.6k | MIT | useful MCP application/server framework, but solves runtime/app construction rather than Amazon Ads decision semantics | No dependency added. |

The official MCP Registry documentation was also rechecked. It assigns servers stable names, versions, repository/package metadata and namespace-ownership verification. That is not the same as this repository's Amazon Ads capability catalog, but it reinforces the generic engineering principle that **identity should be validated against a registry rather than invented at call time**.

This directly exposed a repository gap after the first capability-registry change: `scripts/evaluate_connector_capability_gate.py` still accepted arbitrary `required_capabilities[]` strings. A misspelled or invented ID therefore looked like a legitimate capability that the connector did not expose.

The corrected contract is:

```text
unregistered required capability ID
→ repository/caller configuration error
→ fail closed

registered capability ID
+ absent from connector snapshot
→ connector evidence Unknown / Blocked
→ never_zero
```

No MCP Registry schema, SDK implementation, server manifest, Anthropic/OpenAI runtime code, or third-party tool definition is copied. The implementation is independently authored against the repository's own capability catalog.


## 2026-09-18 incremental scan

### modelcontextprotocol/modelcontextprotocol — ~9.2k stars; specification repository; license metadata NOASSERTION

Fresh review found an actively maintained upstream specification repository, with the 2026-07-28 protocol release documenting a stateless core, multi-round-trip requests, routing, cacheable list results, authorization hardening, and extensions. This is normative protocol evidence, not a reason to copy an MCP server implementation.

Adoption boundary: retain only connector-neutral principles already compatible with this repository: explicit capability discovery, bounded context exposure, authorization separation, and evidence-bearing connector contracts. No specification prose, schemas, SDK code, examples, or workflows are copied. Repository license metadata is not sufficiently explicit for implementation reuse here, so adoption remains abstract/method-level only.

### borghei/Claude-Skills — ~787 stars; active multi-runtime skill library; license metadata NOASSERTION

Fresh review found substantial recent engineering around progressive disclosure across Claude Code, Codex, and other runtimes. The useful generic signal is that large skill bodies can be split into trigger-time maps plus on-demand references to reduce context cost without broadening execution authority.

Adoption decision: reject direct content reuse and do not copy skills, prompts, templates, scripts, or reference text because repository license metadata is not sufficiently explicit. The repository already uses progressive loading through canonical `skills/` plus shared `references/`, so no behavior change is justified solely by this source.

### tardigrde/agent-skill-eval — 1 star; MIT; recently active evaluation harness

Not high-star, but retained as a lower-weight engineering comparison because it provides concrete multi-runtime evaluation mechanics: isolated workspaces, deterministic assertions before model grading, with/without-skill baselines, negative controls, side-effect classification, and cleanup tracking.

Adoption decision: no dependency and no copied schema/workflow/assertion implementation. The repository already has deterministic eval contracts and paired Skill-effectiveness summaries; the remaining potentially useful idea is external runtime/harness execution against real Codex/Claude Code environments, which stays outside this repository until a concrete decision-quality gap requires it. Star count is recorded only as context, not as evidence quality.


## 2026-09-19 full-repository incremental scan

### open-multi-agent/open-multi-agent — ~6.9k stars; MIT; actively maintained

Fresh review found a substantial evaluation subsystem with versioned scorers, deterministic/offline evaluation, explicit scorer-error states that are excluded from quality averages instead of coerced to zero, privacy-bounded payload persistence, and experimental memory-quality measures such as staleness annotation, omission, pollution, and scope leakage.

Adoption decision: no dependency and no copied TypeScript, schemas, scorer prompts, storage implementation, or workflow. The useful generic lesson is retained for a future repository gap: evaluator/scorer failure is missing evidence rather than a zero-quality observation, and scorer/rubric configuration should be versioned when effectiveness claims depend on it. The current Amazon Ads decision-safety priority remains experiment aggregation semantics, so no eval behavior is changed in this PR.

### NVIDIA/skills — ~3.35k stars; Apache-2.0 code with repository documentation carrying its own stated licensing; very active

Fresh review found an actively maintained cross-runtime skill catalog with explicit evaluation/trust-pipeline documentation, benchmark metadata, scanning, release checks, and runtime projections for multiple agent clients.

Adoption decision: use only the generic governance principle that skill trust should combine structural validation, behavioral evaluation, and release evidence rather than relying on popularity or a README claim. No NVIDIA Skill text, benchmark definitions, trust-pipeline implementation, manifests, prompts, or docs are copied. This repository already has structural validation + deterministic eval fixtures, so no duplicate framework is imported.

### eigent-ai/agent-skills — ~23 stars; Apache-2.0; evaluation-oriented but lower adoption signal

The repository separates structural skill review, rubric/judge material, scenarios, score artifacts, and CI review workflow.

Adoption decision: lower-weight corroboration only. Existing repository separation between canonical Skills and `evals/` already covers the useful architecture. No evaluator code, rubric, judge prompt, scenario schema, or CI workflow is copied.

### jhrendon/amazon-mcp — ~2 stars; active code/tests/CI present; no repository license metadata surfaced

Fresh review found a real monorepo with Amazon Ads + Seller MCP surfaces, async report tools, cross-MCP retail/ads correlation, tests, CI, and explicit read/write tool families.

Adoption decision: because no clear repository license surfaced, only abstract capability evidence is retained. The useful connector-neutral signal is that ad performance and retail/seller evidence may arrive through separate surfaces and that report lifecycle/read/write separation should remain explicit. No code, tool names, auth/retry implementation, schemas, optimization rules, prompts, or workflows are copied. Low stars also make it non-load-bearing evidence.


### benchflow-ai/skillsbench — ~1.8k stars; Apache-2.0; benchmark engineering

Fresh review found a real benchmark repository with tests, CI, versioned dataset registry, pinned git-tag/commit identity and task content digests. High stars are context only; the engineering value is explicit benchmark-version provenance.

Adoption decision: method-level only. We use the generic rule that longitudinal Skill-effectiveness results must not cross fixture/evaluator/rubric versions without an explicit comparability decision. No task packages, oracle/verifier code, registry schema, scripts, prompts or leaderboard implementation are copied.

### TiesPetersen/SkillBenchmark — ~14 stars; MIT; lower-weight

Reviewed for paired with-Skill/without-Skill runs and rubric-based judging. It has a real implementation but lower adoption/engineering depth than SkillsBench and overlaps the repository's existing paired-effectiveness protocol.

Adoption decision: no implementation change sourced from this project; retained only as corroboration. No code, rubric, statistical implementation or config copied.
