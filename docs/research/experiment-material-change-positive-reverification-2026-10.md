# Positive re-verification of material holdout boundary changes (v1.77.0)

Reviewed: 2026-10-26. Surface: `scripts/validate_experiment_plan.py` Ready-only semantic gate. Adopted, MINOR. No Amazon Ads writes.

## Gap and priority

P0 internal: an explicitly recorded material scope change could omit `reverified`, use `null`, a string or a number, and still pass `status=Ready` as long as `boundary_monitoring.latest_verified_at` occurred after the change. The prior code rejected only the singleton Python value `False`. A later timestamp is chronology, not affirmative evidence that each changed routing, audience, budget pool, entity or automation boundary was independently rechecked. This is distinct from v1.76.0 identity/arm overlap guards.

External authenticity of holdout delivery is a higher-level unresolved P0 but cannot be proven by adding self-asserted fields. This local gap is independently reproducible and fixable without new external dependencies.

## RED → GREEN

- Starting main: `1877ac1475e6b1ca0ed4b230327b55e048c3f7dd`; main Actions #40271439096 success; no open PR; checked historical experiment branches were behind main.
- Test commit: `5370f7fbcbeefc113ff3cc0b38b6f48892fa765d`. [RED Actions #40276084171](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40276084171): 1613 tests, 6 failures, four compatibility tests passed. Failures cover missing, null, string, numeric 0/1 and one unknown among multiple changes.
- Minimal code commit: `eba5db8b194f3907186ecda1f1ec9e4a3ef8b93c`. [GREEN Actions #40276152016](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40276152016): 1613/1613 PASS, 15 Skills and 55 eval fixtures PASS.
- Implementation: require `change.get("reverified") is True` for every recorded material change in a Ready holdout. Preserve latest verification chronology, current Clean state, the existing explicit False rejection, and exploratory Shadow/Hold/Redesign compatibility. The JSON schema still permits incomplete exploratory records; the semantic Ready gate is intentionally stricter.

## Source scope, open-source review and copyright

[Amazon Sponsored Products schedule bid rules (2023-11-06)](https://advertising.amazon.com/en-us/resources/whats-new/schedule-based-bid-rules-available-for-sponsored-products/) establishes time-varying scheduled bid controls. [Amazon Brand Lift methodology (updated 2025-05-02)](https://advertising.amazon.com/help/G7SUSMZ2GKJP42QS) describes exposed/control groups in its own measurement context, not a Sponsored Products holdout contract. [Amazon SP search-term report (updated 2026-05-18)](https://advertising.amazon.com/help/G3HEFZYWZF84NPS9) excludes non-clicked terms, so absent search-term rows are not proof of zero leakage. These do not define our normalized boolean or authenticate Amazon API responses.

New candidates: fivetran/great_expectations (11,902 stars, Apache-2.0, active tests/CI) and evidentlyai/evidently (8,011, Apache-2.0, tests and mixed recent CI). KuudoAI/amazon_ads_mcp (74, MIT) was already reviewed. Full fork/license/CI/PR sampling in SOURCES. Reject implementation adoption: a single explicit boolean guard has no demonstrated need for an external framework, and stars/CI do not certify Ads data. No external code, prompt, schema, workflow or template copied. Unlicensed or restrictive material remains abstract-principles-only.

[Public DSP audience test discussion (2025-08-29)](https://www.reddit.com/r/datascience/comments/1n3jnpw/) is only a hypothesis source about overlapping exposure, not Amazon policy or verified causality.

## Residual boundaries

`reverified: true` is an internally supplied claim, not a cryptographically verified raw source, a complete trigger/execution history, or proof of zero interference. Next: authorized external boundary readback with source identity and full-window rule history; cross-campaign control interaction and marginal profit. Default Read-only/Suggest/Shadow; actual writes/retries/reconciliation belong to authorized external Executor.
