# Getting Started: Codex, Claude Code, WorkBuddy, and manual loading

This repository is a **multi-Skill Amazon Ads library**, not a live Amazon Ads connector. The safest and most portable first-run path is to clone the whole repository, open the repository root in your agent runtime, and let the runtime load only the Skill needed for the current task.

The canonical Skill tree is `skills/`. Keep the repository structure intact because Skills can progressively load shared files from `references/`, `schemas/`, and `playbooks/`.

## 1. Clone the repository

```bash
git clone https://github.com/zerlinpi/amazon-ads-skills.git
cd amazon-ads-skills
```

To pin a reproducible revision, checkout a release/tag or commit after cloning instead of silently following a moving branch.

No Amazon Ads credentials are required to validate or read this repository. Do not place client secrets, refresh tokens, profile IDs, or advertiser secrets in repository files.

## 2. Validate the checkout

From the repository root:

```bash
python -m unittest discover -s tests -v
python scripts/validate_skills.py .
python scripts/validate_evals.py .
```

A passing repository validation proves package/contract integrity only. It does not prove that a model made a correct Amazon Ads decision and it does not connect to an advertiser account.

## 3. Choose one loading mode

### Recommended: repository-workspace mode

Use this when the runtime can open a local Git repository or working directory. Keep the entire checkout together and start the runtime from the repository root.

- Codex: repository instructions live in `AGENTS.md`; canonical Skills live in `skills/`.
- Claude Code: repository instructions live in `CLAUDE.md`; canonical Skills live in `skills/`.
- WorkBuddy / compatible plugin hosts: runtime metadata is in `.workbuddy-plugin/plugin.json`; keep the full repository available so relative references continue to resolve.
- Other Agent Skills-compatible runtimes: explicitly point the runtime at `skills/` or at the exact `skills/<name>/SKILL.md` entrypoint.

This mode requires no copying of the 15 Skills into runtime-specific folders.

### Optional: native plugin / Skill installer

If your current runtime exposes a native plugin or Skill installer, you may use it instead of repository-workspace mode. Runtime installation commands and storage locations can change between releases, so prefer the current host UI/installer over hardcoding an internal cache directory.

When delegating installation to an agent, require it to preserve the complete Skill directory and all repository-relative references. Do **not** copy only a `SKILL.md` file and discard its referenced files.

### Fallback: explicit Skill loading

If automatic Skill discovery does not trigger, name the exact repository-local entrypoint in the prompt. For a cross-domain request, use:

```text
skills/amazon-ads-optimizer/SKILL.md
```

For a focused request, point to the relevant `skills/<name>/SKILL.md`. Read only that Skill first, then load the referenced supporting files on demand.

## Codex

### Workspace setup

1. Clone the repository.
2. Open `amazon-ads-skills` as the Codex workspace, or start the Codex CLI from the repository root.
3. Confirm that Codex read the repository-level `AGENTS.md`.
4. Give a real task. Let Codex select one Skill; for a task spanning multiple optimization domains, route through `skills/amazon-ads-optimizer/SKILL.md`.

Current Codex builds understand repository `AGENTS.md` instructions and expose Skill/plugin mechanisms, but host-managed Skill roots and installer details can evolve. Repository-workspace mode is therefore the stable default for this project.

### Codex Bootstrap prompt

Paste this as the first task in a fresh Codex session:

```text
Read the repository instructions in AGENTS.md first. This repository is the canonical Amazon Ads Skills source for this workspace.

For my task, inspect only the matching skills/<skill-name>/SKILL.md first and progressively load references, schemas, or playbooks only when the selected Skill requires them. If the task spans multiple optimization domains, start with skills/amazon-ads-optimizer/SKILL.md.

Before analysis, state which Skill you selected, the operating mode, and the minimum inputs you need. Default to Suggest. List missing inputs instead of guessing. Missing fields, unavailable historical reports, unsupported connector capabilities, and absent report rows are not zero.

Do not perform live Amazon Ads writes. Any real mutation must remain outside this repository in an explicitly authorized External Connector / Executor.

Now inspect this repository as Codex would use it and tell me which Skill should handle the task I provide next.
```

### Codex self-install prompt when a native installer is available

Use this only when your Codex build exposes a Skill/plugin installer:

```text
Install or register the Amazon Ads Skills from https://github.com/zerlinpi/amazon-ads-skills using the native Skill/plugin mechanism available in this Codex build.

Treat every direct child under skills/ that contains SKILL.md as an independent Skill. Preserve the repository structure and referenced files; do not flatten the package or copy only SKILL.md. Keep AGENTS.md available as the repository instruction source.

If this Codex build cannot register the repository safely as a plugin/Skill source, do not invent a config path. Fall back to cloning the repository and using repository-workspace mode.

After setup, report the discovered Skill names, confirm the default mode is Suggest, and run the repository validation commands. Do not connect to or modify a live Amazon Ads account.
```

### Codex smoke-test prompt

```text
Read AGENTS.md, then use skills/amazon-ads-audit/SKILL.md for this synthetic task only: I have a US Sponsored Products account and want an account audit, but I have not supplied any campaign/report data yet. State what inputs are missing and stop before inventing metrics or recommendations. Do not perform live Amazon Ads writes.
```

Expected behavior: Codex identifies `amazon-ads-audit`, stays in `Suggest` or read-only analysis, requests the missing evidence, and does not treat missing data as zero.

## Claude Code

### Workspace setup

1. Clone the repository and start Claude Code from the repository root.
2. Keep `CLAUDE.md`, `.claude-plugin/plugin.json`, `skills/`, and shared references together.
3. Claude Code's plugin system uses `.claude-plugin/plugin.json` as plugin metadata. If you distribute this repository through a Claude plugin marketplace, use the current Claude Code `/plugin` / project-configuration flow for that host version.
4. For local development or when marketplace installation is not configured, repository-workspace mode remains valid and avoids duplicating business rules into Claude-specific copies.

### Claude Code Bootstrap prompt

```text
Read the repository instructions in CLAUDE.md and AGENTS.md first. Use the canonical skills/*/SKILL.md definitions; do not create Claude-specific copies.

For each task, state which Skill you selected and why. Read that SKILL.md first, then load only the references/schemas/playbooks it requests. Default to Suggest. List missing inputs instead of guessing.

Do not perform live Amazon Ads writes. Execute means producing a validated proposal for an explicitly authorized External Connector / Executor, not mutating an advertiser account from this repository.

For a cross-domain request, start with skills/amazon-ads-optimizer/SKILL.md.
```

If Claude Code fails to auto-discover a Skill, explicitly name the target path, for example:

```text
Use skills/performance-drop-diagnosis/SKILL.md and follow its progressive references to diagnose this performance drop.
```

## WorkBuddy

WorkBuddy supports Skills/plugins through its installed-Skills and plugin flows. This repository already contains `.workbuddy-plugin/plugin.json`, but a manifest alone is not proof that a particular WorkBuddy build has installed or enabled the plugin.

### Recommended setup

1. Clone/download the **whole repository** for review and development.
2. In a WorkBuddy build that supports third-party plugins, use its current plugin/marketplace import flow with the complete repository/package so `.workbuddy-plugin/plugin.json`, `skills/`, `references/`, `schemas/`, and `playbooks/` remain together.
3. If your build accepts only individual Skill packages, do not blindly zip a single `skills/<name>` folder: some Skills reference shared repository files through relative paths. Either use whole-repository/plugin mode or build a self-contained package that includes every referenced file and revalidate the links.
4. Enable the imported Skill/plugin in WorkBuddy before expecting automatic invocation.

### WorkBuddy Bootstrap prompt

```text
Use the installed Amazon Ads Skills from the amazon-ads-skills repository. Treat skills/ as the canonical Skill tree and load only the Skill relevant to my task first.

Before analysis, state which Skill you selected, operating mode, required inputs, and any missing evidence. Default to Suggest and list missing inputs instead of guessing. Do not perform live Amazon Ads writes or send data to an External Connector / Executor unless I explicitly authorize that external action.

If automatic Skill discovery is unavailable, explicitly read skills/amazon-ads-optimizer/SKILL.md for cross-domain work or the matching skills/<name>/SKILL.md for a focused task.
```

## Manual / explicit Skill loading

Use this path when an agent supports files but does not implement Agent Skills discovery.

1. Give the agent access to the repository root.
2. For a focused task, instruct it to read exactly one `skills/<name>/SKILL.md` first.
3. For a multi-domain task, start with `skills/amazon-ads-optimizer/SKILL.md`.
4. Allow the agent to load only referenced files under `references/`, `schemas/`, `playbooks/`, or the Skill's own `references/` directory.
5. Keep `evals/` out of ordinary account analysis unless you are explicitly running an evaluation.

Generic Bootstrap prompt:

```text
Read the repository instructions and use this repository as a read-only Amazon Ads decision library. Start from the one SKILL.md that best matches my request; use skills/amazon-ads-optimizer/SKILL.md only when the request spans multiple domains.

State which Skill you selected and the evidence it requires. Default to Suggest. List missing inputs instead of guessing. Never turn an absent report row, unsupported field, unavailable history, or missing connector capability into zero.

Do not perform live Amazon Ads writes. If an action would require a real account mutation, output a guarded proposal for an External Connector / Executor instead.
```

## How to verify the runtime loaded the repository correctly

A fresh runtime should be able to do all of the following without advertiser credentials:

1. Identify the matching Skill instead of reading all 15 Skills at once.
2. State the default operating mode as `Suggest`.
3. Ask for missing advertising evidence rather than fabricating it.
4. Preserve marketplace/profile/date/attribution/source scope before high-confidence conclusions.
5. Treat live mutation as an External Connector / Executor responsibility.
6. Run the three deterministic repository validation commands from the repository root when shell access is available.

A plugin card, manifest file, or cloned folder by itself does not prove successful model discovery. Verify behavior with one of the smoke-test prompts above.

## Common setup failures

- **Opened the wrong directory**: opening only `skills/` can hide root `AGENTS.md`, `CLAUDE.md`, runtime manifests, shared schemas, and playbooks. Open the repository root.
- **Copied only SKILL.md**: progressive references can break. Preserve the referenced files and relative layout.
- **Assumed a runtime cache path is permanent**: prefer the host's current native installer or repository-workspace mode instead of hardcoding private/internal directories.
- **Expected plugin metadata to create an Amazon Ads connection**: `.codex-plugin/plugin.json`, `.claude-plugin/plugin.json`, and `.workbuddy-plugin/plugin.json` describe the library; they do not provide advertiser authentication or live API access.
- **Expected missing data to mean zero**: stop and resolve source/coverage/lineage first.
- **Expected Execute to be automatic**: this repository produces guarded proposals. Live writes, retry/idempotency, credentials, and reconciliation belong to an external executor/connector.

## Runtime files at a glance

| Runtime | Repository entrypoints | Stable first-run path |
|---|---|---|
| Codex | `AGENTS.md`, `.codex-plugin/plugin.json`, `skills/` | clone → open repo root → Bootstrap prompt |
| Claude Code | `CLAUDE.md`, `.claude-plugin/plugin.json`, `skills/` | clone → start from repo root → Bootstrap prompt |
| WorkBuddy | `.workbuddy-plugin/plugin.json`, `skills/` | whole-repo/plugin import when supported → Bootstrap prompt |
| Other file-capable agent | `skills/<name>/SKILL.md` | explicit Skill loading |

The repository remains provider-neutral: runtime packaging can differ, but Amazon Ads business logic stays in the same canonical `skills/` tree.
