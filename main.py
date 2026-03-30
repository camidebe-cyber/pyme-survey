"""
FastAPI app - Cuestionario PyME Walmart
SQLite para persistir respuestas. HTMX para UX tipo Typeform.
"""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from db import create_session, get_session, save_answer, get_answers, mark_complete, init_db
from questions import BLOCKS, QUESTIONS, compute_result

TOTAL_Q = len(QUESTIONS)
TEMPL   = Path(__file__).parent / "templates"


# ── App ───────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app       = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory=TEMPL)

# Registrar rutas del admin
from admin import router as admin_router  # noqa: E402
app.include_router(admin_router)

# Formulario alternativo
from formulario_router import router as formulario_router  # noqa: E402
app.include_router(formulario_router)


# ── Survey helpers ────────────────────────────────────────────────────────
def progress_pct(q_index: int) -> int:
    return round((q_index / TOTAL_Q) * 100)


def _q_ctx(q: dict, q_index: int, session_id: str,
           answers: dict, session: dict) -> dict:
    return {
        "session_id":   session_id,
        "q":            q,
        "q_index":      q_index,
        "total":        TOTAL_Q,
        "progress":     progress_pct(q_index),
        "block_label":  BLOCKS[q["block"]]["label"],
        "block_emoji":  BLOCKS[q["block"]]["emoji"],
        "company":      session.get("razon_social") or answers.get("1", ""),
        "saved_answer": answers.get(str(q["id"]), ""),
    }


# ── Routes ────────────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def welcome(request: Request):
    """Pantalla de identificacion: RUT + Razon Social."""
    return templates.TemplateResponse(request, "welcome.html", {})


@app.post("/start")
async def start(
    rut:          str = Form(...),
    razon_social: str = Form(...),
    email:        str = Form(default=""),
):
    """Crea la sesion y redirige al cuestionario."""
    sid = create_session(rut, razon_social, email)
    return RedirectResponse(url=f"/survey/{sid}", status_code=303)


@app.get("/survey/{session_id}", response_class=HTMLResponse)
async def survey(request: Request, session_id: str):
    """Primera pregunta del cuestionario."""
    q       = QUESTIONS[0]
    session = get_session(session_id)
    answers = get_answers(session_id)
    return templates.TemplateResponse(request, "survey.html",
        _q_ctx(q, 0, session_id, answers, session))


@app.post("/answer", response_class=HTMLResponse)
async def answer(
    request:    Request,
    session_id: str = Form(...),
    q_index:    int = Form(...),
    answer:     str = Form(default=""),
):
    try:
        q = QUESTIONS[q_index]
        if answer.strip():
            save_answer(session_id, q["id"], answer.strip())

        next_index = q_index + 1
        answers    = get_answers(session_id)
        session    = get_session(session_id)

        if next_index >= TOTAL_Q:
            mark_complete(session_id)
            result  = compute_result(answers)
            company = session.get("razon_social") or answers.get("1", "PyME")
            return templates.TemplateResponse(request, "result.html",
                {"company": company, **result})

        nq = QUESTIONS[next_index]
        return templates.TemplateResponse(request, "question.html",
            _q_ctx(nq, next_index, session_id, answers, session))

    except Exception as exc:
        # Retorna un mensaje de error visible en el cuestionario (no pantalla en blanco)
        return HTMLResponse(
            f"""<div style='padding:2rem;text-align:center;color:#cc0000;font-family:sans-serif'>
                <p style='font-size:1.5rem'>&#9888; Error inesperado</p>
                <p style='color:#666;margin-top:.5rem'>{exc}</p>
                <p style='margin-top:1rem'>
                  <a href='/' style='color:#002060;font-weight:bold'>&#8592; Volver al inicio</a>
                </p></div>""",
            status_code=500
        )


@app.post("/prev", response_class=HTMLResponse)
async def prev(
    request:    Request,
    session_id: str = Form(...),
    q_index:    int = Form(...),
    answer:     str = Form(default=""),
):
    try:
        q = QUESTIONS[q_index]
        if answer.strip():
            save_answer(session_id, q["id"], answer.strip())

        prev_index = max(0, q_index - 1)
        answers    = get_answers(session_id)
        session    = get_session(session_id)
        pq         = QUESTIONS[prev_index]
        return templates.TemplateResponse(request, "question.html",
            _q_ctx(pq, prev_index, session_id, answers, session))
    except Exception as exc:
        return HTMLResponse(
            f"""<div style='padding:2rem;text-align:center;color:#cc0000;font-family:sans-serif'>
                <p style='font-size:1.5rem'>&#9888; Error inesperado</p>
                <p style='color:#666;margin-top:.5rem'>{exc}</p>
                <p style='margin-top:1rem'>
                  <a href='/' style='color:#002060;font-weight:bold'>&#8592; Volver al inicio</a>
                </p></div>""",
            status_code=500
        )
