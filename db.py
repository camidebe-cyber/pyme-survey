"""
DB helpers – soporta SQLite (local) y PostgreSQL (produccion Render/Neon).
Detecta automaticamente segun la variable DATABASE_URL.
"""
import os
import sqlite3
import uuid
from contextlib import contextmanager
from pathlib import Path

# ── Deteccion de backend ────────────────────────────────────────────────────
DATABASE_URL = os.environ.get("DATABASE_URL", "")
USE_POSTGRES  = DATABASE_URL.startswith("postgres")

# SQLite (solo cuando no hay DATABASE_URL)
_data_dir = Path(os.environ.get("DATA_DIR", Path(__file__).parent))
DB_PATH   = _data_dir / "survey.db"


# ── Conexion genérica ───────────────────────────────────────────────────────
@contextmanager
def get_conn():
    """Devuelve una conexion al backend activo como context manager."""
    if USE_POSTGRES:
        import psycopg2
        import psycopg2.extras
        conn = psycopg2.connect(DATABASE_URL,
                                cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    else:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


def _ph(n: int = 1) -> str:
    """Placeholder correcto segun backend: ? (SQLite) o %s (Postgres)."""
    ph = "%s" if USE_POSTGRES else "?"
    return ", ".join([ph] * n)


def _row(cursor, row):
    """Convierte fila a dict de forma compatible con ambos backends."""
    if USE_POSTGRES:
        cols = [d[0] for d in cursor.description]
        return dict(zip(cols, row))
    return dict(row)


# ── Inicializar tablas ──────────────────────────────────────────────────────
def init_db():
    if USE_POSTGRES:
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id           TEXT PRIMARY KEY,
                    rut          TEXT DEFAULT '',
                    razon_social TEXT DEFAULT '',
                    email        TEXT DEFAULT '',
                    created_at   TIMESTAMPTZ DEFAULT NOW(),
                    completed    INTEGER DEFAULT 0
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS answers (
                    id          SERIAL PRIMARY KEY,
                    session_id  TEXT,
                    question_id INTEGER,
                    answer      TEXT,
                    created_at  TIMESTAMPTZ DEFAULT NOW()
                )
            """)
    else:
        with get_conn() as conn:
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


# ── CRUD ────────────────────────────────────────────────────────────────────
def create_session(rut: str, razon_social: str, email: str) -> str:
    sid = str(uuid.uuid4())
    ph  = _ph(4)
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            f"INSERT INTO sessions (id, rut, razon_social, email) VALUES ({ph})",
            (sid, rut.strip(), razon_social.strip(), email.strip())
        )
    return sid


def get_session(session_id: str) -> dict:
    ph = _ph(1)
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM sessions WHERE id={ph}", (session_id,))
        row = cur.fetchone()
        return _row(cur, row) if row else {}


def save_answer(session_id: str, question_id: int, answer: str):
    ph1, ph3 = _ph(1), _ph(3)
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            f"DELETE FROM answers WHERE session_id={ph1} AND question_id={ph1}",
            (session_id, question_id)
        )
        cur.execute(
            f"INSERT INTO answers (session_id, question_id, answer) VALUES ({ph3})",
            (session_id, question_id, answer)
        )
        if not USE_POSTGRES:
            cur.execute(f"INSERT OR IGNORE INTO sessions (id) VALUES ({ph1})", (session_id,))


def get_answers(session_id: str) -> dict:
    ph = _ph(1)
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            f"SELECT question_id, answer FROM answers WHERE session_id={ph}",
            (session_id,)
        )
        rows = cur.fetchall()
        return {str(r[0] if USE_POSTGRES else r["question_id"]):
                (r[1] if USE_POSTGRES else r["answer"]) for r in rows}


def mark_complete(session_id: str):
    ph = _ph(1)
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(f"UPDATE sessions SET completed=1 WHERE id={ph}", (session_id,))


# ── Alias legacy (compatibilidad con codigo existente) ──────────────────────
def get_db():
    """Alias para compatibilidad con admin.py que usa get_db()."""
    if USE_POSTGRES:
        raise RuntimeError("Usa get_conn() en modo PostgreSQL")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn