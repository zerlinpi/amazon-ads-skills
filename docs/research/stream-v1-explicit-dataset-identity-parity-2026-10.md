# Explicit Stream dataset identity parity across v1/v2 — 2026-10-28

Initial main `e411fea4348eabed3a1a8b8be1bf11cc65ecf8f4` (v2.0.0), no open PR, main Actions #40611590354 SUCCESS. V1 additive/disjoint data with Verified delta reconciliation could return Allowed despite explicit Unknown dataset. The existing v2 dataset placeholder regex used an escaped backslash inside a raw character class and consumed literal 's', so Missing/Unsupported were not recognized. Synthetic internal defects only, not real-account data corruption.

## RED→GREEN

- Tests-only `b2f62de401e0f83725d2e5c4003c4b52d8d5702a`: [RED #40617171450](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40617171450), 2174 tests/8 FAIL, 3 compatibility passes.
- Initial parity fix `222a7d0f6f43a13bde730c7bdbc956f20bcd083b`: [#40617232281](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40617232281), 2174 tests/1 FAIL exposing regex.
- Two v2 regression tests `ba8d1bd63605909c067d311b2fb386b9432ca4dc`: [RED #40617295510](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40617295510), 2176 tests/3 FAIL.
- Regex fix `0c3203e6e3313b0c33894f5f21b64ba0d7ba592a`: [GREEN #40617361659](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40617361659), 2176 PASS, 15 Skill/55 Eval validators PASS.

## Contract, source and IP

Explicit `stream_dataset` must be a concrete unpadded non-placeholder string for either resolved generation. Omitted optional metadata and opaque concrete labels remain compatible. MINOR v2.1.0 per AGENTS.md; no new Skill/schema/dependency/Ads write. [Amazon Stream v2 Overview](https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/overview) and [FAQ](https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/faq), checked 2026-10-28, establish v1/v2 delivery differences and dataset/account filtering but not this normalized JSON contract. Public OpenLineage, OpenEvals, Amazon Ads MCP, Agent Skills, MCP Servers and Amazon Stream Examples were not imported. No third-party code/prompt/schema/workflow/template copied; sample metadata is not a full license/security/CI/issue/PR audit. Public operator cases remain hypotheses.

P0 next: independently authenticate dataset/account/subscription and full delivery window. P1: event/endpoint readback version alignment. P2: campaign interactions and marginal contribution economics. Authorized external Executor owns all writes and ingestion/retries/reconciliation.
