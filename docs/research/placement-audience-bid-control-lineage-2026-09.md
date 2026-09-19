# Placement + audience bid control lineage — 2026-09

Reviewed: 2026-09-19

## Gap

Placement analysis already treated base bid, placement adjustment, bidding strategy, and schedule/event rules as coupled controls, but it did not require the active **audience bid adjustment** state in the placement decision contract. That omission can create false causal attribution when placement performance changes while an overlapping audience-level bid control changes traffic/exposure.

## Current official evidence

Amazon Ads Help, **Bidding strategies for Sponsored Products**, updated 2026-09-14, states that Sponsored Products supports dynamic, fixed, or rule-based bidding and also says advertisers can adjust bids by audience. This is current product/help evidence, not a third-party implementation.

Source: https://advertising.amazon.com/help/GCU2BUWJH2W3A8Z7

Amazon Ads' Sponsored Products best-practices guide separately documents placement bid adjustments across top of search, rest of search, and product pages. The combination supports treating placement and audience adjustments as distinct controls whose realized effects can overlap, without inventing an auction-level composition formula.

Source: https://advertising.amazon.com/library/guides/sponsored-products-best-practices

## Adoption boundary

Adopt only the abstract decision-safety implication:

- capture audience bid adjustment state when supported and relevant;
- include its change timestamp in the coupled-control timeline;
- treat concurrent audience + placement changes as a confounding risk;
- fail closed on precise placement attribution when a material control state is missing or stale;
- re-verify capability scope before relying on exact platform behavior.

No Amazon prose, API schema, prompt, workflow, or implementation is copied. Amazon documentation remains Amazon copyrighted material. Repository-owned wording and tests remain MIT.

## Why this is higher value than adding another optimization heuristic

This closes a causal-identification hole in an existing Skill. A new heuristic that recommends placement increases/decreases while ignoring another active bid control would increase action risk. The safer order is to make the control graph complete first, then size actions only when the realized evidence is interpretable.
