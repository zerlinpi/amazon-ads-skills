# Global SP mixed-resource optimization-plan readback

Run `python -m scripts.evaluate_global_sp_mixed_plan_readback < evidence.json` on a **trusted, externally normalized plan manifest** and independent resource-level readbacks. This read-only classifier does not access Amazon Ads, execute or retry writes, perform idempotency/reconciliation, or authenticate the external plan ledger.

## Why a separate plan gate

The [Amazon Ads Global Sponsored Products API](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns) documents distinct campaign, ad-group and target resources, HTTP 207 indexed update receipts, and later paginated query evidence. A campaign state confirmation cannot confirm a target bid; an ad-group default bid cannot confirm a target bid; success for one update call cannot prove an entire multi-call optimization plan succeeded.

**This plan manifest is a repository-defined adapter contract, not a native Amazon Ads endpoint or response field.** `coverage_status: Complete` and the manifest's source fields are external assertions. An external authorized Executor must separately guarantee that the declared manifest is authentic, immutable, exhaustive and bound to the actual plan. This helper verifies internal consistency and component readback only; it cannot prove a dishonest or omitted manifest.

## Input contract

```json
{
  "manifest": {
    "plan_id": "synthetic-plan-1",
    "global_account_id": "synthetic-global-a",
    "coverage_status": "Complete",
    "source": {
      "source_system": "synthetic-planner",
      "acquisition_channel": "plan",
      "connector_id": "synthetic-plan-adapter"
    },
    "components": [
      {"component_id": "campaign-state", "kind": "campaign",
       "campaign_id": "synthetic-campaign-a"},
      {"component_id": "target-bids", "kind": "target_batch",
       "request_ids": ["synthetic-req-1", "synthetic-req-2"]}
    ]
  },
  "components": [
    {"component_id": "campaign-state", "kind": "campaign",
     "evidence": {"request": {}, "receipt": {}, "readback": {}}},
    {"component_id": "target-bids", "kind": "target_batch",
     "evidence": {"requests": [], "receipt": {}, "readbacks": []}}
  ]
}
```

The nested evidence placeholders above are **not executable examples**: fill them with the respective validated contracts. `kind` is one of `campaign`, `ad_group`, `target`, `ad_group_batch`, or `target_batch`. Campaign uses `campaign_id`; all other kinds use ordered `request_ids` matching the nested request(s). Component IDs must be unique and exactly covered by evidence. One Global Account is required across all requests. Repeated resource identities or request IDs across components are rejected because a final readback cannot prove intermediate sequential changes. Unrecognized `expected_*` plan intent and claimed per-component verdicts are rejected.

Child evidence is classified by the existing independent resource verifier; the plan classifier **never accepts a caller-supplied `Confirmed` status**. Child source, time, native-currency, marketplace, identity, connector capability and pagination rules remain unchanged. No currency conversion, missing-as-zero, inferred receipts or invented coverage.

## Results and limits

Output includes `application_status`, `reasons`, `plan_id` (only after structural validation), and per-component independently computed outcomes. `Confirmed` requires every declared component to be `Confirmed`. Repository safety precedence: `Unknown > Partial > Drifted > Confirmed`. This is not an Amazon API response precedence. A drifted or partial component does not imply the others failed; inspect component outcomes.

This helper does not support campaign multi-item batches, repeated updates to the same entity, mixed ad-product operations, placements, unsupported expected intent, cross-account plans, or external write reconciliation. Even a fully confirmed configured state does **not** establish causal impact, auction bids, profitability, or experimental validity.

## Copyright boundary

Independently authored normalized plan-evidence policy. No third-party code, API payloads, prompt, schema, workflow or template copied.
