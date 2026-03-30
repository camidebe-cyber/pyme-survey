"""
Preguntas del cuestionario PyME Walmart.
25 preguntas, 5 bloques.
"""

BLOCKS = {
    "identificacion": {"label": "Identificación",      "emoji": "🏢"},
    "ecosistema":     {"label": "Ecosistema Retail",   "emoji": "📊"},
    "comercial":      {"label": "Gestión Comercial",   "emoji": "🛒"},
    "negocio":        {"label": "Negocio & Datos",     "emoji": "💼"},
    "operacional":    {"label": "Gestión Operacional", "emoji": "⚙️"},
}

QUESTIONS = [
    # ─ BLOQUE 1: Identificación ────────────────────────────────
    {
        "id": 1, "block": "identificacion", "type": "text",
        "emoji": "🏢",
        "text": "¿Cómo se llama tu empresa o marca?",
        "subtitle": "Con esto personalizamos tu experiencia",
        "options": [], "score_map": {},
        "placeholder": "Ej: Alimentos Los Andes",
    },
    {
        "id": 2, "block": "identificacion", "type": "choice",
        "emoji": "🛍️",
        "text": "¿En qué categoría está tu producto?",
        "subtitle": "",
        "options": [
            {"value": "alimentos",   "label": "Alimentos y Bebidas",  "icon": "🥗"},
            {"value": "limpieza",    "label": "Limpieza y Hogar",     "icon": "🧹"},
            {"value": "cuidado",     "label": "Cuidado Personal",     "icon": "💄"},
            {"value": "textil",      "label": "Textil y Ropa",        "icon": "👕"},
            {"value": "electronica", "label": "Electrónica",         "icon": "📱"},
            {"value": "otro",        "label": "Otra categoría",      "icon": "📦"},
        ],
        "score_map": {},
    },
    {
        "id": 3, "block": "identificacion", "type": "choice",
        "emoji": "📅",
        "text": "¿Hace cuánto tiempo eres proveedor de Walmart?",
        "subtitle": "",
        "options": [
            {"value": "menos6m", "label": "Menos de 6 meses",       "icon": "🌱"},
            {"value": "6a12m",   "label": "Entre 6 meses y 1 año",  "icon": "🌿"},
            {"value": "1a3a",    "label": "Entre 1 y 3 años",       "icon": "🌳"},
            {"value": "mas3a",   "label": "Más de 3 años",          "icon": "🏆"},
        ],
        "score_map": {"menos6m": 0, "6a12m": 1, "1a3a": 2, "mas3a": 2},
    },
    {
        "id": 4, "block": "identificacion", "type": "choice",
        "emoji": "⚡",
        "text": "¿Ingresaste al programa Potencia PyME de Walmart?",
        "subtitle": "¿Participaste de las presentaciones y conversatorios?",
        "options": [
            {"value": "si_cursos",
             "label": "Sí, ingresé y participé de las presentaciones y conversatorios.",
             "icon": "✅"},
            {"value": "si_sin_cursos",
             "label": "Sí, pero no participé de nada adicional.",
             "icon": "📋"},
            {
                "value": "otra_via",
                "label": "No, entré por otra vía.",
                "icon": "🔄",
                "has_text_followup": True,
                "followup_placeholder": "Especifica cuál (máx 30 car.)",
                "followup_maxlength": 30,
            },
        ],
        "score_map": {"si_cursos": 2, "si_sin_cursos": 1, "otra_via": 0},
    },

    # ─ BLOQUE 2: Ecosistema Retail ────────────────────────────
    {
        "id": 5, "block": "ecosistema", "type": "choice",
        "emoji": "📦",
        "text": "¿Conoces tu Fill Rate actual con Walmart?",
        "subtitle": "Fill Rate = % de pedidos que entregas completos y a tiempo al CD",
        "options": [
            {"value": "no",       "label": "No, desconozco qué es el Fill Rate",         "icon": "🤔"},
            {"value": "concepto", "label": "Sí, sé qué es, pero no lo sigo",            "icon": "📖"},
            {"value": "parcial",  "label": "Sí, lo conozco y reviso ocasionalmente",     "icon": "👀"},
            {"value": "si",       "label": "Sí, lo reviso y gestiono activamente",       "icon": "💪"},
        ],
        "score_map": {"no": 0, "concepto": 1, "parcial": 1, "si": 2},
        "tag": "supply",
    },
    {
        "id": 6, "block": "ecosistema", "type": "choice",
        "emoji": "📊",
        "text": "¿Sabes qué es el In-Stock y lo monitoreas?",
        "subtitle": "ISR = % del tiempo que tu producto está disponible en góndola",
        "options": [
            {"value": "no",       "label": "No, no lo conozco",                         "icon": "🤔"},
            {"value": "concepto", "label": "Sí, lo conozco pero no lo sigo",             "icon": "📖"},
            {"value": "si",       "label": "Sí, lo monitoreo activamente",               "icon": "💪"},
        ],
        "score_map": {"no": 0, "concepto": 1, "si": 2},
        "tag": "supply",
    },
    {
        "id": 7, "block": "ecosistema", "type": "choice",
        "emoji": "💻",
        "text": "¿Tienes acceso y usas Retail Link?",
        "subtitle": "Plataforma de Walmart para ver datos de venta, habilitaciones y más",
        "options": [
            {"value": "no_acceso",  "label": "No, no tengo acceso",               "icon": "🚫"},
            {"value": "no_lo_uso",  "label": "Sí, tengo acceso, pero no lo uso",    "icon": "😅"},
            {"value": "uso_basico", "label": "Sí, lo uso para ver ventas básicas", "icon": "📈"},
        ],
        "score_map": {"no_acceso": 0, "no_lo_uso": 0, "uso_basico": 2},
        "tag": "retail_link",
    },
    {
        "id": 8, "block": "ecosistema", "type": "choice",
        "emoji": "🗓️",
        "text": "¿Con qué frecuencia revisas el desempeño de tus ventas?",
        "subtitle": "",
        "options": [
            {"value": "nunca",   "label": "No lo hago",          "icon": "😬"},
            {"value": "mensual", "label": "Una vez al mes",      "icon": "📅"},
            {"value": "semanal", "label": "Semanalmente",        "icon": "📆"},
            {"value": "diario",  "label": "Diariamente",         "icon": "🔥"},
        ],
        "score_map": {"nunca": 0, "mensual": 1, "semanal": 2, "diario": 2},
        "tag": "retail_link",
    },
    {
        "id": 9, "block": "ecosistema", "type": "choice",
        "emoji": "🏥",
        "text": "¿Cómo manejas el proceso de despacho al Centro de Distribución?",
        "subtitle": "Etiquetas, OC, ventanas horarias, documentación",
        "options": [
            {"value": "no_se",  "label": "No, no entiendo bien el proceso",             "icon": "😕"},
            {"value": "basico", "label": "Sí, pero tengo dudas frecuentes",             "icon": "🤷"},
            {"value": "domino", "label": "Sí, lo domino sin problemas",                 "icon": "✅"},
        ],
        "score_map": {"no_se": 0, "basico": 1, "domino": 2},
        "tag": "supply",
    },
    {
        "id": 10, "block": "ecosistema", "type": "choice",
        "emoji": "👁️",
        "text": "¿Tienes visibilidad del inventario de tu producto en tienda?",
        "subtitle": "Cuántas unidades hay en sala y en bodega",
        "options": [
            {"value": "no",      "label": "No, no tengo esa información",              "icon": "❌"},
            {"value": "avisada", "label": "Sí, pero solo cuando me avisan del quiebre", "icon": "🔔"},
            {"value": "si",      "label": "Sí, lo monitoreo regularmente",              "icon": "✅"},
        ],
        "score_map": {"no": 0, "avisada": 1, "si": 2},
        "tag": "supply",
    },
    {
        "id": 11, "block": "ecosistema", "type": "choice",
        "emoji": "🔗",
        "text": "¿Conoces y usas FRONESIS?",
        "subtitle": "Sistema de gestión de espacio y exhibición en tienda Walmart",
        "options": [
            {"value": "no",   "label": "No, no sé qué es FRONESIS",                    "icon": "🤔"},
            {"value": "oido", "label": "Sí, lo conozco pero no lo uso",                "icon": "👂"},
            {"value": "si",   "label": "Sí, lo uso y entiendo cómo funciona",          "icon": "💡"},
        ],
        "score_map": {"no": 0, "oido": 1, "si": 2},
        "tag": "fronesis",
    },

    # ─ BLOQUE 3: Gestión Comercial ──────────────────────────
    {
        "id": 12, "block": "comercial", "type": "choice",
        "emoji": "🏷️",
        "text": "¿Participas en actividades promocionales en Walmart?",
        "subtitle": "Liquidaciones, Precio Especial, Temporadas, Rollback...",
        "options": [
            {"value": "no",              "label": "No, nunca he participado",              "icon": "❌"},
            {"value": "sin_requisitos",  "label": "No, desconozco los requisitos",         "icon": "❓"},
            {"value": "invitado",        "label": "Sí, pero solo cuando me invitan",       "icon": "📩"},
            {"value": "activo",          "label": "Sí, las busco activamente",              "icon": "🙋"},
        ],
        "score_map": {"no": 0, "sin_requisitos": 0, "invitado": 1, "activo": 2},
        "tag": "promociones",
    },
    {
        "id": 13, "block": "comercial", "type": "choice",
        "emoji": "📌",
        "text": "¿Sabes cómo y dónde agendar correctamente una cita para entregar en el CD?",
        "subtitle": "Proceso de agendamiento de ventana horaria en el Centro de Distribución",
        "options": [
            {"value": "no_se",  "label": "No, desconozco el proceso de agendamiento",    "icon": "😕"},
            {"value": "dudas",  "label": "Sí, pero tengo dudas frecuentes",              "icon": "🤷"},
            {"value": "domino", "label": "Sí, lo sé y lo hago sin problemas",           "icon": "✅"},
        ],
        "score_map": {"no_se": 0, "dudas": 1, "domino": 2},
        "tag": "supply",
    },
    {
        "id": 14, "block": "comercial", "type": "choice",
        "emoji": "📰",
        "text": "¿Conoces el Share of Shelf de tu producto?",
        "subtitle": "% del espacio en góndola que tienes vs tu competencia",
        "options": [
            {"value": "no",          "label": "No, no sé qué es el Share of Shelf",       "icon": "🤔"},
            {"value": "visualmente",  "label": "Sí, solo lo veo visualmente en tienda",    "icon": "👀"},
            {"value": "si",          "label": "Sí, lo mido y negocio espacio",            "icon": "📊"},
        ],
        "score_map": {"no": 0, "visualmente": 1, "si": 2},
        "tag": "fronesis",
    },
    {
        "id": 15, "block": "comercial", "type": "choice",
        "emoji": "⚠️",
        "text": "¿Con qué frecuencia tienes quiebres de stock en tienda?",
        "subtitle": "Cuando tu producto no está disponible para el cliente",
        "options": [
            {"value": "sin_visib",   "label": "No tengo visibilidad de mis quiebres",     "icon": "😕"},
            {"value": "frecuente",   "label": "Sí, frecuentemente (más de 1 vez/mes)",   "icon": "🚨"},
            {"value": "ocasional",   "label": "Sí, ocurren ocasionalmente",              "icon": "⚠️"},
            {"value": "raro",        "label": "Sí, ocurren rara vez",                   "icon": "✅"},
        ],
        "score_map": {"sin_visib": 0, "frecuente": 0, "ocasional": 1, "raro": 2},
        "tag": "supply",
    },
    {
        "id": 16, "block": "comercial", "type": "choice",
        "emoji": "🗺️",
        "text": "¿Sabes cómo solicitar cambios de exhibición o espacio adicional?",
        "subtitle": "",
        "options": [
            {"value": "no",        "label": "No, no sé cómo hacerlo",                    "icon": "❓"},
            {"value": "comprador", "label": "Sí, solo por mi comprador",                 "icon": "📞"},
            {"value": "proceso",   "label": "Sí, conozco el proceso formal",              "icon": "✅"},
        ],
        "score_map": {"no": 0, "comprador": 1, "proceso": 2},
        "tag": "fronesis",
    },
    {
        "id": 17, "block": "comercial", "type": "choice",
        "emoji": "💰",
        "text": "¿Calculas tu margen neto después de descuentos y costos logísticos?",
        "subtitle": "Incluye descuentos de factura, MDF, flete al CD, merma",
        "options": [
            {"value": "no",      "label": "No, no lo calculo",                           "icon": "😕"},
            {"value": "parcial", "label": "Sí, calculo algo pero no todo",               "icon": "🤔"},
            {"value": "si",      "label": "Sí, tengo claridad total",                    "icon": "✅"},
        ],
        "score_map": {"no": 0, "parcial": 1, "si": 2},
        "tag": "compradores",
    },

    # ─ BLOQUE 4: Negocio & Datos ─────────────────────────────
    {
        "id": 18, "block": "negocio", "type": "choice",
        "emoji": "📊",
        "text": "¿Qué % de tus ventas totales representa Walmart?",
        "subtitle": "",
        "options": [
            {"value": "menos20", "label": "Menos del 20%",      "icon": "🌱"},
            {"value": "20a50",   "label": "Entre 20% y 50%",   "icon": "📈"},
            {"value": "50a80",   "label": "Entre 50% y 80%",   "icon": "🏆"},
            {"value": "mas80",   "label": "Más del 80%",       "icon": "🎯"},
        ],
        "score_map": {},
    },
    {
        "id": 19, "block": "negocio", "type": "choice",
        "emoji": "👤",
        "text": "¿Tienes alguien dedicado a gestionar la cuenta Walmart?",
        "subtitle": "",
        "options": [
            {"value": "no",        "label": "No, lo hago yo con todo lo demás",          "icon": "😅"},
            {"value": "parcial",   "label": "Sí, yo mismo dedicando tiempo parcial",      "icon": "⏰"},
            {
                "value": "exclusivo",
                "label": "Sí, tengo alguien dedicado exclusivamente",
                "icon": "✅",
                "has_text_followup": True,
                "followup_placeholder": "Mail de esa persona (opcional)",
                "followup_maxlength": 80,
            },
        ],
        "score_map": {"no": 0, "parcial": 1, "exclusivo": 2},
        "tag": "compradores",
    },

    # ─ BLOQUE 5: Gestión Operacional (nuevas preguntas) ────────────
    {
        "id": 20, "block": "operacional", "type": "choice",
        "emoji": "📞",
        "text": "¿Sabes a quién contactar cuando tienes problemas o dudas con Walmart?",
        "subtitle": "",
        "options": [
            {"value": "no",        "label": "No, no sé a quién acudir",                  "icon": "❓"},
            {"value": "uno",       "label": "Sí, tengo un contacto principal",            "icon": "👍"},
            {"value": "varios",    "label": "Sí, tengo contactos según el tema",          "icon": "💪"},
        ],
        "score_map": {"no": 0, "uno": 1, "varios": 2},
        "tag": "compradores",
    },
    {
        "id": 21, "block": "operacional", "type": "choice",
        "emoji": "💬",
        "text": "¿La persona que contactas te responde siempre?",
        "subtitle": "",
        "options": [
            {"value": "no",       "label": "No, rara vez obtengo respuesta",              "icon": "❌"},
            {"value": "aveces",   "label": "Sí, a veces depende del tema",               "icon": "⚠️"},
            {"value": "siempre",  "label": "Sí, siempre obtengo respuesta oportuna",      "icon": "✅"},
        ],
        "score_map": {"no": 0, "aveces": 1, "siempre": 2},
        "tag": "compradores",
    },
    {
        "id": 22, "block": "operacional", "type": "choice",
        "emoji": "🔄",
        "text": "¿Cuándo hay un rechazo, entiendes por qué ocurrió y qué hacer para evitarlo?",
        "subtitle": "Rechazo en el Centro de Distribución",
        "options": [
            {"value": "no",       "label": "No, no entiendo los motivos del rechazo",    "icon": "❌"},
            {"value": "parcial",  "label": "Sí, entiendo pero me cuesta corregirlo",     "icon": "⚠️"},
            {"value": "si",       "label": "Sí, entiendo y corrijo de inmediato",         "icon": "✅"},
        ],
        "score_map": {"no": 0, "parcial": 1, "si": 2},
        "tag": "operacional",
    },
    {
        "id": 23, "block": "operacional", "type": "choice",
        "emoji": "📦",
        "text": "¿Sabes qué es el Fee de Última Milla y por qué se te cobra?",
        "subtitle": "Cargo asociado a la distribución desde el CD hasta la tienda",
        "options": [
            {"value": "no",       "label": "No, no sé qué es",                           "icon": "❌"},
            {"value": "concepto", "label": "Sí, lo conozco pero no entiendo bien por qué", "icon": "⚠️"},
            {"value": "si",       "label": "Sí, lo conozco y entiendo por qué se cobra",  "icon": "✅"},
        ],
        "score_map": {"no": 0, "concepto": 1, "si": 2},
        "tag": "operacional",
    },
    {
        "id": 24, "block": "operacional", "type": "choice",
        "emoji": "🔄",
        "text": "¿Sabes qué es el Fee de Reposición y por qué se te cobra?",
        "subtitle": "Cargo asociado al proceso de reposición de producto en tienda",
        "options": [
            {"value": "no",       "label": "No, no sé qué es",                           "icon": "❌"},
            {"value": "concepto", "label": "Sí, lo conozco pero no entiendo bien por qué", "icon": "⚠️"},
            {"value": "si",       "label": "Sí, lo conozco y entiendo por qué se cobra",  "icon": "✅"},
        ],
        "score_map": {"no": 0, "concepto": 1, "si": 2},
        "tag": "operacional",
    },
    {
        "id": 25, "block": "operacional", "type": "choice",
        "emoji": "⚙️",
        "text": "¿Tienes claro si tu reposición es interna o externa y qué implica?",
        "subtitle": "Reposición interna = personal de tienda / externa = personal propio o tercero",
        "options": [
            {"value": "no",      "label": "No, no tengo claridad sobre esto",             "icon": "❌"},
            {"value": "parcial", "label": "Sí, lo sé pero no entiendo todas las implicancias", "icon": "⚠️"},
            {"value": "si",      "label": "Sí, tengo plena claridad",                     "icon": "✅"},
        ],
        "score_map": {"no": 0, "parcial": 1, "si": 2},
        "tag": "operacional",
    },
]

# ─ Tags → Conversatorios/Mentorías recomendadas ────────────────────

AREA_LABELS = {
    "supply":      {"label": "Supply Chain & CD",          "emoji": "🏥",
                   "desc": "Logística, Fill Rate, ISR, despacho al CD"},
    "retail_link": {"label": "Retail Link & Datos",         "emoji": "💻",
                   "desc": "Uso de datos, reportes, análisis de venta"},
    "fronesis":    {"label": "FRONESIS & Exhibición",       "emoji": "🗺️",
                   "desc": "Espacio en góndola, módulos, exhibición"},
    "promociones": {"label": "Promociones",                  "emoji": "🏷️",
                   "desc": "Planificación promocional, calendarios, activaciones"},
    "compradores": {"label": "Mentoría con Compradores",     "emoji": "🤝",
                   "desc": "KPIs, negociación, relación comercial y contactos"},
    "operacional": {"label": "Fees & Gestión Operacional",  "emoji": "⚙️",
                   "desc": "Fee Última Milla, Fee Reposición, rechazos y procesos clave"},
}


def compute_result(answers: dict) -> dict:
    """
    Calcula score, segmentación y áreas débiles.
    answers: {str(question_id): answer_value}
    """
    score     = 0
    max_score = 0
    tag_scores: dict[str, list[tuple[int, int]]] = {k: [] for k in AREA_LABELS}

    for q in QUESTIONS:
        qid = str(q["id"])
        if not q["score_map"] or qid not in answers:
            continue
        if q["type"] in ("multi", "text", "textarea"):
            continue  # cualitativos, no puntuan

        val     = answers[qid].split("|||")[0]  # ignorar followup
        pts     = q["score_map"].get(val, 0)
        max_pts = max(q["score_map"].values()) if q["score_map"] else 0
        score     += pts
        max_score += max_pts

        tag = q.get("tag")
        if tag and tag in tag_scores:
            tag_scores[tag].append((pts, max_pts))

    pct = round((score / max_score) * 100) if max_score else 0

    # Segmentación (solo visible en admin)
    if pct <= 45:
        segment       = "intermedia"
        segment_label = "PyME Intermedia"
        segment_desc  = (
            "Tu negocio tiene un gran potencial en Walmart. "
            "Los conversatorios y mentorías te ayudarán a dominar "
            "las herramientas y procesos clave para crecer."
        )
    else:
        segment       = "madura"
        segment_label = "PyME Madura"
        segment_desc  = (
            "Ya tienes una base sólida en Walmart. "
            "Enfocaremos los conversatorios en profundizar en las áreas "
            "donde aún hay margen de mejora y escalar tus resultados."
        )

    # Áreas débiles (score < 55% del máx por área)
    weak_areas = []
    for tag, pairs in tag_scores.items():
        if not pairs:
            continue
        earned = sum(p[0] for p in pairs)
        total  = sum(p[1] for p in pairs)
        if total and (earned / total) < 0.55:
            weak_areas.append(tag)

    if not weak_areas:
        weak_areas = ["retail_link", "supply"]

    return {
        "score":         score,
        "max_score":     max_score,
        "pct":           pct,
        "segment":       segment,
        "segment_label": segment_label,
        "segment_desc":  segment_desc,
        "weak_areas":    weak_areas,
        "area_labels":   AREA_LABELS,
    }
