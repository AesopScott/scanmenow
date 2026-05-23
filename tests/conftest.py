"""Shared pytest fixtures for scanmenow tests."""

import os
import tempfile
import pytest


@pytest.fixture
def tmp_db_path(tmp_path):
    """Provide a temporary SQLite DB path for storage tests."""
    return str(tmp_path / "test_scanmenow.db")
