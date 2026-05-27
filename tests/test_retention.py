"""Tests for the retention policy module."""

from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock
import pytest
from scanmenow.retention.evaluator import evaluate_retention
from scanmenow.retention.policy import RetentionPolicy, RetentionReport
from scanmenow.storage.models import Finding, ScanJob
from scanmenow.storage.repository import SqliteRepository


def test_retention_policy_max_age_days_must_be_positive() -> None:
    with pytest.raises(ValueError, match="max_age_days"):
        RetentionPolicy(max_age_days=0)


def test_retention_policy_negative_days_raises() -> None:
    with pytest.raises(ValueError):
        RetentionPolicy(max_age_days=-5)


def test_retention_policy_dry_run_default() -> None:
    policy = RetentionPolicy(max_age_days=30)
    assert policy.dry_run is True


def test_retention_policy_live_mode() -> None:
    policy = RetentionPolicy(max_age_days=30, dry_run=False)
    assert policy.dry_run is False
