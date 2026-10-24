
import json
import sqlite3
from datetime import datetime, timezone

from config import DATABASE_PATH


def get_connection(database_path=None):
    """Open a SQLite connection for the experiment database."""
    connection = sqlite3.connect(str(database_path or DATABASE_PATH))
    connection.row_factory = sqlite3.Row
    return connection


def init_db(database_path=None):
    """Create the experiment history table if it does not exist."""
    with get_connection(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS experiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                workload TEXT NOT NULL,
                iterations_requested INTEGER NOT NULL,
                iterations_completed INTEGER NOT NULL,
                measurement_interval INTEGER NOT NULL,
                duration_seconds REAL NOT NULL,
                initial_memory_mb REAL NOT NULL,
                peak_memory_mb REAL NOT NULL,
                final_memory_mb REAL NOT NULL,
                memory_growth_mb REAL NOT NULL,
                measurements_json TEXT NOT NULL
            )
            """
        )


def save_experiment(
    result,
    iterations_requested,
    measurement_interval,
    database_path=None,
):
    """Save an experiment summary and its measurement timeline."""
    created_at = datetime.now(timezone.utc).isoformat(
        timespec="seconds"
    )

    with get_connection(database_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO experiments (
                created_at,
                workload,
                iterations_requested,
                iterations_completed,
                measurement_interval,
                duration_seconds,
                initial_memory_mb,
                peak_memory_mb,
                final_memory_mb,
                memory_growth_mb,
                measurements_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                created_at,
                result["workload"],
                iterations_requested,
                result["iterations_completed"],
                measurement_interval,
                result["duration_seconds"],
                result["initial_memory_mb"],
                result["peak_memory_mb"],
                result["final_memory_mb"],
                result["memory_growth_mb"],
                json.dumps(result["measurements"]),
            ),
        )

        return cursor.lastrowid


def list_experiments(database_path=None, limit=25):
    """Return recent experiment records, newest first."""
    with get_connection(database_path) as connection:
        rows = connection.execute(
            """
            SELECT *
            FROM experiments
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]


def get_experiment(experiment_id, database_path=None):
    """Retrieve one experiment and decode its measurement timeline."""
    with get_connection(database_path) as connection:
        row = connection.execute(
            "SELECT * FROM experiments WHERE id = ?",
            (experiment_id,),
        ).fetchone()

    if row is None:
        return None

    result = dict(row)
    result["measurements"] = json.loads(
        result.pop("measurements_json")
    )

    return result