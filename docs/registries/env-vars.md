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

**Status:** ⚠ planned — no code yet

---

## Summary

| Variable | Required | Default | Consumers | Status |
|----------|----------|---------|-----------|--------|
| `SCANMENOW_DB_PATH` | no | `~/.scanmenow/scanmenow.db` | storage/db.py | ✓ implemented |
| `SCANMENOW_LOG_LEVEL` | no | `INFO` | cli.py or __init__.py | ⚠ planned — not yet consumed |

---

## Audit Trail — Proof of Registry Verification

**Last audit:** 2026-05-23T00:00:00Z (updated by /finish-build — post-code verification)

**Boundaries checked:** Environment variables (post-code verification against shipped implementation)

**Evidence recorded:**
- 1 entry fully implemented ✓ (`SCANMENOW_DB_PATH`)
- 1 entry planned ⚠ (`SCANMENOW_LOG_LEVEL` — not yet consumed in code, deferred to future task)
- 0 shape mismatches
- New identifiers introduced on task #2: `SCANMENOW_DB_PATH`, `SCANMENOW_LOG_LEVEL`
- Registries match current code diff: ✓ verified

**Gaps resolved:**
- `SCANMENOW_DB_PATH` default implemented via `DEFAULT_DB_PATH` constant in `db.py`

**Soft flags:**
- `SCANMENOW_LOG_LEVEL` is documented but not yet wired into logging config — carry forward to a future task

**Status:** ✓ Audit complete (post-code)
