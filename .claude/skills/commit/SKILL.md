---
description: Stage and commit changes with a conventional commit message. Use when the user asks to commit, create a commit, or save changes to git.
argument-hint: "[#<issue>] [--no-verify]"
disable-model-invocation: true
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git commit:*)
---

# Commit

Arguments: $ARGUMENTS

## Argument parsing
- If `$ARGUMENTS` contains `#` followed by digits (e.g. `#15`), treat that as a GitHub issue reference and include it in the commit subject as a prefix: `#15 - type: description`
- If `$ARGUMENTS` contains `--no-verify`, pass `--no-verify` to `git commit`
- Both can be combined: `/commit #15 --no-verify`

## Commit types
Choose the single best type for the change:

| Emoji | Type | Use for |
|-------|------|---------|
| ✨ | `feat` | New feature or capability |
| 🐛 | `fix` | Bug fix |
| 📝 | `docs` | Documentation only |
| ♻️ | `refactor` | Restructuring without behaviour change |
| 🎨 | `style` | Formatting, naming, no logic change |
| ⚡️ | `perf` | Performance improvement |
| ✅ | `test` | Adding or fixing tests |
| 🧹 | `chore` | Tooling, config, dependencies |
| 🔥 | `remove` | Deleting code or files |
| 🚑 | `hotfix` | Critical production fix |
| 🔒 | `security` | Security improvement |

## Process

1. Run `git status` and `git diff` to understand what changed
2. If nothing is staged, review unstaged files and stage the appropriate ones with `git add`
3. Determine the commit type and an optional scope from the diff
4. Draft the subject line:
   - With issue: `#N - emoji type(scope): short description`
   - Without issue: `emoji type(scope): short description`
   - Max 72 characters, imperative mood ("Add" not "Added")
5. Add a blank line and a short body paragraph only when the *why* is non-obvious
6. Commit — use `--no-verify` only if that flag was in `$ARGUMENTS`

## Rules
- No Claude co-authorship footer
- No trailing period on the subject line
- Scope is optional; use it when the change is clearly scoped to one module/area
- Keep commits atomic — if the diff mixes unrelated concerns, say so and ask whether to split