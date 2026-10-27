#!/usr/bin/env python3
"""Deterministically compare two read-only control-state snapshots.

This helper classifies evidence; it never authorizes or performs Amazon Ads writes.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any

VALID_EVIDENCE = {"observed", "derived"}
REGISTRY_PATH = Path(__file__).resolve().parents[1] / "references" / "control-requirement-registry.json"


ACCOUNT_ID_FIELDS = (
    "global_advertiser_account_id",
    "regional_advertiser_account_id",
    "legacy_advertiser_account_id",
    "advertiser_account_id",
    "regional_profile_id",
)
ACCOUNT_CONTEXT_FIELDS = ("manager_account_id", "country_code")
UNUSABLE_IDENTITY_LABELS = {
    "unknown", "unsupported", "partial", "missing", "unavailable",
    "not_available", "not_supported", "not_applicable", "n/a",
}


def _unusable_identity_label(value: Any) -> bool:
    """Reject reserved evidence labels, not real observed identity strings."""
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        return True
    return re.sub(r"[\s-]+", "_", value.casefold()) in UNUSABLE_IDENTITY_LABELS


def _scope_identity_problem(bscope: Any, pscope: Any) -> str | None:
    """Compare explicit account identities without inventing global/profile mappings."""
    if not isinstance(bscope, dict) or not isinstance(pscope, dict):
        return "decision scope must be an object"
    if (
        _unusable_identity_label(bscope.get("marketplace_id"))
        or _unusable_identity_label(pscope.get("marketplace_id"))
        or bscope["marketplace_id"] != pscope["marketplace_id"]
    ):
        return "scope mismatch or missing/unknown marketplace_id"

    # Optional scope identities must not become valid simply because the
    # same unavailable label appears in both observations.
    for field in ("campaign_id", "ad_group_id", "entity_id", "entity_type"):
        for scope in (bscope, pscope):
            if scope.get(field) is not None and _unusable_identity_label(scope[field]):
                return f"decision-scope {field} is missing or unknown"

    before_profile, after_profile = bscope.get("profile_id"), pscope.get("profile_id")
    if before_profile is not None or after_profile is not None:
        if (
            _unusable_identity_label(before_profile)
            or _unusable_identity_label(after_profile)
            or before_profile != after_profile
        ):
            return "scope mismatch or missing/unknown profile_id"

    before_explicit = "account_identity" in bscope
    after_explicit = "account_identity" in pscope
    if before_explicit != after_explicit:
        return "account identity envelope is present on only one side"

    if not before_explicit:
        if not before_profile:
            return "scope missing profile_id and global advertiser identity"
        return None

    before_identity, after_identity = bscope["account_identity"], pscope["account_identity"]
    if not isinstance(before_identity, dict) or not isinstance(after_identity, dict):
        return "account identity envelope is malformed"

    shared_strong = False
    for field in (*ACCOUNT_ID_FIELDS, *ACCOUNT_CONTEXT_FIELDS):
        before_value, after_value = before_identity.get(field), after_identity.get(field)
        if before_value is None and after_value is None:
            continue
        if (
            _unusable_identity_label(before_value)
            or _unusable_identity_label(after_value)
            or before_value != after_value
        ):
            return f"account identity mismatch or missing {field}"
        if field in ACCOUNT_ID_FIELDS:
            shared_strong = True

    if not shared_strong:
        return "account identity lacks a shared strong advertiser/profile identifier"
    if not before_profile and not before_identity.get("global_advertiser_account_id"):
        return "profile-less Global SP scope lacks global advertiser account identity"
    return None



def _source_lineage_problem(bsource: Any, psource: Any) -> str | None:
    """Do not infer equivalence across absent or differently acquired control evidence.

    readback_id identifies individual observations and may legitimately change.
    This envelope has no verified cross-source mapping contract, so a mismatch
    in source/acquisition/connector identity cannot be silently accepted.
    """
    if not isinstance(bsource, dict) or not isinstance(psource, dict):
        return "control-state source provenance must be an object on both sides"
    for field in ("source_system", "acquisition_channel"):
        before, after = bsource.get(field), psource.get(field)
        if (
            _unusable_identity_label(before)
            or _unusable_identity_label(after)
            or before != after
        ):
            return f"control-state source provenance missing or changed for {field}"
    # A supplied readback ID must identify a concrete observation. An
    # unavailable label is not independent provenance, even when the two
    # snapshots otherwise have complete material-control inventories.
    # Null/omitted IDs remain compatible with legacy optional evidence.
    for side, source in (("baseline", bsource), ("post", psource)):
        readback = source.get("readback_id")
        if readback is not None and (
            _unusable_identity_label(readback)
            or re.sub(r"[\s-]+", "_", readback.casefold()) in {"not_applicable", "n/a"}
        ):
            return f"{side} control-state source readback_id is missing or unknown"
    before_connector, after_connector = bsource.get("connector_id"), psource.get("connector_id")
    if before_connector is None and after_connector is None:
        return None
    if (
        _unusable_identity_label(before_connector)
        or _unusable_identity_label(after_connector)
        or before_connector != after_connector
    ):
        return "control-state source provenance missing or changed for connector_id"
    return None


def _rfc3339_instant(value: Any) -> tuple[datetime, Decimal] | None:
    """Parse an explicit UTC instant, retaining fractions beyond microseconds."""
    if not isinstance(value, str) or value.endswith("-00:00"):
        return None
    match = re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.(?P<fraction>\d+))?(?:Z|[+-](?:[01]\d|2[0-3]):[0-5]\d)",
        value,
    )
    if match is None:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return (
        parsed.astimezone(timezone.utc).replace(microsecond=0),
        Decimal("0." + (match.group("fraction") or "0")),
    )



def _same_transition_provenance(before: Any, after: Any) -> bool:
    """One readback cannot assert two incompatible transition histories.

    Provenance is optional; absent/null on both sides is legacy-compatible.
    When supplied, preserve exact actor/mode/status/reason evidence and compare
    transition timestamps as UTC instants with full fractional precision.
    """
    if before is None or after is None:
        return before is None and after is None
    if not isinstance(before, dict) or not isinstance(after, dict):
        return False
    if before.keys() != after.keys():
        return False
    for field in before:
        if field == "transition_observed_at":
            left, right = before[field], after[field]
            if left is None or right is None:
                if left is not None or right is not None:
                    return False
            else:
                left_instant = _rfc3339_instant(left)
                right_instant = _rfc3339_instant(right)
                if left_instant is None or right_instant is None or left_instant != right_instant:
                    return False
        elif not _json_state_equal(before[field], after[field]):
            return False
    return True



def _control_map(snapshot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["control_type"]: item for item in snapshot.get("controls", [])}


def _json_state_equal(before: Any, after: Any) -> bool:
    """Compare JSON states without Python's bool/int equality aliasing.

    JSON booleans are distinct from numbers even though False == 0 and
    True == 1 in Python. Preserve normal numeric equality (0 == 0.0),
    and apply the distinction inside nested objects and arrays.
    """
    if isinstance(before, bool) or isinstance(after, bool):
        return type(before) is type(after) and before == after
    if isinstance(before, dict) and isinstance(after, dict):
        return before.keys() == after.keys() and all(
            _json_state_equal(before[key], after[key]) for key in before
        )
    if isinstance(before, list) and isinstance(after, list):
        return len(before) == len(after) and all(
            _json_state_equal(left, right) for left, right in zip(before, after)
        )
    return before == after



def _sp_rule_state_equal(control_type: str, before: Any, after: Any) -> bool:
    """Compare identity-keyed SP rule members independent of adapter row order.

    Call only after complete-collection and unique rule_id validation. This
    preserves exact member fields (including activation evidence), and does
    not infer rule execution continuity or reorder other material lists.
    """
    fields = {
        "schedule_or_event_rule": ("schedule_rules", "event_rules"),
        "budget_or_pacing": ("active_budget_rules",),
    }.get(control_type)
    if not fields or not isinstance(before, dict) or not isinstance(after, dict):
        return _json_state_equal(before, after)
    normalized_before, normalized_after = dict(before), dict(after)
    for field in fields:
        left, right = before.get(field), after.get(field)
        if isinstance(left, list) and isinstance(right, list):
            normalized_before[field] = sorted(left, key=lambda item: item["rule_id"])
            normalized_after[field] = sorted(right, key=lambda item: item["rule_id"])
    return _json_state_equal(normalized_before, normalized_after)


def _control_inventory_problem(snapshot: dict[str, Any], side: str) -> str | None:
    """Reject ambiguous or malformed control identities before mapping can overwrite them."""
    controls = snapshot.get("controls")
    if not isinstance(controls, list):
        return f"{side} controls must be a list"
    seen: set[str] = set()
    for index, item in enumerate(controls):
        if not isinstance(item, dict):
            return f"{side} control at index {index} is not an object"
        control_type = item.get("control_type")
        if not isinstance(control_type, str) or not control_type:
            return f"{side} control at index {index} lacks a valid control_type"
        if control_type in seen:
            return f"{side} duplicate control_type: {control_type}"
        seen.add(control_type)
    return None


def _registry_requirement(provenance: dict[str, Any]) -> tuple[set[str] | None, str | None]:
    registry_id = provenance.get("requirement_registry_id")
    surface = provenance.get("decision_surface")
    if not registry_id:
        return None, "material-control requirement registry identity is missing"
    try:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None, "material-control requirement registry is unavailable"
    if registry.get("registry_id") != registry_id:
        return None, "material-control requirement registry identity is unknown or stale"
    entry = registry.get("decision_surfaces", {}).get(surface)
    if not isinstance(entry, dict):
        return None, "decision surface is absent from the material-control requirement registry"
    required = entry.get("required_control_types")
    if not isinstance(required, list) or not required:
        return None, "registry requirement set is missing"
    return set(required), None


def _collection_problem(control: dict[str, Any], control_type: str, side: str) -> str | None:
    state = control.get("state")
    if not isinstance(state, list):
        return None
    evidence = control.get("collection_evidence")
    if not isinstance(evidence, dict):
        return f"{side} {control_type} collection lacks completeness evidence"
    expected = {"enumeration_status": "Complete", "pagination_status": "Complete", "capability_status": "Supported"}
    incomplete = [key for key, value in expected.items() if evidence.get(key) != value]
    if incomplete:
        return f"{side} {control_type} collection completeness is unproven: " + ", ".join(incomplete)
    return None


def _nested_collection_problem(control: dict[str, Any], control_type: str, field: str, side: str) -> str | None:
    state = control.get("state")
    if not isinstance(state, dict) or not isinstance(state.get(field), list):
        return None
    evidence_map = control.get("nested_collection_evidence")
    if not isinstance(evidence_map, dict):
        return f"{side} {control_type}.{field} collection lacks completeness evidence"
    evidence = evidence_map.get(field)
    if not isinstance(evidence, dict):
        return f"{side} {control_type}.{field} collection lacks completeness evidence"
    expected = {"enumeration_status": "Complete", "pagination_status": "Complete", "capability_status": "Supported"}
    incomplete = [key for key, value in expected.items() if evidence.get(key) != value]
    if incomplete:
        return f"{side} {control_type}.{field} collection completeness is unproven: " + ", ".join(incomplete)
    return None


def _deep_extra_collection_problem(
    control: dict[str, Any], control_type: str, side: str, *, strict_evidence: bool = False
) -> str | None:
    """Require independent evidence for lists below the first state-object level.

    Direct state fields retain legacy nested_collection_evidence keys; deeper
    list paths use JSON Pointer (RFC 6901), including array indices.
    """
    evidence_map = control.get("nested_collection_evidence")
    expected = {"enumeration_status": "Complete", "pagination_status": "Complete", "capability_status": "Supported"}
    proven_paths: set[str] = set()

    # Root-list completeness is checked by _collection_problem. Descendant
    # lists still require independent evidence, including list-in-list values.
    descendant_depth = 0 if isinstance(control.get("state"), list) else 1

    def walk(value: Any, pointer: str, depth: int) -> str | None:
        if isinstance(value, list):
            if depth > descendant_depth:
                proven_paths.add(pointer)
                evidence = evidence_map.get(pointer) if isinstance(evidence_map, dict) else None
                if not isinstance(evidence, dict):
                    return f"{side} {control_type}{pointer} collection lacks completeness evidence"
                if strict_evidence and set(evidence) != set(expected):
                    return f"{side} {control_type}{pointer} collection proof has unrecognized fields"
                incomplete = [key for key, required in expected.items() if evidence.get(key) != required]
                if incomplete:
                    return f"{side} {control_type}{pointer} collection completeness is unproven: " + ", ".join(incomplete)
            for index, child in enumerate(value):
                problem = walk(child, f"{pointer}/{index}", depth + 1)
                if problem:
                    return problem
        elif isinstance(value, dict):
            for field, child in value.items():
                escaped = str(field).replace("~", "~0").replace("/", "~1")
                problem = walk(child, f"{pointer}/{escaped}", depth + 1)
                if problem:
                    return problem
        return None

    problem = walk(control.get("state"), "", 0)
    if problem:
        return problem
    if strict_evidence:
        if not isinstance(evidence_map, dict):
            return f"{side} {control_type} descendant collection proof must be an object"
        extra_paths = set(evidence_map) - proven_paths
        if extra_paths:
            return f"{side} {control_type} descendant collection proof has unmapped pointers: " + ", ".join(sorted(extra_paths))
    return None


def _coverage_problem(snapshot: dict[str, Any], control_map: dict[str, dict[str, Any]], side: str) -> str | None:
    coverage = snapshot.get("coverage")
    if not isinstance(coverage, dict):
        return f"{side} material-control coverage is missing"
    if coverage.get("coverage_status") != "Complete":
        return f"{side} material-control coverage is not Complete"
    provenance = coverage.get("requirement_provenance")
    if not isinstance(provenance, dict) or provenance.get("derivation_status") != "Verified":
        return f"{side} material-control requirement provenance is not Verified"
    if not provenance.get("decision_surface"):
        return f"{side} material-control requirement decision surface is missing"
    registry_required, registry_problem = _registry_requirement(provenance)
    if registry_problem:
        return f"{side} {registry_problem}"
    required = coverage.get("required_control_types")
    if not isinstance(required, list) or not required:
        return f"{side} required material-control set is missing"
    if set(required) != registry_required:
        return f"{side} required material-control set does not match the versioned registry"
    missing = sorted(set(required) - set(control_map))
    if missing:
        return f"{side} required controls are not evidenced: " + ", ".join(missing)
    null_state = sorted(control_type for control_type in control_map if control_map[control_type].get("state") is None)
    if null_state:
        return f"{side} required controls have unknown state: " + ", ".join(null_state)
    for control_type in sorted(control_map):
        control = control_map[control_type]
        # Complete inventory and observed status cannot make an explicit
        # Unknown/Unsupported value (or non-finite JSON number) usable.
        state_problem = _explicit_material_state_problem(control.get("state"))
        if state_problem:
            return f"{side} {control_type} has invalid material state: {state_problem}"
        problem = _collection_problem(control, control_type, side)
        if problem:
            return problem
        # Every material control, including registry-required object states,
        # needs independent proof for its nested collections. A verified
        # registry requirement does not prove that a connector enumerated a
        # list inside the observed state.
        if isinstance(control.get("state"), dict):
            for field, value in control["state"].items():
                if isinstance(value, list):
                    problem = _nested_collection_problem(control, control_type, field, side)
                    if problem:
                        return problem
        if isinstance(control.get("state"), (dict, list)):
            problem = _deep_extra_collection_problem(control, control_type, side)
            if problem:
                return problem
    return None


def _observed_budget_amount(value: Any) -> bool:
    """Require a finite nonnegative amount, not an evidence-status placeholder.

    Accept JSON numbers or exact plain decimal strings. Python booleans are
    numbers by inheritance but are never valid monetary observations.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float, str, Decimal)):
        return False
    if isinstance(value, str) and re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", value) is None:
        return False
    try:
        amount = Decimal(str(value))
    except (ValueError, ArithmeticError):
        return False
    return amount.is_finite() and amount >= 0


def _explicit_material_state_problem(value: Any, pointer: str = "$") -> str | None:
    """Reject explicit unavailable state leaves across *all* material controls.

    This generic check is deliberately narrow: it does not invent a
    control-specific schema or interpret valid zero, False or other observed
    values. It rejects only reserved evidence placeholders, blank scalar
    strings and non-finite numeric leaves, including in nested structures.
    """
    if value is None:
        return f"{pointer} contains an explicit null/unknown observation"
    if isinstance(value, str):
        normalized = re.sub(r"[\s-]+", "_", value.strip().casefold())
        if not normalized or normalized in {
            "unknown", "unsupported", "partial", "missing", "unavailable",
            "not_available", "not_supported", "not_applicable", "n/a",
        }:
            return f"{pointer} contains an explicit unknown/unsupported placeholder"
    elif isinstance(value, (float, Decimal)):
        if not Decimal(str(value)).is_finite():
            return f"{pointer} contains a non-finite numeric observation"
    elif isinstance(value, dict):
        for key, child in value.items():
            escaped = str(key).replace("~", "~0").replace("/", "~1")
            problem = _explicit_material_state_problem(child, f"{pointer}/{escaped}")
            if problem:
                return problem
    elif isinstance(value, list):
        for index, child in enumerate(value):
            problem = _explicit_material_state_problem(child, f"{pointer}/{index}")
            if problem:
                return problem
    return None


def _audience_member_problem(control: Any, side: str) -> str | None:
    """A complete audience list is not proof that its members are usable.

    This is the repository's normalized read-side shape, not an Amazon-native
    request schema. A complete empty list is valid only with collection proof
    from _coverage_problem. Each populated row needs stable identity and a
    finite nonnegative observed bid boost; duplicates are ambiguous.
    """
    state = control.get("state") if isinstance(control, dict) else None
    if not isinstance(state, list):
        return f"{side} Sponsored Products audience bid adjustment must be a source-supported list"
    seen: set[str] = set()
    for index, member in enumerate(state):
        if not isinstance(member, dict):
            return f"{side} Sponsored Products audience member {index} is not an object"
        identity = member.get("audience_id")
        if not isinstance(identity, str) or not identity.strip() or identity != identity.strip():
            return f"{side} Sponsored Products audience member {index} lacks a stable audience_id"
        if identity in seen:
            return f"{side} Sponsored Products duplicate audience_id: {identity}"
        seen.add(identity)
        if not _observed_budget_amount(member.get("bid_boost")):
            return f"{side} Sponsored Products audience member {index} has unknown or invalid bid_boost"
    return None


def _rule_member_problem(members: Any, collection: str, amount_field: str, side: str, observed_at: Any) -> str | None:
    """Check normalized SP rule member identity and observed modifier values.

    Complete pagination proves collection coverage, not usable member fields.
    This read-side shape is repository-owned, not an Amazon API schema; it
    does not establish rule activation, schedule timing or bid composition.
    """
    if not isinstance(members, list):
        return f"{side} Sponsored Products {collection} is not a rule list"
    seen: set[str] = set()
    for index, member in enumerate(members):
        if not isinstance(member, dict):
            return f"{side} Sponsored Products {collection} member {index} is not an object"
        identity = member.get("rule_id")
        if not isinstance(identity, str) or not identity.strip() or identity != identity.strip():
            return f"{side} Sponsored Products {collection} member {index} lacks stable rule_id"
        if identity in seen:
            return f"{side} Sponsored Products {collection} has duplicate rule_id: {identity}"
        seen.add(identity)
        if not _observed_budget_amount(member.get(amount_field)):
            return f"{side} Sponsored Products {collection} member {index} has unknown or invalid {amount_field}"
        # Optional normalized activation evidence is not a platform enum or
        # continuous-time execution proof. If supplied, it must be usable:
        # repeated Unknown/Unsupported is not a stable competing control.
        if "activation_status" in member:
            status = member["activation_status"]
            if not isinstance(status, str) or status not in {"active", "inactive", "scheduled"}:
                return f"{side} Sponsored Products {collection} member {index} has unknown or invalid activation_status"
        # Explicit transition evidence must be valid, source-observed and no
        # later than its snapshot. This is not continuous rule execution proof.
        if "activation_effective_at" in member:
            if "activation_status" not in member:
                return f"{side} Sponsored Products {collection} member {index} has activation_effective_at without activation_status"
            instant = _rfc3339_instant(member["activation_effective_at"])
            observation = _rfc3339_instant(observed_at)
            if instant is None or observation is None or instant > observation:
                return f"{side} Sponsored Products {collection} member {index} has invalid or future activation_effective_at"
    return None


def _rule_activation_presence_problem(bmap: dict[str, dict[str, Any]], pmap: dict[str, dict[str, Any]]) -> str | None:
    """Reject one-sided optional activation evidence for the same rule identity.

    Added/removed rules are still competing control changes. This only checks
    common IDs, after each snapshot's member identity/value checks have passed.
    """
    for control_type, fields in (
        ("schedule_or_event_rule", ("schedule_rules", "event_rules")),
        ("budget_or_pacing", ("active_budget_rules",)),
    ):
        before = bmap.get(control_type, {}).get("state")
        after = pmap.get(control_type, {}).get("state")
        if not isinstance(before, dict) or not isinstance(after, dict):
            continue
        for field in fields:
            bmembers, pmembers = before.get(field), after.get(field)
            if not isinstance(bmembers, list) or not isinstance(pmembers, list):
                continue
            bby_id = {member["rule_id"]: member for member in bmembers if isinstance(member, dict) and "rule_id" in member}
            pby_id = {member["rule_id"]: member for member in pmembers if isinstance(member, dict) and "rule_id" in member}
            for rule_id in bby_id.keys() & pby_id.keys():
                for evidence_field in ("activation_status", "activation_effective_at"):
                    if (evidence_field in bby_id[rule_id]) != (evidence_field in pby_id[rule_id]):
                        return f"Sponsored Products {field} rule {rule_id} has one-sided {evidence_field} evidence"
    return None


def _surface_specific_state_problem(snapshot: dict[str, Any], control_map: dict[str, dict[str, Any]], side: str) -> str | None:
    """Validate decision-surface state that generic control presence cannot prove."""
    coverage = snapshot.get("coverage", {})
    provenance = coverage.get("requirement_provenance", {}) if isinstance(coverage, dict) else {}
    surface = provenance.get("decision_surface")

    if surface in {"sponsored_products_bid_change", "sponsored_products_budget_change"}:
        audience_problem = _audience_member_problem(control_map.get("audience_bid_adjustment"), side)
        if audience_problem:
            return audience_problem

        bidding_control = control_map.get("bidding_strategy")
        bidding_state = bidding_control.get("state") if isinstance(bidding_control, dict) else None
        # Rule-based bidding is a distinct ROAS-guardrail strategy, not a
        # schedule/event bid rule. A bare "rule_based" label omits a material
        # auction control and cannot prove that competing controls were stable.
        # This is a normalized read-side contract, not an Amazon API payload.
        known_simple_strategies = {"dynamic_down_only", "dynamic_up_and_down", "fixed"}
        if isinstance(bidding_state, str):
            normalized = bidding_state.lower().replace("-", "_")
            if bidding_state != bidding_state.strip() or normalized not in known_simple_strategies:
                return f"{side} Sponsored Products bidding strategy is unknown or lacks rule-based ROAS guardrail evidence"
        elif isinstance(bidding_state, dict):
            if set(bidding_state) != {"strategy", "roas_guardrail"}:
                return f"{side} Sponsored Products bidding strategy rule-based configuration has missing or unverified fields"
            strategy = bidding_state.get("strategy")
            if (
                not isinstance(strategy, str)
                or strategy != strategy.strip()
                or strategy.lower().replace("-", "_") != "rule_based"
            ):
                return f"{side} Sponsored Products bidding strategy state is unknown or unrecognized"
            guardrail = bidding_state.get("roas_guardrail")
            if not _observed_budget_amount(guardrail) or Decimal(str(guardrail)) <= 0:
                return f"{side} Sponsored Products bidding strategy rule-based ROAS guardrail is missing or invalid"
        else:
            return f"{side} Sponsored Products bidding strategy state is unknown or unrecognized"

        # An invalid base bid cannot establish a valid treatment or a stable
        # competing control, even when both snapshots repeat the same label.
        # Platform-specific bid minima/ceilings are separate dated capability checks.
        base_control = control_map.get("base_bid")
        base_state = base_control.get("state") if isinstance(base_control, dict) else None
        if not _observed_budget_amount(base_state):
            return f"{side} Sponsored Products base_bid has unknown or invalid numeric evidence"

        # Video bid boosts are independent of placement adjustments. An
        # unsupported, missing, boolean, negative, or non-finite modifier
        # cannot establish an unchanged material control in a causal review.
        # Platform-specific upper bounds remain a dated capability check.
        video_control = control_map.get("video_bid_adjustment")
        video_state = video_control.get("state") if isinstance(video_control, dict) else None
        if not _observed_budget_amount(video_state):
            return f"{side} Sponsored Products video_bid_adjustment has unknown or invalid numeric evidence"

        placement_control = control_map.get("placement_adjustment")
        placement_state = placement_control.get("state") if isinstance(placement_control, dict) else None
        if not isinstance(placement_state, dict):
            return f"{side} Sponsored Products placement state is not structured enough to prove all placement surfaces"
        required_placements = {"top_of_search", "rest_of_search", "product_pages"}
        missing_placements = sorted(required_placements - set(placement_state))
        if missing_placements:
            return f"{side} Sponsored Products placement state is missing: " + ", ".join(missing_placements)
        # Unknown adapter keys are not verified placement surfaces. Treat
        # them as unresolved evidence, even if repeated on both readbacks.
        unknown_placements = sorted(set(placement_state) - required_placements - {"amazon_business"})
        if unknown_placements:
            return f"{side} Sponsored Products placement state has unmapped dimensions: " + ", ".join(unknown_placements)
        for field in sorted(required_placements):
            # Presence is not numeric evidence: Unknown, Unsupported, booleans,
            # non-finite and negative modifiers cannot establish stability.
            # Exact platform upper limits remain a separate dated capability gate.
            if not _observed_budget_amount(placement_state.get(field)):
                return f"{side} Sponsored Products placement state has unknown or invalid {field}"

        # Amazon Business placements are a distinct Sponsored Products boost.
        # When supplied, the modifier must be observed numeric evidence, not
        # an unsupported/unknown placeholder. Its absence in legacy snapshots
        # is NOT proof of zero or universal marketplace ineligibility.
        if "amazon_business" in placement_state and not _observed_budget_amount(placement_state["amazon_business"]):
            return f"{side} Sponsored Products placement state has unknown or invalid amazon_business"

        # A complete material-control inventory is not proof of a usable site
        # restriction. These two labels are repository-normalized read-side
        # evidence, not Amazon API enum tokens or proof of account eligibility.
        # A new/unmapped site mode requires an explicit adapter contract.
        routing_control = control_map.get("targeting_or_routing")
        routing_state = routing_control.get("state") if isinstance(routing_control, dict) else None
        if not isinstance(routing_state, dict) or routing_state.get("site_restriction") not in (
            "ALL_ELIGIBLE", "AMAZON_BUSINESS"
        ) or not isinstance(routing_state.get("site_restriction"), str):
            return f"{side} Sponsored Products targeting_or_routing has missing, unknown or unrecognized site_restriction"

        # Optional retailer scope is adapter-normalized evidence, not an
        # Amazon API enum or proof of marketplace/account eligibility. A
        # Sponsored Products across-retailers control cannot substantiate an
        # Amazon Business placement boost or Business-exclusive site routing.
        # Both-absent legacy snapshots retain compatibility without asserting
        # that retailer scope was independently verified.
        if "retailer_scope" in routing_state:
            retailer_scope = routing_state["retailer_scope"]
            if not isinstance(retailer_scope, str) or retailer_scope not in {
                "AMAZON_STORE", "ACROSS_RETAILERS"
            }:
                return f"{side} Sponsored Products retailer_scope is missing, unknown or unmapped"
            if retailer_scope == "ACROSS_RETAILERS" and (
                "amazon_business" in placement_state
                or routing_state["site_restriction"] == "AMAZON_BUSINESS"
            ):
                return f"{side} Sponsored Products retailer_scope contradicts Amazon Business placement or site routing"

        rule_control = control_map.get("schedule_or_event_rule")
        rule_state = rule_control.get("state") if isinstance(rule_control, dict) else None
        if not isinstance(rule_state, dict):
            return f"{side} Sponsored Products bid-rule state is not structured enough to prove schedule and event rule coverage"
        required_rule_surfaces = {"schedule_rules", "event_rules"}
        missing_rule_surfaces = sorted(required_rule_surfaces - set(rule_state))
        if missing_rule_surfaces:
            return f"{side} Sponsored Products bid-rule state is missing: " + ", ".join(missing_rule_surfaces)
        for field in sorted(required_rule_surfaces):
            if not isinstance(rule_state.get(field), list):
                return f"{side} Sponsored Products {field} must be source-supported list evidence"
            nested_problem = _nested_collection_problem(rule_control, "schedule_or_event_rule", field, side)
            if nested_problem:
                return nested_problem
            member_problem = _rule_member_problem(rule_state[field], field, "bid_increase", side, snapshot.get("observed_at"))
            if member_problem:
                return member_problem

        # Active budget rules are material even when the intended treatment
        # is a bid change. A complete list with unverified members cannot
        # prove that competing budget controls stayed stable.
        budget_control = control_map.get("budget_or_pacing")
        budget_state = budget_control.get("state") if isinstance(budget_control, dict) else None
        if isinstance(budget_state, dict) and isinstance(budget_state.get("active_budget_rules"), list):
            member_problem = _rule_member_problem(
                budget_state["active_budget_rules"], "active_budget_rules", "increase_percent", side,
                snapshot.get("observed_at")
            )
            if member_problem:
                return member_problem

    if surface != "sponsored_products_budget_change":
        return None

    budget_control = control_map.get("budget_or_pacing")
    state = budget_control.get("state") if isinstance(budget_control, dict) else None
    if not isinstance(state, dict):
        return f"{side} Sponsored Products budget state is not structured enough to prove effective budget controls"

    required_fields = {"base_average_daily_budget", "effective_daily_budget", "active_budget_rules", "average_daily_budget_policy"}
    missing = sorted(required_fields - set(state))
    if missing:
        return f"{side} Sponsored Products budget state is missing: " + ", ".join(missing)
    for field in ("base_average_daily_budget", "effective_daily_budget"):
        if not _observed_budget_amount(state.get(field)):
            return f"{side} Sponsored Products budget state has unknown or invalid {field}"
    policy = state.get("average_daily_budget_policy")
    # A connector's Unknown/Unsupported label is not a stable observed policy.
    # A structured policy requires its own verified contract; arbitrary dicts
    # cannot be accepted as proof of a known account/platform setting.
    if (not isinstance(policy, str) or not policy.strip()
            or policy.strip().casefold().replace("-", "_").replace(" ", "_") in {
                "unknown", "unsupported", "partial", "missing", "unavailable", "not_available",
            }):
        return f"{side} Sponsored Products budget state has unknown average_daily_budget_policy"
    if not isinstance(state.get("active_budget_rules"), list):
        return f"{side} Sponsored Products active_budget_rules must be source-supported list evidence"
    nested_problem = _nested_collection_problem(budget_control, "budget_or_pacing", "active_budget_rules", side)
    if nested_problem:
        return nested_problem
    return None



def _sp_intervening_state_problem(control_type: str, state: Any, label: str, surface: str) -> str | None:
    """Apply the same basic SP value semantics to positive event evidence.

    An event can prove a confounder only when its observed before/after values
    are usable. This does not prove event-log completeness or raw API origin.
    """
    if control_type in {"base_bid", "video_bid_adjustment"}:
        if not _observed_budget_amount(state):
            return f"{label} {control_type} has unknown or invalid numeric evidence"
    elif control_type == "placement_adjustment":
        required = {"top_of_search", "rest_of_search", "product_pages"}
        if not isinstance(state, dict) or not required.issubset(state):
            return f"{label} placement_adjustment lacks the required placement surfaces"
        unknown_placements = sorted(set(state) - required - {"amazon_business"})
        if unknown_placements:
            return f"{label} placement_adjustment has unmapped dimensions: " + ", ".join(unknown_placements)
        for field in sorted(required | ({"amazon_business"} if "amazon_business" in state else set())):
            if not _observed_budget_amount(state[field]):
                return f"{label} placement_adjustment has unknown or invalid {field}"
    elif control_type == "audience_bid_adjustment":
        return _audience_member_problem({"state": state}, label)
    elif control_type == "bidding_strategy":
        if isinstance(state, str):
            if (state != state.strip()
                    or state.lower().replace("-", "_") not in {
                        "dynamic_down_only", "dynamic_up_and_down", "fixed"
                    }):
                return f"{label} bidding_strategy is unknown or unrecognized"
        elif isinstance(state, dict):
            strategy = state.get("strategy")
            if (set(state) != {"strategy", "roas_guardrail"}
                    or not isinstance(strategy, str)
                    or strategy != strategy.strip()
                    or strategy.lower().replace("-", "_") != "rule_based"
                    or not _observed_budget_amount(state.get("roas_guardrail"))
                    or Decimal(str(state["roas_guardrail"])) <= 0):
                return f"{label} bidding_strategy lacks usable rule-based guardrail evidence"
        else:
            return f"{label} bidding_strategy is unknown or unrecognized"
    elif control_type == "budget_or_pacing":
        # A positive mid-window budget event must not bypass the same
        # observed amount/policy contract used at SP budget endpoints.
        # Bid reviews retain legacy partial budget shape compatibility, but
        # any explicitly supplied amount or policy must still be usable.
        if not isinstance(state, dict) or not isinstance(state.get("active_budget_rules"), list):
            return f"{label} budget_or_pacing lacks observed active_budget_rules"
        if surface == "sponsored_products_budget_change":
            required = {
                "base_average_daily_budget", "effective_daily_budget",
                "active_budget_rules", "average_daily_budget_policy",
            }
            if not required.issubset(state):
                return f"{label} budget_or_pacing lacks required budget policy fields"
        for field in ("base_average_daily_budget", "effective_daily_budget"):
            if field in state and not _observed_budget_amount(state[field]):
                return f"{label} budget_or_pacing has unknown or invalid {field}"
        if "average_daily_budget_policy" in state:
            policy = state["average_daily_budget_policy"]
            if (not isinstance(policy, str) or policy != policy.strip()
                    or _explicit_material_state_problem(policy)):
                return f"{label} budget_or_pacing has unknown average_daily_budget_policy"
    elif control_type == "targeting_or_routing":
        # Site/retailer labels are repository-normalized read-side evidence,
        # not native Amazon API enums or universal eligibility claims.
        if (not isinstance(state, dict)
                or not isinstance(state.get("site_restriction"), str)
                or state["site_restriction"] not in {"ALL_ELIGIBLE", "AMAZON_BUSINESS"}):
            return f"{label} targeting_or_routing lacks a verified site_restriction"
        if "retailer_scope" in state:
            retailer = state["retailer_scope"]
            if not isinstance(retailer, str) or retailer not in {"AMAZON_STORE", "ACROSS_RETAILERS"}:
                return f"{label} targeting_or_routing has unmapped retailer_scope"
            if retailer == "ACROSS_RETAILERS" and state["site_restriction"] == "AMAZON_BUSINESS":
                return f"{label} targeting_or_routing contradicts across-retailer site eligibility"
    return None



def _event_rule_collection_evidence_problem(event: dict[str, Any], label: str) -> str | None:
    """Validate opt-in *paired* SP rule-list proof without claiming event-log coverage.

    Legacy events without this optional envelope remain compatible but do not
    establish completeness. An explicit partial, malformed or one-sided proof
    must not be promoted into an observed control transition.
    """
    if "rule_collection_evidence" not in event:
        return None
    collections = {
        "schedule_or_event_rule": {"schedule_rules", "event_rules"},
        "budget_or_pacing": {"active_budget_rules"},
    }.get(event["control_type"])
    if collections is None:
        return f"{label} rule_collection_evidence is not applicable to this control"
    evidence = event["rule_collection_evidence"]
    if not isinstance(evidence, dict) or set(evidence) != {"before", "after"}:
        return f"{label} rule collection proof requires before and after phases"
    expected = {
        "enumeration_status": "Complete",
        "pagination_status": "Complete",
        "capability_status": "Supported",
    }
    for phase in ("before", "after"):
        phase_evidence = evidence[phase]
        if not isinstance(phase_evidence, dict) or set(phase_evidence) != collections:
            return f"{label} {phase} rule collection proof lacks exact collection coverage"
        for collection in sorted(collections):
            proof = phase_evidence[collection]
            if not isinstance(proof, dict) or set(proof) != set(expected):
                return f"{label} {phase}.{collection} collection completeness proof is malformed"
            if any(proof[field] != required for field, required in expected.items()):
                return f"{label} {phase}.{collection} collection completeness is unproven"
    return None


def _intervening_control_events_problem(
    baseline: dict[str, Any],
    post: dict[str, Any],
    required: set[str],
    observed_instants: list[tuple[datetime, Decimal]],
) -> tuple[str | None, set[str]]:
    """Check explicit *positive* mid-window transition evidence, never infer no events.

    Optional post-owned event records can expose a change-and-revert that two
    endpoint readbacks miss. Empty/omitted records do not prove continuous
    execution, exhaustive event capture or absence of other transitions.
    """
    if "control_events" in baseline:
        return "intervening control_events must be attached to the post readback", set()
    if "control_events" not in post:
        return None, set()
    events = post["control_events"]
    if not isinstance(events, list):
        return "post control_events must be an array of observed events", set()
    surface = baseline["coverage"]["requirement_provenance"]["decision_surface"]

    seen: set[str] = set()
    changed: set[str] = set()
    # A concrete source readback ID denotes one observation instant, even
    # when several control events were observed in that same readback.
    event_readback_instants: dict[str, tuple[datetime, Decimal]] = {}
    # Two event rows for the same control and instant cannot assert
    # incompatible transitions. Distinct controls at one instant are valid.
    same_instant_transitions: dict[tuple[str, tuple[datetime, Decimal]], tuple[Any, Any]] = {}
    # Only a shared concrete source readback can bind different control
    # surfaces into one co-observed state. Equal timestamps alone cannot.
    co_observed_states: dict[str, dict[str, tuple[Any, Any]]] = {}
    for index, event in enumerate(events):
        label = f"post control_events[{index}]"
        if not isinstance(event, dict):
            return f"{label} must be an object", set()
        fields = {
            "event_id", "event_at", "scope", "source", "control_type",
            "before_state", "after_state", "evidence_status",
        }
        optional_fields = {"rule_collection_evidence", "rule_descendant_collection_evidence"}
        if not fields.issubset(event) or not set(event).issubset(fields | optional_fields):
            return f"{label} has missing or unrecognized evidence fields", set()
        event_id = event["event_id"]
        if _unusable_identity_label(event_id) or event_id in seen:
            return f"{label} has missing, unknown or duplicate event_id", set()
        seen.add(event_id)
        if event_id in {
            baseline["source"].get("readback_id"), post["source"].get("readback_id")
        }:
            return f"{label} reuses an endpoint readback observation identity", set()
        if event["scope"] != baseline["scope"] or event["scope"] != post["scope"]:
            return f"{label} decision scope does not match both endpoint observations", set()
        if _source_lineage_problem(baseline["source"], event["source"]) or _source_lineage_problem(
            post["source"], event["source"]
        ):
            return f"{label} source lineage is missing or inconsistent", set()
        event_readback = event["source"].get("readback_id")
        if event_readback is not None and event_readback in {
            baseline["source"].get("readback_id"), post["source"].get("readback_id")
        }:
            return f"{label} source reuses an endpoint readback observation", set()
        if event["evidence_status"] != "observed":
            return f"{label} is not a positively observed control transition", set()
        control_type = event["control_type"]
        if not isinstance(control_type, str) or control_type not in required:
            return f"{label} control_type is outside the registered material set", set()
        instant = _rfc3339_instant(event["event_at"])
        if instant is None or not (observed_instants[0] < instant < observed_instants[1]):
            return f"{label} has invalid or out-of-window event_at", set()

        descendant_proof = event.get("rule_descendant_collection_evidence")
        if "rule_descendant_collection_evidence" in event:
            if (surface not in {"sponsored_products_bid_change", "sponsored_products_budget_change"}
                    or control_type not in {"schedule_or_event_rule", "budget_or_pacing"}
                    or "rule_collection_evidence" not in event):
                return f"{label} descendant rule proof requires an applicable SP rule event and outer proof", set()
            if (not isinstance(descendant_proof, dict)
                    or set(descendant_proof) != {"before", "after"}
                    or any(not isinstance(descendant_proof[phase], dict) for phase in ("before", "after"))):
                return f"{label} descendant rule proof requires before and after pointer maps", set()

        for field in ("before_state", "after_state"):
            state = event[field]
            if state is None or _explicit_material_state_problem(state):
                return f"{label} has missing or unresolved {field}", set()
            # Endpoint validation already rejects malformed SP bid/placement/
            # audience/strategy values. Event-only evidence must not bypass
            # those semantics to manufacture a confounder or isolated action.
            if surface in {"sponsored_products_bid_change", "sponsored_products_budget_change"}:
                event_state_problem = _sp_intervening_state_problem(control_type, state, label, surface)
                if event_state_problem:
                    return event_state_problem, set()
                # Non-rule routing/audience event evidence cannot bypass the
                # collection guards already required for endpoint snapshots.
                # No event-side proof contract exists for these extra lists;
                # even an empty descendant array remains unverified.
                if control_type in {"targeting_or_routing", "audience_bid_adjustment"}:
                    collection_control = {"state": state}
                    if control_type == "targeting_or_routing" and isinstance(state, dict):
                        for list_field, value in state.items():
                            if isinstance(value, list):
                                collection_problem = _nested_collection_problem(
                                    collection_control, control_type, list_field, f"{label} {field}"
                                )
                                if collection_problem:
                                    return collection_problem, set()
                    collection_problem = _deep_extra_collection_problem(
                        collection_control, control_type, f"{label} {field}"
                    )
                    if collection_problem:
                        return collection_problem, set()
            # Rule members must be usable before identity-keyed comparison;
            # otherwise a reordered list or malformed ID could masquerade as
            # a control transition. This does not prove collection completeness.
            if control_type in {"schedule_or_event_rule", "budget_or_pacing"}:
                rule_fields = (
                    (("schedule_rules", "bid_increase"), ("event_rules", "bid_increase"))
                    if control_type == "schedule_or_event_rule"
                    else (("active_budget_rules", "increase_percent"),)
                )
                if not isinstance(state, dict):
                    return f"{label} has unstructured {field} rule evidence", set()
                # The paired rule_collection_evidence envelope certifies only
                # registered rule lists. An extra direct array has no event-side
                # completeness contract; even an empty list cannot be inferred
                # complete from a different collection's proof.
                known_rule_lists = {collection for collection, _ in rule_fields}
                extra_direct_lists = sorted(
                    name for name, value in state.items()
                    if isinstance(value, list) and name not in known_rule_lists
                )
                if extra_direct_lists:
                    return (
                        f"{label} {field} has unproven direct rule collections: "
                        + ", ".join(extra_direct_lists),
                        set(),
                    )
                for collection, modifier in rule_fields:
                    if _rule_member_problem(
                        state.get(collection), collection, modifier, label, event["event_at"]
                    ):
                        return f"{label} has incomplete or invalid {field}.{collection}", set()
                # A Complete declaration for the outer schedule/event/budget
                # rule list cannot certify a nested list inside a rule member.
                # Endpoint readbacks already require separate JSON-pointer
                # evidence for such descendants. The event contract has no
                # descendant-proof field, so fail closed even for empty lists.
                phase = "before" if field == "before_state" else "after"
                descendant_control = {"state": state}
                if descendant_proof is not None:
                    descendant_control["nested_collection_evidence"] = descendant_proof[phase]
                descendant_problem = _deep_extra_collection_problem(
                    descendant_control, control_type, f"{label} {field}",
                    strict_evidence=descendant_proof is not None,
                )
                if descendant_problem:
                    return descendant_problem, set()

        if "rule_collection_evidence" in event:
            if surface not in {"sponsored_products_bid_change", "sponsored_products_budget_change"}:
                return f"{label} rule collection proof has no registered SP contract", set()
            proof_problem = _event_rule_collection_evidence_problem(event, label)
            if proof_problem:
                return proof_problem, set()
        before_state, after_state = event["before_state"], event["after_state"]
        if (surface in {"sponsored_products_bid_change", "sponsored_products_budget_change"}
                and control_type in {"schedule_or_event_rule", "budget_or_pacing"}):
            # Reuse endpoint identity-keyed parity: optional activation metadata
            # on only one side is missing evidence, not a verified transition.
            # New/removed rule IDs are not silently treated as inactive.
            activation_problem = _rule_activation_presence_problem(
                {control_type: {"state": before_state}},
                {control_type: {"state": after_state}},
            )
            if activation_problem:
                return f"{label} {activation_problem}", set()
        if surface in {"sponsored_products_bid_change", "sponsored_products_budget_change"}:
            # A field observed on only one side cannot establish a known
            # transition. Both-absent optional evidence remains compatible.
            if control_type == "budget_or_pacing":
                for optional_field in (
                    "base_average_daily_budget", "effective_daily_budget",
                    "average_daily_budget_policy",
                ):
                    if (optional_field in before_state) != (optional_field in after_state):
                        return f"{label} has one-sided {optional_field} evidence", set()
        if control_type == "targeting_or_routing":
            # An optional retailer dimension appearing on only one side
            # cannot establish the before/after routing transition.
            if ("retailer_scope" in before_state) != ("retailer_scope" in after_state):
                return f"{label} has one-sided retailer_scope evidence", set()
        same = (
            _sp_rule_state_equal(control_type, before_state, after_state)
            if control_type in {"schedule_or_event_rule", "budget_or_pacing"}
            else _json_state_equal(before_state, after_state)
        )
        if same:
            return f"{label} does not contain an observed material state change", set()
        if event_readback is not None:
            prior_instant = event_readback_instants.get(event_readback)
            if prior_instant is not None and prior_instant != instant:
                return f"{label} reuses source.readback_id for a different event_at instant", set()
            event_readback_instants[event_readback] = instant
        transition_key = (control_type, instant)
        prior_transition = same_instant_transitions.get(transition_key)
        if prior_transition is not None:
            previous_before, previous_after = prior_transition
            state_equal = (
                lambda left, right: _sp_rule_state_equal(control_type, left, right)
                if control_type in {"schedule_or_event_rule", "budget_or_pacing"}
                else _json_state_equal(left, right)
            )
            if not (state_equal(previous_before, before_state)
                    and state_equal(previous_after, after_state)):
                return f"{label} contradicts another observed transition for the same control and event_at", set()
        else:
            same_instant_transitions[transition_key] = (before_state, after_state)
        if event_readback is not None:
            co_observed_states.setdefault(event_readback, {})[control_type] = (
                before_state, after_state
            )
        changed.add(control_type)

    # The SP endpoint contract already rejects an across-retailer routing
    # state combined with an Amazon Business placement modifier. Do not
    # let two event rows from the *same* readback bypass that invariant.
    # Separate/missing readbacks are not proof of a simultaneous snapshot.
    if surface in {"sponsored_products_bid_change", "sponsored_products_budget_change"}:
        for readback, controls in co_observed_states.items():
            if not {"targeting_or_routing", "placement_adjustment"}.issubset(controls):
                continue
            for phase in (0, 1):
                routing = controls["targeting_or_routing"][phase]
                placement = controls["placement_adjustment"][phase]
                if (isinstance(routing, dict) and isinstance(placement, dict)
                        and routing.get("retailer_scope") == "ACROSS_RETAILERS"
                        and "amazon_business" in placement):
                    return (
                        f"event readback {readback} contradicts co-observed "
                        "across-retailer routing and Amazon Business placement",
                        set(),
                    )
    return None, changed


def compare_control_state(baseline: dict[str, Any], post: dict[str, Any], intended_treatment: str | None = None) -> dict[str, Any]:
    """Return a fail-closed comparability classification and evidence reasons."""
    reasons: list[str] = []
    bscope, pscope = baseline.get("scope", {}), post.get("scope", {})
    scope_problem = _scope_identity_problem(bscope, pscope)
    if scope_problem:
        return {"classification": "Unknown", "reasons": [scope_problem]}
    source_problem = _source_lineage_problem(baseline.get("source"), post.get("source"))
    if source_problem:
        return {"classification": "Unknown", "reasons": [source_problem]}
    for key in ("campaign_id", "ad_group_id", "entity_id"):
        if bscope.get(key) != pscope.get(key):
            return {"classification": "Unknown", "reasons": [f"decision-scope identity changed for {key}"]}

    if bscope.get("entity_id") is not None:
        before_type, after_type = bscope.get("entity_type"), pscope.get("entity_type")
        if not before_type or not after_type:
            return {"classification": "Unknown", "reasons": ["entity_id is present without a complete entity_type identity"]}
        if before_type != after_type:
            return {"classification": "Unknown", "reasons": ["decision-scope identity changed for entity_type"]}

    observed_instants: list[tuple[datetime, Decimal]] = []
    for snapshot, side in ((baseline, "baseline"), (post, "post")):
        inventory_problem = _control_inventory_problem(snapshot, side)
        if inventory_problem:
            return {"classification": "Unknown", "reasons": [inventory_problem]}
        observed = _rfc3339_instant(snapshot.get("observed_at"))
        if observed is None:
            return {"classification": "Unknown", "reasons": [f"{side} observed_at is not a verified RFC3339 instant"]}
        observed_instants.append(observed)
        for control in snapshot["controls"]:
            effective_at = control.get("effective_at")
            if effective_at is None:
                continue  # Missing effective_at remains guarded when a control changes.
            effective = _rfc3339_instant(effective_at)
            if effective is None:
                return {"classification": "Unknown", "reasons": [f"{side} {control['control_type']} effective_at is not a verified RFC3339 instant"]}
            if effective > observed:
                return {"classification": "Unknown", "reasons": [f"{side} {control['control_type']} effective_at is later than observed_at"]}

    if observed_instants[1] < observed_instants[0]:
        return {"classification": "Unknown", "reasons": ["post observed_at precedes baseline observed_at"]}

    # One readback observation cannot carry two distinct observation times.
    # Compare exact UTC instants, including submicrosecond fractional digits.
    # Equivalent timezone-offset spellings of the same instant remain valid.
    before_readback = baseline["source"].get("readback_id")
    after_readback = post["source"].get("readback_id")
    if (before_readback is not None and before_readback == after_readback
            and observed_instants[0] != observed_instants[1]):
        return {
            "classification": "Unknown",
            "reasons": ["conflicting observed_at instants reuse the same source.readback_id observation"],
        }

    bmap, pmap = _control_map(baseline), _control_map(post)
    for snapshot, control_map, side in ((baseline, bmap, "baseline"), (post, pmap, "post")):
        problem = _coverage_problem(snapshot, control_map, side)
        if problem:
            return {"classification": "Unknown", "reasons": [problem]}
        state_problem = _surface_specific_state_problem(snapshot, control_map, side)
        if state_problem:
            return {"classification": "Unknown", "reasons": [state_problem]}

    required_before = set(baseline["coverage"]["required_control_types"])
    required_after = set(post["coverage"]["required_control_types"])
    if required_before != required_after:
        return {"classification": "Unknown", "reasons": ["material-control requirement set changed between snapshots"]}

    # One readback observation cannot assert contradictory effective times or
    # evidence statuses for the same control, even if its state is unchanged.
    # Compare UTC instants rather than timestamp spellings, preserving the
    # original fractional precision. Null/omitted legacy readback IDs remain
    # compatible; a changed effective_at under a distinct ID is not itself
    # proof that the material control value changed.
    if before_readback is not None and before_readback == after_readback:
        for control_type in sorted(set(bmap) & set(pmap)):
            before_control, after_control = bmap[control_type], pmap[control_type]
            before_effective = before_control.get("effective_at")
            after_effective = after_control.get("effective_at")
            if ((before_effective is None) != (after_effective is None)
                    or (before_effective is not None
                        and _rfc3339_instant(before_effective) != _rfc3339_instant(after_effective))):
                return {
                    "classification": "Unknown",
                    "reasons": [f"conflicting {control_type} effective_at reuses the same source.readback_id observation"],
                }
            if before_control.get("evidence_status") != after_control.get("evidence_status"):
                return {
                    "classification": "Unknown",
                    "reasons": [f"conflicting {control_type} evidence_status reuses the same source.readback_id observation"],
                }
            if not _same_transition_provenance(
                before_control.get("transition_provenance"),
                after_control.get("transition_provenance"),
            ):
                return {
                    "classification": "Unknown",
                    "reasons": [f"conflicting {control_type} transition_provenance reuses the same source.readback_id observation"],
                }

    provenance_before = baseline["coverage"]["requirement_provenance"]
    provenance_after = post["coverage"]["requirement_provenance"]
    if provenance_before.get("decision_surface") != provenance_after.get("decision_surface"):
        return {"classification": "Unknown", "reasons": ["material-control requirement decision surface changed between snapshots"]}
    if provenance_before.get("requirement_registry_id") != provenance_after.get("requirement_registry_id"):
        return {"classification": "Unknown", "reasons": ["material-control requirement registry changed between snapshots"]}

    if provenance_before.get("decision_surface") in {"sponsored_products_bid_change", "sponsored_products_budget_change"}:
        # A shared marketplace/profile cannot identify a specific SP campaign.
        # Both-absent campaign IDs are unknown, not a verified identity match.
        if _unusable_identity_label(bscope.get("campaign_id")) or _unusable_identity_label(pscope.get("campaign_id")):
            return {"classification": "Unknown", "reasons": ["Sponsored Products bid/budget causal comparison requires concrete campaign_id on both snapshots"]}
        before_placement = bmap["placement_adjustment"]["state"]
        after_placement = pmap["placement_adjustment"]["state"]
        # One-sided optional evidence cannot establish an unchanged B2B
        # modifier or a causal effect. Both absent stays legacy-compatible,
        # without claiming B2B capability/eligibility was independently proved.
        if ("amazon_business" in before_placement) != ("amazon_business" in after_placement):
            return {"classification": "Unknown", "reasons": ["amazon_business placement evidence is missing on one side"]}
        before_routing = bmap["targeting_or_routing"]["state"]
        after_routing = pmap["targeting_or_routing"]["state"]
        if ("retailer_scope" in before_routing) != ("retailer_scope" in after_routing):
            return {"classification": "Unknown", "reasons": ["retailer_scope evidence is missing on one side"]}
        activation_problem = _rule_activation_presence_problem(bmap, pmap)
        if activation_problem:
            return {"classification": "Unknown", "reasons": [activation_problem]}

    all_types = sorted(set(bmap) | set(pmap))
    if not all_types:
        return {"classification": "Unknown", "reasons": ["no material control evidence"]}

    changed: list[str] = []
    unknown: list[str] = []
    timestamp_unknown: list[str] = []
    for control_type in all_types:
        before, after = bmap.get(control_type), pmap.get(control_type)
        if before is None or after is None:
            unknown.append(control_type)
            continue
        if before.get("evidence_status") not in VALID_EVIDENCE or after.get("evidence_status") not in VALID_EVIDENCE:
            unknown.append(control_type)
            continue
        # For registered SP causal surfaces, rule rows form ID-keyed sets;
        # an adapter's enumeration order is not itself a material change.
        same_state = (
            _sp_rule_state_equal(control_type, before.get("state"), after.get("state"))
            if provenance_before.get("decision_surface") in {
                "sponsored_products_bid_change", "sponsored_products_budget_change"
            }
            else _json_state_equal(before.get("state"), after.get("state"))
        )
        if not same_state:
            changed.append(control_type)
            if not before.get("effective_at") or not after.get("effective_at"):
                timestamp_unknown.append(control_type)

    if unknown:
        reasons.append("missing/invalid/unknown/stale/unsupported evidence: " + ", ".join(unknown))
    if timestamp_unknown:
        reasons.append("changed control lacks effective_at: " + ", ".join(timestamp_unknown))
    if reasons:
        return {"classification": "Unknown", "reasons": reasons, "changed_controls": changed}

    # A readback_id identifies one observed snapshot, not a reusable account
    # or connector. Contradictory material states cannot be independently
    # observed under the exact same non-null readback identity.
    before_readback = baseline["source"].get("readback_id")
    after_readback = post["source"].get("readback_id")
    if (changed and before_readback is not None
            and type(before_readback) is type(after_readback)
            and before_readback == after_readback):
        return {
            "classification": "Unknown",
            "reasons": ["conflicting material states reuse the same source.readback_id observation"],
            "changed_controls": changed,
        }

    event_problem, intervening_changes = _intervening_control_events_problem(
        baseline, post, required_before, observed_instants
    )
    if event_problem:
        return {"classification": "Unknown", "reasons": [event_problem], "changed_controls": changed}
    # A positively observed intervening competing change is a confounder
    # even if the control later reverted to its original endpoint state.
    # The absence of events never certifies continuous control stability.
    if intervening_changes:
        if intended_treatment and (
            intended_treatment not in required_before or intended_treatment not in changed
        ):
            return {
                "classification": "Unknown",
                "reasons": ["intended treatment has no verified endpoint state change"],
                "changed_controls": changed,
            }
        all_evidenced_changes = sorted(set(changed) | intervening_changes)
        if intended_treatment and intervening_changes - {intended_treatment}:
            return {
                "classification": "Confounded",
                "reasons": ["observed intervening competing control changes: " +
                            ", ".join(sorted(intervening_changes - {intended_treatment}))],
                "changed_controls": all_evidenced_changes,
            }
        if not intended_treatment:
            return {
                "classification": "Directional",
                "reasons": ["observed intervening material control changes without an identified treatment"],
                "changed_controls": all_evidenced_changes,
            }

    if intended_treatment:
        if intended_treatment not in required_before:
            return {"classification": "Unknown", "reasons": ["intended treatment is outside the evidenced material-control set"]}
        if intended_treatment not in changed:
            return {"classification": "Unknown", "reasons": ["intended treatment has no observed state change"]}
        overlaps = [c for c in changed if c != intended_treatment]
        if not overlaps:
            return {"classification": "Treatment Isolated", "reasons": ["only intended treatment changed within a complete, registry-verified material-control set"], "changed_controls": changed}
        return {"classification": "Confounded", "reasons": ["overlapping material controls changed: " + ", ".join(overlaps)], "changed_controls": changed}

    if not changed:
        return {"classification": "Comparable", "reasons": ["no evidenced material control changes within a complete, registry-verified material-control set"], "changed_controls": []}
    return {"classification": "Directional", "reasons": ["material controls changed without an identified treatment"], "changed_controls": changed}


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare control-state snapshots without executing writes")
    parser.add_argument("baseline", type=Path)
    parser.add_argument("post", type=Path)
    parser.add_argument("--treatment", dest="treatment")
    args = parser.parse_args()
    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    post = json.loads(args.post.read_text(encoding="utf-8"))
    print(json.dumps(compare_control_state(baseline, post, args.treatment), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
