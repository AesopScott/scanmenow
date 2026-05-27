"""Tests for the Repository protocol, SqliteRepository, and get_repository factory."""

import os
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from scanmenow.storage.base import Repository, get_repository
from scanmenow.storage.models import Finding, ScanJob
from scanmenow.storage.repository import SqliteRepository


# ---------------------------------------------------------------------------
# Protocol compliance -- SqliteRepository
# ---------------------------------------------------------------------------


def test_sqlite_repository_implements_protocol(tmp_db_path: Path) -> None:
    """SqliteRepository must satisfy the Repository runtime-checkable protocol."""
    repo = SqliteRepository(db_path=tmp_db_path)
    assert isinstance(repo, Repository)


def test_sqlite_repository_save_and_retrieve_job(tmp_db_path: Path) -> None:
    repo = SqliteRepository(db_path=tmp_db_path)
    job = ScanJob(source_path="/data/test.txt")
    saved = repo.save_job(job)
    assert saved.job_id == job.job_id


def test_sqlite_repository_save_and_retrieve_finding(tmp_db_path: Path) -> None:
    repo = SqliteRepository(db_path=tmp_db_path)
    job = ScanJob(source_path="/data/test.txt")
    repo.save_job(job)

    finding = Finding(
        job_id=job.job_id,
        entity_type="EMAIL_ADDRESS",
        start=0,
        end=5,
        score=0.9,
        text_snippet="hello",
        source_file="/data/test.txt",
    )
    saved = repo.save_finding(finding)
    assert saved.finding_id == finding.finding_id

    results = repo.get_findings_for_job(job.job_id)
    assert len(results) == 1
    assert results[0].entity_type == "EMAIL_ADDRESS"


def test_sqlite_repository_delete_finding(tmp_db_path: Path) -> None:
    repo = SqliteRepository(db_path=tmp_db_path)
    job = ScanJob(source_path="/data/test.txt")
    repo.save_job(job)
    finding = Finding(job_id=job.job_id, entity_type="PHONE_NUMBER")
    repo.save_finding(finding)

    repo.delete_finding(finding.finding_id)
    results = repo.get_findings_for_job(job.job_id)
    assert results == []


def test_sqlite_repository_get_overlapping_findings(tmp_db_path: Path) -> None:
    repo = SqliteRepository(db_path=tmp_db_path)
    job = ScanJob(source_path="/data/test.txt")
    repo.save_job(job)

    # span [10, 20]
    f1 = Finding(job_id=job.job_id, entity_type="A", start=10, end=20)
    # span [25, 35] -- overlaps [15, 30]: 25<=30 and 35>=15
    f2 = Finding(job_id=job.job_id, entity_type="B", start=25, end=35)
    # span [50, 60] -- no overlap with [15, 30]
    f3 = Finding(job_id=job.job_id, entity_type="C", start=50, end=60)

    for f in (f1, f2, f3):
        repo.save_finding(f)

    overlapping = repo.get_overlapping_findings(job.job_id, start=15, end=30)
    entity_types = {f.entity_type for f in overlapping}
    assert "A" in entity_types
    assert "B" in entity_types
    assert "C" not in entity_types


# ---------------------------------------------------------------------------
# get_repository factory -- env routing
# ---------------------------------------------------------------------------


def test_get_repository_defaults_to_sqlite(tmp_db_path: Path, monkeypatch) -> None:
    monkeypatch.delenv("SCANMENOW_BACKEND", raising=False)
    repo = get_repository(db_path=tmp_db_path)
    assert isinstance(repo, SqliteRepository)


def test_get_repository_sqlite_explicit(tmp_db_path: Path, monkeypatch) -> None:
    monkeypatch.delenv("SCANMENOW_BACKEND", raising=False)
    repo = get_repository(backend="sqlite", db_path=tmp_db_path)
    assert isinstance(repo, SqliteRepository)


def test_get_repository_env_var_sqlite(tmp_db_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SCANMENOW_BACKEND", "sqlite")
    repo = get_repository(db_path=tmp_db_path)
    assert isinstance(repo, SqliteRepository)


def test_get_repository_unknown_backend_raises(monkeypatch) -> None:
    monkeypatch.delenv("SCANMENOW_BACKEND", raising=False)
    with pytest.raises(ValueError, match="Unknown backend"):
        get_repository(backend="mysql")


# ---------------------------------------------------------------------------
# Age-based retention query
# ---------------------------------------------------------------------------


def test_get_findings_older_than_empty_created_at_kept(tmp_db_path: Path) -> None:
    """Findings with empty created_at must NOT appear in older-than results."""
    repo = SqliteRepository(db_path=tmp_db_path)
    job = ScanJob(source_path="/data/test.txt")
    repo.save_job(job)

    from scanmenow.storage.db import get_connection, init_db

    init_db(tmp_db_path)
    conn = get_connection(tmp_db_path)
    with conn:
        conn.execute(
            """
            INSERT INTO findings
                (finding_id, job_id, entity_type, start, end, score,
                 text_snippet, source_file, created_at)
            VALUES ('blank-created-at', ?, 'EMAIL_ADDRESS', 0, 1, 0.9, '', '', '')
            """,
            (job.job_id,),
        )
    conn.close()

    results = repo.get_findings_older_than(0)
    ids = [f.finding_id for f in results]
    assert "blank-created-at" not in ids
