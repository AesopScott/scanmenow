# Environment Variables Registry

Every environment variable used in this project. For each: who sets it, who reads it, required vs optional, default value. Update whenever a variable is added, removed, renamed, or its semantics change.

---

## `SCANMENOW_DB_PATH`

Path to the SQLite `.db` file where scan jobs and findings are persisted.

**Type:** string (file path)
**Required:** no — falls back to default
**Default:** `~/.scanmenow/scanmenow.db` (recommended — create parent dir on first run)
**Example:** `/var/data/scanmenow/scans.db` (MochaHost server path)

**Producers (who sets it)**
- Shell / `.env` file — operator sets before running the app
- Future: Electron app settings UI writes a `.env` or passes it to the Python subprocess

**Consumers (who reads it)**
- `src/scanmenow/storage/db.py` — `init_db()` reads this to determine the DB file location

**Adjacent constraint — Default implemented:** `db.py` defines `DEFAULT_DB_PATH = Path.home() / ".scanmenow" / "scanmenow.db"`. `get_db_path()` returns this when `SCANMENOW_DB_PATH` is absent. Parent directory is created automatically on first connection.

**Status:** ✓ implemented

---

## `SCANMENOW_LOG_LEVEL`

Controls logging verbosity for the Python backend.

**Type:** string (one of `DEBUG`, `INFO`, `WARNING`, `ERROR`)
**Required:** no
**Default:** `INFO`
**Example:** `DEBUG` (for development), `WARNING` (for production)

**Producers (who sets it)**
- Shell / `.env` file — operator sets before running
- Future: Electron settings panel

**Consumers (who reads it)**
- `src/scanmenow/__init__.py` or `src/scanmenow/cli.py` — configures Python `logging` module at startup

**Status:** ⚠ **MANDATORY for Task #5** — no code consumer exists anywhere; carried 4 consecutive audits (Tasks #2, #3, #9, #5). cli.py is being modified in Task #5 to add `scanmenow scan` — this is the last natural opportunity. Must be wired at `cli.py` startup before `/finish-build` on Task #5. Do not carry to Task #6+.

---

## `TESSERACT_CMD`

Overrides the Tesseract OCR binary path used by `pytesseract`. Required on Windows where Tesseract is not on `PATH` by default.

**Type:** string (file path)
**Required:** no — falls back to platform default
**Default (Windows):** `C:\Program Files\Tesseract-OCR\tesseract.exe`
**Default (Linux):** resolved from `PATH` (`/usr/bin/tesseract` or equivalent)
**Example:** `C:\Program Files\Tesseract-OCR\tesseract.exe`

**Producers (who sets it)**
- Shell / `.env` file — operator sets if Tesseract is installed at a non-default path
- Future: Electron settings UI or dependency bootstrapper (Task #12)

**Consumers (who reads it)**
- `src/scanmenow/walker/reader.py` — `_read_image()` and `_read_image_pdf()` set `pytesseract.pytesseract.tesseract_cmd` from this var ⚠ planned Task #5

**Adjacent constraint — Graceful fallback:** If Tesseract binary is not found at the resolved path, `reader.py` logs a `WARNING` and returns `""` for image files rather than raising. Scan continues; image files are counted as skipped.

**Status:** ⚠ planned — Task #5; env var documented pre-build so registry is ready before code lands

---

## `LIBREOFFICE_CMD`

Overrides the LibreOffice headless binary path used for `.doc` legacy file extraction.

**Type:** string (file path)
**Required:** no — falls back to platform default
**Default (Windows):** `C:\Program Files\LibreOffice\program\soffice.exe`
**Default (Linux):** `/usr/bin/soffice` (or resolved from `PATH`)
**Example:** `/opt/libreoffice7.6/program/soffice`

**Producers (who sets it)**
- Shell / `.env` file — operator sets if LibreOffice is installed at a non-default path
- Future: Electron settings UI or dependency bootstrapper (Task #12)

**Consumers (who reads it)**
- `src/scanmenow/walker/reader.py` — `_read_doc()` resolves LibreOffice binary via this var before running headless subprocess ⚠ planned Task #5

**Adjacent constraint — Graceful fallback:** If LibreOffice binary is not found at the resolved path, `reader.py` logs a `WARNING` and returns `""` for `.doc` files rather than raising. Scan continues; `.doc` files are counted as skipped.

**Adjacent constraint — System dependency:** LibreOffice is a system-level binary, not a pip package. Installation is the responsibility of the end user or the dependency bootstrapper (Task #12). Unlike Python packages, it cannot be installed via `uv add`.

**Status:** ⚠ planned — Task #5; env var documented pre-build so registry is ready before code lands

---

## `SCANMENOW_CORPUS_PATH`

Path to the independent benchmark corpus directory produced by Task H.

**Type:** string (directory path)
**Required:** no — benchmark runner skips gracefully if unset (CI does not fail on missing corpus)
**Default:** none — must be set explicitly or overridden by `--corpus` CLI argument
**Example:** `/data/scanmenow-corpus` or `./corpus`

**Producers (who sets it)**
- Shell / `.env` file — operator sets before running benchmarks
- CI pipeline — sets to mounted corpus path for accuracy gate runs

**Consumers (who reads it)**
- `src/scanmenow/benchmark/runner.py` — reads at startup to locate corpus; falls back to `--corpus` CLI arg; skips benchmark gracefully if neither is set ⚠ planned Task #4

**Adjacent constraint — Graceful CI skip:** If `SCANMENOW_CORPUS_PATH` is unset and no `--corpus` arg is given, the benchmark runner must exit 0 with a clear "corpus not found, skipping" message rather than failing. This allows CI to run without a corpus during Tasks #3/#5/#9 build phases.

**Adjacent constraint — CLI override:** `scanmenow benchmark --corpus <path>` overrides `SCANMENOW_CORPUS_PATH` for a single run. The env var is the persistent default; the CLI arg is the per-run override.

**Status:** ⚠ planned — Task #4; env var documented pre-build so registry is ready before code lands

---

## `SCANMENOW_BACKEND`

Selects the storage backend — SQLite (local, default) or Firestore (cloud).

**Type:** string (`sqlite` | `firestore`)
**Required:** no
**Default:** `sqlite`
**Example:** `firestore` (for cloud deployment)

**Producers (who sets it)**
- Shell / `.env` file — operator sets for cloud deployment
- Future: Electron settings UI

**Consumers (who reads it)**
- `src/scanmenow/storage/base.py` — `get_repository()` factory routes on this value ⚠ planned Task #8

**Adjacent constraint — Lazy Firestore import:** `FirestoreRepository` (and `google-cloud-firestore`) must not be imported unless `SCANMENOW_BACKEND=firestore`. SQLite mode must work with no GCP credentials and without the Firestore package installed.

**Status:** ⚠ planned — Task #8; env var documented pre-build

---

## `SCANMENOW_FIRESTORE_PROJECT`

GCP project ID used when the Firestore backend is active.

**Type:** string (GCP project ID)
**Required:** yes if `SCANMENOW_BACKEND=firestore`; ignored otherwise
**Default:** none
**Example:** `my-gcp-project-12345`

**Producers (who sets it)**
- Shell / `.env` file — operator sets for cloud deployment
- CI pipeline sets for integration testing

**Consumers (who reads it)**
- `src/scanmenow/cloud/client.py` — `get_firestore_client()` reads this to initialize the Firestore client ⚠ planned Task #8
- Raises `RuntimeError` with actionable message if missing when Firestore backend is requested

**Status:** ⚠ planned — Task #8; env var documented pre-build

---

## `GOOGLE_APPLICATION_CREDENTIALS`

Standard GCP authentication env var pointing to a service account JSON key file.

**Type:** string (file path)
**Required:** yes for production Firestore; not required in dev if using `gcloud auth application-default login`
**Default:** GCP SDK default credential resolution
**Example:** `/secrets/gcp-sa.json`

**Producers (who sets it)**
- Shell / CI pipeline — standard GCP authentication setup
- This is a GCP-standard variable, not ScanMeNow-specific

**Consumers (who reads it)**
- `src/scanmenow/cloud/client.py` — `google-cloud-firestore` SDK reads this automatically ⚠ planned Task #8

**Status:** ⚠ planned — Task #8; standard GCP variable, not set or owned by ScanMeNow directly

---

## Summary

| Variable | Required | Default | Consumers | Status |
|----------|----------|---------|-----------|--------|
| `SCANMENOW_DB_PATH` | no | `~/.scanmenow/scanmenow.db` | storage/db.py | ✓ implemented |
| `SCANMENOW_LOG_LEVEL` | no | `INFO` | cli.py or __init__.py | ⚠ planned — not yet consumed (3rd carry) |
| `TESSERACT_CMD` | no | platform-detected | walker/reader.py (planned) | ⚠ planned Task #5 |
| `LIBREOFFICE_CMD` | no | platform-detected | walker/reader.py (planned) | ⚠ planned Task #5 |
| `SCANMENOW_CORPUS_PATH` | no | none (skips gracefully) | benchmark/runner.py (planned) | ⚠ planned Task #4 |
| `SCANMENOW_BACKEND` | no | `sqlite` | storage/base.py (planned) | ⚠ planned Task #8 |
| `SCANMENOW_FIRESTORE_PROJECT` | no | none (required if backend=firestore) | cloud/client.py (planned) | ⚠ planned Task #8 |
| `GOOGLE_APPLICATION_CREDENTIALS` | no | GCP default | cloud/client.py (planned) | ⚠ planned Task #8 (GCP standard var) |

---

## Audit Trail — Proof of Registry Verification

**Last audit:** 2026-05-27T00:00:00Z (by /cross-boundary-audit — pre-build plan validation for Task #5)

**Boundaries checked:** Environment variables (verified against Task #5 plan — TESSERACT_CMD and LIBREOFFICE_CMD pre-registered)

**Evidence recorded:**
- 1 entry fully implemented ✓ (`SCANMENOW_DB_PATH` — unchanged)
- 1 entry still unimplemented ⚠ (`SCANMENOW_LOG_LEVEL` — carried forward 3rd time; no code consumer exists)
- 2 new entries pre-registered ⚠ (`TESSERACT_CMD`, `LIBREOFFICE_CMD` — planned Task #5, not yet in code)
- 0 shape mismatches
- Registries match current code diff: ✓ (current code) · ⚠ 2 new vars pre-registered for Task #5

**Soft flags (previous audit):**
- `SCANMENOW_LOG_LEVEL` carried 3 consecutive audits without being wired. Recommended: implement in cli.py startup in Task #5.

**Status:** ✓ Audit complete (pre-build plan validation for Task #5)

**Task #9 audit note (2026-05-27T00:00:00Z):** Task #9 adds no environment variables. Registry verified — no changes needed. `SCANMENOW_LOG_LEVEL` now carried 4 consecutive audits — flagged for mandatory resolution in Task #5.

---

**Build-start audit — 2026-05-27T16:00:00Z (by /cross-boundary-audit — pre-code validation, Task #5 branch)**

**Branch:** task/5-group-d-filesystem-walker-integration (cut from main, Task #3 merged)

**Boundaries checked:** All 8 environment variables — full code scan of src/ and tests/

**Evidence recorded:**
- 1 entry fully implemented ✓ (`SCANMENOW_DB_PATH` — `storage/db.py:12` — unchanged)
- 1 entry escalated to **hard mandate** ⚠→🚫 (`SCANMENOW_LOG_LEVEL` — 4th carry; must be wired in Task #5 cli.py startup; see entry above)
- 2 entries planned Task #5, not yet in code ⚠ (`TESSERACT_CMD`, `LIBREOFFICE_CMD` — `walker/reader.py` does not exist yet)
- 4 entries planned Task #8, not yet in code ⚠ (`SCANMENOW_BACKEND`, `SCANMENOW_FIRESTORE_PROJECT`, `GOOGLE_APPLICATION_CREDENTIALS` — expected)
- 0 shape mismatches
- Registries match current code diff: ✓ (no Task #5 code written yet; all ⚠ entries correctly reflect planned state)

**New identifiers Task #5 will introduce (to verify at post-build audit):**
- `TESSERACT_CMD` consumed at `src/scanmenow/walker/reader.py` — `_read_image()` and `_read_image_pdf()`
- `LIBREOFFICE_CMD` consumed at `src/scanmenow/walker/reader.py` — `_read_doc()`
- `SCANMENOW_LOG_LEVEL` consumed at `src/scanmenow/cli.py` — startup logging configuration (MANDATORY)

**Hard mandate:** `SCANMENOW_LOG_LEVEL` must have a code consumer in `cli.py` before this task's PR is opened. The post-build audit will fail if it remains unwired.

**Status:** ✓ Build-start audit complete (Task #5)
