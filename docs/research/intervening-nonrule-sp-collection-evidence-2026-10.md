# Unproven non-rule SP event collections — 2026-10-28

## Fresh read and gap

Starting main `dd1bf95333bfb3f92219c2bf4e017c33da592e39` (v1.113.0), main CI SUCCESS and no open PR. Read all 15 Skills and inspected AGENTS/CLAUDE, README, SOURCES/research, references, playbooks, schemas, scripts/tests/evals and three runtime manifests. Three sampled prior branches were behind main. P0 complete authenticated event-window coverage remains unsolved. A separate deterministic gap existed: positive mid-window SP routing/audience events accepted list descendants that endpoint snapshots require independent completeness proof for, potentially returning `Confounded` from unverified collections.

## RED→GREEN and compatibility

Test-only `d2193043bcf823fba91bb2e3b7ce3027d8316f79`, [Actions #40589410469](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40589410469): 2130 tests, five expected FAIL, no ERROR. Code `4c8ac7ee0fd88dcc0c2f74d19e712c61a28ba66d`, [Actions #40589486007](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40589486007): 2130 PASS, 15 Skill validators PASS, 55 Eval validators PASS. Nine synthetic deterministic tests: direct empty/nonempty routing arrays, deep routing empty arrays, empty/deep audience arrays; four flat/scalar compatibility cases. Reused `_nested_collection_problem` and `_deep_extra_collection_problem` for both event phases. No new schema; non-rule event array proof is not available. No Ads API calls, writes or new dependencies.

## Sources, licensing, remaining

[Amazon bidding help updated 2026-09-28](https://advertising.amazon.com/help/GCU2BUWJH2W3A8Z7), [schedule-based rules](https://advertising.amazon.com/resources/whats-new/schedule-based-bid-rules-available-for-sponsored-products) and [Marketing Stream v2 FAQ](https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/faq) support time-varying controls and cautious data semantics but do not define our event shape. OpenLineage (Apache-2.0), OpenEvals (MIT), KuudoAI Amazon Ads MCP (MIT), Agent Skills (Apache-2.0), MCP Servers (NOASSERTION) reviewed for metadata and sampled CI/PR; no external code/prompt/schema/workflow/template copied. Practitioner advice is hypothesis, not platform norm. P0 full-window source completeness, P1 event/endpoint version joins, P2 optional authenticated non-rule collection proof if connector supports it, P3 marginal-profit causal evidence. Default Suggest/Shadow; external Executor handles writes.
