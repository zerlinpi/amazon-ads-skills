# Unmapped Sponsored Products placement dimension evidence — 2026-10-27

## Verified gap and priority

At fresh main `253cb53e4aa3c07cae7012599be002a05d290f27` (successful main Actions #40524466419, zero open PR), the SP placement validator required `top_of_search`, `rest_of_search` and `product_pages` and validated optional `amazon_business`, but accepted any additional key in an otherwise complete/observed state. In both endpoints and positive mid-window events, a fabricated `unmapped_placement` could therefore yield `Confounded` or `Treatment Isolated` rather than `Unknown`. This is an independently reproducible P1 evidence/adapter-contract gap, distinct from P0 complete event-history capture.

## RED → GREEN

Tests-only commit `94a19671d814f18a280e42ded7b401873fa12c29` triggered [RED Actions #40534057133](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40534057133): **2086 tests, 5 FAIL**, three compatibility tests passing. Minimal code commit `69a9413469b526ba0269669deef487ea9cac98bd` triggered [GREEN Actions #40534159070](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40534159070): **2086/2086 PASS**, 15 Skills and 55 Eval fixtures PASS. Synthetic cases include extra placement keys in either event phase, both phases, one endpoint, both endpoints; compatibility includes standard placement, optional B2B modifier and isolated base-bid treatment. No Amazon Ads API calls or account writes.

## Evidence and boundaries

Amazon [rest-of-search placement launch (2024-01-09)](https://advertising.amazon.com/resources/whats-new/improve-campaign-performance) describes three standard SP placement bid-adjustment controls. [Amazon Business advertising](https://advertising.amazon.com/channels/amazon-business) and [Prime Day 2026 advanced strategies](https://advertising.amazon.com/library/guides/prime-day-guide-advanced-strategies) describe a separate Amazon Business bid adjustment. These public sources justify cautious review of unrecognized keys; they do not define this repository's snake_case schema or prevent future Amazon features. Source/adapter capability must be refreshed before expanding the allowlist.

Sampled GitHub metadata/licenses/activity: OpenLineage 2728 stars Apache-2.0, OpenEvals 1233 MIT, KuudoAI Amazon Ads MCP 74 MIT, Agent Skills 26695 Apache-2.0, MCP Servers 91601 NOASSERTION; nonfork at inspection. Selected PRs and Actions were checked, not a full code/security/issue/dependency-license or mirror audit. These projects were already reviewed in SOURCES; no import has a verified benefit to this narrow standard-library evidence check. No external code, prompt, schema, workflow, template or protected prose copied; NOASSERTION/restricted material is principles-only. Reddit budget/bid advice is an unverified experiment hypothesis, not platform specification or causal evidence.

## Remaining gaps

P0: independently authenticated complete time-window event capture and restatement reconciliation (not derivable from empty event arrays). P1: rule member collection completeness and cross-control temporal interactions. P2: connector-native metric/source/date/grain/currency/attribution identity. P3: cross-campaign auction interference and incremental contribution margin. Preserve 15 Skills, missing/unsupported/partial/unknown as unknown, Observation/Hypothesis/Cause/Action/Outcome separation, Read-only/Suggest/Shadow defaults and external authorized Executor ownership of all writes/retries/idempotency/reconciliation.
