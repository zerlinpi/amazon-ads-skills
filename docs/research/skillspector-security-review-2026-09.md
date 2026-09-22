# NVIDIA SkillSpector review — 2026-09-23

## Why this source was reviewed

This repository supports Agent Skills across Codex, Claude Code and WorkBuddy runtimes and already treats retrieved connector/tool content as untrusted evidence rather than instructions. A fresh GitHub scan for high-signal Agent Skills / MCP / execution-safety projects surfaced `NVIDIA/SkillSpector`, so it was reviewed for a possible remaining supply-chain or runtime-safety gap.

## Repository evidence

Point-in-time discovery context on 2026-09-23:

- repository: `NVIDIA/SkillSpector`
- non-fork, non-archived
- approximately 18.1k stars and 1.5k forks
- Apache-2.0 license
- active push observed on 2026-09-22
- Python implementation with issues, pull requests and public project activity
- stated scope includes scanning Agent Skills for prompt injection, data exfiltration, malicious patterns and supply-chain risks across Claude Code, Codex and MCP-oriented workflows

Stars are discovery context only; they are not an adoption criterion.

Source:
- https://github.com/NVIDIA/SkillSpector

## Adoption / rejection decision

**Do not add SkillSpector as a dependency and do not copy its rules, prompts, scanner implementation, schemas or workflow.**

The project is high-quality corroborating evidence that skill-file supply-chain risk deserves explicit review, but the current repository already has a narrower trust boundary that is directly relevant to its runtime model: connector/tool/free-text output is evidence data, not trusted instruction, and runtime-specific manifests point back to the canonical `skills/` tree instead of maintaining independent business logic copies.

No deterministic regression currently demonstrates that adding a third-party scanner would improve Amazon Ads decision quality or action safety beyond the existing repository validator, review process and connector-content trust boundary. Introducing a scanner now would therefore add dependency and CI surface without a proven repository-specific failure mode.

## Revisit trigger

Revisit this decision only if one of the following becomes true:

1. the repository begins ingesting or installing third-party skill bundles dynamically;
2. runtime manifests or generated skills can contain externally supplied executable instructions;
3. a deterministic malicious-skill fixture bypasses the current validator/review controls;
4. a scanner can be integrated as an optional, reproducible CI check without becoming a required runtime dependency and demonstrates materially better detection on repository-owned fixtures.

If a revisit is justified, start RED-first with repository-owned adversarial fixtures and compare detection/false-positive behavior. Do not adopt scanner output as an authorization signal for Amazon Ads writes.

## Copyright / license boundary

Apache-2.0 would permit reuse under its terms, but this review intentionally uses only abstract security lessons and public repository metadata. No SkillSpector code, prompt, rule definition, schema, workflow, documentation prose or protected implementation is copied into this repository.
