"""Tests for the cloud module -- Firestore client factory and FirestoreRepository."""

import sys
from unittest.mock import MagicMock, patch

import pytest

from scanmenow.storage.models import Finding, ScanJob


# ---------------------------------------------------------------------------
# get_firestore_client -- lazy import safety
# ---------------------------------------------------------------------------


def test_get_firestore_client_raises_import_error_when_package_missing(
    monkeypatch,
) -> None:
    """ImportError is raised with a helpful install hint when GCP package absent."""
    import importlib

    blocked = {"google.cloud": None, "google.cloud.firestore": None}
    with patch.dict(sys.modules, blocked):
        if "scanmenow.cloud.client" in sys.modules:
            del sys.modules["scanmenow.cloud.client"]
        from scanmenow.cloud import client as cloud_client
        importlib.reload(cloud_client)
        with pytest.raises(ImportError, match="google-cloud-firestore"):
            cloud_client.get_firestore_client()


def test_get_firestore_client_passes_project_kwarg(monkeypatch) -> None:
    """SCANMENOW_FIRESTORE_PROJECT env var is forwarded to the Firestore client."""
    monkeypatch.setenv("SCANMENOW_FIRESTORE_PROJECT", "my-gcp-project")

    mock_firestore = MagicMock()
    mock_client_instance = MagicMock()
    mock_firestore.Client.return_value = mock_client_instance

    google_cloud_mock = MagicMock()
    google_cloud_mock.firestore = mock_firestore
    fakes = {"google": MagicMock(), "google.cloud": google_cloud_mock, "google.cloud.firestore": mock_firestore}
    with patch.dict(sys.modules, fakes):
        import importlib
        if "scanmenow.cloud.client" in sys.modules:
            del sys.modules["scanmenow.cloud.client"]
        from scanmenow.cloud import client as cloud_client
        importlib.reload(cloud_client)
        result = cloud_client.get_firestore_client()
        mock_firestore.Client.assert_called_once_with(project="my-gcp-project")
        assert result is mock_client_instance


def test_get_firestore_client_no_project_kwarg_when_env_absent(monkeypatch) -> None:
    """When SCANMENOW_FIRESTORE_PROJECT is not set, project kwarg is omitted."""
    monkeypatch.delenv("SCANMENOW_FIRESTORE_PROJECT", raising=False)

    mock_firestore = MagicMock()
    mock_client_instance = MagicMock()
    mock_firestore.Client.return_value = mock_client_instance

    google_cloud_mock = MagicMock()
    google_cloud_mock.firestore = mock_firestore
    fakes = {"google": MagicMock(), "google.cloud": google_cloud_mock, "google.cloud.firestore": mock_firestore}
    with patch.dict(sys.modules, fakes):
        import importlib
        if "scanmenow.cloud.client" in sys.modules:
            del sys.modules["scanmenow.cloud.client"]
        from scanmenow.cloud import client as cloud_client
        importlib.reload(cloud_client)
        result = cloud_client.get_firestore_client()
        mock_firestore.Client.assert_called_once_with()
        assert result is mock_client_instance


# ---------------------------------------------------------------------------
# FirestoreRepository -- unit tests with a mock client
# ---------------------------------------------------------------------------


def _make_mock_client():
    """Build a minimal Firestore client mock."""
    client = MagicMock()
    collection = MagicMock()
    client.collection.return_value = collection
    doc_ref = MagicMock()
    collection.document.return_value = doc_ref
    return client, collection, doc_ref


def test_firestore_repository_save_job() -> None:
    from scanmenow.cloud.repository import FirestoreRepository

    client, collection, doc_ref = _make_mock_client()
    repo = FirestoreRepository(client=client)

    job = ScanJob(source_path="/data/test.txt")
    returned = repo.save_job(job)

    assert returned is job
    client.collection.assert_called_with("scan_jobs")
    collection.document.assert_called_with(job.job_id)
    doc_ref.set.assert_called_once()


def test_firestore_repository_save_finding() -> None:
    from scanmenow.cloud.repository import FirestoreRepository

    client, collection, doc_ref = _make_mock_client()
    repo = FirestoreRepository(client=client)

    finding = Finding(job_id="job-123", entity_type="EMAIL_ADDRESS", start=0, end=10)
    returned = repo.save_finding(finding)

    assert returned is finding
    client.collection.assert_called_with("findings")
    collection.document.assert_called_with(finding.finding_id)
    doc_ref.set.assert_called_once()
    payload = doc_ref.set.call_args[0][0]
    assert payload["entity_type"] == "EMAIL_ADDRESS"
    assert payload["job_id"] == "job-123"


def test_firestore_repository_delete_finding() -> None:
    from scanmenow.cloud.repository import FirestoreRepository

    client, collection, doc_ref = _make_mock_client()
    repo = FirestoreRepository(client=client)

    repo.delete_finding("finding-abc")
    client.collection.assert_called_with("findings")
    collection.document.assert_called_with("finding-abc")
    doc_ref.delete.assert_called_once()


def test_firestore_repository_get_findings_for_job() -> None:
    from scanmenow.cloud.repository import FirestoreRepository

    client = MagicMock()
    collection_mock = MagicMock()
    client.collection.return_value = collection_mock

    query_mock = MagicMock()
    collection_mock.where.return_value = query_mock
    query_mock.order_by.return_value = query_mock

    doc1 = MagicMock()
    doc1.to_dict.return_value = {
        "finding_id": "f1", "job_id": "job-123", "entity_type": "PHONE",
        "start": 0, "end": 5, "score": 0.9,
        "text_snippet": "555", "source_file": "/x.txt",
        "created_at": "2024-01-01T00:00:00+00:00",
    }
    doc2 = MagicMock()
    doc2.to_dict.return_value = {
        "finding_id": "f2", "job_id": "job-123", "entity_type": "EMAIL",
        "start": 10, "end": 20, "score": 0.85,
        "text_snippet": "a@b.c", "source_file": "/x.txt",
        "created_at": "2024-01-01T00:00:00+00:00",
    }
    query_mock.stream.return_value = iter([doc1, doc2])

    repo = FirestoreRepository(client=client)
    findings = repo.get_findings_for_job("job-123")

    assert len(findings) == 2
    assert findings[0].finding_id == "f1"
    assert findings[1].entity_type == "EMAIL"


def test_firestore_repository_client_lazily_initialized() -> None:
    """FirestoreRepository._client is None at construction; set only after _db() call."""
    from scanmenow.cloud.repository import FirestoreRepository

    repo = FirestoreRepository(client=None)
    assert repo._client is None

