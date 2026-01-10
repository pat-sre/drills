import sqlite3
from contextlib import contextmanager
from typing import Iterator

from .config import DB_PATH


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    """Context manager for database connections."""
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    """Initialize database schema."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS exercise_stats (
                topic TEXT,
                name TEXT,
                attempts INTEGER DEFAULT 0,
                passes INTEGER DEFAULT 0,
                PRIMARY KEY (topic, name)
            )
        """)


def record_attempt(topic: str, name: str, passed: bool) -> None:
    """Record an exercise attempt."""
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO exercise_stats (topic, name, attempts, passes)
            VALUES (?, ?, 1, ?)
            ON CONFLICT(topic, name) DO UPDATE SET
                attempts = attempts + 1,
                passes = passes + ?
            """,
            (topic, name, 1 if passed else 0, 1 if passed else 0),
        )


def get_all_stats() -> dict[tuple[str, str], dict[str, int]]:
    """Get stats for all exercises."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT topic, name, attempts, passes FROM exercise_stats"
        ).fetchall()
    return {(r[0], r[1]): {"attempts": r[2], "passes": r[3]} for r in rows}


def reset_stats(topic: str, name: str) -> None:
    """Reset stats for an exercise."""
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM exercise_stats WHERE topic = ? AND name = ?",
            (topic, name),
        )
