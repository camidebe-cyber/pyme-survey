"""
Admin routes: dashboard de monitoreo y exportacion CSV.
Acceso: /resultados
"""
import csv
import io
import os
import socket
import sqlite3
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from questions import QUESTIONS, AREA_LABELS, compute_result

PORT    = int(os.environ.get("PORT", 8777))
_data   = Path(os.environ.get("DATA_DIR", str(Path(__file__).parent)))
DB_PATH = _data / "survey.db"


def get_local_ip() -> str:
    """Detecta la mejor IP de red disponible (Walmart LAN o Hotspot movil)."""
    candidates = []
    try:
        import subprocess
        # ipconfig es el metodo mas confiable en Windows
        out = subprocess.check_output("ipconfig", text=True, timeout=3)
        for line in out.splitlines():
            if "IPv4" in line:
                ip = line.split(":")[-1].strip()
                if ip and not ip.startswith("127.") and not ip.startswith("169.254"):
                    candidates.append(ip)
    except Exception:
        pass

    if not candidates:
        # Fallback: socket trick
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("10.0.0.0", 80))
            candidates.append(s.getsockname()[0])
            s.close()
        except Exception:
            pass

    # Preferir IPs de hotspot (192.168.x.x) sobre IPs corporativas (10.x.x.x)
    for ip in candidates:
        if ip.startswith("192.168."):
            return ip
    return candidates[0] if candidates else "localhost"


def get_survey_url() -> tuple[str, str]:
    """Retorna (url, tipo_red). Respeta PUBLIC_URL si esta en la nube."""
    public = os.environ.get("PUBLIC_URL", "").rstrip("/")
    if public:
        return public + "/", "cloud"
    ip = get_local_ip()
    url = f"http://{ip}:{PORT}/"
    if ip == "localhost":
        tipo = "local"
    elif ip.startswith("192.168."):
        tipo = "hotspot"
    else:
        tipo = "lan"
    return url, tipo

DB_PATH   = Path(__file__).parent / "survey.db"
TEMPL     = Path(__file__).parent / "templates"
router    = APIRouter()
templates = Jinja2Templates(directory=TEMPL)

Q_MAP = {str(q["id"]): q for q in QUESTIONS}


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _all_sessions() -> list[dict]:
    with get_db() as conn:
        sessions = conn.execute(
            """SELECT id, rut, razon_social, email, created_at, completed
               FROM sessions ORDER BY created_at DESC"""
        ).fetchall()
        all_answers = conn.execute(
            "SELECT session_id, question_id, answer FROM answers"
        ).fetchall()

    ans_map: dict[str, dict] = {}
    for a in all_answers:
        ans_map.setdefault(a["session_id"], {})[str(a["question_id"])] = a["answer"]

    rows = []
    for s in sessions:
        sid     = s["id"]
        answers = ans_map.get(sid, {})
        result  = compute_result(answers)
        rows.append({
            "id":           sid,
            "rut":          s["rut"]          or "",
            "razon_social": s["razon_social"] or "",
            "email":        s["email"]        or "",
            "created_at":   s["created_at"]   or "",
            "completed":    bool(s["completed"]),
            "answers":      answers,
            **result,
        })
    return rows


def _stats(rows: list[dict]) -> dict:
    total       = len(rows)
    completadas = sum(1 for r in rows if r["completed"])
    intermedias = sum(1 for r in rows if r["completed"] and r["segment"] == "intermedia")
    maduras     = sum(1 for r in rows if r["completed"] and r["segment"] == "madura")
    pct_inter   = round(intermedias / completadas * 100) if completadas else 0
    pct_mad     = round(maduras    / completadas * 100) if completadas else 0
    avg_score   = round(sum(r["pct"] for r in rows if r["completed"]) / completadas) if completadas else 0
    return {
        "total": total, "completadas": completadas,
        "intermedias": intermedias, "maduras": maduras,
        "pct_inter": pct_inter, "pct_mad": pct_mad,
        "avg_score": avg_score,
        "en_progreso": total - completadas,
    }


# ── Reset datos (para limpiar pruebas) ────────────────────────────────────
@router.post("/resultados/reset")
async def reset_data():
    """Borra TODOS los datos. Solo para uso interno/testing."""
    with get_db() as conn:
        conn.execute("DELETE FROM answers")
        conn.execute("DELETE FROM sessions")
    return RedirectResponse(url="/resultados", status_code=303)


# ── Dashboard ───────────────────────────────────────────────────────────────
@router.get("/resultados", response_class=HTMLResponse)
async def dashboard(request: Request, q: str = ""):
    rows  = _all_sessions()
    if q:
        q_low = q.lower()
        rows  = [r for r in rows
                 if q_low in r["rut"].lower()
                 or q_low in r["razon_social"].lower()
                 or q_low in r["email"].lower()]
    stats = _stats(_all_sessions())
    survey_url, net_type = get_survey_url()
    return templates.TemplateResponse(request, "admin.html", {
        "rows":        rows,
        "stats":       stats,
        "q":           q,
        "area_labels": AREA_LABELS,
        "survey_url":  survey_url,
        "net_type":    net_type,
    })


# ── Detalle por sesion ────────────────────────────────────────────────────────
@router.get("/resultados/{session_id}", response_class=HTMLResponse)
async def detail(request: Request, session_id: str):
    rows = _all_sessions()
    row  = next((r for r in rows if r["id"] == session_id), None)
    if not row:
        return HTMLResponse("Sesion no encontrada", status_code=404)
    return templates.TemplateResponse(request, "admin_detail.html", {
        "s":           row,
        "questions":   QUESTIONS,
        "area_labels": AREA_LABELS,
    })


# ── Export CSV ────────────────────────────────────────────────────────────────
@router.get("/resultados/export/csv")
async def export_csv():
    rows = _all_sessions()

    output = io.StringIO()
    writer = csv.writer(output)

    # Encabezados
    headers = [
        "RUT", "Razon Social", "Email", "Fecha", "Completada",
        "Segmento", "Score %", "Puntaje", "Max Puntaje", "Areas Debiles",
    ]
    for q in QUESTIONS:
        headers.append(f"P{q['id']} - {q['text'][:40]}")
    writer.writerow(headers)

    # Filas
    for r in rows:
        row_data = [
            r["rut"],
            r["razon_social"],
            r["email"],
            r["created_at"][:16] if r["created_at"] else "",
            "Si" if r["completed"] else "No",
            r["segment_label"],
            r["pct"],
            r["score"],
            r["max_score"],
            " | ".join(AREA_LABELS[a]["label"] for a in r["weak_areas"] if a in AREA_LABELS),
        ]
        for q in QUESTIONS:
            row_data.append(r["answers"].get(str(q["id"]), ""))
        writer.writerow(row_data)

    output.seek(0)
    fecha = datetime.now().strftime("%Y%m%d_%H%M")
    return StreamingResponse(
        iter([output.getvalue().encode("utf-8-sig")]),  # utf-8-sig para Excel
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=pymes_cuestionario_{fecha}.csv"},
    )
