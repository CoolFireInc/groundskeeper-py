# groundsKeeper

`groundsKeeper` is a conservative Linux home-directory health and audit tool.
The CLI command is `gk`.

The first implementation is intentionally read-only. It reports findings and
explains why each one was flagged, but it does not delete, move, or clean files.

## Commands

```bash
gk version
gk audit
gk inventory
```

`gk audit` currently scans application cache directories directly under
`~/.cache` and reports non-empty cache directories with:

- path
- size
- severity
- reason
- recommendation

Future scanners can be added for areas such as desktop launchers, Snap,
Flatpak, JetBrains, Thunderbird, KDE, AppImages, and other home-directory
health checks.

`gk inventory` prints a read-only table of installed software found from
available package and app sources:

- APT packages from `dpkg-query`
- Snap packages from `snap list`
- Flatpak apps from `flatpak list --app`
- AppImage files in common application locations

If a source is unavailable or cannot be read, it is skipped without modifying
the system.

## Development

```bash
python -m pip install -e ".[dev]"
uv run pytest
uv run ruff check .
uv run gk inventory
```

## Safety

The project defaults to read-only behavior. Cleanup actions should only be
introduced after audit findings are precise, explainable, and tested.
