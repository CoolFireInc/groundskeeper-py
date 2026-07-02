from __future__ import annotations

from collections.abc import Sequence

from rich.console import Console
from rich.table import Table

from gk.inventory import InstalledApplication
from gk.models import Finding


def format_size(size_bytes: int | None) -> str:
    if size_bytes is None:
        return "-"

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
    table.add_column("Category")
    table.add_column("Confidence")
    table.add_column("Severity", style="bold")
    table.add_column("Size", justify="right")
    table.add_column("Path", overflow="fold")
    table.add_column("Title", overflow="fold")
    table.add_column("Recommendation", overflow="fold")

    for finding in findings:
        table.add_row(
            finding.category.value,
            finding.confidence.value,
            finding.severity.value,
            format_size(finding.size_bytes),
            str(finding.path) if finding.path is not None else "-",
            finding.title,
            finding.recommendation,
        )

    console.print(table)


def render_inventory(
    applications: Sequence[InstalledApplication],
    console: Console | None = None,
) -> None:
    console = console or Console()

    if not applications:
        console.print("[green]No installed applications found.[/green]")
        return

    table = Table(title="groundsKeeper installed software inventory")
    table.add_column("Source")
    table.add_column("Name", overflow="fold")
    table.add_column("Identifier", overflow="fold")
    table.add_column("Version", overflow="fold")
    table.add_column("Path", overflow="fold")

    for application in applications:
        table.add_row(
            application.source.value,
            application.name,
            application.identifier,
            application.version or "-",
            str(application.path) if application.path is not None else "-",
        )

    console.print(table)
