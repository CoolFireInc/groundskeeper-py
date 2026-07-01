# Architecture

## Overview

groundsKeeper is a Python CLI application for conservative Linux workstation
health auditing. Its executable is `gk`.

The project exists to help users understand the state of their home directory
and workstation environment before taking action. It is not primarily a cleanup
utility. Cleanup may become part of the system later, but the foundation is
audit, explanation, and reversible maintenance.

The core philosophy is:

- Audit first.
- Understand before acting.
- Preserve user data.
- Never delete when quarantine is possible.
- Read-only by default.
- Every recommendation must explain why.
- Every destructive operation must be reversible.

## Design Goals

### Safety

groundsKeeper must avoid destructive behavior by default. Scanners only inspect
the system and return findings. They do not delete, move, rewrite, or repair
files.

Future cleanup behavior must be explicit, reversible, and logged. When cleanup
is possible, quarantine should be preferred over deletion.

### Transparency

Every finding and recommendation must explain why it exists. A user should be
able to understand what was flagged, where it was found, how confident the tool
is, and what the recommended next step means.

### Modularity

The project is organized around independent scanners. Each scanner owns one
domain of knowledge and returns structured findings. Reporting, cleanup, and
storage are separate concerns.

### Extensibility

New scanners should be easy to add without changing the CLI or report logic.
Future plugin support should allow third-party scanners and reports to integrate
with the same finding model.

### Performance

Audits should avoid unnecessary full-disk traversal. Scanners should inspect
well-known locations, skip irrelevant paths quickly, and report partial results
where appropriate instead of failing an entire audit.

### Cross-Distribution Compatibility

Linux distributions vary in packaging systems, desktop environments, service
layouts, and user conventions. groundsKeeper should avoid hard-coded
distribution assumptions where possible and prefer feature detection,
well-known standards, and conservative heuristics.

## Layers

The high-level architecture is:

```text
CLI
  ↓
Scanner Framework
  ↓
Scanners
  ↓
Finding Model
  ↓
Reports
  ↓
Future Cleanup Engine
```

### CLI

The CLI is the user entry point exposed as `gk`. It parses options, selects
scanners, runs audits, and chooses report output.

The CLI should stay thin. It should not contain scanner-specific logic or cleanup
implementation details.

### Scanner Framework

The scanner framework defines the contract that all scanners follow. It provides
the structure for running one or more scanners and collecting their findings.

The framework should allow scanners to be added, selected, skipped, grouped, and
eventually loaded from plugins.

### Scanners

Scanners inspect specific areas of the system. They never modify files, never
print directly, and never perform cleanup.

Only the future cleanup engine may make changes.

### Finding Model

Findings are the shared data structure between scanners, reports, history, and
future cleanup actions. Scanners return findings instead of producing text or
side effects.

### Reports

Reports convert findings into user-facing output. Reports are independent from
scanners, so the same findings can be rendered as terminal output, HTML, JSON,
Markdown, or other formats.

### Future Cleanup Engine

The cleanup engine is a future component that consumes findings and performs
explicit maintenance actions. It should not be coupled to scanner internals.

## Scanner Design

Each scanner is independent and focused on one domain. Examples include:

- `CacheScanner`
- `DesktopLauncherScanner`
- `SnapScanner`
- `FlatpakScanner`
- `JetBrainsScanner`
- `ThunderbirdScanner`
- `KDEScanner`
- `BrowserScanner`
- `ApacheScanner`
- `PHPScanner`
- `MariaDBScanner`

Every scanner returns `Finding` objects.

Scanner rules:

- Scanners never print directly.
- Scanners never modify files.
- Scanners never delete, move, repair, or rewrite data.
- Scanners should explain why each finding was created.
- Scanners should handle missing paths and permission errors conservatively.
- Scanners should keep domain-specific assumptions local to the scanner.

This design allows scanners to evolve independently while keeping the rest of
the application stable.

## Finding Model

The finding model is the central contract of the project. Every finding should
contain enough information for a user, report, cleanup plan, or history database
to understand what was discovered.

A mature finding should contain information such as:

- `id`
- `title`
- `description`
- `severity`
- `category`
- `path`
- `size`
- `recommendation`
- `scanner`
- `confidence`

Every finding must explain why it exists. A finding without a reason is not
actionable enough for groundsKeeper.

The model should support future cleanup without requiring scanners to know how
cleanup works. For example, a scanner may identify a stale cache directory, but
it should not decide how quarantine, restore, or deletion are implemented.

## Reporting

Reports are independent of scanners. They receive findings and render them for a
specific audience or toolchain.

Supported and planned report formats include:

- Rich terminal output
- HTML
- JSON
- Markdown

The Rich terminal report is the default interactive format. JSON should provide
machine-readable output for scripts and automation. HTML and Markdown reports can
support review, sharing, and historical comparison.

## Cleanup Engine

The cleanup engine is a future component. It consumes findings and performs
explicit, user-approved actions such as:

- cache cleanup
- launcher repair
- quarantine
- restore

No scanner should know how cleanup works. Scanners describe what they found;
cleanup actions decide what can be done safely.

The cleanup engine should support dry runs, explicit confirmation, operation
logs, restore metadata, and never-touch rules.

## Quarantine

Quarantine is the preferred safety mechanism for potentially destructive
maintenance.

Everything should move before deletion. Nothing is permanently deleted
immediately. Each move is logged with enough metadata to support restore.

A quarantine record should include the original path, quarantine path, timestamp,
scanner or cleanup action that requested the move, and enough context to explain
why the move occurred.

## Logging

groundsKeeper should eventually use a SQLite database for local history.

The database should store:

- audit history
- quarantine history
- restore history
- cleanup history

History allows users to understand what changed over time, compare audits, and
reverse maintenance actions when needed.

## Guiding Principles

- Read-only by default.
- Explain every recommendation.
- Prefer moving over deleting.
- Avoid distribution-specific assumptions.
- Favor correctness over aggressiveness.
- Preserve user data.
- Keep scanners independent.
- Keep cleanup reversible.
