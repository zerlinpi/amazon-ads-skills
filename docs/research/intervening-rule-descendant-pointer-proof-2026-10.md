# Optional SP rule-event descendant JSON Pointer proof — 2026-10-28

## Fresh read and gap

Starting main `945dedcdf5409ef3a0bc1aa128530eec5571bb97` (v1.112.0), last main Actions #40562795295 SUCCESS, zero open PR. Three sampled earlier branches were behind main with no commits ahead. Read all 15 canonical Skills, AGENTS/CLAUDE, source/research/reference, schemas, scripts/tests/evals, playbook and three runtime manifests. Main's event comparator correctly rejected nested arrays without independent proof, but unlike endpoint snapshots it offered no opt-in descendant-proof envelope. This blocked verified complex rule observations even when the adapter had separately captured complete nested collections. This is an internal normalized evidence expressiveness gap, not an Amazon-native event schema or an actual source-integrity incident.

## Contract and behavior

For positively observed Sponsored Products bid/budget schedule/event/budget-rule transitions, optional `rule_descendant_collection_evidence` is a pair of `before` and `after` maps. Each map is keyed by exact RFC 6901 JSON Pointers rooted at that event-side state. Every descendant list inside rule members, including empty lists, needs its own `enumeration_status=Complete`, `pagination_status=Complete`, `capability_status=Supported` proof. Reject extra/unmapped pointers, missing phases, malformed proof fields and incomplete statuses. Require independent outer `rule_collection_evidence`; neither outer proof nor descendant proof certifies the full experiment-window event log. Legacy nested lists without proof stay Unknown, flat legacy rule transitions remain compatible. Read-only comparator only; no API calls or Executor.

## RED→GREEN

- Branch `feat/intervening-rule-descendant-proof-20261028`, PR #226.
- Initial RED tests-only `5c0f7f2729a69859492bf02a9aefcfcdcff7ba44`, Actions #40572482495: 2121 tests, 4 FAIL / 1 ERROR (the ERROR was a schema-absence assertion using direct indexing, not a production crash).
- Corrected RED `e49a11ecf5d0ca9737d89abdf5a71159209e5e88`, [Actions #40572576136](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40572576136): 2121 tests, 5 FAIL, no ERROR. Fourteen deterministic tests.
- Production/schema `ea7916a699f767ff4eb5682e8c11d9209664bc90`, [Actions #40572696421](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40572696421): 2121/2121 PASS; Skill and Eval validators PASS. The final documentation/version commit and PR/main CI must be verified separately.

## Sources, license and decision

[Amazon Sponsored Products schedule-based bid rules](https://advertising.amazon.com/resources/whats-new/schedule-based-bid-rules-available-for-sponsored-products) and [Marketing Stream v2 FAQ](https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/faq) support time-varying controls and explicit source completeness/restatement caveats; they do not define this adapter JSON structure. Reviewed OpenLineage (Apache-2.0), OpenEvals (MIT), KuudoAI Amazon Ads MCP (MIT), Agent Skills (Apache-2.0), MCP Servers (NOASSERTION), including stars, recent push, fork, sample Actions and PR. No external framework added because local stdlib code suffices; no third-party code, prompt, schema, template or workflow copied. Reddit experience is not treated as Amazon policy or causal proof. Details in docs/SOURCES.md.

## Remaining gaps

P0 independently authenticated complete control-event window and revision/version lineage; P1 cross-source proof-to-endpoint identity/batch consistency; P2 connector source/account/grain and profitability causality. A Complete self-reported proof is not independent authentication.
