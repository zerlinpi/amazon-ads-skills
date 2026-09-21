# MCP Skills content identity and custom-host integrity — 2026-09-21

## Scope

This pass re-read the current `main` decision/runtime architecture and then re-scanned Agent Skills, MCP, evaluation, multi-agent and Amazon Advertising API repositories. The goal was not to add another Skill or another agent framework. The question was whether a newly stable upstream contract exposes a concrete portability or safety gap in the repository's existing progressive-loading path.

## Fresh gap found

The repository already had a metadata-only catalog and selected exactly one Skill body through `scripts/resolve_skill_context.py`. That prevented an advertising platform from preloading all 15 Skill bodies.

The missing boundary was **content identity**:

```text
repository path
→ selected Skill / deferred resource
→ no digest or byte-size identity
→ host cache or materialization can only trust the path
→ changed bytes can be mistaken for the previously reviewed content
```

This is distinct from Amazon Ads data lineage. It is runtime/package lineage for the decision instructions themselves.

## Normative source: MCP Skills extension

Repository reviewed: `modelcontextprotocol/ext-skills`

Point-in-time GitHub metadata observed on 2026-09-21:

- about 658 stars and 60 forks;
- non-fork, non-archived;
- active commits through 2026-09-18;
- Apache-2.0 code license; project documentation is stated as CC-BY-4.0;
- maintained by the MCP Skills Over MCP Working Group.

The stable Skills extension is identified as `io.modelcontextprotocol/skills` and is specified against MCP base protocol revision 2026-07-28 or later. The stable extension defines `skills/list`, `skills/get`, optional directory reading, and a Skill entry whose resource manifest carries content digests and byte sizes. SEP-2640 was finalized in September 2026.

Adoption boundary:

- adopted the **generic integrity method**: selected Skill resources need stable content identity, not only paths;
- independently implemented SHA-256 + byte-size identity in the repository-owned custom-host resolver;
- did **not** copy the MCP schema, TypeScript interfaces, examples, URI layout, server implementation, approval model, or documentation prose;
- did **not** turn this repository into an MCP server;
- did **not** claim that the custom `resource_manifest` is the wire-format `skills/get` response.

Official source:

- https://github.com/modelcontextprotocol/ext-skills
- https://github.com/modelcontextprotocol/ext-skills/blob/main/specification/stable/skills.mdx

## Resulting repository contract

For one activated Skill, `scripts/resolve_skill_context.py` now returns:

- the same metadata-only discovery catalog;
- one `preload_files` entrypoint;
- the same deferred `resource_candidates`;
- `resource_manifest[]` entries with repository-local path, role, SHA-256 digest, and raw byte size;
- a `manifest_policy` that states the selected Skill directory is completely enumerated, shared candidates are hashed, the shared-candidate scope is direct references from the selected `SKILL.md`, and file contents are not included.

The manifest covers the complete selected Skill directory so same-path content changes are detectable. It also hashes directly referenced shared repository resources because this project intentionally keeps some canonical references under root `references/`, `schemas/`, `scripts/` and `playbooks/`.

This remains progressive disclosure: hashes and sizes do not preload resource bodies into model context.

## RED → GREEN evidence

RED commit:

- `d309ecd91ed05b7c16de477a135585e689dfec5e`
- deterministic regression required the new manifest and independently recomputed SHA-256/size values;
- GitHub Actions run `35556158322` failed in the new test with `KeyError: 'resource_manifest'`;
- 308 tests ran and the new regression was the only error.

GREEN commit:

- `79321d0519372eb63b4e176f561a6db3852084e5`
- minimal implementation added repository-local content identity without loading bodies or granting write authority;
- GitHub Actions run `35556231251` completed successfully.

## High-star / active project review

Stars are discovery metadata only and were not used as an adoption score. Previously reviewed projects such as `anthropics/skills`, `google/skills`, `agentskills/agentskills`, `vercel-labs/agent-skills`, `openai/codex`, `openai/openai-agents-python`, `mcp-use/mcp-use`, `langchain-ai/langgraph`, `crewAIInc/crewAI`, `promptfoo/promptfoo`, `confident-ai/deepeval`, `mem0ai/mem0`, MCP SDK/Registry projects and NVIDIA Skill/evaluation projects were de-duplicated rather than counted again.

### mattpocock/skills

Point-in-time metadata: about 266.5k stars, MIT, non-fork, active push through 2026-09-18. The repository has agent/runtime directories, Skills, scripts, documentation and a release workflow.

Decision: rejected for direct adoption in this change. It is a broad engineering Skill collection and does not provide stronger evidence for Amazon Ads decision semantics or the newly normative MCP content-integrity boundary. No Skill text, prompts, scripts, templates or workflow implementation copied.

### obra/superpowers

Point-in-time metadata: about 289.3k stars, MIT, non-fork, active push through 2026-09-20. It contains multi-runtime plugin projections, Skills, hooks, scripts and tests.

Decision: useful corroboration for test-first behavior and multi-runtime portability, but both are already repository invariants. Importing its runtime/plugin model would duplicate the external-runtime layer and would not improve an Amazon Ads decision. No code, prompts, Skill text or workflows copied.

### addyosmani/agent-skills

Point-in-time metadata: about 97.8k stars, MIT, non-fork, active push through 2026-09-20. The repository exposes multiple runtime projections, Skills, references, evals/scripts and a GitHub Actions plugin-install test.

Decision: rejected for direct adoption. Its production engineering and testing practices corroborate progressive disclosure and deterministic validation already present here, but it does not supersede the normative Agent Skills or MCP Skills specifications. No Skill content, TDD prompt, hook, eval, installer or workflow copied.

### denisneuf/python-amazon-ad-api

Point-in-time metadata: about 202 stars, MIT, non-fork, active push through 2026-09-17, with an implementation package, tests and multiple GitHub Actions workflows.

Decision: relevant direct Amazon Advertising API engineering evidence, but its value is transport/API-client implementation. This repository intentionally leaves authentication, request execution, retries and live mutation to an external Connector/Executor. No SDK code, endpoint wrapper, model, auth flow or test implementation copied.

### amzn/amazon-advertising-api-php-sdk

Point-in-time metadata: about 92 stars, Apache-2.0, archived, last push observed in 2020, with tests but no current workflow directory found.

Decision: rejected as stale implementation evidence. The Amazon namespace and permissive license do not make an archived SDK a better source than current Amazon Ads documentation or an active connector for present-day capability semantics. No code copied.

### StacklokLabs/skills-mcp

Point-in-time metadata: about 2 stars, recent push on 2026-09-21, no repository license surfaced in metadata during this review.

Decision: lower-weight corroboration only. It is directly related to serving Skills over MCP, but the official final MCP Skills extension is stronger normative evidence. With no clear license, no code, schema, prompt or workflow is reused.

## Why this gap outranked new PPC rules

Current Amazon Ads scans continued to surface active reporting, search-term and budget documentation, but the repository already has explicit contracts for search-term origin, report row eligibility, budget-rule/control state, reporting-generation lineage, historical availability, freshness/backfill and connector capability.

The newly final MCP Skills extension changed the evidence status of content identity: it is no longer only an experimental cache idea. The repository's custom-host resolver had a directly observable missing field and could be fixed with one deterministic regression and a small read-only implementation.

No 16th Skill was added. No live Amazon Ads write path was added.

## Remaining boundary

The custom resolver is still a repository-local helper, not an MCP Skills server. A future hosted distribution layer must decide how canonical shared files outside an individual `skills/<name>/` directory are materialized or mapped without duplicating business logic. That should be solved only if a real MCP-serving deployment requires it, with its own RED fixture and integrity/identity contract.
