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

**Adjacent constraint — Missing default:** If this variable is absent and no fallback is coded, `init_db()` will raise `TypeError` or create the file in the current working directory unexpectedly. **Must implement a default in `db.py` before shipping.**

**Status:** ⚠ planned — default value not yet implemented in code

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

**Status:** ⚠ planned — no code yet

---

## Summary

| Variable | Required | Default | Consumers | Status |
|----------|----------|---------|-----------|--------|
| `SCANMENOW_DB_PATH` | no | `~/.scanmenow/scanmenow.db` | storage/db.py | ⚠ planned, default unimplemented |
| `SCANMENOW_LOG_LEVEL` | no | `INFO` | cli.py or __init__.py | ⚠ planned |

---

## Audit Trail — Proof of Registry Verification

**Last audit:** 2026-05-23T00:00:00Z (by /cross-boundary-audit)

**Boundaries checked:** Environment variables (pre-code, plan-based audit)

**Evidence recorded:**
- 0 entries with complete producer/consumer pairs ✓ (no code yet)
- 2 entries planned ⚠ (pre-code)
- 0 shape mismatches
- New identifiers introduced on task #2: `SCANMENOW_DB_PATH`, `SCANMENOW_LOG_LEVEL`
- Registries match current code diff: N/A — pre-code audit

**Gaps identified:**
- `SCANMENOW_DB_PATH` has no default value implemented — `db.py` must handle missing var gracefully

**Status:** Audit complete (pre-code)
