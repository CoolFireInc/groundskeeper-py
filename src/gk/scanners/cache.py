from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from gk.models import Finding, Severity

LOW_SEVERITY_BYTES = 1 * 1024 * 1024 * 1024
MEDIUM_SEVERITY_BYTES = 5 * 1024 * 1024 * 1024


@dataclass(frozen=True, slots=True)
class CacheDirectoryScanner:
    home: Path | None = None

    name: str = "cache-directories"

    def scan(self) -> list[Finding]:
        cache_root = self.cache_root
        if not cache_root.is_dir():
            return []

        findings: list[Finding] = []
        for path in sorted(cache_root.iterdir(), key=lambda item: item.name.casefold()):
            if not path.is_dir() or path.is_symlink():
                continue

            size_bytes = directory_size(path)
            if size_bytes == 0:
                continue

            findings.append(
                Finding(
                    path=path,
                    size_bytes=size_bytes,
                    severity=severity_for_size(size_bytes),
                    scanner=self.name,
                    reason=(
                        "This is a non-empty application cache directory under "
                        "~/.cache. Cache data can accumulate over time and is "
                        "worth reviewing."
                    ),
                    recommendation=(
                        "Review the owning application's cache settings before "
                        "removing anything."
                    ),
                )
            )

        return findings

    @property
    def cache_root(self) -> Path:
        home = self.home or Path.home()
        return home / ".cache"


def severity_for_size(size_bytes: int) -> Severity:
    if size_bytes >= MEDIUM_SEVERITY_BYTES:
        return Severity.MEDIUM
    if size_bytes >= LOW_SEVERITY_BYTES:
        return Severity.LOW
    return Severity.INFO


def directory_size(path: Path) -> int:
    total = 0
    for root, dirnames, filenames in os.walk(path, followlinks=False):
        root_path = Path(root)

        kept_dirnames: list[str] = []
        for dirname in dirnames:
            child = root_path / dirname
            if child.is_symlink():
                continue
            kept_dirnames.append(dirname)
            total += safe_size(child)
        dirnames[:] = kept_dirnames

        for filename in filenames:
            total += safe_size(root_path / filename)

    return total


def safe_size(path: Path) -> int:
    try:
        return path.stat(follow_symlinks=False).st_size
    except OSError:
        return 0
