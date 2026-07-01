from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from gk import __version__
from gk.audit import run_audit
from gk.inventory import collect_inventory
from gk.report import render_findings, render_inventory
from gk.scanners.cache import CacheDirectoryScanner

app = typer.Typer(
    help="Conservative Linux home-directory health and audit tool.",
    no_args_is_help=True,
)
console = Console()


@app.command()
def version() -> None:
    """Print the installed gk version."""
    console.print(__version__)


@app.command()
def audit(
    home: Annotated[
        Path | None,
        typer.Option(
            "--home",
            help=(
                "Home directory to audit. "
                "Defaults to the current user's home directory."
            ),
        ),
    ] = None,
) -> None:
    """Run a read-only home-directory audit."""
    scanner = CacheDirectoryScanner(home=home)
    findings = run_audit([scanner])
    render_findings(findings, console=console)


@app.command()
def inventory() -> None:
    """Print a read-only installed software inventory."""
    applications = collect_inventory()
    render_inventory(applications, console=console)
