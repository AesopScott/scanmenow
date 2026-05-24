"""Smoke tests for SQLite storage — CRUD and CSV export (Proof Unit 5)."""

import csv
from pathlib import Path
from scanmenow.storage.models import ScanJob, Finding
from scanmenow.storage.repository import create_job, save_finding, get_findings_for_job, export_csv


def test_create_and_query_job(tmp_db_path):
    """ScanJob round-trips through create_job → get_findings_for_job."""
    job = ScanJob(source_path="/data/scans")
    saved = create_job(job, db_path=tmp_db_path)
    assert saved.job_id == job.job_id
    # No findings yet — query returns empty list
    findings = get_findings_for_job(job.job_id, db_path=tmp_db_path)
    assert findings == []


def test_save_and_retrieve_findings(tmp_db_path):
    """Two Findings saved under a job are retrieved in offset order."""
    job = ScanJob(source_path="/data/scans")
    create_job(job, db_path=tmp_db_path)

    f1 = Finding(job_id=job.job_id, entity_type="EMAIL_ADDRESS", start=15, end=35, score=0.9, text_snippet="<redacted>")
    f2 = Finding(job_id=job.job_id, entity_type="PERSON", start=5, end=14, score=0.85, text_snippet="<redacted>")
    save_finding(f1, db_path=tmp_db_path)
    save_finding(f2, db_path=tmp_db_path)

    results = get_findings_for_job(job.job_id, db_path=tmp_db_path)
    assert len(results) == 2
    # Ordered by start offset
    assert results[0].entity_type == "PERSON"
    assert results[1].entity_type == "EMAIL_ADDRESS"


def test_export_csv(tmp_db_path, tmp_path):
    """CSV export produces correct headers and row count."""
    job = ScanJob(source_path="/data/scans")
    create_job(job, db_path=tmp_db_path)

    f1 = Finding(job_id=job.job_id, entity_type="EMAIL_ADDRESS", start=15, end=35, score=0.9, text_snippet="<redacted>")
    f2 = Finding(job_id=job.job_id, entity_type="PERSON", start=5, end=14, score=0.85, text_snippet="<redacted>")
    save_finding(f1, db_path=tmp_db_path)
    save_finding(f2, db_path=tmp_db_path)

    csv_path = tmp_path / "findings.csv"
    count = export_csv(job.job_id, csv_path, db_path=tmp_db_path)

    assert count == 2
    assert csv_path.exists()

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert reader.fieldnames == ["job_id", "entity_type", "start", "end", "score", "text_snippet"]
    assert len(rows) == 2
