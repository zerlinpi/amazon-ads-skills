# Experiment metric semantics evidence — 2026-09

## Decision gap

A Ready experiment can currently identify its primary metric by display name and success rule without binding the conversion metric to an attribution family or semantic version. That is unsafe when the same business concept can be reported under distinct attribution semantics.

## Public platform evidence

Amazon Ads announced that, effective 2026-01-01, standard Purchases, Sales, and ROAS for affected Store-ad inventory use a shopping-signal enhanced last-touch methodology. Amazon also continues to expose eligible 14-day `all views` conversion metrics through Unified Reporting, including `Purchases (all views)`. These are distinct measurement semantics and should not be silently substituted in an experiment baseline, treatment readout, or optimization-memory outcome.

Amazon Ads also made Unified Reporting generally available on 2026-06-08 across multiple manager/advertiser accounts, ad products, countries, metrics, and dimensions. Standardized reporting surfaces reduce manual stitching but do not make distinct attribution families interchangeable.

Sources:
- https://advertising.amazon.com/resources/whats-new/view-attribution-updates-for-amazon-store-ads
- https://advertising.amazon.com/resources/whats-new/streamline-campaign-analysis-with-unified-reporting

## Repository adoption

The repository should use a generic semantic envelope rather than hard-code a permanent list of Amazon API field names. For a Ready conversion experiment, the minimum decision identity is:

- `metric_family`
- `attribution_family`
- `semantic_version`

Unknown or unresolved semantics remain acceptable for `Shadow Only`, `Hold`, or `Redesign`; they must not be promoted to Ready evidence by guessing from missing data.

The validator may use conservative name recognition only to identify obvious conversion metrics that require the gate. The semantic values themselves remain explicit caller evidence rather than inferred attribution truth.

## Copyright and implementation boundary

Only public platform facts are summarized here. No Amazon API schema, implementation, prompt, workflow, UI, or protected template is copied. Repository tests, field names, and validation behavior are independently designed. No live Amazon Ads write capability is introduced.
