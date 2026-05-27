# Firestore Collections Registry

Every Firestore collection used in this project. For each: document key, fields, field types, constraints, and the implementing code. Update whenever a collection is added, removed, or its schema changes.

**When active:** Only when `SCANMENOW_BACKEND=firestore`. SQLite-only deployments do not use Firestore.

**GCP project:** set via `SCANMENOW_FIRESTORE_PROJECT` env var (see `docs/registries/env-vars.md`).

---

## `scan_jobs`

Mirrors the SQLite `scan_jobs` table. One document per scan run.

**Document key:** `{job_id}` (UUID string)

| Field | Type | Nullable | Default | Notes |
|-------|------|----------|---------|-------|
| `job_id` | string | no | — | same as document key; denormalized for query convenience |
| `source_path` | string | no | `""` | path passed to `scanmenow scan` |
| `status` | string | no | `"pending"` | one of: `pending`, `running`, `completed`, `failed` |
| `created_at` | string | no | ISO 8601 UTC | set by `ScanJob` dataclass on construction |
| `completed_at` | string | yes | `null` | set when status transitions to `completed` or `failed` |

**Written by:** `FirestoreRepository.save_job()` — `src/scanmenow/cloud/repository.py`
**Read by:** future — `FirestoreRepository.get_job()` (not yet implemented; Task #8 only adds write path)

**SQLite mirror:** `scan_jobs` table — `src/scanmenow/storage/db.py`

---

## `findings`

Mirrors the SQLite `findings` table. One document per detected PII/PHI entity.

**Document key:** `{finding_id}` (UUID string)

| Field | Type | Nullable | Default | Notes |
|-------|------|----------|---------|-------|
| `finding_id` | string | no | — | same as document key |
| `job_id` | string | no | — | foreign key to `scan_jobs/{job_id}`; Firestore does not enforce FK |
| `entity_type` | string | no | — | one of the registered entity types (see `entity-types.md`) |
| `start` | integer | no | — | character offset start (inclusive) |
| `end` | integer | no | — | character offset end (exclusive) |
| `score` | float | no | — | detection confidence 0.0–1.0 |
| `text_snippet` | string | no | `""` | raw detected text |
| `source_file` | string | no | `""` | file path where entity was found |
| `created_at` | string | no | `""` | ISO 8601 UTC; empty string treated as "keep" by retention policy |

**Written by:**
- `FirestoreRepository.save_finding()` — `src/scanmenow/cloud/repository.py`

**Read by:**
- `FirestoreRepository.get_findings_for_job()` — queries `WHERE job_id == <id>`, ordered by `start`
- `FirestoreRepository.get_findings_older_than()` — queries `WHERE created_at != "" AND created_at < <cutoff>`

**Deleted by:**
- `FirestoreRepository.delete_finding()` — deletes document by `finding_id`

**SQLite mirror:** `findings` table — `src/scanmenow/storage/db.py`

**Index note:** Firestore requires a composite index for queries combining inequality filters (e.g., `created_at != "" AND created_at < cutoff`). This index must be created manually in the GCP console or via `firestore.indexes.json` before retention queries will work in production.

---

## Summary

| Collection | Document key | Implemented | Status |
|------------|-------------|-------------|--------|
| `scan_jobs` | `{job_id}` | `FirestoreRepository.save_job()` | ✓ implemented (Task #8) |
| `findings` | `{finding_id}` | `FirestoreRepository.save_finding/delete/get_*()` | ✓ implemented (Task #8) |

---

## Audit Trail

**First recorded:** 2026-05-27 — Task #8 post-code cross-boundary audit

**Status:** ✓ registry created alongside implementation
