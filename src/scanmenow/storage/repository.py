"""CRUD operations and CSV export for scan jobs and findings."""

import csv
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List

from scanmenow.storage.db import get_connection, init_db
from scanmenow.storage.models import Finding, ScanJob

CSV_HEADERS = ["job_id", "entity_type", "start", "end", "score", "text_snippet"]


def create_job(job: ScanJob, db_path: Path | None = None) -> ScanJob:
    """Persist a ScanJob to the database."""
    init_db(db_path)
    conn = get_connection(db_path)
    with conn:
        conn.execute(
            """
            INSERT INTO scan_jobs (job_id, source_path, status, created_at, completed_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (job.job_id, job.source_path, job.status, job.created_at, job.completed_at),
        )
    conn.close()
    return job


def save_finding(finding: Finding, db_path: Path | None = None) -> Finding:
    """Persist a Finding to the database."""
    init_db(db_path)
    conn = get_connection(db_path)
    with conn:
        conn.execute(
            """
            INSERT INTO findings
                (finding_id, job_id, entity_type, start, end, score,
                 text_snippet, source_file, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                finding.finding_id,
                finding.job_id,
                finding.entity_type,
                finding.start,
                finding.end,
                finding.score,
                finding.text_snippet,
                finding.source_file,
                finding.created_at,
            ),
        )
    conn.close()
    return finding


def get_findings_for_job(job_id: str, db_path: Path | None = None) -> List[Finding]:
    """Retrieve all findings for a given job ID."""
    init_db(db_path)
    conn = get_connection(db_path)
    try:
        rows = conn.execute(
            "SELECT * FROM findings WHERE job_id = ? ORDER BY start",
            (job_id,),
        ).fetchall()
    finally:
        conn.close()
    return [
        Finding(
            finding_id=row["finding_id"],
            job_id=row["job_id"],
            entity_type=row["entity_type"],
            start=row["start"],
            end=row["end"],
            score=row["score"],
            text_snippet=row["text_snippet"],
            source_file=row["source_file"],
            created_at=row["created_at"] if "created_at" in row.keys() else "",
        )
        for row in rows
    ]


def get_findings_older_than(days: int, db_path: Path | None = None) -> List[Finding]:
    """Retrieve all findings whose created_at is older than the given number of days.

    Findings with an empty created_at are treated as keep (conservative default).
    """
    init_db(db_path)
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    conn = get_connection(db_path)
    try:
        rows = conn.execute(
            """
            SELECT * FROM findings
            WHERE created_at != '' AND created_at < ?
            ORDER BY created_at
            """,
            (cutoff,),
        ).fetchall()
    finally:
        conn.close()
    return [
        Finding(
            finding_id=row["finding_id"],
            job_id=row["job_id"],
            entity_type=row["entity_type"],
            start=row["start"],
            end=row["end"],
            score=row["score"],
            text_snippet=row["text_snippet"],
            source_file=row["source_file"],
            created_at=row["created_at"] if "created_at" in row.keys() else "",
        )
        for row in rows
    ]


def delete_finding(finding_id: str, db_path: Path | None = None) -> None:
    """Delete a finding by its ID."""
    init_db(db_path)
    conn = get_connection(db_path)
    with conn:
        conn.execute("DELETE FROM findings WHERE finding_id = ?", (finding_id,))
    conn.close()


def export_csv(job_id: str, output_path: Path, db_path: Path | None = None) -> int:
    """Export all findings for a job to a CSV file (Excel-importable)."""
    init_db(db_path)
    findings = get_findings_for_job(job_id, db_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writeheader()
        for finding in findings:
            writer.writerow({
                "job_id": finding.job_id,
                "entity_type": finding.entity_type,
                "start": finding.start,
                "end": finding.end,
                "score": finding.score,
                "text_snippet": finding.text_snippet,
            })
    return len(findings)


class SqliteRepository:
    """Class-based repository wrapping the module-level SQLite functions.

    Implements the Repository protocol defined in storage.base.
    Preserves all module-level functions for backward compatibility.
    """

    def __init__(self, db_path: Path | None = None) -> None:
        self._db_path = db_path

    def save_job(self, job: ScanJob) -> ScanJob:
        return create_job(job, self._db_path)

    def save_finding(self, finding: Finding) -> Finding:
        return save_finding(finding, self._db_path)

    def get_findings_for_job(self, job_id: str) -> List[Finding]:
        return get_findings_for_job(job_id, self._db_path)

    def get_findings_older_than(self, days: int) -> List[Finding]:
        return get_findings_older_than(days, self._db_path)

    def delete_finding(self, finding_id: str) -> None:
        delete_finding(finding_id, self._db_path)

    def get_overlapping_findings(
        self, job_id: str, start: int, end: int
    ) -> List[Finding]:
        """Return all findings for job_id whose span overlaps [start, end].

        Pre-registered for Task #5 (get_overlapping_findings contract).
        Returns only findings where f.start <= end AND f.end >= start.
        """
        all_findings = get_findings_for_job(job_id, self._db_path)
        return [
            f for f in all_findings if f.start <= end and f.end >= start
        ]
