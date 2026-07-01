from __future__ import annotations

from pathlib import Path

from gk.models import Severity
from gk.scanners.cache import CacheDirectoryScanner, severity_for_size


def test_cache_scanner_reports_non_empty_cache_directories(tmp_path: Path) -> None:
    cache_dir = tmp_path / ".cache"
    app_cache = cache_dir / "example-app"
    app_cache.mkdir(parents=True)
    (app_cache / "data.bin").write_bytes(b"cache-data")
    (cache_dir / "loose-file").write_text("not a directory")
    (cache_dir / "empty-app").mkdir()

    findings = CacheDirectoryScanner(home=tmp_path).scan()

    assert len(findings) == 1
    finding = findings[0]
    assert finding.path == app_cache
    assert finding.size_bytes >= len(b"cache-data")
    assert finding.severity is Severity.INFO
    assert finding.scanner == "cache-directories"
    assert "under ~/.cache" in finding.reason
    assert "Review" in finding.recommendation


def test_cache_scanner_returns_no_findings_without_cache_directory(
    tmp_path: Path,
) -> None:
    assert CacheDirectoryScanner(home=tmp_path).scan() == []


def test_cache_scanner_does_not_follow_symlinked_directories(tmp_path: Path) -> None:
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "data.bin").write_bytes(b"external")

    cache_dir = tmp_path / ".cache"
    cache_dir.mkdir()
    (cache_dir / "linked").symlink_to(outside, target_is_directory=True)

    assert CacheDirectoryScanner(home=tmp_path).scan() == []


def test_severity_for_size() -> None:
    assert severity_for_size(1) is Severity.INFO
    assert severity_for_size(1024**3) is Severity.LOW
    assert severity_for_size(5 * 1024**3) is Severity.MEDIUM
