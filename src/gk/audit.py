from __future__ import annotations

from collections.abc import Iterable

from gk.models import Finding
from gk.scanners.base import Scanner


def run_audit(scanners: Iterable[Scanner]) -> list[Finding]:
    findings: list[Finding] = []
    for scanner in scanners:
        findings.extend(scanner.scan())
    return findings
