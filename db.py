"""
DB helpers compartidos entre main.py, admin.py y formulario_router.py.
Single Responsibility: solo acceso a datos.
"""
import os
import sqlite3
import uuid
from pathlib import Path

_data_dir = Path(os.environ.get("DATA_DIR", Path(__file__).parent))
DB_PATH   = _data_dir / "survey.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS sessions (
                id           TEXT PRIMARY KEY,
                rut          TEXT DEFAULT '',
                razon_social TEXT DEFAULT '',
                email        TEXT DEFAULT '',
                created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
                completed    INTEGER  DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS answers (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id  TEXT,
                question_id INTEGER,
                answer      TEXT,
                created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
        for col, default in [("rut", "''"), ("razon_social", "''"), ("email", "''")]:
            try:
                conn.execute(f"ALTER TABLE sessions ADD COLUMN {col} TEXT DEFAULT {default}")
            except Exception:
                pass


def create_session(rut: str, razon_social: str, email: str) -> str:
    sid = str(uuid.uuid4())
    with get_db() as conn:
        conn.execute(
            "INSERT INTO sessions (id, rut, razon_social, email) VALUES (?,?,?,?)",
            (sid, rut.strip(), razon_social.strip(), email.strip())
        )
    return sid


def get_session(session_id: str) -> dict:
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM sessions WHERE id=?", (session_id,)
        ).fetchone()
    return dict(row) if row else {}


def save_answer(session_id: str, question_id: int, answer: str):
    with get_db() as conn:
        conn.execute(
            "DELETE FROM answers WHERE session_id=? AND question_id=?",
            (session_id, question_id)
        )
        conn.execute(
            "INSERT INTO answers (session_id, question_id, answer) VALUES (?,?,?)",
            (session_id, question_id, answer)
        )
        conn.execute(
            "INSERT OR IGNORE INTO sessions (id) VALUES (?)", (session_id,)
        )


def get_answers(session_id: str) -> dict:
    with get_db() as conn:
        rows = conn.execute(
            "SELECT question_id, answer FROM answers WHERE session_id=?",
            (session_id,)
        ).fetchall()
    return {str(r["question_id"]): r["answer"] for r in rows}


def mark_complete(session_id: str):
    with get_db() as conn:
        conn.execute("UPDATE sessions SET completed=1 WHERE id=?", (session_id,))
