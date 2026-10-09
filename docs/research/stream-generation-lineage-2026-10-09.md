# Marketing Stream generation / acquisition-channel lineage — 2026-10-09

## Reproduced gap
The current metric aggregation gate only checked the exact channel
`amazon_marketing_stream_v2`. A generic `amazon_marketing_stream`
source with `stream_generation=v2` returned `Not Applicable`, even
though the data must be reconciled by full record identity and highest
`streamBatch.version` before summing.

## Smallest safe change
Resolve channel and generation together. Explicit v1/v2 declarations
can pass only when coherent. Generic channel requires a declared v1/v2
generation. Missing, contradictory or unknown provenance remains
`Unknown`; non-Stream sources with Stream-only metadata also fail closed.
Verified v2 record-key coverage and highest-version selection may pass,
subject to the repository's separate completeness, metric and lineage
checks. No Stream ingestion/Executor or new Skill is introduced.

## Sources and IP boundary
- Amazon official Stream v2 overview, proprietary documentation:
  https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/overview
  Adopt factual total-value/re-delivery semantics only; no source text copied.
- Amazon official Stream v1→v2 migration, proprietary documentation:
  https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/migrate-from-v1
  Use only published version distinctions and migration context.
- Amazon-owned amzn/amazon-marketing-stream-examples, MIT-0 (previously
  reviewed under SOURCES): https://github.com/amzn/amazon-marketing-stream-examples
  Reject ingestion/code reuse; S3/SQS/upsert/retry remains external.
- KuudoAI/amazon_ads_mcp, MIT (previously reviewed under SOURCES):
  https://github.com/KuudoAI/amazon_ads_mcp
  Reject connector implementation reuse; no new dependency.
- Operator/Reddit discussions: no reproducible evidence for a source
  identity rule; do not treat anecdotes as platform specification.

The regression fixtures are synthetic and authored independently.
