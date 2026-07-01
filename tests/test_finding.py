from __future__ import annotations

from pathlib import Path

import pytest

from gk.models import Category, Confidence, Finding, Severity


def make_finding(**overrides: object) -> Finding:
    values = {
        "id": "test-finding",
        "title": "Test finding",
        "category": Category.UNKNOWN,
        "severity": Severity.INFO,
        "path": Path("/tmp/cache"),
        "size_bytes": 10,
        "recommendation": "Review before removing.",
        "reason": "It is non-empty.",
        "scanner": "test",
        "confidence": Confidence.MEDIUM,
    }
    values.update(overrides)
    return Finding(**values)


def test_finding_valid_construction() -> None:
    finding = make_finding()

    assert finding.id == "test-finding"
    assert finding.title == "Test finding"
    assert finding.category is Category.UNKNOWN
    assert finding.severity is Severity.INFO
    assert finding.path == Path("/tmp/cache")
    assert finding.size_bytes == 10
    assert finding.recommendation == "Review before removing."
    assert finding.reason == "It is non-empty."
    assert finding.scanner == "test"
    assert finding.confidence is Confidence.MEDIUM


@pytest.mark.parametrize(
    "field_name",
    ["id", "title", "reason", "recommendation", "scanner"],
)
def test_finding_requires_non_empty_strings(field_name: str) -> None:
    with pytest.raises(ValueError, match=field_name):
        make_finding(**{field_name: " "})


def test_finding_rejects_negative_size() -> None:
    with pytest.raises(ValueError, match="zero or greater"):
        make_finding(size_bytes=-1)


def test_finding_allows_none_path_and_none_size() -> None:
    finding = make_finding(path=None, size_bytes=None)

    assert finding.path is None
    assert finding.size_bytes is None
