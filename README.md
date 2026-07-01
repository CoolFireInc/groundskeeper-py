# groundsKeeper

`groundsKeeper` is a conservative Linux home-directory health and audit tool.
The CLI command is `gk`.

The first implementation is intentionally read-only. It reports findings and
explains why each one was flagged, but it does not delete, move, or clean files.

## Commands

```bash
gk version
gk audit
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

## Development

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
```

## Safety

The project defaults to read-only behavior. Cleanup actions should only be
introduced after audit findings are precise, explainable, and tested.
