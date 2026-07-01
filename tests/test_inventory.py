from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import pytest

from gk.inventory import (
    AppImageInventoryProvider,
    AptInventoryProvider,
    FlatpakInventoryProvider,
    InstalledApplication,
    InstallSource,
    SnapInventoryProvider,
    parse_dpkg_query_output,
    parse_flatpak_list_output,
    parse_snap_list_output,
)


def make_application(**overrides: object) -> InstalledApplication:
    values = {
        "name": "Example",
        "source": InstallSource.UNKNOWN,
        "identifier": "example",
        "version": None,
        "path": None,
    }
    values.update(overrides)
    return InstalledApplication(**values)


@pytest.mark.parametrize("field_name", ["name", "identifier"])
def test_installed_application_requires_non_empty_strings(field_name: str) -> None:
    with pytest.raises(ValueError, match=field_name):
        make_application(**{field_name: " "})


def test_parse_dpkg_query_output() -> None:
    applications = parse_dpkg_query_output(
        "bash\t5.2.21-2ubuntu4\n"
        "python3\t3.12.3-0ubuntu2\n"
        "\n"
    )

    assert [(app.name, app.identifier, app.version) for app in applications] == [
        ("bash", "bash", "5.2.21-2ubuntu4"),
        ("python3", "python3", "3.12.3-0ubuntu2"),
    ]
    assert all(app.source is InstallSource.APT for app in applications)
    assert all(app.path is None for app in applications)


def test_parse_snap_list_output() -> None:
    applications = parse_snap_list_output(
        "Name               Version          Rev    Tracking       Publisher   Notes\n"
        "firefox            127.0.2-1        4483   latest/stable  mozilla**   -\n"
        "bare               1.0              5      latest/stable  canonical** base\n"
    )

    assert [(app.name, app.identifier, app.version) for app in applications] == [
        ("firefox", "firefox", "127.0.2-1"),
        ("bare", "bare", "1.0"),
    ]
    assert all(app.source is InstallSource.SNAP for app in applications)


def test_parse_flatpak_list_output() -> None:
    applications = parse_flatpak_list_output(
        "org.mozilla.firefox\tFirefox\t127.0.2\n"
        "org.gnome.Calculator\tCalculator\t\n"
    )

    assert [(app.name, app.identifier, app.version) for app in applications] == [
        ("Firefox", "org.mozilla.firefox", "127.0.2"),
        ("Calculator", "org.gnome.Calculator", None),
    ]
    assert all(app.source is InstallSource.FLATPAK for app in applications)


def test_appimage_provider_detects_appimage_files(tmp_path: Path) -> None:
    applications_dir = tmp_path / "Applications"
    nested_dir = tmp_path / "nested" / "tools"
    applications_dir.mkdir()
    nested_dir.mkdir(parents=True)
    primary = applications_dir / "Example.AppImage"
    nested = nested_dir / "Nested.AppImage"
    ignored = applications_dir / "not-an-app.txt"
    primary.write_text("appimage")
    nested.write_text("appimage")
    ignored.write_text("text")

    applications = AppImageInventoryProvider(
        home=tmp_path,
        locations=[applications_dir],
        include_limited_home_scan=True,
        max_home_depth=2,
    ).scan()

    paths = [app.path for app in applications]
    assert paths == [primary, nested]
    assert [app.name for app in applications] == ["Example", "Nested"]
    assert all(app.source is InstallSource.APPIMAGE for app in applications)
    assert all(app.version is None for app in applications)


def test_command_providers_return_empty_lists_when_command_is_missing() -> None:
    def missing_command_runner(_args: Sequence[str], _timeout: float) -> str | None:
        return None

    assert AptInventoryProvider(command_runner=missing_command_runner).scan() == []
    assert SnapInventoryProvider(command_runner=missing_command_runner).scan() == []
    assert FlatpakInventoryProvider(command_runner=missing_command_runner).scan() == []
