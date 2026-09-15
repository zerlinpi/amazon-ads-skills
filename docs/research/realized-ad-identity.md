# Platform-managed realized ad identity

## Why this matters

Amazon Ads increasingly supports campaign formats where the advertiser's configured controls do not fully determine the shopper-visible ad realization. A campaign can keep the same targeting/bid/budget state while Amazon changes the delivery surface, dynamically chooses a product grouping, varies the realized ad experience, or uses advertiser-provided signals as model inputs rather than hard delivery boundaries.

The repository therefore separates:

```text
configured controls
!= realized ad identity
```

The shared decision policy lives in `references/realized-ad-identity.md`.

## Current Amazon Ads evidence

### Sponsored Products / Sponsored Brands prompts

Amazon Ads' March 10, 2026 launch announcement states that supported U.S. Sponsored Products and Sponsored Brands campaigns can have prompts automatically enabled for existing campaigns, with prompt-level performance reporting. This shows that shopper-visible delivery can change without an ordinary advertiser edit to campaign bid, budget, targeting or structure.

### Sponsored Brands collections

Amazon Ads' May 27, 2026 launch announcement states that Sponsored Brands collections support manual or automatic product selection. Under automatic control, Amazon AI dynamically curates relevant product groupings from the advertiser catalog based on campaign targets and shopping signals. Amazon's public setup guide further describes automatic collections as dynamically selecting products for shoppers, while manual collections use advertiser-selected products.

This establishes a second, materially different case: the same campaign/targeting configuration can produce a changing **realized product mix**.

### Brand+ / Performance+ Audience Signals

Amazon Ads' July 22, 2026 launch announcement describes Audience Signals for Brand+ and Performance+ as advertiser-provided audience data used to guide AI optimization. For Brand+ Prospecting, Amazon explicitly describes these signals as optimization inputs while retaining full reach discovery.

This establishes a third semantic distinction: a configured audience can be an **optimization signal** without being a hard audience-only targeting or holdout boundary.

Therefore the repository does not infer any of the following from a configured audience signal alone:

```text
signal members = all delivered users
non-members = excluded
configured signal = experiment cohort boundary
```

The exact semantics remain product-specific. A hard include, hard exclude, optimization signal, and unknown audience control are treated differently.

The feature announcements list availability and access paths that are product-specific and time-sensitive; the repository does not generalize them into a universal rule for every ad product or account.

## Generic adaptation

The repository independently derives the following safety framework:

1. keep configured controls separate from realized surface/product/creative/audience delivery identity;
2. treat platform-managed realization shifts as potential causal confounders, not automatic causes;
3. require account/campaign eligibility plus realized delivery evidence before assigning causality;
4. do not equate eligible catalog products with products actually shown;
5. do not equate an optimization signal with a hard eligibility or experiment boundary;
6. do not convert missing realization dimensions from an active connector into zero/unchanged state;
7. in post-change review, verify realization comparability separately from control readback;
8. downgrade ASIN-, audience-, or single-action causal claims when realized composition is unknown or materially changes.

This extends the earlier delivery-surface rule without replacing it: delivery surface is one realization dimension; product, creative/message, and actual audience composition are additional dimensions.

## Memory and replay implication

Once realized identity affects both drop diagnosis and post-change review, leaving realization context as unconstrained free-form event fields creates a cross-Agent replay risk: different runtimes can record the same surface/product/creative state under different names, and later history cannot reliably determine whether two evaluation windows were comparable.

The repository therefore adds a **bounded, optional canonical snapshot** rather than making every realization field mandatory:

- `schemas/optimization-event.json` defines `realization_snapshot` for material readback/evaluation/correction events;
- `schemas/entity-history.json` exposes compact derived realization retrieval views;
- the event snapshot remains the source of truth, while the derived view is only an index/summary;
- unavailable realization dimensions stay `Unknown` / `Unavailable` instead of being synthesized as zero or unchanged;
- compact identifiers/hashes are preferred to persisting full prompt/creative payloads or large product lists.

This keeps the schema backward-compatible and runtime-neutral while giving Codex, Claude Code, WorkBuddy and other agents a shared vocabulary for replay.

## Adjacent agent-memory research reviewed

A fresh scan also reviewed `riponcm/projectmem` and its 2026 PROJECTMEM paper. The project is MIT licensed and independently demonstrates an append-only event log with deterministic projections into compact summaries plus pre-action memory gates. Those high-level properties are consistent with this repository's existing append-first optimization-memory architecture.

No ProjectMem source code, schema, prompts, CLI, MCP implementation, or file layout was copied. The project was used only as corroborating evidence that typed append-only events plus derived summaries are a practical multi-agent memory pattern; the Amazon Ads realization snapshot fields and decision semantics here were designed independently for this repository.

A second replay-oriented memory project, Mneme, was reviewed but not adopted because its repository currently states the license as TBD/pre-release. Its concepts therefore were not used as an implementation source.

## Sources

Primary public vendor sources:

- Amazon Ads, “Sponsored Products prompts and Sponsored Brands prompts”, launch announcement dated March 10, 2026; U.S. GA dated March 25, 2026.
- Amazon Ads, “Scale product discovery with AI-powered Sponsored Brands collections”, launch announcement dated May 27, 2026.
- Amazon Ads, “Sponsored Brands collections: Promote related products and reach more shoppers”, public setup guide, retrieved September 2026.
- Amazon Ads, “Brand+ and Performance+ expand AI, keep advertiser control”, launch announcement dated July 22, 2026; Audience Signals described as AI optimization inputs, with Brand+ Prospecting retaining reach discovery.

Adjacent open research / implementation reviewed:

- `riponcm/projectmem` / PROJECTMEM (arXiv:2606.12329), MIT license; reviewed for append-only event-log + deterministic derived-summary architecture only.
- `BrettNye/Mneme`, pre-release with license marked TBD; rejected as an implementation/adaptation source.

## Copyright / license boundary

Amazon Ads Help, What's New and guide pages are public vendor documentation, not open-source software licensed for redistribution. This repository uses only factual platform behavior and independently rewrites it into a causal/data-governance method. It does not copy Amazon UI, ad creative, report templates, API schemas, proprietary AI selection logic, prompts, screenshots, or substantial source prose.

ProjectMem is MIT licensed, but this change still does not copy its implementation. Mneme's license is unresolved/TBD, so no implementation, schema, prose, prompt, or workflow from it is adopted.

## Rejected adjacent candidates

General Agent Skills/Claude plugin collections were not adopted because the repository already implements thin `SKILL.md`, progressive loading, shared references, deterministic policy checks, capability replay and multi-runtime manifests. No reviewed skill-layout candidate provided a non-overlapping method with stronger value than making realized-ad reasoning safer.

Replay/memory systems that focus on generic belief stores were also rejected as direct dependencies: this repository needs a narrow Amazon Ads optimization ledger, not a general-purpose agent memory platform.

## Safety boundary

The policy and schema changes govern evidence interpretation and replay only. Live campaign/product/creative/audience mutations remain outside the Skill layer and require an explicitly authorized external Connector / Executor.
