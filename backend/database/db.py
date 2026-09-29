import os
import sqlite3
import json
import hashlib
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
    with an immutable created_at timestamp and a SHA-256 hash column
    for tamper-proof integrity (IT Act 2000 Sec 43A / 72A).
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
                result TEXT,
                sha256_hash TEXT
            );
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_records_created_at
            ON records(created_at DESC);
        """)
        # Safe migration if table was previously created without sha256_hash
        try:
            conn.execute("ALTER TABLE records ADD COLUMN sha256_hash TEXT;")
        except sqlite3.OperationalError:
            pass  # Column already exists
    conn.close()


def generate_sha256_hash(payload: Union[str, Dict[str, Any]]) -> str:
    """
    Generates a deterministic SHA-256 cryptographic digital fingerprint of output content.
    Fulfills IT Act 2000 Section 43A & 72A tamper-proof integrity requirements.
    """
    if isinstance(payload, dict):
        # Sort keys to ensure deterministic byte representation
        serialized = json.dumps(payload, sort_keys=True)
    elif isinstance(payload, str):
        serialized = payload
    else:
        serialized = str(payload)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def save_transformation(
    record_id: str,
    title: str,
    raw_text: str,
    settings: Union[str, Dict[str, Any]],
    result: Union[str, Dict[str, Any]],
    sha256_hash: Optional[str] = None,
    db_path: str = DEFAULT_DB_PATH
) -> str:
    """
    Inserts or updates a transformation record with an immutable UTC ISO timestamp
    and digital SHA-256 hash fingerprint.
    """
    init_db(db_path)

    # Ensure hash is computed if not explicitly passed
    if sha256_hash is None:
        sha256_hash = generate_sha256_hash(result)

    settings_str = json.dumps(settings) if isinstance(settings, dict) else str(settings)
    result_str = json.dumps(result) if isinstance(result, dict) else str(result)
    
    # Immutable UTC ISO timestamp with 'Z' suffix
    created_at = datetime.utcnow().isoformat() + "Z"

    conn = _get_connection(db_path)
    with conn:
        conn.execute("""
            INSERT OR REPLACE INTO records (id, created_at, title, raw_text, settings, result, sha256_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (record_id, created_at, title, raw_text, settings_str, result_str, sha256_hash))
    conn.close()
    return record_id


def fetch_history(limit: int = 10, db_path: str = DEFAULT_DB_PATH) -> List[Dict[str, Any]]:
    """
    Fetches the most recent transformation records including cryptographic hash and timestamp.
    """
    init_db(db_path)
    conn = _get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, created_at, title, raw_text, settings, result, sha256_hash
        FROM records
        ORDER BY created_at DESC
        LIMIT ?;
    """, (limit,))
    rows = cursor.fetchall()
    
    records = []
    for row in rows:
        item = dict(row)
        for col in ["settings", "result"]:
            if item.get(col):
                try:
                    item[col] = json.loads(item[col])
                except (json.JSONDecodeError, TypeError):
                    pass
        records.append(item)

    conn.close()
    return records


# ====================================================================
# 🛡️ DPDP Act 2023 (Sec 12) Right to Erasure / Purge Functions
# ====================================================================
def delete_record(record_id: Union[str, int], db_path: str = DEFAULT_DB_PATH) -> bool:
    """
    DPDP Act 2023 (Sec 12) Right to Erasure.
    Permanently wipes a specific transformation record by ID from history.
    """
    init_db(db_path)
    conn = _get_connection(db_path)
    with conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM records WHERE id = ?", (str(record_id),))
        deleted = cursor.rowcount > 0
    conn.close()
    return deleted


def purge_all_history(db_path: str = DEFAULT_DB_PATH) -> bool:
    """
    DPDP Act 2023 (Sec 12) Complete History Purge.
    Permanently deletes all historical records from the database.
    """
    init_db(db_path)
    conn = _get_connection(db_path)
    with conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM records")
    conn.close()
    return True


# ====================================================================
# 🔍 Security Auditing Function
# ====================================================================
def verify_record_integrity(record_id: str, db_path: str = DEFAULT_DB_PATH) -> Dict[str, Any]:
    """
    Auditing utility:
    Recomputes the SHA-256 hash of the stored output JSON and compares it against
    the stored digital fingerprint to verify that no tampering occurred.
    """
    init_db(db_path)
    conn = _get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, created_at, result, sha256_hash
        FROM records
        WHERE id = ?;
    """, (record_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"verified": False, "error": "Record not found"}

    stored_hash = row["sha256_hash"]
    computed_hash = generate_sha256_hash(row["result"])
    is_intact = (stored_hash == computed_hash)

    return {
        "record_id": record_id,
        "created_at": row["created_at"],
        "stored_sha256": stored_hash,
        "computed_sha256": computed_hash,
        "is_intact": is_intact,
        "audit_status": "VERIFIED_AUTHENTIC" if is_intact else "TAMPER_DETECTED"
    }

# =====================================================================
# PROVENANCE LEDGER & CRYPTOGRAPHIC CHAIN (SIH CYBERSECURITY)
# =====================================================================

def init_ledger():
    """Initializes the cryptographic provenance ledger table."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS provenance_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            block_index INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            source_hash TEXT NOT NULL,
            output_hash TEXT NOT NULL,
            parameters TEXT NOT NULL,
            operator TEXT NOT NULL,
            previous_hash TEXT NOT NULL,
            block_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Ensure table is created at startup
init_ledger()

def add_ledger_entry(source_text: str, output_data: Any, parameters: dict, operator: str = "Security_Analyst_01"):
    """Appends an immutable block to the Provenance Ledger."""
    conn = _get_connection()
    cursor = conn.cursor()
    
    source_hash = generate_sha256_hash(source_text)
    output_hash = generate_sha256_hash(output_data)
    param_str = json.dumps(parameters, sort_keys=True)
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    cursor.execute("SELECT block_index, block_hash FROM provenance_ledger ORDER BY id DESC LIMIT 1")
    last_block = cursor.fetchone()
    
    if last_block:
        block_index = last_block["block_index"] + 1
        previous_hash = last_block["block_hash"]
    else:
        block_index = 1
        previous_hash = "0" * 64  # Genesis block
        
    block_payload = f"{block_index}|{timestamp}|{source_hash}|{output_hash}|{param_str}|{operator}|{previous_hash}"
    block_hash = generate_sha256_hash(block_payload)
    
    cursor.execute("""
        INSERT INTO provenance_ledger 
        (block_index, timestamp, source_hash, output_hash, parameters, operator, previous_hash, block_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (block_index, timestamp, source_hash, output_hash, param_str, operator, previous_hash, block_hash))
    
    conn.commit()
    conn.close()
    return {"block_index": block_index, "block_hash": block_hash, "output_hash": output_hash}

def verify_content(content_text: str):
    """Verifies if input text matches any authentic output in the ledger."""
    target_hash = generate_sha256_hash(content_text.strip())
    conn = _get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM provenance_ledger 
        WHERE output_hash = ? OR source_hash = ?
        ORDER BY id DESC LIMIT 1
    """, (target_hash, target_hash))
    match = cursor.fetchone()
    conn.close()
    
    if match:
        return {
            "status": "AUTHENTIC",
            "is_authentic": True,
            "computed_hash": target_hash,
            "matched_block": {
                "block_index": match["block_index"],
                "timestamp": match["timestamp"],
                "operator": match["operator"],
                "parameters": json.loads(match["parameters"]),
                "block_hash": match["block_hash"]
            }
        }
    return {
        "status": "TAMPERED",
        "is_authentic": False,
        "computed_hash": target_hash,
        "matched_block": None
    }
