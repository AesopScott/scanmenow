"""Firestore-backed implementation of the Repository protocol."""

from datetime import datetime, timedelta, timezone
from typing import Any, List

from scanmenow.storage.models import Finding, ScanJob


class FirestoreRepository:
    """Repository implementation backed by Google Cloud Firestore.

    Collections
    -----------
    ``scan_jobs``
        Documents keyed by ``job_id``.

    ``findings``
        Documents keyed by ``finding_id``, each carrying a ``job_id`` field
        for filtering.

    The ``google-cloud-firestore`` package is imported lazily in
    :func:`scanmenow.cloud.client.get_firestore_client`; this class itself
    never imports it at module level so SQLite-only deployments are unaffected.
    """

    def __init__(self, client: Any | None = None) -> None:
        """Initialise with an optional pre-built Firestore client.

        If *client* is ``None`` the client is created on first use via
        :func:`~scanmenow.cloud.client.get_firestore_client`.  Passing an
        explicit client (e.g. pointing at the emulator) is the primary test
        hook.
        """
        self._client = client

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _db(self) -> Any:
        if self._client is None:
            from scanmenow.cloud.client import get_firestore_client

            self._client = get_firestore_client()
        return self._client

    # ------------------------------------------------------------------
    # Repository protocol
    # ------------------------------------------------------------------

    def save_job(self, job: ScanJob) -> ScanJob:
        """Persist a ScanJob document to Firestore."""
        self._db().collection("scan_jobs").document(job.job_id).set(
            {
                "job_id": job.job_id,
                "source_path": job.source_path,
                "status": job.status,
                "created_at": job.created_at,
                "completed_at": job.completed_at,
            }
        )
        return job

    def save_finding(self, finding: Finding) -> Finding:
        """Persist a Finding document to Firestore."""
        self._db().collection("findings").document(finding.finding_id).set(
            {
                "finding_id": finding.finding_id,
                "job_id": finding.job_id,
                "entity_type": finding.entity_type,
                "start": finding.start,
                "end": finding.end,
                "score": finding.score,
                "text_snippet": finding.text_snippet,
                "source_file": finding.source_file,
                "created_at": finding.created_at,
            }
        )
        return finding

    def get_findings_for_job(self, job_id: str) -> List[Finding]:
        """Return all findings for *job_id*, ordered by start offset."""
        docs = (
            self._db()
            .collection("findings")
            .where("job_id", "==", job_id)
            .order_by("start")
            .stream()
        )
        return [self._doc_to_finding(d.to_dict()) for d in docs]

    def get_findings_older_than(self, days: int) -> List[Finding]:
        """Return findings whose created_at is older than *days* days.

        Documents with an empty or missing ``created_at`` are skipped
        (conservative keep-by-default behaviour).
        """
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        docs = (
            self._db()
            .collection("findings")
            .where("created_at", "!=", "")
            .where("created_at", "<", cutoff)
            .order_by("created_at")
            .stream()
        )
        return [self._doc_to_finding(d.to_dict()) for d in docs]

    def delete_finding(self, finding_id: str) -> None:
        """Delete the finding document with the given *finding_id*."""
        self._db().collection("findings").document(finding_id).delete()

    def get_overlapping_findings(
        self, job_id: str, start: int, end: int
    ) -> List[Finding]:
        """Return all findings for *job_id* whose span overlaps [start, end].

        Firestore lacks a native range-overlap query; we retrieve all findings
        for the job and filter in Python.  For very large result sets consider
        adding server-side filtering on ``start``/``end`` individually.
        """
        all_findings = self.get_findings_for_job(job_id)
        return [f for f in all_findings if f.start <= end and f.end >= start]

    # ------------------------------------------------------------------
    # Private conversion
    # ------------------------------------------------------------------

    @staticmethod
    def _doc_to_finding(data: dict) -> Finding:
        return Finding(
            finding_id=data.get("finding_id", ""),
            job_id=data.get("job_id", ""),
            entity_type=data.get("entity_type", ""),
            start=int(data.get("start", 0)),
            end=int(data.get("end", 0)),
            score=float(data.get("score", 0.0)),
            text_snippet=data.get("text_snippet", ""),
            source_file=data.get("source_file", ""),
            created_at=data.get("created_at", ""),
        )
