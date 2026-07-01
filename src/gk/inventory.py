from __future__ import annotations

import subprocess
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Protocol

from gk.models import require_non_empty

DEFAULT_COMMAND_TIMEOUT_SECONDS = 5.0
DEFAULT_HOME_SCAN_DEPTH = 3


class InstallSource(StrEnum):
    APT = "apt"
    SNAP = "snap"
    FLATPAK = "flatpak"
    APPIMAGE = "appimage"
    MANUAL = "manual"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class InstalledApplication:
    name: str
    source: InstallSource
    identifier: str
    version: str | None
    path: Path | None

    def __post_init__(self) -> None:
        require_non_empty("name", self.name)
        require_non_empty("identifier", self.identifier)


type CommandRunner = Callable[[Sequence[str], float], str | None]


class InventoryProvider(Protocol):
    name: str

    def scan(self) -> Sequence[InstalledApplication]:
        """Return read-only installed application inventory."""
        ...


def run_command(args: Sequence[str], timeout: float) -> str | None:
    try:
        completed = subprocess.run(
            args,
            capture_output=True,
            check=True,
            text=True,
            timeout=timeout,
        )
    except (
        FileNotFoundError,
        OSError,
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
    ):
        return None

    return completed.stdout


@dataclass(frozen=True, slots=True)
class AptInventoryProvider:
    command_runner: CommandRunner = run_command
    timeout: float = DEFAULT_COMMAND_TIMEOUT_SECONDS

    name: str = "apt"

    def scan(self) -> list[InstalledApplication]:
        output = self.command_runner(
            ["dpkg-query", "-W", "-f=${Package}\\t${Version}\\n"],
            self.timeout,
        )
        if output is None:
            return []

        return parse_dpkg_query_output(output)


@dataclass(frozen=True, slots=True)
class SnapInventoryProvider:
    command_runner: CommandRunner = run_command
    timeout: float = DEFAULT_COMMAND_TIMEOUT_SECONDS

    name: str = "snap"

    def scan(self) -> list[InstalledApplication]:
        output = self.command_runner(["snap", "list"], self.timeout)
        if output is None:
            return []

        return parse_snap_list_output(output)


@dataclass(frozen=True, slots=True)
class FlatpakInventoryProvider:
    command_runner: CommandRunner = run_command
    timeout: float = DEFAULT_COMMAND_TIMEOUT_SECONDS

    name: str = "flatpak"

    def scan(self) -> list[InstalledApplication]:
        output = self.command_runner(
            ["flatpak", "list", "--app", "--columns=application,name,version"],
            self.timeout,
        )
        if output is None:
            return []

        return parse_flatpak_list_output(output)


@dataclass(frozen=True, slots=True)
class AppImageInventoryProvider:
    home: Path | None = None
    locations: Sequence[Path] | None = None
    include_limited_home_scan: bool = True
    max_home_depth: int = DEFAULT_HOME_SCAN_DEPTH

    name: str = "appimage"

    def scan(self) -> list[InstalledApplication]:
        return scan_appimages(
            home=self.home,
            locations=self.locations,
            include_limited_home_scan=self.include_limited_home_scan,
            max_home_depth=self.max_home_depth,
        )


def parse_dpkg_query_output(output: str) -> list[InstalledApplication]:
    applications: list[InstalledApplication] = []
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue

        name, separator, version = line.partition("\t")
        if not separator:
            parts = line.split(maxsplit=1)
            if len(parts) != 2:
                continue
            name, version = parts

        applications.append(
            InstalledApplication(
                name=name,
                source=InstallSource.APT,
                identifier=name,
                version=version or None,
                path=None,
            )
        )

    return applications


def parse_snap_list_output(output: str) -> list[InstalledApplication]:
    applications: list[InstalledApplication] = []
    for line in output.splitlines():
        line = line.strip()
        if not line or line.casefold().startswith("name "):
            continue

        parts = line.split()
        if len(parts) < 2:
            continue

        applications.append(
            InstalledApplication(
                name=parts[0],
                source=InstallSource.SNAP,
                identifier=parts[0],
                version=parts[1],
                path=None,
            )
        )

    return applications


def parse_flatpak_list_output(output: str) -> list[InstalledApplication]:
    applications: list[InstalledApplication] = []
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue

        parts = line.split("\t")
        if len(parts) == 1:
            parts = line.split(maxsplit=2)

        identifier = parts[0].strip()
        name = parts[1].strip() if len(parts) > 1 and parts[1].strip() else identifier
        version = parts[2].strip() if len(parts) > 2 and parts[2].strip() else None
        if not identifier:
            continue

        applications.append(
            InstalledApplication(
                name=name,
                source=InstallSource.FLATPAK,
                identifier=identifier,
                version=version,
                path=None,
            )
        )

    return applications


def scan_appimages(
    *,
    home: Path | None = None,
    locations: Sequence[Path] | None = None,
    include_limited_home_scan: bool = True,
    max_home_depth: int = DEFAULT_HOME_SCAN_DEPTH,
) -> list[InstalledApplication]:
    home = home or Path.home()
    paths = find_appimage_paths(
        home=home,
        locations=locations,
        include_limited_home_scan=include_limited_home_scan,
        max_home_depth=max_home_depth,
    )

    return [
        InstalledApplication(
            name=path.stem,
            source=InstallSource.APPIMAGE,
            identifier=str(path),
            version=None,
            path=path,
        )
        for path in paths
    ]


def find_appimage_paths(
    *,
    home: Path,
    locations: Sequence[Path] | None = None,
    include_limited_home_scan: bool,
    max_home_depth: int,
) -> list[Path]:
    roots = locations if locations is not None else default_appimage_locations(home)
    discovered: set[Path] = set()

    for root in roots:
        discovered.update(find_appimages_under(root, max_depth=max_home_depth))

    if include_limited_home_scan:
        discovered.update(find_appimages_under(home, max_depth=max_home_depth))

    return sorted(discovered, key=lambda path: str(path).casefold())


def default_appimage_locations(home: Path) -> list[Path]:
    return [
        home / "Applications",
        home / ".local" / "bin",
        home / "bin",
        Path("/usr/local/bin"),
        Path("/opt"),
    ]


def find_appimages_under(root: Path, *, max_depth: int) -> Iterable[Path]:
    if max_depth < 0 or not root.exists():
        return []

    if root.is_file():
        return [root] if is_appimage(root) else []

    found: list[Path] = []
    stack: list[tuple[Path, int]] = [(root, 0)]
    while stack:
        current, depth = stack.pop()
        try:
            children = list(current.iterdir())
        except OSError:
            continue

        for child in children:
            if child.is_symlink():
                continue
            if child.is_file() and is_appimage(child):
                found.append(child)
            elif child.is_dir() and depth < max_depth:
                stack.append((child, depth + 1))

    return found


def is_appimage(path: Path) -> bool:
    return path.name.casefold().endswith(".appimage")


def collect_inventory(
    providers: Iterable[InventoryProvider] | None = None,
) -> list[InstalledApplication]:
    if providers is None:
        providers = default_inventory_providers()

    applications: list[InstalledApplication] = []
    for provider in providers:
        try:
            applications.extend(provider.scan())
        except Exception:
            continue

    return sorted(
        applications,
        key=lambda app: (
            app.source.value,
            app.name.casefold(),
            app.identifier.casefold(),
        ),
    )


def default_inventory_providers() -> list[InventoryProvider]:
    return [
        AptInventoryProvider(),
        SnapInventoryProvider(),
        FlatpakInventoryProvider(),
        AppImageInventoryProvider(),
    ]
