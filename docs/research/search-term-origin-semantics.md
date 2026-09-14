# Search-term origin semantics research

## Why this matters

Amazon Ads optimization workflows often treat a Search Term report row as if the displayed string were always a shopper-entered search query. Current Amazon Sponsored Products documentation makes that assumption unsafe: a search term can be the phrase a customer used to search for products, **or** a term inferred as the best match to the advertised product in a non-search context, including off-Amazon social placements.

That distinction materially changes what the row can prove. Performance on an inferred best-match row is valid evidence about observed traffic quality, but the displayed text is not automatically evidence of literal shopper intent and does not automatically map to a Negative Exact / Phrase or Exact-keyword control.

## Primary source

### Amazon Ads — Search term report for Sponsored Products

- Public vendor documentation.
- Updated: May 18, 2026.
- Source: https://advertising.amazon.com/help/G3HEFZYWZF84NPS9
- Relevant factual behavior adopted:
  - search-term rows may represent customer search phrases;
  - in non-search contexts, a search term may instead be inferred as the best match to the product;
  - the report only includes search terms that received at least one ad click.

## Independent adaptation

The repository does **not** copy Amazon documentation text, report templates, UI, API payloads, or implementation details. It independently derives the following generic decision-safety rules:

1. Track `term_origin` when search-term semantics affect an action.
2. Distinguish `literal_query`, `inferred_non_search`, and `unknown` rather than assuming every displayed term is a literal shopper query.
3. Treat inferred rows as valid traffic/performance evidence without overstating shopper intent.
4. Gate Exact harvesting and Negative keyword actions on evidence that the displayed string maps to the intended keyword control.
5. When origin/control mapping is unresolved, prefer `Directional`, `Hold`, or `Manual Review` over action-safe negative/harvest recommendations.

## Copyright / license handling

Amazon Ads help pages are public vendor documentation, not open-source code licensed for redistribution. This repository uses only factual platform behavior and independently written diagnostic/safety methodology. No Amazon prose, screenshots, schemas, prompts, or proprietary implementation are copied.
