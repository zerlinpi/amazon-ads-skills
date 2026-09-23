from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_deduplicated_reach_reference_guards_non_additive_aggregation():
    path = ROOT / "references" / "deduplicated-reach-frequency.md"
    assert path.exists(), "RED: shared reach/frequency measurement contract is missing"
    text = path.read_text(encoding="utf-8").lower()
    required = [
        "deduplicated reach",
        "non-additive",
        "do not sum",
        "frequency",
        "time grain",
        "scope",
        "cross-account",
        "missing",
        "not zero",
        "comparable",
    ]
    for token in required:
        assert token in text, f"missing reach/frequency safety invariant: {token}"


def test_data_lineage_routes_reach_frequency_semantics():
    text = (ROOT / "references" / "data-lineage.md").read_text(encoding="utf-8").lower()
    assert "deduplicated-reach-frequency.md" in text
    assert "non-additive" in text
