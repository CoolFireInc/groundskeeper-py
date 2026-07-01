from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class Severity(StrEnum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True, slots=True)
class Finding:
    path: Path
    size_bytes: int
    severity: Severity
    recommendation: str
    reason: str
    scanner: str

    def __post_init__(self) -> None:
        if self.size_bytes < 0:
            msg = "size_bytes must be zero or greater"
            raise ValueError(msg)
        if not self.reason.strip():
            msg = "findings must explain why they were flagged"
            raise ValueError(msg)
        if not self.recommendation.strip():
            msg = "findings must include a recommendation"
            raise ValueError(msg)
        if not self.scanner.strip():
            msg = "findings must include the scanner name"
            raise ValueError(msg)
