"""Data models for scanmenow storage layer."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
import uuid


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_uuid() -> str:
    return str(uuid.uuid4())


@dataclass
class ScanJob:
    """Represents a single scan run."""

    job_id: str = field(default_factory=_new_uuid)
    source_path: str = ""
    status: str = "pending"
    created_at: str = field(default_factory=_now_iso)
    completed_at: Optional[str] = None


@dataclass
class Finding:
    """A single detected PII/PHI entity within a scan job."""

    finding_id: str = field(default_factory=_new_uuid)
    job_id: str = ""
    entity_type: str = ""
    start: int = 0
    end: int = 0
    score: float = 0.0
    text_snippet: str = ""
    source_file: str = ""
