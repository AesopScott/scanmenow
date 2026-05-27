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
| `source_line` | INTEGER | ⚠ planned (Task #5) — line number within `source_file` where the entity was found. Added via `ALTER TABLE findings ADD COLUMN source_line INTEGER` in `init_db()`. Nullable — NULL for pre-Task #5 findings and formats where line tracking is not meaningful. |
| `created_at` | TEXT (ISO 8601) | ⚠ planned (Task #8) — timestamp when the finding was saved. Added via `ALTER TABLE findings ADD COLUMN created_at TEXT NOT NULL DEFAULT ''` in `init_db()` (idempotent — catches `OperationalError` for duplicate column). Required by retention evaluator for age-based policy enforcement. Empty string is treated as "keep" by the evaluator (conservative). |

**Producers**
- `src/scanmenow/storage/db.py` — `init_db()` creates the table schema; Task #5 adds migration for `source_line`
- `src/scanmenow/storage/repository.py` — `save_finding()` inserts a row; Task #5 adds `source_line` to INSERT

**Consumers**
- `src/scanmenow/storage/repository.py` — `get_findings_for_job()`, `export_csv()`
- `src/scanmenow/storage/repository.py` — `get_overlapping_findings(job_id, start, end)` ⚠ planned (Task #5) — queries findings WHERE start ≤ ? AND end ≥ ? for span collision detection
- `tests/test_storage.py` — smoke test saves and queries findings
- `tests/test_span_collision.py` — ⚠ planned (Task #5) — asserts multi-entity behavior on overlapping spans; calls `get_overlapping_findings()`
- `tests/test_scanner.py` — ⚠ planned (Task #5) — asserts `source_line` is populated after scan

**Adjacent constraint — CSV export:** `export_csv()` must use headers in this exact order: `job_id, entity_type, start, end, score, text_snippet` (per Proof Unit 5). Column order change = breaking change for analyst consumers. `CSV_HEADERS` constant in `repository.py` enforces this order. Task #5 adds `source_line` to `CSV_HEADERS`.

**Adjacent constraint — Span collision contract:** When multiple recognizers fire on the same `(start, end)` span, all findings are stored independently — no deduplication. `get_overlapping_findings()` is the designated query for consumers that need to collapse or surface overlaps. This is a documented contract; do not add dedup logic to `save_finding()`.

**Status:** ✓ implemented (current schema) · ⚠ `source_line` column and `get_overlapping_findings()` planned for Task #5

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
| `findings` | db.py, repository.py | repository.py, test_storage.py, test_span_collision.py (planned) | ✓ implemented · `source_line` ⚠ Task #5 · `created_at` ⚠ Task #8 |
| `evidence` | repository.py (via text_snippet) | repository.py | ✓ collapsed into findings.text_snippet |

---

## Audit Trail — Proof of Registry Verification

**Last audit:** 2026-05-27T00:00:00Z (by /cross-boundary-audit — pre-build plan validation for Task #5)

**Boundaries checked:** SQLite tables (verified against Task #5 plan — `source_line` column and `get_overlapping_findings()` pre-registered)

**Evidence recorded:**
- 2 entries with complete producer/consumer pairs ✓ (`scan_jobs` unchanged; `findings` current schema verified)
- 1 entry resolved ✓ (`evidence` collapsed into `findings.text_snippet` — unchanged)
- New identifiers introduced on Task #5 (pre-registered): `findings.source_line` column (ALTER TABLE migration), `get_overlapping_findings()` consumer function
- Registries match current code diff: ✓ (current code) · ⚠ `source_line` pre-registered, not yet in code

**Gaps resolved this audit:**
- `findings.source_line` pre-registered in schema table to align registry with Task #5 plan before build starts
- `get_overlapping_findings()` pre-registered as planned consumer with span collision contract documented

**Soft flags:**
- `source_file` column in `findings` not in CSV_HEADERS (intentional — analyst export only needs 6 listed fields; source_file available via direct DB query). Task #5 adds `source_line` to CSV_HEADERS.
- `findings.entity_type` stores custom entity type strings — see `entity-types.md` for the full registry of valid values

**Status:** ✓ Audit complete (pre-build plan validation for Task #5)
