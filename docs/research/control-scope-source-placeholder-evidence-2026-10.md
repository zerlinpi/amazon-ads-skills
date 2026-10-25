# Scope/source placeholder evidence — 2026-10-25

Main `b3296c46e1068d2c04aa39b4dbf57b99b1c497b4` could classify changed base bid as `Treatment Isolated` with repeated `marketplace_id="Unknown"`, `connector_id="Unsupported"` or `source_system="Unknown"`. Matching placeholders do not establish identity.

**Priority:** P0 fixed: cross-surface scope/account/source identity evidence. P1: Amazon Business placement marketplace/campaign/retailer eligibility + connector capability. P2: continuous rule-execution history. P3: external adapter raw HTTP authentication.

**RED:** `e93ce2134391513d57fc2cc3d79dc698bea8c952`, 20 synthetic tests, 1294 total, 17 failures: https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40163083690 . **GREEN:** `01b569d8d31699345941149e0e547e274d8d2f9c`, 1294/1294, 15 Skills, 55 eval fixtures: https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40163139367 . Positive controls preserve real IDs and both-absent optional connector IDs. No zero or absence imputation.

Official Amazon Ads MCP account-context guidance: https://advertising.amazon.com/API/docs/en-us/mcp/get-started . Global SP account/marketplace scope: https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns . Neither authenticates the adapter. GitHub candidate metadata, license, CI and sampled PR review recorded in SOURCES; no third-party code, prompts, schema, templates or workflows copied. Reddit anecdotes used only to discover migration risks. No live Ads writes.
