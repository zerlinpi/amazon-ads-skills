# Runtime onboarding research

Reviewed: 2026-09-17

## Problem

The repository already exposed runtime manifests and canonical `skills/`, but did not tell a first-time user how to obtain the repository, choose a loading mode, verify discovery, or recover when automatic Skill discovery did not trigger. A Codex-style first-run simulation also found a stale example that could anchor a model to a repository-global bid-change percentage despite the current contextual action-sizing policy.

This review is limited to **discovery, installation, workspace loading, and first-use behavior**. It does not add a live Amazon Ads connector or execution authority.

## OpenAI Codex

Sources reviewed:

- https://github.com/openai/codex
- repository `AGENTS.md` / project-instruction behavior documented in the Codex source tree;
- current Skill installer samples and Skill host-root implementation;
- current Codex plugin/marketplace implementation and `.codex-plugin/plugin.json` conventions.

License: the `openai/codex` repository is Apache-2.0.

Relevant facts:

- Codex treats repository `AGENTS.md` as durable project instructions.
- Codex has native Skill/plugin discovery and installation mechanisms.
- Current source still contains a Skill installer that can install public GitHub Skill paths under the Codex home Skill area.
- The host-root implementation simultaneously marks the old `$CODEX_HOME/skills` user location as backward-compatible/deprecated, so that storage path is not treated here as a durable project contract.
- Codex also exposes project configuration and runtime-managed extra Skill-root concepts, but this repository does not depend on undocumented/internal field names for onboarding.

Adoption boundary:

- Adopted only the generic behavior: repository instructions, canonical Skill tree, optional native installation, and an explicit-path fallback.
- The stable project recommendation is therefore **clone → open repository root → let Codex read `AGENTS.md` → progressively load `skills/`**.
- No Codex source code, internal JSON-RPC messages, marketplace implementation, installer implementation, or config schema was copied.
- No internal cache/storage path is presented as a required permanent path.

## Anthropic Claude Code

Sources reviewed:

- https://github.com/anthropics/claude-code
- plugin-development documentation in that repository, including `.claude-plugin/plugin.json`, plugin installation/discovery guidance, and recommendations to document installation and usage.

License/adoption status: the current `anthropics/claude-code` repository states `All rights reserved` and makes use subject to Anthropic terms; it is **not** treated as an open-source implementation source for this project.

Relevant facts:

- Claude Code plugin metadata uses `.claude-plugin/plugin.json`.
- Its plugin flow supports installation through the current `/plugin` / marketplace or project configuration mechanisms.
- Plugin skills become available as part of the installed plugin.

Adoption boundary:

- Only factual runtime behavior and generic onboarding concepts were independently paraphrased.
- No Anthropic code, plugin templates, documentation prose, commands beyond public interface names, or proprietary implementation was copied.
- This repository does not claim to be published in an Anthropic marketplace. Repository-workspace mode remains the portable local-development fallback.

## WorkBuddy / CodeBuddy

Public vendor documentation reviewed:

- https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market
- https://www.workbuddy.ai/docs/zh/cli/plugin-marketplaces
- https://www.workbuddy.ai/docs/zh/cli/plugins
- https://www.workbuddy.ai/docs/zh/cli/plugins-reference

Relevant facts:

- WorkBuddy exposes a Skill Marketplace with install/enable/disable/update management.
- Current CodeBuddy/WorkBuddy plugin documentation supports GitHub/Git/local marketplace sources and plugin installation flows.
- Plugin Skills use a `skills/` tree with `SKILL.md` files and are discovered after plugin installation/loading.

Adoption boundary:

- Vendor documentation is treated as copyrighted documentation. Only public interface behavior is independently summarized.
- No vendor documentation prose, sample plugin implementation, marketplace catalog, or internal cache behavior is copied.
- This project does not add a WorkBuddy marketplace catalog in this change because the current repository has `.workbuddy-plugin/plugin.json`, while the documented marketplace flow has additional catalog/source requirements. Claiming one-step marketplace installation without that packaging would overstate current support.
- Because some Amazon Ads Skills load shared repository files through relative paths, onboarding explicitly warns against blindly packaging only one Skill folder unless all referenced dependencies are preserved and revalidated.

## Resulting portable onboarding contract

The repository now documents three layers instead of pretending all runtimes install identically:

1. **Repository-workspace mode (recommended)** — clone the full repository and open the repository root.
2. **Native runtime installer (optional)** — use the host's current plugin/Skill installer when available, without hardcoding private cache paths.
3. **Explicit Skill loading (fallback)** — point the agent at `skills/<name>/SKILL.md`; use `skills/amazon-ads-optimizer/SKILL.md` for cross-domain work.

A bootstrap/smoke-test must verify behavior rather than infer successful discovery from the presence of a manifest. The expected behavior is: select one Skill, default to Suggest, list missing inputs rather than guessing, preserve missing/unsupported/unavailable states instead of coercing them to zero, and leave live Amazon Ads mutation to an explicitly authorized external Connector / Executor.

## Rejected alternatives

- **Hardcoding `$CODEX_HOME/skills` as the required Codex setup path** — rejected because current Codex source marks the legacy user Skill location as backward-compatible/deprecated while installer/runtime mechanisms are evolving.
- **Inventing `.codex/config.toml` Skill fields** — rejected because no stable user-facing requirement was needed for repository-workspace mode.
- **Claiming this GitHub repository can already be installed from an Anthropic or WorkBuddy marketplace by one universal command** — rejected because marketplace publication/catalog registration is a separate packaging/distribution step.
- **Copying every Skill into runtime-specific directories** — rejected because it duplicates business logic and risks breaking relative progressive-loading references.
- **Keeping the old `single bid change <= 20%` example** — rejected because it conflicts with the current contextual action-sizing policy and can anchor a model to false precision.
