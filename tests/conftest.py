"""Shared pytest fixtures for scanmenow tests."""

from pathlib import Path
import pytest


@pytest.fixture
def tmp_db_path(tmp_path) -> Path:
    """Provide a temporary SQLite DB path for storage tests."""
    return tmp_path / "test_scanmenow.db"
