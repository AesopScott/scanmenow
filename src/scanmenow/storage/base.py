"""Repository protocol and backend factory for scanmenow storage layer."""

import os
from pathlib import Path
from typing import List, Protocol, runtime_checkable

from scanmenow.storage.models import Finding, ScanJob


@runtime_checkable
class Repository(Protocol):
    """Abstract repository interface for persisting scan jobs and findings.

    Concrete implementations:
        - SqliteRepository  (default, local)
        - FirestoreRepository  (cloud, SCANMENOW_BACKEND=firestore)
    """

    def save_job(self, job: ScanJob) -> ScanJob:
        """Persist a ScanJob and return it."""
        ...

    def save_finding(self, finding: Finding) -> Finding:
        """Persist a Finding and return it."""
        ...

    def get_findings_for_job(self, job_id: str) -> List[Finding]:
        """Return all findings for a job, ordered by start offset."""
        ...

    def get_findings_older_than(self, days: int) -> List[Finding]:
        """Return findings whose created_at is older than *days* days.

        Findings with an empty created_at are conservatively treated as "keep".
        """
        ...

    def delete_finding(self, finding_id: str) -> None:
        """Delete a finding by its primary key."""
        ...

    def get_overlapping_findings(
        self, job_id: str, start: int, end: int
    ) -> List[Finding]:
        """Return all findings for job_id whose span overlaps [start, end].

        Used by the scanner (Task #5) to detect duplicate/overlapping detections.
        """
        ...


def get_repository(
    backend: str | None = None,
    db_path: Path | None = None,
) -> Repository:
    """Instantiate and return the configured repository backend.

    The backend is selected from (in priority order):
        1. The ``backend`` argument (if provided).
        2. The ``SCANMENOW_BACKEND`` environment variable.
        3. Default: ``"sqlite"``.

    Args:
        backend: Override the backend selection (``"sqlite"`` or ``"firestore"``).
        db_path: For SQLite only -- path override for the DB file.

    Returns:
        A Repository-protocol-compliant object.

    Raises:
        ValueError: If the resolved backend name is not recognised.
    """
    resolved = (backend or os.getenv("SCANMENOW_BACKEND", "sqlite")).lower().strip()

    if resolved == "sqlite":
        from scanmenow.storage.repository import SqliteRepository

        return SqliteRepository(db_path=db_path)

    if resolved == "firestore":
        from scanmenow.cloud.repository import FirestoreRepository

        return FirestoreRepository()

    raise ValueError(
        f"Unknown backend {resolved!r}. "
        "Set SCANMENOW_BACKEND to 'sqlite' or 'firestore'."
    )
