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

**Adjacent constraint — Foreign key:** `findings.job_id` references `scan_jobs.job_id`. SQLite foreign key enforcement requires `PRAGMA foreign_keys = ON` at connection time.

**Status:** ⚠ planned — no code yet

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

**Adjacent constraint — CSV export:** `export_csv()` must use headers in this exact order: `job_id, entity_type, start, end, score, text_snippet` (per Proof Unit 5). Column order change = breaking change for analyst consumers.

**Status:** ⚠ planned — no code yet

---

## `evidence`

⚠ **Shape unresolved.** The plan references an `Evidence` model alongside `ScanJob` and `Finding`, but the relationship is not yet defined: embedded in `findings.text_snippet`, a separate table with a FK, or a JSON blob column?

**Proposed resolution:** At implementation time, decide whether `evidence` is a separate table (1:1 with `findings`, stores raw text for internal use only) or collapsed into the `findings.text_snippet` column. Update this registry entry before writing `storage/models.py`.

**Schema / shape:** TBD

**Producers:** TBD

**Consumers:** TBD

**Status:** ⚠ shape unresolved — must resolve before implementing `storage/models.py`

---

## Summary

| Table | Producers | Consumers | Status |
|-------|-----------|-----------|--------|
| `scan_jobs` | db.py, repository.py | repository.py, test_storage.py | ⚠ planned |
| `findings` | db.py, repository.py | repository.py, test_storage.py | ⚠ planned |
| `evidence` | TBD | TBD | ⚠ shape unresolved |

---

## Audit Trail — Proof of Registry Verification

**Last audit:** 2026-05-23T00:00:00Z (by /cross-boundary-audit)

**Boundaries checked:** SQLite tables (pre-code, plan-based audit)

**Evidence recorded:**
- 0 entries with complete producer/consumer pairs ✓ (no code yet)
- 2 entries with planned producers/consumers ⚠ (pre-code)
- 1 entry with unresolved shape ⚠ (evidence table)
- New identifiers introduced on task #2: `scan_jobs`, `findings`, `evidence`
- Registries match current code diff: N/A — pre-code audit

**Gaps identified:**
- `evidence` table shape is unresolved — relationship to `findings` must be decided before implementation
- Foreign key enforcement requires `PRAGMA foreign_keys = ON` at every connection

**Status:** Audit complete (pre-code)
