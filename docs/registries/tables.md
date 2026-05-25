# SQLite Tables Registry

Every SQLite table used in this project. For each: producers, consumers, schema shape, status. Update whenever a table is added, removed, renamed, or its columns change.

**Storage target:** Local `.db` file at `SCANMENOW_DB_PATH`. Also compatible with MochaHost shared hosting (SQLite available server-side).

---

## `scan_jobs`

A single scan run — tracks job identity, status, and timing.

**Schema / shape:**
| Column | Type | Notes |
|--------|------|-------|
| `job_id` | TEXT (UUID) | Primary key |
| `status` | TEXT | e.g. `running`, `complete`, `failed` |
| `source_path` | TEXT | Directory or file scanned |
| `created_at` | TEXT (ISO 8601) | Job creation timestamp |
| `completed_at` | TEXT (ISO 8601) | Nullable — set on completion |

**Producers**
- `src/scanmenow/storage/db.py` — `init_db()` creates the table schema
- `src/scanmenow/storage/repository.py` — `create_job()` inserts a row

**Consumers**
- `src/scanmenow/storage/repository.py` — `get_findings_for_job()` joins on `job_id`
- `tests/test_storage.py` — smoke test creates and queries a job

**Adjacent constraint — Foreign key:** `findings.job_id` references `scan_jobs.job_id`. `PRAGMA foreign_keys = ON` is enforced in `get_connection()` at every connection open.

**Status:** ✓ implemented

---

## `findings`

One row per detected PII/PHI entity within a scan job.

**Schema / shape:**
| Column | Type | Notes |
|--------|------|-------|
| `finding_id` | TEXT (UUID) | Primary key |
| `job_id` | TEXT (UUID) | FK → `scan_jobs.job_id` |
| `entity_type` | TEXT | e.g. `EMAIL_ADDRESS`, `PERSON` |
| `start` | INTEGER | Character offset start |
| `end` | INTEGER | Character offset end |
| `score` | REAL | Presidio confidence score (0.0–1.0) |
| `text_snippet` | TEXT | Safe evidence — redacted by default |
| `source_file` | TEXT | File where entity was found |

**Producers**
- `src/scanmenow/storage/db.py` — `init_db()` creates the table schema
- `src/scanmenow/storage/repository.py` — `save_finding()` inserts a row

**Consumers**
- `src/scanmenow/storage/repository.py` — `get_findings_for_job()`, `export_csv()`
- `tests/test_storage.py` — smoke test saves and queries findings

**Adjacent constraint — CSV export:** `export_csv()` must use headers in this exact order: `job_id, entity_type, start, end, score, text_snippet` (per Proof Unit 5). Column order change = breaking change for analyst consumers. `CSV_HEADERS` constant in `repository.py` enforces this order.

**Status:** ✓ implemented

---

## `evidence`

**Resolution (Task #2):** Collapsed into `findings.text_snippet`. No separate table. Safe evidence snippets are stored as a TEXT column on the `findings` table — redacted by default, never the raw sensitive value.

**Schema / shape:** See `findings.text_snippet` column.

**Producers:** `src/scanmenow/storage/repository.py` — `save_finding()` writes `text_snippet`

**Consumers:** `src/scanmenow/storage/repository.py` — `export_csv()` includes `text_snippet` in CSV output

**Status:** ✓ resolved — collapsed into findings.text_snippet

---

## Summary

| Table | Producers | Consumers | Status |
|-------|-----------|-----------|--------|
| `scan_jobs` | db.py, repository.py | repository.py, test_storage.py | ✓ implemented |
| `findings` | db.py, repository.py | repository.py, test_storage.py | ✓ implemented |
| `evidence` | repository.py (via text_snippet) | repository.py | ✓ collapsed into findings.text_snippet |

---

## Audit Trail — Proof of Registry Verification

**Last audit:** 2026-05-25T00:00:00Z (by /cross-boundary-audit — pre-build plan validation for Task #3)

**Boundaries checked:** SQLite tables (re-verified against Task #3 plan — no table changes planned)

**Evidence recorded:**
- 2 entries with complete producer/consumer pairs ✓ (unchanged from Task #2 ship)
- 1 entry resolved ✓ (`evidence` collapsed into `findings.text_snippet`)
- New identifiers introduced on task #3: none — Task #3 adds no new tables
- Registries match current code diff: ✓ verified

**Gaps resolved:**
- `evidence` table shape resolved — collapsed into `findings.text_snippet` column
- `PRAGMA foreign_keys = ON` implemented in `get_connection()` (db.py:30)

**Soft flags:**
- `source_file` column in `findings` not listed in CSV_HEADERS (intentional — analyst export only needs the 6 listed fields; source_file visible via direct DB query)
- `findings.entity_type` will store Task #3 custom entity type strings — see `entity-types.md` for the full registry of valid values

**Status:** ✓ Audit complete (pre-build plan validation for Task #3)
