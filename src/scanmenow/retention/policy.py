"""Retention policy data models."""

from dataclasses import dataclass, field
from typing import List

from scanmenow.storage.models import Finding


@dataclass
class RetentionPolicy:
    """Configuration for an age-based retention sweep.

    Attributes:
        max_age_days: Findings older than this many days are eligible for
            deletion.  Must be a positive integer.
        dry_run: When ``True`` (default), no deletions are performed -- the
            run only reports what *would* be deleted.  Set to ``False`` to
            perform live deletions.
    """

    max_age_days: int
    dry_run: bool = True

    def __post_init__(self) -> None:
        if self.max_age_days < 1:
            raise ValueError(
                f"max_age_days must be at least 1, got {self.max_age_days}"
            )


@dataclass
class RetentionReport:
    """Result of a retention policy evaluation run.

    Attributes:
        policy: The policy that was evaluated.
        candidates: Findings that matched the age threshold.
        deleted: Findings that were actually deleted (empty in dry-run mode).
        dry_run: Whether this was a dry-run (no deletions performed).
    """

    policy: RetentionPolicy
    candidates: List[Finding] = field(default_factory=list)
    deleted: List[Finding] = field(default_factory=list)
    dry_run: bool = True

    @property
    def candidate_count(self) -> int:
        """Number of findings eligible for deletion."""
        return len(self.candidates)

    @property
    def deleted_count(self) -> int:
        """Number of findings actually deleted."""
        return len(self.deleted)
