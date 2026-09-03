import os
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Union, Optional

# Points to 'data/history.db' in the project root
DEFAULT_DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data",
    "history.db"
)


def _get_connection(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Helper to ensure data directory exists and return an SQLite connection."""
    db_dir = os.path.dirname(os.path.abspath(db_path))
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DEFAULT_DB_PATH) -> None:
    """
    Initializes the SQLite database and creates the 'records' table
    along with an index on created_at for fast lookups.
    """
    conn = _get_connection(db_path)
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id TEXT PRIMARY KEY,
                created_at TIMESTAMP NOT NULL,
                title TEXT NOT NULL,
                raw_text TEXT,
                settings TEXT,
                result TEXT
            );
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_records_created_at
            ON records(created_at DESC);
        """)
    conn.close()


def save_transformation(
    record_id: str,
    title: str,
    raw_text: str,
    settings: Union[str, Dict[str, Any]],
    result: Union[str, Dict[str, Any]],
    db_path: str = DEFAULT_DB_PATH
) -> str:
    """
    Inserts or updates a transformation record in the 'records' table.
    Accepts settings and result either as pre-serialized JSON strings or Python dicts.
    """
    init_db(db_path)
    created_at = datetime.utcnow().isoformat() + "Z"

    # Serialize JSON if dictionaries or lists were passed
    settings_str = (
        json.dumps(settings)
        if isinstance(settings, (dict, list))
        else str(settings)
    )
    result_str = (
        json.dumps(result)
        if isinstance(result, (dict, list))
        else str(result)
    )

    conn = _get_connection(db_path)
    with conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO records (id, created_at, title, raw_text, settings, result)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (record_id, created_at, title, raw_text, settings_str, result_str)
        )
    conn.close()
    return record_id


def fetch_history(
    limit: int = 10,
    db_path: str = DEFAULT_DB_PATH
) -> List[Dict[str, Any]]:
    """
    Retrieves the most recent records from the database ordered by created_at DESC.
    Automatically parses settings and result JSON strings back into Python dictionaries.
    """
    init_db(db_path)
    conn = _get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, created_at, title, raw_text, settings, result
        FROM records
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()

    history = []
    for row in rows:
        row_dict = dict(row)
        # Parse JSON fields back to dicts for clean consumption
        for col in ["settings", "result"]:
            if row_dict.get(col):
                try:
                    row_dict[col] = json.loads(row_dict[col])
                except (json.JSONDecodeError, TypeError):
                    pass
        history.append(row_dict)

    return history
