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

**Supported file formats:** `.txt`, `.csv`, `.json`, `.pdf`, `.docx`, `.xlsx`, `.pptx`, `.doc`, `.png`, `.jpg`, `.jpeg`, `.tiff`, `.tif`, `.bmp`, `.gif`

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

## `scanmenow benchmark` ⚠ planned (Task #4)

Run the benchmark accuracy gate against an independent corpus. Reads golden findings from the corpus, runs the detection engine, and reports recall/precision per entity type.

**Arguments / options:**
- `--corpus PATH` / `-c PATH` — corpus directory; overrides `SCANMENOW_CORPUS_PATH` env var
- `--format csv|json` / `-f` — report output format (default: `json`)
- `--output FILE` / `-o FILE` — write report to file (default: stdout)
- `--threshold-file PATH` — override `docs/benchmark_thresholds.json` (default: repo path)

**Environment variable:** `SCANMENOW_CORPUS_PATH` — persistent corpus path; `--corpus` overrides per-run

**Graceful skip:** If neither `--corpus` nor `SCANMENOW_CORPUS_PATH` is set, exits 0 with "corpus not found — skipping benchmark" (CI-safe).

**Declaration (producer)**
- `src/scanmenow/cli.py` — `@app.command()` Typer subcommand ⚠ planned Task #4

**Implementation (producer)**
- `src/scanmenow/benchmark/runner.py` — `run_benchmark()` ⚠ planned Task #4
- `src/scanmenow/benchmark/report.py` — `render_report()` ⚠ planned Task #4
- `docs/benchmark_thresholds.json` — per-label recall thresholds (Task #4 owns, already written)

**Consumers**
- `tests/test_benchmark.py` — CI accuracy gate ⚠ planned Task #4

**Status:** ⚠ planned — Task #4; not yet implemented

---

## `scanmenow retain` ⚠ planned (Task #8)

Age-based retention policy evaluation and enforcement. Queries findings older than a threshold and either reports them (dry-run) or deletes them (live mode).

**Arguments / options:**
- `--max-age-days N` — findings older than N days are considered expired (default: 90)
- `--dry-run` — report expired findings without deleting (default)
- `--confirm` — delete expired findings after printing count and warning

**Declaration (producer)**
- `src/scanmenow/cli.py` — `@app.command()` Typer subcommand ⚠ planned Task #8

**Implementation (producer)**
- `src/scanmenow/retention/evaluator.py` — `evaluate_retention()` ⚠ planned Task #8
- `src/scanmenow/retention/policy.py` — `RetentionPolicy`, `RetentionReport` ⚠ planned Task #8
- `src/scanmenow/storage/base.py` — `get_repository()` factory ⚠ planned Task #8

**Consumers**
- `tests/test_retention.py` ⚠ planned Task #8

**Status:** ⚠ planned — Task #8; not yet implemented

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
| `scanmenow benchmark` | cli.py (planned) | benchmark/runner.py (planned) | ⚠ planned Task #4 |
| `scanmenow retain` | cli.py (planned) | retention/evaluator.py (planned) | ⚠ planned Task #8 |
| `scanmenow reduce` | — | — | ⚠ placeholder — Phase 2 |

---

## Audit Trail — Proof of Registry Verification

**Last audit:** 2026-05-27T00:00:00Z (by /cross-boundary-audit — pre-build plan validation for Task #5)
**Correction:** 2026-05-27 (orchestrator cross-session sync — added TIFF/BMP formats and benchmark command)

**Boundaries checked:** CLI entry points (verified against Task #5 plan — `scanmenow scan` pre-registered with full argument spec; `scanmenow benchmark` pre-registered per Task #4 backlog contracts)

**Evidence recorded:**
- 1 entry with complete producer/consumer pairs ✓ (`scanmenow` root — unchanged)
- 0 shape mismatches
- New identifiers introduced on Task #5 (pre-registered): `scanmenow scan <path>` with full argument spec
- New identifiers introduced on Task #4 (pre-registered): `scanmenow benchmark` with `--corpus`, `--format`, `--output`, `--threshold-file` args
- Registries match current code diff: ✓ (current code) · ⚠ `scanmenow scan` and `scanmenow benchmark` pre-registered, not yet in code

**Corrections applied:**
- `scanmenow scan` supported formats: added `.tiff`, `.tif`, `.bmp` (backlog correction `6f57cfce` stated these are required; cross-boundary-audit missed them)
- `scanmenow benchmark` pre-registered (Task #4 backlog contract references `--corpus` flag and `SCANMENOW_CORPUS_PATH`; was not in registry)

**Status:** ✓ Audit complete (pre-build plan validation for Task #5) + orchestrator corrections applied

**Task #9 audit note (2026-05-27T00:00:00Z):** Task #9 adds no CLI commands. Registry verified — no changes needed.
