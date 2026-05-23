# Cross-Boundary Registries

## What are boundaries?

A **boundary** is anywhere two pieces of code, config, or infrastructure refer to the same name independently and can disagree. Examples:

- A SQLite table named in a schema creation script AND referenced in a query — if one renames the table, the other breaks silently.
- An environment variable read by `db.py` but never documented — operators set the wrong name and get a cryptic error.
- A CLI command declared in `pyproject.toml` but implemented with a different name in `cli.py` — the entry point is dead on install.

Registries make every such name explicit: who produces it, who consumes it, what shape it has, and whether they agree.

## Registries in this project

| File | Boundary kind | What it tracks |
|------|--------------|----------------|
| `tables.md` | SQLite tables | Table names, column schemas, FK relationships, CSV export contract |
| `cli-commands.md` | CLI entry points | Typer commands declared in pyproject.toml and implemented in cli.py |
| `env-vars.md` | Environment variables | Config vars, defaults, required/optional, who reads them |

## Rules

1. **Every PR that touches a cross-boundary name must update the relevant registry in the same commit.** Adding a table? Update `tables.md`. Adding an env var? Update `env-vars.md`. Renaming a CLI command? Update `cli-commands.md`.

2. **Each registry includes an Audit Trail section** showing the last `/cross-boundary-audit` run, counts of verified entries, and any gaps found.

3. **Run `/cross-boundary-audit` after finishing a task** to verify code matches the registries. The audit also runs as part of `/finish-build`.

4. **Gaps are not blockers by default** — an `⚠ planned` entry means the name is registered but code hasn't landed yet. An `⚠ orphan` or `⚠ shape mismatch` means code exists but disagreed — that needs a fix before merge.

## Detected by

These boundary kinds were detected by `/cross-boundary-audit` on 2026-05-23 (Task #2 pre-code audit). As the project grows, new kinds may be added — REST endpoints when the API layer is built, event names when async jobs are introduced, etc.
