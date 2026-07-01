from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from gk.models import Finding


class Scanner(Protocol):
    name: str

    def scan(self) -> Sequence[Finding]:
        """Return read-only audit findings."""
        ...
