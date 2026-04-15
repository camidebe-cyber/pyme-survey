"""
Genera imagen PNG de la card Escala de Puntaje + Segmentacion
con los numeros actualizados (umbral 40 pts).
"""
from PIL import Image, ImageDraw, ImageFont
import os

# ── Escala 2x para alta resolucion ────────────────────────────────
SCALE = 2
W, H   = 520 * SCALE, 430 * SCALE
R      = 14 * SCALE   # radio esquinas

# ── Colores ───────────────────────────────────────────────────────
NAVY     = (0,  30,  96)
BLUE     = (0,  83, 226)
SPARK    = (255, 194,  32)
WHITE    = (255, 255, 255)
GREEN    = ( 42, 135,   3)
RED      = (234,  17,   0)
AMBER    = (153,  82,  19)
CARD_BG  = (238, 242, 255)
TEXT     = ( 44,  44,  85)
LINE     = (220, 228, 245)
GREEN_BG = (234, 246, 236)
YELL_BG  = (255, 249, 230)
AMB_TXT  = (107,  58,   0)


def s(n): return int(n * SCALE)


# ── Fuentes ───────────────────────────────────────────────────────
FONT_DIR = r"C:\Windows\Fonts"
def font(size, bold=False):
    try:
        name = "calibrib.ttf" if bold else "calibri.ttf"
        return ImageFont.truetype(os.path.join(FONT_DIR, name), s(size))
    except Exception:
        return ImageFont.load_default()


# ── Helpers ───────────────────────────────────────────────────────
def rounded_rect(draw, xy, radius, fill, outline=None, outline_w=2):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle([x0, y0, x1, y1],
                           radius=radius, fill=fill,
                           outline=outline, width=outline_w)


def centered_text(draw, text, cx, cy, font, color):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2), text, font=font, fill=color)


# ── Canvas ────────────────────────────────────────────────────────
img  = Image.new("RGB", (W, H), (240, 244, 251))  # fondo gris claro
draw = ImageDraw.Draw(img)

# Card principal redondeada
rounded_rect(draw, [s(10), s(10), W - s(10), H - s(10)],
             R, CARD_BG)

# ── HEADER NAVY ───────────────────────────────────────────────────
hdr_h = s(52)
rounded_rect(draw, [s(10), s(10), W - s(10), s(10) + hdr_h],
             R, NAVY)
# Tapa esquinas redondeadas abajo del header
draw.rectangle([s(10), s(10) + hdr_h - R, W - s(10), s(10) + hdr_h],
               fill=NAVY)

# Titulo header
centered_text(draw, "Escala de Puntaje",
              W // 2, s(10) + hdr_h // 2,
              font(15, bold=True), WHITE)

# Badge "Total: 46 pts" esquina derecha
bdg_w, bdg_h = s(90), s(22)
bdg_x = W - s(10) - bdg_w - s(8)
bdg_y = s(10) + (hdr_h - bdg_h) // 2
rounded_rect(draw, [bdg_x, bdg_y, bdg_x + bdg_w, bdg_y + bdg_h],
             s(10), SPARK)
centered_text(draw, "Total: 46 pts",
              bdg_x + bdg_w // 2, bdg_y + bdg_h // 2,
              font(9, bold=True), NAVY)

# ── FILAS 0 / 1 / 2 ──────────────────────────────────────────────
rows = [
    ("0", "No conoce / No lo hace",              RED,   (255, 240, 240)),
    ("1", "Conoce pero no gestiona activamente",  AMBER, (255, 248, 235)),
    ("2", "Domina y gestiona con regularidad",    GREEN, (234, 246, 236)),
]
row_start_y = s(10) + hdr_h + s(12)
row_h       = s(60)
row_gap     = s(8)

for i, (pts, label, color, bg) in enumerate(rows):
    ry = row_start_y + i * (row_h + row_gap)

    # Card fila
    rounded_rect(draw, [s(20), ry, W - s(20), ry + row_h],
                 s(10), bg)
    # Acento izquierdo
    draw.rectangle([s(20), ry, s(20) + s(6), ry + row_h], fill=color)
    rounded_rect(draw, [s(20), ry, s(20) + s(6), ry + s(10)],
                 s(4), color)  # arregla esquinas arriba
    rounded_rect(draw, [s(20), ry + row_h - s(10), s(20) + s(6), ry + row_h],
                 s(4), color)  # arregla esquinas abajo

    # Circulo numero
    cx, cy = s(20) + s(30), ry + row_h // 2
    draw.ellipse([cx - s(16), cy - s(16), cx + s(16), cy + s(16)],
                 fill=color)
    centered_text(draw, pts, cx, cy, font(16, bold=True), WHITE)

    # Texto label
    bbox = draw.textbbox((0, 0), label, font=font(13))
    th = bbox[3] - bbox[1]
    draw.text((s(20) + s(60), ry + row_h // 2 - th // 2),
              label, font=font(13), fill=TEXT)

# ── SECCION SEGMENTACION ─────────────────────────────────────────
seg_y = row_start_y + 3 * (row_h + row_gap) + s(10)

# Linea separadora
draw.rectangle([s(20), seg_y, W - s(20), seg_y + s(2)], fill=LINE)
seg_y += s(10)

# Titulo SEGMENTACION
draw.text((s(20), seg_y), "SEGMENTACION",
          font=font(10, bold=True), fill=NAVY)
seg_y += s(22)

# Barra bicolor
bar_h   = s(32)
total_w = W - s(40)
inter_w = int(total_w * (40 / 46))   # 0-39 = 39 pts de 46
madu_w  = total_w - inter_w

rounded_rect(draw,
    [s(20), seg_y, s(20) + inter_w, seg_y + bar_h],
    s(10), YELL_BG, outline=SPARK, outline_w=s(2))
rounded_rect(draw,
    [s(20) + inter_w, seg_y, s(20) + total_w, seg_y + bar_h],
    s(10), GREEN_BG, outline=GREEN, outline_w=s(2))

centered_text(draw, "Intermedia  0-39 pts",
              s(20) + inter_w // 2, seg_y + bar_h // 2,
              font(9, bold=True), AMB_TXT)
centered_text(draw, "Madura  40-46 pts",
              s(20) + inter_w + madu_w // 2, seg_y + bar_h // 2,
              font(9, bold=True), GREEN)

# Labels umbral
label_y = seg_y + bar_h + s(6)
draw.text((s(20), label_y), "0 pts",
          font=font(8), fill=(136, 136, 136))
umbral_x = s(20) + inter_w - s(35)
draw.text((umbral_x, label_y), "Umbral: 40 pts",
          font=font(8, bold=True), fill=NAVY)
draw.text((W - s(50), label_y), "46 pts",
          font=font(8), fill=(136, 136, 136))

# ── GUARDAR ───────────────────────────────────────────────────────
OUT = r"C:\Users\c0b0w1w\Documents\puppy_workspace\pyme_survey\escala_puntaje.png"
img.save(OUT, dpi=(300, 300))
print("PNG guardado:", OUT)