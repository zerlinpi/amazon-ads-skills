#!/usr/bin/env python3
"""Read-only Global SP receipt-to-marketplace-readback evidence gate.

This consumes a connector-normalized *single-item* Global Sponsored Products
campaign update and subsequent query evidence. It never sends Ads API requests,
retries writes, or infers effective state from delivery status.
"""
from __future__ import annotations

import json
import re
import sys
from decimal import Decimal
from typing import Any

from scripts.compare_control_state import _rfc3339_instant

STATES = {"ENABLED", "PAUSED", "ARCHIVED"}
# Country codes enumerated in Amazon's Global Sponsored Products API guide
# (verified 2026-10-24). Unsupported/new codes fail closed until reviewed;
# this is a versioned platform eligibility assertion, not an ISO-3166 catalog.
SUPPORTED_GLOBAL_SP_MARKETPLACES = frozenset({
    "AE", "AU", "BE", "BR", "CA", "DE", "EG", "ES", "FR", "GB", "IN",
    "IT", "JP", "MX", "NL", "PL", "SA", "SE", "SG", "TR", "US",
})


def _result(status: str, reason: str, mismatched: list[str] | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {"application_status": status, "reasons": [reason]}
    if mismatched is not None:
        result["mismatched_marketplaces"] = mismatched
    return result


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


# Repository-owned provenance labels, not Amazon-native ID formats. Match
# whole normalized placeholders only; a real ID may contain "unknown".
_UNAVAILABLE_IDENTITIES = {
    "unknown", "unsupported", "partial", "missing", "unavailable",
    "not available", "not supported",
}


def _concrete_identity(value: Any) -> bool:
    if not _nonempty(value) or value != value.strip():
        return False
    label = " ".join(value.casefold().replace("_", " ").replace("-", " ").split())
    return label not in _UNAVAILABLE_IDENTITIES


def _monetary_amount(value: Any) -> Decimal | None:
    """Require a finite, nonnegative plain decimal *string*, never a JSON float.

    The trusted adapter must preserve source precision when normalizing API
    numeric values. No FX conversion or inferred missing/zero budget occurs here.
    """
    if not isinstance(value, str) or re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", value) is None:
        return None
    return Decimal(value)


def _marketplace_identity_issue(
    readback: dict[str, Any],
    markets: list[str],
    state_rows: list[dict[str, Any]],
    budget_rows: list[dict[str, Any]] | None = None,
) -> str | None:
    """Bind optional raw marketplace IDs to normalized country codes.

    Raw marketplace IDs (for example in query status marketplace settings)
    are not ISO country codes. An external adapter may assert a sourced
    one-to-one crosswalk; this verifies internal evidence consistency only,
    not the independent authenticity of the adapter or its mapping source.
    Legacy normalized country-code-only envelopes remain compatible.
    """
    rows = state_rows + (budget_rows if budget_rows is not None else [])
    if ("marketplace_identity_map" not in readback
            and not any("marketplace_id" in row for row in rows)):
        return None
    entries = readback.get("marketplace_identity_map")
    if not isinstance(entries, list) or not entries:
        return "raw marketplace identity requires an explicit verified crosswalk"
    crosswalk: dict[str, str] = {}
    raw_ids: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            return "marketplace identity crosswalk entry is malformed"
        country, raw_id = entry.get("marketplace"), entry.get("marketplace_id")
        if not _concrete_identity(country) or not _concrete_identity(raw_id):
            return "marketplace identity crosswalk has missing identifiers"
        if entry.get("evidence_status") != "verified":
            return "marketplace identity crosswalk is not verified"
        source = entry.get("source")
        if (not isinstance(source, dict)
                or any(not _concrete_identity(source.get(key)) for key in
                       ("source_system", "acquisition_channel", "connector_id"))):
            return "marketplace identity crosswalk source lineage is unverified"
        if country in crosswalk or raw_id in raw_ids:
            return "marketplace identity crosswalk is not one-to-one"
        crosswalk[country] = raw_id
        raw_ids.add(raw_id)
    if set(crosswalk) != set(markets):
        return "marketplace identity crosswalk does not cover requested scope"
    for row in rows:
        country = row["marketplace"]
        if row.get("marketplace_id") != crosswalk.get(country):
            return f"marketplace {country} raw identity does not bind to country code"
    return None




def _query_request_binding_issue(
    query: dict[str, Any],
    pages: list[dict[str, Any]],
    request: dict[str, Any],
) -> str | None:
    """Cross-check optional adapter-retained query filters against each page request.

    This is a narrow single-campaign query contract, not a reconstruction of
    arbitrary Amazon Ads API filters or independent authentication of HTTP.
    A fingerprint alone is an external assertion, never proof of raw filters.
    """
    has_filters = "request_filters" in query
    if not has_filters:
        if any("request_body" in page for page in pages):
            return "query page request bodies have no declared filter binding"
        return None  # Legacy fingerprint-only adapters remain compatible.

    filters = query["request_filters"]
    required = {
        "adProductFilter": "SPONSORED_PRODUCTS",
        "marketplaceScopeFilter": "GLOBAL",
        "campaignIdFilter": request["campaign_id"],
    }
    if not isinstance(filters, dict) or set(filters) not in (
        set(required), set(required) | {"maxResults"}
    ):
        return "query request filters are missing, unsupported or ambiguous"
    for name, expected in required.items():
        value = filters.get(name)
        if (not isinstance(value, dict) or set(value) != {"include"}
                or value["include"] != [expected]):
            return f"query {name} does not uniquely select intended campaign scope"
    if "maxResults" in filters and (
        type(filters["maxResults"]) is not int or filters["maxResults"] <= 0
    ):
        return "query maxResults is not a positive integer"

    for index, page in enumerate(pages):
        body = page.get("request_body")
        if not isinstance(body, dict):
            return f"query page {index} has no verifiable request body"
        # The first native query may omit nextToken or explicitly send null.
        # Every continuation page must carry the exact preceding nextToken.
        expected_body = dict(filters)
        token = page["request_token"]
        if token is not None:
            expected_body["nextToken"] = token
        elif "nextToken" in body and body["nextToken"] is None:
            expected_body["nextToken"] = None
        if body != expected_body:
            return f"query page {index} request filters or nextToken contradict trace"
    return None


def _pagination_trace_issue(
    readback: dict[str, Any],
    request: dict[str, Any],
    source: dict[str, str],
    completed: Any,
    observed: Any,
) -> str | None:
    """Validate an optional adapter-retained query nextToken chain.

    This only detects internal contradictions. The external adapter remains
    responsible for raw API authenticity, result coverage and filter capture.
    """
    if "pagination_trace" not in readback:
        return None
    trace = readback["pagination_trace"]
    if not isinstance(trace, dict):
        return "query pagination trace is malformed"
    query, pages = trace.get("query"), trace.get("pages")
    if not isinstance(query, dict) or not isinstance(pages, list) or not pages:
        return "query pagination trace has missing query identity or pages"
    if (query.get("global_account_id") != request["global_account_id"]
            or query.get("campaign_id") != request["campaign_id"]
            or query.get("ad_product") != "SPONSORED_PRODUCTS"
            or query.get("marketplace_scope") != "GLOBAL"
            or not _nonempty(query.get("query_fingerprint"))):
        return "query pagination trace identity or filter fingerprint is unverified"
    # The query-level source is optional for older adapters, but an explicitly
    # supplied declaration must not contradict the page/envelope lineage.
    if "source" in query and query["source"] != source:
        return "query pagination query source contradicts readback envelope"

    expected_token: str | None = None
    seen_tokens: set[str] = set()
    previous_observed = None
    for index, page in enumerate(pages):
        if not isinstance(page, dict):
            return "query pagination page is malformed"
        if "request_token" not in page or "next_token" not in page:
            return "query pagination page has missing token evidence"
        incoming, outgoing = page["request_token"], page["next_token"]
        if (incoming is not None and not _nonempty(incoming)
                or outgoing is not None and not _nonempty(outgoing)):
            return "query pagination token is malformed"
        if incoming != expected_token:
            return "query pagination continuation token does not bind to prior page"
        if outgoing is not None:
            if outgoing in seen_tokens:
                return "query pagination continuation token repeats"
            seen_tokens.add(outgoing)
        if index < len(pages) - 1 and outgoing is None:
            return "query pagination trace continues after a terminal page"
        if index == len(pages) - 1 and outgoing is not None:
            return "query pagination trace has no terminal page"
        if (page.get("global_account_id") != request["global_account_id"]
                or page.get("campaign_id") != request["campaign_id"]
                or page.get("query_fingerprint") != query["query_fingerprint"]
                or page.get("source") != source):
            return "query pagination page identity, filters or source contradict envelope"
        page_time = _rfc3339_instant(page.get("observed_at"))
        if (page_time is None or page_time <= completed or page_time > observed
                or previous_observed is not None and page_time < previous_observed):
            return "query pagination page observation time is inconsistent"
        previous_observed = page_time
        expected_token = outgoing
    return _query_request_binding_issue(query, pages, request)



def _native_campaign_page_provenance_issue(
    readback: dict[str, Any],
    request: dict[str, Any],
) -> str | None:
    """Bind two explicitly supplied evidence surfaces to one query page.

    The trusted adapter asserts provenance; this only checks internal
    consistency, not native HTTP authenticity or completeness of results.
    """
    has_native = "raw_campaign" in readback
    has_trace = "pagination_trace" in readback
    has_binding = "raw_campaign_provenance" in readback
    if not has_native and not has_binding:
        return None
    if not has_trace and not has_binding:
        return None  # Legacy native-only envelope is still supported.
    if not has_native or not has_trace or not has_binding:
        return "native campaign and query pagination evidence lack a shared page binding"
    binding = readback["raw_campaign_provenance"]
    trace = readback["pagination_trace"]
    if not isinstance(binding, dict) or not isinstance(trace, dict):
        return "native campaign page provenance is malformed"
    pages, query = trace.get("pages"), trace.get("query")
    page_index = binding.get("page_index")
    if (not isinstance(pages, list) or not isinstance(query, dict)
            or type(page_index) is not int or page_index < 0 or page_index >= len(pages)):
        return "native campaign page index is missing or outside query trace"
    page = pages[page_index]
    if not isinstance(page, dict):
        return "native campaign source page is malformed"
    if (binding.get("global_account_id") != request["global_account_id"]
            or binding.get("campaign_id") != request["campaign_id"]
            or not _nonempty(binding.get("query_fingerprint"))
            or binding["query_fingerprint"] != query.get("query_fingerprint")):
        return "native campaign page identity or query filters contradict trace"
    if (not isinstance(binding.get("source"), dict)
            or binding["source"] != page.get("source")
            or binding["source"] != readback.get("source")):
        return "native campaign source does not bind to query page"
    binding_time = _rfc3339_instant(binding.get("observed_at"))
    page_time = _rfc3339_instant(page.get("observed_at"))
    if binding_time is None or page_time is None or binding_time != page_time:
        return "native campaign observation time does not bind to query page"
    return None



def _native_campaign_response_membership_issue(
    readback: dict[str, Any],
    request: dict[str, Any],
) -> str | None:
    """Check opt-in retained query responses against native campaign provenance.

    A page-index/source assertion alone does not prove that a retained native
    campaign was in that page's response. This compares trusted adapter copies;
    it does not authenticate HTTP or certify omitted results.
    """
    trace = readback.get("pagination_trace")
    if not isinstance(trace, dict):
        return None  # Existing trace/provenance validators handle this.
    pages = trace.get("pages")
    if not isinstance(pages, list) or not pages:
        return None
    if not any(isinstance(page, dict) and "response_body" in page for page in pages):
        return None  # Legacy page metadata remains compatible.

    native = readback.get("raw_campaign")
    binding = readback.get("raw_campaign_provenance")
    if not isinstance(native, dict) or not isinstance(binding, dict):
        return "native query response evidence lacks a bound campaign snapshot"
    claimed_index = binding.get("page_index")
    if type(claimed_index) is not int or not 0 <= claimed_index < len(pages):
        return "native query response page index is invalid"

    found_on: list[int] = []
    for index, page in enumerate(pages):
        if not isinstance(page, dict):
            return "native query response page metadata is malformed"
        body = page.get("response_body")
        if (not isinstance(body, dict) or "campaigns" not in body
                or "nextToken" not in body
                or body["nextToken"] != page.get("next_token")
                or not isinstance(body["campaigns"], list)):
            return f"native query response page {index} is missing or inconsistent"
        for campaign in body["campaigns"]:
            if (not isinstance(campaign, dict)
                    or campaign.get("campaignId") != request["campaign_id"]):
                return f"native query response page {index} has an unexpected campaign"
            found_on.append(index)
            if campaign != native:
                return f"native query response page {index} contradicts retained campaign"
    if found_on != [claimed_index]:
        return "native campaign is absent, duplicated or on a different query page"
    return None



def _native_campaign_config_issue(
    readback: dict[str, Any],
    request: dict[str, Any],
    markets: list[str],
    actual: dict[str, str],
) -> str | None:
    """Cross-check explicitly retained native query configuration, if supplied.

    The trusted adapter still authenticates the source and query completion.
    This checks that the retained campaign resource cannot contradict its
    normalized per-marketplace configured-state assertions. Delivery status
    is deliberately not used to derive configured state.
    """
    if "raw_campaign" not in readback:
        return None
    native = readback["raw_campaign"]
    if not isinstance(native, dict):
        return "retained native campaign query resource is malformed"
    if native.get("campaignId") != request["campaign_id"]:
        return "native campaign identity contradicts request"
    for alias in ("globalAccountId", "global_account_id", "campaign_id"):
        if alias in native:
            expected = request["campaign_id"] if alias == "campaign_id" else request["global_account_id"]
            if native[alias] != expected:
                return f"native campaign {alias} contradicts request"
    if native.get("adProduct") != "SPONSORED_PRODUCTS" or native.get("marketplaceScope") != "GLOBAL":
        return "native campaign product or scope is not Global Sponsored Products"
    native_markets = native.get("marketplaces")
    if (not isinstance(native_markets, list)
            or any(not _nonempty(m) for m in native_markets)
            or len(set(native_markets)) != len(native_markets)
            or set(native_markets) != set(markets)):
        return "native campaign marketplace scope is missing, duplicated or contradictory"
    global_state = native.get("state")
    if not isinstance(global_state, str) or global_state not in STATES:
        return "native campaign configured global state is missing or unsupported"
    configurations = native.get("marketplaceConfigurations")
    if not isinstance(configurations, list):
        return "native campaign marketplace configurations are not a complete list"
    overrides: dict[str, str] = {}
    seen: set[str] = set()
    for config in configurations:
        if not isinstance(config, dict) or not _nonempty(config.get("marketplace")):
            return "native campaign marketplace configuration is malformed"
        market = config["marketplace"]
        if market not in actual or market in seen:
            return "native campaign marketplace configuration is duplicated or out of scope"
        seen.add(market)
        values = config.get("overrides")
        if not isinstance(values, dict):
            return f"native campaign {market} overrides are malformed"
        if "state" in values:
            state = values["state"]
            if not isinstance(state, str) or state not in STATES:
                return f"native campaign {market} override state is unsupported"
            overrides[market] = state
    for market in markets:
        if actual[market] != overrides.get(market, global_state):
            return f"native campaign {market} configured state contradicts normalized readback"
    return None



def _native_campaign_budget_issue(
    readback: dict[str, Any],
    request: dict[str, Any],
    markets: list[str],
    normalized: dict[str, dict[str, Any]],
) -> str | None:
    """Check retained native campaign budgets against independently normalized rows.

    Only the supported daily monetary budget is compared. Native numeric
    lexemes must be retained as decimal text by the trusted adapter: a JSON
    float cannot prove original precision. This is not HTTP authentication.
    """
    native = readback.get("raw_campaign")
    if not isinstance(native, dict) or "budgets" not in native:
        return None  # Legacy normalized-only/native-state-only envelopes.
    budgets = native["budgets"]
    if not isinstance(budgets, list) or len(budgets) != 1 or not isinstance(budgets[0], dict):
        return "native campaign monetary budgets are missing, ambiguous or malformed"
    budget = budgets[0]
    if budget.get("budgetType") != "MONETARY" or budget.get("recurrenceTimePeriod") != "DAILY":
        return "native campaign budget type or recurrence is unsupported"
    value = budget.get("budgetValue")
    if not isinstance(value, dict):
        return "native campaign budget value is malformed"
    monetary = value.get("monetaryBudgetValue")
    if not isinstance(monetary, dict):
        return "native campaign monetary budget value is malformed"
    settings = monetary.get("marketplaceSettings")
    if not isinstance(settings, list):
        return "native campaign monetary marketplace settings are missing"
    actual: dict[str, tuple[str, Decimal]] = {}
    for entry in settings:
        if not isinstance(entry, dict) or not _nonempty(entry.get("marketplace")):
            return "native campaign monetary marketplace entry is malformed"
        market = entry["marketplace"]
        if market not in markets or market in actual:
            return "native campaign monetary marketplace is duplicated or out of scope"
        amount = entry.get("monetaryBudget")
        if not isinstance(amount, dict):
            return f"native campaign {market} monetary budget is malformed"
        currency = amount.get("currencyCode")
        decimal = _monetary_amount(amount.get("value"))
        if (not isinstance(currency, str)
                or re.fullmatch(r"[A-Z]{3}", currency) is None
                or decimal is None):
            return f"native campaign {market} monetary currency or exact amount is unverified"
        actual[market] = (currency, decimal)
    if set(actual) != set(markets):
        return "native campaign monetary marketplace coverage is incomplete"
    for market in markets:
        row = normalized[market]
        if (actual[market][0] != row["currency_code"]
                or actual[market][1] != _monetary_amount(row["amount"])
                or row["budget_type"] != "MONETARY"
                or row["recurrence"] != "DAILY"):
            return f"native campaign {market} monetary budget contradicts normalized readback"
    return None


def evaluate_global_sp_readback(evidence: Any) -> dict[str, Any]:
    """Classify one Global SP campaign update without equating HTTP 207 to application.

    Caller must normalize each marketplace's *configured effective state* from
    source-supported Global SP query fields and explicit overrides. This gate
    does not accept deliveryStatus as a substitute for configured state.
    """
    unknown = lambda message: _result("Unknown", message)
    if not isinstance(evidence, dict):
        return unknown("application evidence must be an object")
    request, receipt = evidence.get("request"), evidence.get("receipt")
    if not isinstance(request, dict) or not isinstance(receipt, dict):
        return unknown("request and HTTP receipt must be objects")

    for key in ("global_account_id", "campaign_id"):
        if not _concrete_identity(request.get(key)):
            return unknown(f"request has missing or unavailable {key}")
    if "request_id" in request and not _concrete_identity(request["request_id"]):
        return unknown("request_id is not a concrete correlation identity")
    markets = request.get("marketplaces")
    expected = request.get("expected_effective_states")
    if (not isinstance(markets, list) or not markets
            or any(not isinstance(m, str) or m not in SUPPORTED_GLOBAL_SP_MARKETPLACES
                   for m in markets)
            or len(set(markets)) != len(markets)):
        return unknown("request marketplaces must be distinct supported Global SP country codes")
    if (not isinstance(expected, dict) or set(expected) != set(markets)
            or any(not isinstance(value, str) or value not in STATES for value in expected.values())):
        return unknown("expected effective states must cover every requested marketplace")
    completed = _rfc3339_instant(request.get("completed_at"))
    if completed is None:
        return unknown("request completed_at is not a verified instant")

    if type(receipt.get("http_status")) is not int or receipt["http_status"] != 207:
        return unknown("HTTP response is not a verified Global SP 207 multi-status receipt")
    receipt_indices: list[int] = []
    for group in ("success", "error", "partialSuccess"):
        entries = receipt.get(group)
        if not isinstance(entries, list):
            return unknown(f"receipt {group} array is missing")
        for entry in entries:
            if (not isinstance(entry, dict)
                    or type(entry.get("index")) is not int):
                return unknown(f"receipt {group} has invalid request index")
            receipt_indices.append(entry["index"])
    # Explicitly single-item. Never interpret a subset of a multi-item batch
    # as complete application of the whole batch.
    if receipt_indices != [0]:
        return unknown("receipt indices do not uniquely cover one request item")
    if receipt.get("error") or receipt.get("partialSuccess"):
        return _result("Partial", "Global SP 207 contains error or partialSuccess; application is not fully confirmed")
    if len(receipt["success"]) != 1:
        return unknown("Global SP receipt lacks an unambiguous success for request index 0")

    # HTTP 207 is an indexed write receipt, not a query. A trusted adapter
    # may preserve explicit request/resource identities at either level.
    # If supplied, they must bind to THIS campaign before an independent
    # query can confirm the intended update. Native campaignId and normalized
    # campaign_id aliases are both checked; a conflicting alias is not ignored.
    if "resource_type" in receipt and receipt["resource_type"] != "campaign":
        return unknown("receipt resource type contradicts campaign update")
    for field in ("request_id", "global_account_id", "campaign_id"):
        if field in receipt and (
            not _nonempty(request.get(field)) or receipt[field] != request[field]
        ):
            return unknown(f"receipt {field} contradicts or cannot bind to request")
    success_item = receipt["success"][0]
    for field in ("request_id", "global_account_id", "campaign_id"):
        if field in success_item and (
            not _nonempty(request.get(field)) or success_item[field] != request[field]
        ):
            return unknown(f"receipt success {field} contradicts or cannot bind to request")
    if "campaign" in success_item:
        returned = success_item["campaign"]
        if not isinstance(returned, dict):
            return unknown("receipt campaign resource is malformed")
        if not any(alias in returned for alias in ("campaignId", "campaign_id")):
            return unknown("receipt campaign resource has no campaign identity")
        for alias in ("campaignId", "campaign_id"):
            if alias in returned and returned[alias] != request["campaign_id"]:
                return unknown(f"receipt campaign {alias} contradicts request")
        for alias in ("globalAccountId", "global_account_id"):
            if alias in returned and returned[alias] != request["global_account_id"]:
                return unknown(f"receipt campaign {alias} contradicts global account")

    # This is a CAMPAIGN configured-state / optional daily-budget gate, not
    # an ad-group, target, placement or general-purpose write reconciler.
    # Future normalized expected_* intent must be explicitly supported before
    # this helper can claim that the *whole intended change* was confirmed.
    supported_intent = {"expected_effective_states", "expected_marketplace_budgets"}
    unsupported_intent = sorted(
        key for key in request if key.startswith("expected_") and key not in supported_intent
    )
    if unsupported_intent:
        return unknown("unverified request intent: " + ", ".join(unsupported_intent))

    readback = evidence.get("readback")
    if not isinstance(readback, dict):
        return unknown("successful receipt is not post-write readback")
    for key in ("global_account_id", "campaign_id"):
        if not _nonempty(readback.get(key)) or readback[key] != request[key]:
            return unknown(f"readback {key} identity is missing or mismatched")
    source = readback.get("source")
    if (not isinstance(source, dict)
            or any(not _concrete_identity(source.get(k)) for k in
                   ("source_system", "acquisition_channel", "connector_id"))):
        return unknown("readback source and connector lineage are unverified")
    observed = _rfc3339_instant(readback.get("observed_at"))
    if observed is None or observed <= completed:
        return unknown("readback must be observed after request completion")
    for field, required in (("coverage_status", "Complete"),
                            ("pagination_status", "Complete"),
                            ("capability_status", "Supported")):
        if readback.get(field) != required:
            return unknown(f"readback {field} is not {required}")

    pagination_issue = _pagination_trace_issue(readback, request, source, completed, observed)
    if pagination_issue is not None:
        return unknown(pagination_issue)

    native_page_issue = _native_campaign_page_provenance_issue(readback, request)
    if native_page_issue is not None:
        return unknown(native_page_issue)

    response_membership_issue = _native_campaign_response_membership_issue(readback, request)
    if response_membership_issue is not None:
        return unknown(response_membership_issue)

    rows = readback.get("marketplace_states")
    if not isinstance(rows, list):
        return unknown("readback marketplace_states must be an explicit list")
    actual: dict[str, str] = {}
    for row in rows:
        if not isinstance(row, dict) or not _nonempty(row.get("marketplace")):
            return unknown("readback has an invalid marketplace identity")
        market = row["marketplace"]
        if market in actual:
            return unknown(f"readback duplicate marketplace: {market}")
        if row.get("evidence_status") != "observed":
            return unknown(f"readback {market} effective state is not observed")
        # Optional state-row lineage, like budget-row lineage, must not
        # contradict the trusted envelope or the original request.
        for identity in ("global_account_id", "campaign_id"):
            if identity in row and row[identity] != request[identity]:
                return unknown(f"readback {market} state {identity} contradicts request")
        if "source" in row:
            row_source = row["source"]
            if (not isinstance(row_source, dict)
                    or any(row_source.get(key) != source[key] for key in
                           ("source_system", "acquisition_channel", "connector_id"))):
                return unknown(f"readback {market} state source contradicts envelope")
        if "observed_at" in row:
            row_observed = _rfc3339_instant(row["observed_at"])
            if row_observed is None or row_observed <= completed or row_observed > observed:
                return unknown(f"readback {market} state observation time is inconsistent")
        state = row.get("effective_state")
        if not isinstance(state, str) or state not in STATES:
            return unknown(f"readback {market} effective configured state is missing or unsupported")
        actual[market] = state
    if set(actual) != set(markets):
        return unknown("readback marketplace coverage differs from requested marketplace scope")
    native_issue = _native_campaign_config_issue(readback, request, markets, actual)
    if native_issue is not None:
        return unknown(native_issue)
    identity_issue = _marketplace_identity_issue(readback, markets, rows)
    if identity_issue is not None:
        return unknown(identity_issue)

    budget_mismatched: set[str] = set()
    # Optional, independently evidenced monetary-budget comparison. A state
    # readback capability is NOT proof of budget visibility or completeness.
    if "expected_marketplace_budgets" in request:
        expected_budgets = request["expected_marketplace_budgets"]
        if not isinstance(expected_budgets, dict) or set(expected_budgets) != set(markets):
            return unknown("expected monetary budgets must cover every requested marketplace")
        for market, budget in expected_budgets.items():
            if (not isinstance(budget, dict)
                    or not isinstance(budget.get("currency_code"), str)
                    or re.fullmatch(r"[A-Z]{3}", budget["currency_code"]) is None
                    or budget.get("budget_type") != "MONETARY"
                    or budget.get("recurrence") != "DAILY"
                    or _monetary_amount(budget.get("amount")) is None):
                return unknown(f"request {market} monetary budget identity or amount is unsupported")
        for field, required in (("budget_coverage_status", "Complete"),
                                ("budget_pagination_status", "Complete"),
                                ("budget_capability_status", "Supported")):
            if readback.get(field) != required:
                return unknown(f"readback {field} is not {required}")
        budget_rows = readback.get("marketplace_budgets")
        if not isinstance(budget_rows, list):
            return unknown("readback marketplace_budgets must be an explicit list")
        actual_budgets: dict[str, dict[str, Any]] = {}
        for row in budget_rows:
            if not isinstance(row, dict) or not _nonempty(row.get("marketplace")):
                return unknown("readback has an invalid budget marketplace identity")
            market = row["marketplace"]
            if market in actual_budgets:
                return unknown(f"readback duplicate budget marketplace: {market}")
            if row.get("evidence_status") != "observed":
                return unknown(f"readback {market} monetary budget is not observed")
            # Optional row-level lineage must not contradict the trusted
            # readback envelope. Absent row metadata inherits the envelope's
            # assertion; explicitly stale or cross-source rows fail closed.
            for identity in ("global_account_id", "campaign_id"):
                if identity in row and row[identity] != request[identity]:
                    return unknown(f"readback {market} budget {identity} contradicts request")
            if "source" in row:
                row_source = row["source"]
                if (not isinstance(row_source, dict)
                        or any(row_source.get(key) != source[key] for key in
                               ("source_system", "acquisition_channel", "connector_id"))):
                    return unknown(f"readback {market} budget source contradicts envelope")
            if "observed_at" in row:
                row_observed = _rfc3339_instant(row["observed_at"])
                if row_observed is None or row_observed <= completed or row_observed > observed:
                    return unknown(f"readback {market} budget observation time is inconsistent")
            if (not isinstance(row.get("currency_code"), str)
                    or re.fullmatch(r"[A-Z]{3}", row["currency_code"]) is None
                    or not _nonempty(row.get("budget_type"))
                    or not _nonempty(row.get("recurrence"))
                    or _monetary_amount(row.get("amount")) is None):
                return unknown(f"readback {market} monetary budget identity or amount is unverified")
            actual_budgets[market] = row
        if set(actual_budgets) != set(markets):
            return unknown("readback monetary budget coverage differs from requested marketplace scope")
        native_budget_issue = _native_campaign_budget_issue(readback, request, markets, actual_budgets)
        if native_budget_issue is not None:
            return unknown(native_budget_issue)
        identity_issue = _marketplace_identity_issue(readback, markets, rows, budget_rows)
        if identity_issue is not None:
            return unknown(identity_issue)
        for market in markets:
            desired, observed_budget = expected_budgets[market], actual_budgets[market]
            if (desired["currency_code"] != observed_budget["currency_code"]
                    or desired["budget_type"] != observed_budget["budget_type"]
                    or desired["recurrence"] != observed_budget["recurrence"]
                    or _monetary_amount(desired["amount"]) != _monetary_amount(observed_budget["amount"])):
                budget_mismatched.add(market)

    mismatched = sorted({m for m in markets if actual[m] != expected[m]} | budget_mismatched)
    if mismatched:
        if budget_mismatched:
            return _result("Drifted", "observed marketplace configured state or monetary budget differs from intended state", mismatched)
        return _result("Drifted", "observed marketplace configured state differs from intended state", mismatched)
    if "expected_marketplace_budgets" in request:
        return _result("Confirmed", "complete per-marketplace configured-state and monetary-budget readback agree")
    return _result("Confirmed", "single-item 207 success and complete post-write marketplace configured-state readback agree")


def main() -> None:
    evidence = json.load(sys.stdin)
    print(json.dumps(evaluate_global_sp_readback(evidence), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
