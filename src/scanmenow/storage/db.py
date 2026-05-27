"""SQLite database initialization and connection management."""

import os
import sqlite3
from pathlib import Path

DEFAULT_DB_PATH = Path.home() / ".scanmenow" / "scanmenow.db"


def get_db_path() -> Path:
    """Return the DB file path from SCANMENOW_DB_PATH env var or default."""
    raw = os.getenv("SCANMENOW_DB_PATH")
    return Path(raw) if raw else DEFAULT_DB_PATH


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    """
    Open a SQLite connection with foreign key enforcement enabled.

    Args:
        db_path: Path to the .db file. Uses get_db_path() if not provided.

    Returns:
        sqlite3.Connection with row_factory set to sqlite3.Row.
    """
    path = db_path or get_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: Path | None = None) -> None:
    """
    Create the database schema if it does not already exist.

    Idempotent: safe to call on an existing database. ALTER TABLE migrations
    are guarded against duplicate-column errors.

    Args:
        db_path: Path to the .db file. Uses get_db_path() if not provided.
    """
    conn = get_connection(db_path)
    with conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS scan_jobs (
                job_id       TEXT PRIMARY KEY,
                source_path  TEXT NOT NULL DEFAULT '',
                status       TEXT NOT NULL DEFAULT 'pending',
                created_at   TEXT NOT NULL,
                completed_at TEXT
            );

            CREATE TABLE IF NOT EXISTS findings (
                finding_id   TEXT PRIMARY KEY,
                job_id       TEXT NOT NULL REFERENCES scan_jobs(job_id),
                entity_type  TEXT NOT NULL,
                start        INTEGER NOT NULL,
                end          INTEGER NOT NULL,
                score        REAL NOT NULL,
                text_snippet TEXT NOT NULL DEFAULT '',
                source_file  TEXT NOT NULL DEFAULT ''
            );
        """)
        # Idempotent migrations -- catch OperationalError for duplicate column.
        for migration in [
            "ALTER TABLE findings ADD COLUMN created_at TEXT NOT NULL DEFAULT ''",
        ]:
            try:
                conn.execute(migration)
            except sqlite3.OperationalError:
                pass  # column already exists
    conn.close()
