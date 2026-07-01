# Roadmap

This roadmap describes the planned development path for groundsKeeper as a
Linux workstation health and maintenance platform.

## Milestone 0: Foundation

Establish the project structure, CLI, and testable scanner architecture.

- CLI
- Finding model
- Scanner framework
- Tests
- CI

## Milestone 1: Inventory

Build an inventory of installed and user-managed software sources.

- APT
- Snap
- Flatpak
- AppImages
- Manual installs

## Milestone 2: Filesystem Audit

Add scanners for common home-directory health issues.

- Cache scanner
- Config scanner
- Desktop launchers
- Broken symlinks
- Autostart
- Systemd user services

## Milestone 3: Application Intelligence

Add application-aware scanners for large, complex, or commonly stale user data.

- JetBrains
- Thunderbird
- Chrome
- Firefox
- FreeCAD
- VS Code
- Claude
- Docker

## Milestone 4: Developer Environment

Add scanners for developer workstation services, runtimes, and local
development state.

- Apache
- Nginx
- PHP
- PHP-FPM
- MariaDB
- PostgreSQL
- Python virtual environments
- Node
- Rust
- Go

## Milestone 5: Reporting

Expand reporting from terminal output into structured and historical formats.

- Rich
- HTML
- JSON
- Markdown
- Statistics
- Historical comparisons

## Milestone 6: Safe Cleanup

Introduce explicit, reversible maintenance actions after audit quality is
established.

- Quarantine
- Restore
- Cache cleanup
- Launcher repair
- Remove orphan data
- Never-touch rules

## Milestone 7: Configuration

Allow users and teams to tune scanner behavior without changing code.

- User config file
- Custom rules
- Ignore lists
- Profiles

## Milestone 8: Plugins

Open the scanner and reporting systems to extension outside the core project.

- Plugin API
- Third-party scanners
- Custom reports

## Milestone 9: GUI (Optional)

Explore a graphical frontend for users who prefer interactive inspection and
maintenance workflows.

- Qt/KDE frontend
- Dashboard
- Interactive cleanup
- Historical charts

## Long-Term Vision

groundsKeeper should become a Linux workstation health and maintenance platform,
not simply a cleanup utility.

The project should help users understand what is installed, what is stale, what
is misconfigured, what is consuming space, and what can be safely improved. Its
value should come from careful inspection, transparent recommendations,
reversible operations, and historical context.

Over time, groundsKeeper can provide a unified view across package managers,
desktop integration, application state, developer services, caches, launchers,
and local databases. The goal is a tool that helps maintain a workstation with
the caution expected for personal data and the structure expected from mature
open-source infrastructure.
