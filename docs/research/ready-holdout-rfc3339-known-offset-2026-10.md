# Ready holdout known-offset RFC3339 evidence — 2026-10-27

## Verified gap

Fresh main 9b75d8f9d37ba8cc8d2515fb459399d8486ab9ed (v1.90.0), main push Actions #40390785509 SUCCESS, no open PR at start. Read recent commits/Actions, inventoried tree, all 15 canonical Skills, relevant references, schemas, research, tests, scripts and runtime manifests. Other directories were inventoried rather than exhaustively line-audited. Four related historical branches had zero commits ahead of main.

Ready holdout validation used Python datetime.fromisoformat, which accepts space separators, offset seconds and -00:00 as timezone-aware instants. This allowed ambiguous/noncanonical timestamps to count as boundary, launch, material-change or isolation verification. This is an independent temporal-evidence defect, not another metric-name patch.

## RED → GREEN

- RED 9118fb40901f92a6b814efb092d8a2746668656d, [Actions #40398537707](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40398537707): 1830 tests, 9 FAIL; five new compatibility cases passed.
- GREEN 14a96bec12da27084d490273fee16e2f7fb5e6ac, [Actions #40398664913](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40398664913): 1830/1830 PASS, Skills/Evals PASS. Minimal regex and known-offset check before parsing; no new Skill, schema, dependency, external write or executor authority.

## Sources and rights

[RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339) and [RFC 9557](https://www.rfc-editor.org/rfc/rfc9557.html) explain timestamp shape and unknown local offsets; [Python 3.12 docs](https://docs.python.org/3.12/library/datetime.html) explain permissive ISO parsing. [Amazon Ads budget/bidding rules](https://advertising.amazon.com/library/guides/budget-rules) and [Marketing Stream v2](https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/overview) provide control/reporting context, not this repository's internal policy. Re-reviewed nonfork MetricFlow (1848, Apache-2.0), OpenLineage (2726, Apache-2.0), OpenEvals (1232, MIT), Amazon Ads MCP (74, MIT), Agent Skills (26663, Apache-2.0), MCP Servers (91593, NOASSERTION). Rejected imports; sampled Actions/PRs are not exhaustive code/security/license audits. No third-party code/prompt/schema/workflow/template copied. Practitioner anecdotes are not platform requirements.

## Residual gaps

P0 externally authenticated provenance and interval-complete control-state evidence, not established by syntactically valid timestamps. P1 compatible ratio numerators/denominators, currency/date/grain/attribution/overlap. P2 cross-campaign budget/bid/placement interference and marginal contribution economics. Read-only/Suggest/Shadow; authorized Executor alone handles live writes.
