from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class Category(StrEnum):
    CACHE = "cache"
    CONFIG = "config"
    APPLICATION_DATA = "application_data"
    DESKTOP_LAUNCHER = "desktop_launcher"
    PACKAGE_DATA = "package_data"
    SYSTEMD_USER = "systemd_user"
    DEVELOPMENT = "development"
    UNKNOWN = "unknown"


class Confidence(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Severity(StrEnum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True, slots=True)
class Finding:
    id: str
    title: str
    category: Category
    severity: Severity
    path: Path | None
    size_bytes: int | None
    recommendation: str
    reason: str
    scanner: str
    confidence: Confidence

    def __post_init__(self) -> None:
        require_non_empty("id", self.id)
        require_non_empty("title", self.title)
        require_non_empty("reason", self.reason)
        require_non_empty("recommendation", self.recommendation)
        require_non_empty("scanner", self.scanner)

        if self.size_bytes is not None and self.size_bytes < 0:
            msg = "size_bytes must be zero or greater"
            raise ValueError(msg)


def require_non_empty(field_name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        msg = f"{field_name} must be a non-empty string"
        raise ValueError(msg)
