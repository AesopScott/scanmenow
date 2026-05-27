"""Retention policy evaluator -- applies a RetentionPolicy to a Repository."""

from scanmenow.retention.policy import RetentionPolicy, RetentionReport
from scanmenow.storage.base import Repository


def evaluate_retention(repo: Repository, policy: RetentionPolicy) -> RetentionReport:
    """Evaluate and optionally enforce a retention policy.

    Steps
    -----
    1. Query the repository for all findings older than
       ``policy.max_age_days`` days.
    2. In *dry-run* mode (the default): return a report listing the
       candidates but perform no deletions.
    3. In *live* mode (``dry_run=False``): delete each candidate and
       record it in the report.

    Findings with an empty ``created_at`` are skipped by the repository
    query itself (conservative keep-by-default behaviour).

    Args:
        repo: Any Repository-protocol-compliant object (SQLite or Firestore).
        policy: The RetentionPolicy to apply.

    Returns:
        A RetentionReport describing which findings were candidates and
        which (if any) were deleted.
    """
    candidates = repo.get_findings_older_than(policy.max_age_days)

    report = RetentionReport(
        policy=policy,
        candidates=candidates,
        deleted=[],
        dry_run=policy.dry_run,
    )

    if policy.dry_run:
        return report

    for finding in candidates:
        repo.delete_finding(finding.finding_id)
        report.deleted.append(finding)

    return report
