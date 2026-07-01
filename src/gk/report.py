from __future__ import annotations

from collections.abc import Sequence

from rich.console import Console
from rich.table import Table

from gk.models import Finding


def format_size(size_bytes: int) -> str:
    value = float(size_bytes)
    for unit in ("B", "KiB", "MiB", "GiB"):
        if value < 1024 or unit == "GiB":
            if unit == "B":
                return f"{int(value)} {unit}"
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{value:.1f} GiB"


def render_findings(
    findings: Sequence[Finding],
    console: Console | None = None,
) -> None:
    console = console or Console()

    if not findings:
        console.print("[green]No findings.[/green]")
        return

    table = Table(title="groundsKeeper audit findings")
    table.add_column("Severity", style="bold")
    table.add_column("Size", justify="right")
    table.add_column("Path", overflow="fold")
    table.add_column("Why flagged", overflow="fold")
    table.add_column("Recommendation", overflow="fold")

    for finding in findings:
        table.add_row(
            finding.severity.value,
            format_size(finding.size_bytes),
            str(finding.path),
            finding.reason,
            finding.recommendation,
        )

    console.print(table)
