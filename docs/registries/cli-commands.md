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

## `scanmenow scan <path>` ⚠ planned (Task #5)

Scan a local directory or file for PHI/PII. Walks the filesystem, reads all supported file formats, runs detection, and persists findings to SQLite.

**Arguments / options:**
- `<path>` — *(required)* directory or file to scan
- `--depth N` / `-d N` — maximum traversal depth (default: unlimited)
- `--skip PATTERN` / `-s PATTERN` — additional glob skip pattern; repeatable; merged with defaults
- `--follow-symlinks` — follow symbolic links (default: skip symlinks)
- `--include-hidden` — include hidden files and directories (default: skip)
- `--output FILE` / `-o FILE` — export findings to this path after scan completes
- `--format csv|json` / `-f` — export format when `--output` is given (default: `csv`)

**Default skip patterns** (applied before `--skip` additions):
`.git`, `__pycache__`, `.venv`, `node_modules`, `dist`, `build`, `*.pyc`, `*.log`, `*.tmp`

**Supported file formats:** `.txt`, `.csv`, `.json`, `.pdf`, `.docx`, `.xlsx`, `.pptx`, `.doc`, `.png`, `.jpg`, `.jpeg`, `.gif`

**Output behavior:** Silent during scan; prints a progress line only for files with findings. Prints summary table at end (files scanned, files with findings, total findings, job ID, DB path).

**Declaration (producer)**
- `src/scanmenow/cli.py` — `@app.command()` Typer subcommand ⚠ planned Task #5

**Implementation (producer)**
- `src/scanmenow/scanner.py` — `run_scan()` ⚠ planned Task #5
- `src/scanmenow/walker/walker.py` — `FileSystemWalker` ⚠ planned Task #5
- `src/scanmenow/walker/reader.py` — `read_file_text()` ⚠ planned Task #5

**Consumers**
- `tests/test_cli_scan.py` — CLI integration test ⚠ planned Task #5
- Future: Electron subprocess bridge calls `scanmenow scan <path>`

**Status:** ⚠ planned — Task #5; not yet implemented

---

## Future subcommands (post-Task #5)

| Command | Planned in | Description |
|---------|------------|-------------|
| `scanmenow reduce --mode dry-run` | Task Phase 2 | Dry-run reduction pass |
| `scanmenow reduce --out <dir>` | Task Phase 2 | Write redacted output |

---

## Summary

| Command | Declared | Implemented | Status |
|---------|----------|-------------|--------|
| `scanmenow` (root) | pyproject.toml | cli.py | ✓ implemented |
| `scanmenow scan <path>` | cli.py (planned) | scanner.py, walker/ (planned) | ⚠ planned Task #5 |
| `scanmenow reduce` | — | — | ⚠ placeholder — Phase 2 |

---

## Audit Trail — Proof of Registry Verification

**Last audit:** 2026-05-27T00:00:00Z (by /cross-boundary-audit — pre-build plan validation for Task #5)

**Boundaries checked:** CLI entry points (verified against Task #5 plan — `scanmenow scan` pre-registered with full argument spec)

**Evidence recorded:**
- 1 entry with complete producer/consumer pairs ✓ (`scanmenow` root — unchanged)
- 0 shape mismatches
- New identifiers introduced on Task #5 (pre-registered): `scanmenow scan <path>` with full argument spec
- Registries match current code diff: ✓ (current code) · ⚠ `scanmenow scan` pre-registered, not yet in code

**Gaps identified:** none in current code; `scanmenow scan` pre-registered for Task #5 build

**Status:** ✓ Audit complete (pre-build plan validation for Task #5)
