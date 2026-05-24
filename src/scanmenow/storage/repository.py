"""CRUD operations and CSV export for scan jobs and findings."""

import csv
from pathlib import Path
from typing import List

from scanmenow.storage.db import get_connection, init_db
from scanmenow.storage.models import Finding, ScanJob

CSV_HEADERS = ["job_id", "entity_type", "start", "end", "score", "text_snippet"]


def create_job(job: ScanJob, db_path: Path | None = None) -> ScanJob:
    """
    Persist a ScanJob to the database.

    Args:
        job: The ScanJob to insert.
        db_path: Optional path override for the DB file.

    Returns:
        The inserted ScanJob (unchanged).
    """
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
    """
    Persist a Finding to the database.

    Args:
        finding: The Finding to insert.
        db_path: Optional path override for the DB file.

    Returns:
        The inserted Finding (unchanged).
    """
    init_db(db_path)
    conn = get_connection(db_path)
    with conn:
        conn.execute(
            """
            INSERT INTO findings
                (finding_id, job_id, entity_type, start, end, score, text_snippet, source_file)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
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
            ),
        )
    conn.close()
    return finding


def get_findings_for_job(job_id: str, db_path: Path | None = None) -> List[Finding]:
    """
    Retrieve all findings for a given job ID.

    Args:
        job_id: The job to look up.
        db_path: Optional path override for the DB file.

    Returns:
        List of Finding objects.
    """
    init_db(db_path)
    conn = get_connection(db_path)
    rows = conn.execute(
        "SELECT * FROM findings WHERE job_id = ? ORDER BY start",
        (job_id,),
    ).fetchall()
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
        )
        for row in rows
    ]


def export_csv(job_id: str, output_path: Path, db_path: Path | None = None) -> int:
    """
    Export all findings for a job to a CSV file (Excel-importable).

    Headers: job_id, entity_type, start, end, score, text_snippet

    Args:
        job_id: The job whose findings to export.
        output_path: Destination CSV file path.
        db_path: Optional path override for the DB file.

    Returns:
        Number of rows written (excluding header).
    """
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
