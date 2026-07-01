from __future__ import annotations

from pathlib import Path

import pytest

from gk.models import Finding, Severity


def test_finding_requires_reason() -> None:
    with pytest.raises(ValueError, match="why"):
        Finding(
            path=Path("/tmp/cache"),
            size_bytes=10,
            severity=Severity.INFO,
            recommendation="Review before removing.",
            reason=" ",
            scanner="test",
        )


def test_finding_requires_recommendation() -> None:
    with pytest.raises(ValueError, match="recommendation"):
        Finding(
            path=Path("/tmp/cache"),
            size_bytes=10,
            severity=Severity.INFO,
            recommendation=" ",
            reason="It is non-empty.",
            scanner="test",
        )


def test_finding_rejects_negative_size() -> None:
    with pytest.raises(ValueError, match="zero or greater"):
        Finding(
            path=Path("/tmp/cache"),
            size_bytes=-1,
            severity=Severity.INFO,
            recommendation="Review before removing.",
            reason="It is non-empty.",
            scanner="test",
        )
