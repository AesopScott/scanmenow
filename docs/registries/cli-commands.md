# CLI Commands Registry

Every command exposed by the `scanmenow` CLI entry point. For each: declaration site, implementation site, arguments, status. Update whenever a command is added, removed, or its arguments change.

**Entry point:** `scanmenow` — declared in `pyproject.toml [project.scripts]`, implemented via Typer in `src/scanmenow/cli.py`.

**Runtime:** `uv run scanmenow <command>` (development). Future: embedded Python subprocess called from Electron UI.

---

## `scanmenow` (root command)

The root Typer app. Provides `--help` and version info. Parent for all subcommands.

**Arguments / options:**
- `--help` — prints usage and available subcommands
- `--version` — prints package version (optional, add if useful)

**Declaration (producer)**
- `pyproject.toml:[project.scripts]` — `scanmenow = "scanmenow.cli:app"`

**Implementation (producer)**
- `src/scanmenow/cli.py` — `app = typer.Typer()`

**Consumers**
- `tests/test_cli.py` — `uv run scanmenow --help` smoke test (Proof Unit 1)
- Future: Electron subprocess bridge calls `scanmenow <subcommand>`

**Status:** ✓ implemented — `pyproject.toml` declares the entry point; `cli.py` implements the root `app` with `--version` (`-v`) and `--help`. `no_args_is_help=True` set.

---

## Future subcommands (not in Task #2 scope)

The following subcommands are documented here as placeholders to prevent naming collisions. They will be registered as planned tasks complete.

| Command | Planned in | Description |
|---------|------------|-------------|
| `scanmenow scan <path>` | Task #5+ | Run a scan against a local directory |
| `scanmenow reduce --mode dry-run` | Task Phase 2 | Dry-run reduction pass |
| `scanmenow reduce --out <dir>` | Task Phase 2 | Write redacted output |

---

## Summary

| Command | Declared | Implemented | Status |
|---------|----------|-------------|--------|
| `scanmenow` (root) | pyproject.toml | cli.py | ✓ implemented |

---

## Audit Trail — Proof of Registry Verification

**Last audit:** 2026-05-23T00:00:00Z (updated by /finish-build — post-code verification)

**Boundaries checked:** CLI entry points (post-code verification against shipped implementation)

**Evidence recorded:**
- 1 entry with complete producer/consumer pairs ✓ (code shipped and smoke-tested)
- 0 shape mismatches
- New identifiers introduced on task #2: `scanmenow` entry point
- Registries match current code diff: ✓ verified (Proof Unit 1 passes — exit 0, help text present)

**Gaps identified:** none

**Status:** ✓ Audit complete (post-code)
