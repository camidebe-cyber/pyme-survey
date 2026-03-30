"""
Router para la experiencia alternativa /formulario.
Misma DB, mismo panel. Diseño renovado para comparar.
"""
from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from db import create_session, get_session, get_answers, mark_complete, save_answer
from questions import BLOCKS, QUESTIONS, compute_result

TEMPL    = Path(__file__).parent / "templates"
router   = APIRouter(prefix="/formulario")
templates = Jinja2Templates(directory=TEMPL)

TOTAL_Q  = len(QUESTIONS)


def _progress(q_index: int) -> int:
    return round((q_index / TOTAL_Q) * 100)


def _q_ctx(q: dict, q_index: int, session_id: str,
           answers: dict, session: dict) -> dict:
    return {
        "session_id":   session_id,
        "q":            q,
        "q_index":      q_index,
        "total":        TOTAL_Q,
        "progress":     _progress(q_index),
        "block_label":  BLOCKS[q["block"]]["label"],
        "block_emoji":  BLOCKS[q["block"]]["emoji"],
        "company":      session.get("razon_social") or answers.get("1", ""),
        "saved_answer": answers.get(str(q["id"]), ""),
        # flag para que las partials sepan que el target del HTMX swap
        # vive dentro de /formulario (cambia hx-target si fuera necesario)
        "base_prefix":  "/formulario",
    }


@router.get("", response_class=HTMLResponse)
async def formulario_welcome(request: Request):
    return templates.TemplateResponse(request, "formulario_welcome.html", {})


@router.post("/start")
async def formulario_start(
    rut:          str = Form(...),
    razon_social: str = Form(...),
    email:        str = Form(default=""),
):
    sid = create_session(rut, razon_social, email)
    return RedirectResponse(url=f"/formulario/{sid}", status_code=303)


@router.get("/{session_id}", response_class=HTMLResponse)
async def formulario_survey(request: Request, session_id: str):
    q       = QUESTIONS[0]
    session = get_session(session_id)
    answers = get_answers(session_id)
    return templates.TemplateResponse(
        request, "formulario_survey.html",
        _q_ctx(q, 0, session_id, answers, session)
    )
