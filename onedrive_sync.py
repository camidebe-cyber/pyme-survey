"""
onedrive_sync.py
================
Envia un webhook a Power Automate cada vez que una PyME
termina el cuestionario. Power Automate agrega la fila al
Excel en OneDrive de Camila automaticamente.

Configuracion:
    Variable de entorno en Render:
        POWER_AUTOMATE_URL = https://prod-XX.westus.logic.azure.com/...

Si la variable no esta configurada, el modulo no hace nada
y logea un aviso (no rompe la app).
"""
import asyncio
import logging
import os
from datetime import datetime

log = logging.getLogger(__name__)

POWER_AUTOMATE_URL = os.environ.get("POWER_AUTOMATE_URL", "")


def _build_payload(session: dict, answers: dict, result: dict) -> dict:
    """Arma el JSON que se envia a Power Automate."""
    from questions import QUESTIONS, AREA_LABELS  # evita import circular

    # Respuestas como string separado por pipes para Excel
    respuestas_flat = {
        f"P{q['id']}": answers.get(str(q["id"]), "")
        for q in QUESTIONS
    }

    areas_debiles = " | ".join(
        AREA_LABELS[a]["label"]
        for a in result.get("weak_areas", [])
        if a in AREA_LABELS
    )

    return {
        # Identificacion
        "rut":          session.get("rut", ""),
        "razon_social": session.get("razon_social", ""),
        "email":        session.get("email", ""),
        "fecha":        datetime.now().strftime("%Y-%m-%d %H:%M"),
        # Resultado
        "segmento":     result.get("segment_label", ""),
        "score_pct":    result.get("pct", 0),
        "score":        result.get("score", 0),
        "max_score":    result.get("max_score", 0),
        "areas_debiles": areas_debiles,
        # Respuestas individuales
        **respuestas_flat,
    }


async def notify_new_response(session: dict, answers: dict, result: dict) -> None:
    """
    Llama al webhook de Power Automate de forma asincrona.
    Si falla, solo logea — nunca rompe el flujo de la app.
    """
    if not POWER_AUTOMATE_URL:
        log.warning("[OneDrive Sync] POWER_AUTOMATE_URL no configurada. Saltando sync.")
        return

    payload = _build_payload(session, answers, result)

    try:
        import httpx
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                POWER_AUTOMATE_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
            )
        if resp.status_code in (200, 202):
            log.info(f"[OneDrive Sync] OK para {payload['razon_social']}")
        else:
            log.warning(f"[OneDrive Sync] Status inesperado: {resp.status_code}")

    except Exception as exc:
        # Nunca debe romper la experiencia del usuario
        log.error(f"[OneDrive Sync] Error al notificar: {exc}")