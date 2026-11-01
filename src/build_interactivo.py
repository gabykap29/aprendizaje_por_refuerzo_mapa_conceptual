# -*- coding: utf-8 -*-
"""PDF interactivo de una sola página: el mapa conceptual y, al hacer clic en un cuadro,
se abre SOLO el contenido de ese cuadro (capas PDF + acciones SetOCGState, sin JavaScript).

Uso:  python src/build_interactivo.py [salida.pdf]
Prueba:  OPEN=mdp python src/build_interactivo.py prueba.pdf   (deja abierta esa capa, para revisar el diseño)
Requiere: reportlab, pypdf
"""

import math
import os
import re
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    ArrayObject,
    DictionaryObject,
    FloatObject,
    NameObject,
    NumberObject,
    TextStringObject,
)
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle

from contenido import NODOS, COMPARATIVO

RAIZ = Path(__file__).resolve().parent.parent  # raíz del repositorio
OUT = (
    sys.argv[1]
    if len(sys.argv) > 1
    else str(RAIZ / "pdf" / "Mapa_Conceptual_Aprendizaje_por_Refuerzo.pdf")
)
OPEN = os.environ.get("OPEN")  # solo para pruebas de diseño
W, H = 1700, 1100

# ------------------------------------------------------------------ fuentes
FUENTES = RAIZ / "fuentes"  # fuentes incluidas en el repo (ver fuentes/licencias)
NOTO = str(FUENTES / "NotoSans-%s.ttf")
SERIF = str(FUENTES / "NotoSerif-%s.ttf")
for name, style in [
    ("Noto", "Regular"),
    ("Noto-Bold", "Bold"),
    ("Noto-Italic", "Italic"),
    ("Noto-BoldItalic", "BoldItalic"),
]:
    pdfmetrics.registerFont(TTFont(name, NOTO % style))
for name, style in [
    ("Serif", "Regular"),
    ("Serif-Bold", "Bold"),
    ("Serif-Italic", "Italic"),
    ("Serif-BoldItalic", "BoldItalic"),
]:
    pdfmetrics.registerFont(TTFont(name, SERIF % style))
pdfmetrics.registerFontFamily(
    "Noto",
    normal="Noto",
    bold="Noto-Bold",
    italic="Noto-Italic",
    boldItalic="Noto-BoldItalic",
)
pdfmetrics.registerFontFamily(
    "Serif",
    normal="Serif",
    bold="Serif-Bold",
    italic="Serif-Italic",
    boldItalic="Serif-BoldItalic",
)
pdfmetrics.registerFont(
    TTFont("DejaVu", str(FUENTES / "DejaVuSans.ttf"))
)
pdfmetrics.registerFont(
    TTFont("DejaVu-Bold", str(FUENTES / "DejaVuSans-Bold.ttf"))
)
pdfmetrics.registerFontFamily(
    "DejaVu",
    normal="DejaVu",
    bold="DejaVu-Bold",
    italic="DejaVu",
    boldItalic="DejaVu-Bold",
)

_noto = pdfmetrics.getFont("Noto").face.charToGlyph
_serif = pdfmetrics.getFont("Serif").face.charToGlyph
_sym = re.compile(r"[^\x00-\x7F]")


def fx(text):
    """Símbolos que Noto Sans/Serif no tienen (flechas, ∑, ≤…) → DejaVu Sans."""

    def rep(m):
        ch = m.group(0)
        return (
            ch
            if (ord(ch) in _noto and ord(ch) in _serif)
            else '<font name="DejaVu">%s</font>' % ch
        )

    return _sym.sub(rep, text)


def P(text, style):
    return Paragraph(fx(text), style)


# ------------------------------------------------------------------ paleta (apunte / libro de texto)
PAPER = HexColor("#FAF7F0")
SHEET = HexColor("#FFFEFB")
INK = HexColor("#262320")
MUTED = HexColor("#6B645A")
RULE = HexColor("#D8D2C4")
CATS = {
    "fund": dict(nombre="Fundamentos", color="#2F4B7C", tint="#E6EBF4"),
    "metodo": dict(nombre="Métodos de solución", color="#2A7F86", tint="#DDEEEF"),
    "taxo": dict(nombre="Conceptos transversales", color="#A96B14", tint="#F6E9CF"),
    "valor": dict(nombre="Basados en valor", color="#55802F", tint="#E7EFD8"),
    "politica": dict(nombre="Basados en política", color="#8C3B5C", tint="#F1E1E8"),
}
hexc = HexColor
NODE = {n["id"]: n for n in NODOS}
ORDEN = [n["id"] for n in NODOS]
PANEL_KEYS = ["n:" + i for i in ORDEN] + ["tabla"]


def Y(y):
    return H - y


def st(name, size, lead=None, color=INK, font="Noto", **kw):
    return ParagraphStyle(
        name,
        fontName=font,
        fontSize=size,
        leading=lead or size * 1.38,
        textColor=color,
        **kw,
    )


# ------------------------------------------------------------------ registro de enlaces y capas
CLOSE_BTN = {}
# Datos de la portada
UNIVERSIDAD = "Universidad Gran Rosario"
MATERIA = "Aprendizaje por Refuerzo"
INTEGRANTES = [
    "Acosta Gabriel Hernan Miguel",
    "Benitez Dante Flavian",
    "Mazza Agustin",
    "Rios Facundo",
    "Ruiz Diaz Alejandro",
]
PROFESORES = ["Guadalupe Pascal", "Julián E. Tornillo", "Cristian Oyarzo"]
# Ajustes que cambia build_paginas.py para la versión de páginas (celular / cualquier visor)
BACKDROP = True
CLOSE_LABEL = "Cerrar  ×"
CLOSE_W = 118
MAP_NOTE = "PDF interactivo: abrir con Adobe Acrobat Reader para ver las explicaciones desplegables."
ANN = []  # {"rect": (x, ytop, w, h), "owner": clave de capa o "nodes", "on": [...], "off": [...]}


def add_link(x, ytop, w, h, owner, on=(), off=()):
    ANN.append(dict(rect=(x, ytop, w, h), owner=owner, on=list(on), off=list(off)))


def others(target):
    """Todas las capas de panel menos la destino, más la capa de enlaces del mapa (que debe quedar
    apagada mientras hay un panel abierto). Así el resultado es el mismo aunque el visor entregue
    el clic a una anotación que pertenece a otra capa."""
    return [k for k in PANEL_KEYS if k != target] + ["nodes"]


def begin_layer(c, key):
    c._code.append("/OC /oc_%s BDC" % key)


def end_layer(c):
    c._code.append("EMC")


# ------------------------------------------------------------------ utilidades de dibujo
def box(c, x, ytop, w, h, r=0, fill=None, stroke=None, lw=1, alpha=None):
    c.saveState()
    if alpha is not None:
        c.setFillAlpha(alpha)
    if fill is not None:
        c.setFillColor(fill)
    if stroke is not None:
        c.setStrokeColor(stroke)
        c.setLineWidth(lw)
    c.roundRect(
        x,
        Y(ytop + h),
        w,
        h,
        r,
        stroke=1 if stroke is not None else 0,
        fill=1 if fill is not None else 0,
    )
    c.restoreState()


def spaced(c, x, y, text, font, size, color, space=1.2):
    t = c.beginText(x, Y(y))
    t.setFont(font, size)
    t.setFillColor(color)
    t.setCharSpace(space)
    t.textOut(text)
    t.setCharSpace(
        0
    )  # Tc es parte del estado gráfico: si no se resetea, contamina el texto siguiente
    c.drawText(t)


# ------------------------------------------------------------------ mapa
EDGES = [
    ("comp", "mdp", "se formalizan como", 0.5, "solid"),
    ("mdp", "v", "define", 0.5, "solid"),
    ("mdp", "q", "define", 0.5, "solid"),
    ("q", "v", "V = Σ π · Q", 0.5, "solid"),
    ("v", "predctrl", "predicción", 0.5, "solid"),
    ("q", "predctrl", "control", 0.5, "solid"),
    ("mdp", "dp", "modelo conocido", 0.5, "solid"),
    ("mdp", "mc", "sin modelo", 0.5, "solid"),
    ("mdp", "td", "sin modelo", 0.55, "solid"),
    ("mc", "td", "TD = MC + DP", 0.5, "dash"),
    ("td", "sarsa", "control on-policy", 0.45, "solid"),
    ("td", "qlearn", "control off-policy", 0.5, "solid"),
    ("sarsa", "onoff", "", 0.5, "solid"),
    ("qlearn", "onoff", "", 0.5, "solid"),
    ("egreedy", "sarsa", "explora con ε", 0.5, "solid"),
    ("egreedy", "qlearn", "explora con ε", 0.5, "solid"),
    ("qlearn", "dqn", "+ red neuronal", 0.5, "solid"),
    ("vspol", "sarsa", "valor", 0.5, "solid"),
    ("vspol", "pg", "política", 0.5, "solid"),
    ("vspol", "a2c", "híbrido", 0.5, "solid"),
    ("mc", "pg", "retorno completo", 0.5, "solid"),
    ("pg", "a2c", "+ crítico (ventaja)", 0.5, "solid"),
    ("a2c", "a3c", "+ workers asíncronos", 0.5, "solid"),
]
BANDS = [
    (50, 100, 1600, 245, "FUNDAMENTOS", "fund"),
    (50, 378, 1180, 165, "MÉTODOS DE SOLUCIÓN", "metodo"),
    (50, 566, 350, 484, "FAMILIA BASADA EN POLÍTICA", "politica"),
    (870, 566, 790, 410, "FAMILIA BASADA EN VALOR", "valor"),
]


def clip(cx, cy, w, h, tx, ty, pad=0):
    dx, dy = tx - cx, ty - cy
    sx = (w / 2 + pad) / abs(dx) if dx else 1e9
    sy = (h / 2 + pad) / abs(dy) if dy else 1e9
    t = min(sx, sy)
    return cx + dx * t, cy + dy * t


def arrow(c, x, y, ang, size=10):
    p = c.beginPath()
    p.moveTo(x, y)
    p.lineTo(x - size * math.cos(ang - 0.35), y - size * math.sin(ang - 0.35))
    p.lineTo(x - size * math.cos(ang + 0.35), y - size * math.sin(ang + 0.35))
    p.close()
    c.drawPath(p, stroke=0, fill=1)


def draw_map(c):
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)

    c.setFillColor(INK)
    c.setFont("Serif-Bold", 33)
    c.drawString(50, Y(54), "Aprendizaje por Refuerzo")
    tw = stringWidth("Aprendizaje por Refuerzo", "Serif-Bold", 33)
    c.setFont("Serif-Italic", 22)
    c.setFillColor(MUTED)
    c.drawString(50 + tw + 16, Y(54), "mapa conceptual")
    c.setFont("Noto", 14.5)
    c.drawString(
        50,
        Y(80),
        "Para visualizar el contenido, se debe hacer click en un Cuadro.",
    )

    # Créditos (arriba a la derecha): universidad, materia, integrantes y profesores
    cx = 1070
    spaced(c, cx, 30, (UNIVERSIDAD + "  ·  " + MATERIA).upper(), "Noto-Bold", 10.5, INK, 1.2)
    c.saveState()
    c.setStrokeColor(RULE)
    c.setLineWidth(0.8)
    c.line(cx, Y(38), 1650, Y(38))
    c.restoreState()
    spaced(c, cx, 52, "INTEGRANTES", "Noto-Bold", 9.5, MUTED, 1.4)
    spaced(c, 1460, 52, "PROFESORES", "Noto-Bold", 9.5, MUTED, 1.4)
    c.setFont("Noto", 11)
    c.setFillColor(INK)
    for k, nombre in enumerate(INTEGRANTES):
        col, fila = divmod(k, 3)
        c.drawString(cx + col * 195, Y(67 + fila * 13.5), nombre)
    for k, nombre in enumerate(PROFESORES):
        c.drawString(1460, Y(67 + k * 13.5), nombre)

    for bx, by, bw, bh, label, key in BANDS:
        cat = CATS[key]
        box(c, bx, by, bw, bh, 6, fill=hexc(cat["tint"]), alpha=0.55)
        ly = by + (bh - 12 if key == "valor" else 24)
        spaced(c, bx + 16, ly, label, "Noto-Bold", 11.5, hexc(cat["color"]), 1.4)

    labels = []
    for a, b, text, t, style in EDGES:
        ax, ay, aw, ah = NODE[a]["pos"]
        bx, by, bw, bh = NODE[b]["pos"]
        x1, y1 = clip(ax, ay, aw, ah, bx, by, 3)
        x2, y2 = clip(bx, by, bw, bh, ax, ay, 4)
        c.saveState()
        c.setStrokeColor(MUTED)
        c.setFillColor(MUTED)
        c.setLineWidth(1.3)
        if style == "dash":
            c.setDash(5, 4)
        c.line(x1, Y(y1), x2, Y(y2))
        c.restoreState()
        if style != "dash":
            c.setFillColor(MUTED)
            arrow(c, x2, Y(y2), math.atan2(-(y2 - y1), x2 - x1))
        if text:
            labels.append((x1 + (x2 - x1) * t, y1 + (y2 - y1) * t, text))

    for n in NODOS:
        cx, cy, w, h = n["pos"]
        x, y = cx - w / 2, cy - h / 2
        cat = CATS[n["cat"]]
        box(c, x, y, w, h, 4, fill=white, stroke=hexc(cat["color"]), lw=1.6)
        # pestaña en la esquina: indica que el cuadro se abre
        c.saveState()
        c.setFillColor(hexc(cat["color"]))
        p = c.beginPath()
        p.moveTo(x + w, Y(y + h) + 20)
        p.lineTo(x + w, Y(y + h))
        p.lineTo(x + w - 20, Y(y + h))
        p.close()
        c.drawPath(p, stroke=0, fill=1)
        c.restoreState()
        pt = P(
            n["corto"],
            ParagraphStyle(
                "nt",
                fontName="Serif-Bold",
                fontSize=14.5,
                leading=17.5,
                alignment=TA_CENTER,
                textColor=INK,
            ),
        )
        ps = P(
            n["mapsub"],
            ParagraphStyle(
                "ns",
                fontName="Noto",
                fontSize=11,
                leading=13.5,
                alignment=TA_CENTER,
                textColor=hexc(cat["color"]),
            ),
        )
        _, ht = pt.wrap(w - 26, 500)
        _, hs = ps.wrap(w - 26, 500)
        top = y + (h - (ht + 4 + hs)) / 2
        if ht + 4 + hs > h - 10:
            print("AVISO: texto desborda en", n["id"])
        pt.drawOn(c, x + 13, Y(top + ht))
        ps.drawOn(c, x + 13, Y(top + ht + 4 + hs))
        add_link(x, y, w, h, "nodes", on=["n:" + n["id"]], off=others("n:" + n["id"]))

    for lx, ly, text in labels:
        pp = P(
            text,
            ParagraphStyle(
                "el",
                fontName="Serif-Italic",
                fontSize=12,
                leading=14,
                alignment=TA_CENTER,
                textColor=INK,
            ),
        )
        tw_ = sum(stringWidth(ch, "Serif-Italic", 12) for ch in text) + 10
        box(c, lx - tw_ / 2, ly - 9, tw_, 18, 0, fill=PAPER)
        _, ph = pp.wrap(tw_, 40)
        pp.drawOn(c, lx - tw_ / 2, Y(ly + ph / 2 - 0.5))

    # botón del cuadro comparativo
    bx, by, bw, bh = 430, 1012, 330, 40
    box(c, bx, by, bw, bh, 3, fill=INK)
    pp = P(
        "Cuadro comparativo de algoritmos",
        ParagraphStyle(
            "b",
            fontName="Serif-Bold",
            fontSize=15,
            leading=18,
            alignment=TA_CENTER,
            textColor=white,
        ),
    )
    _, ph = pp.wrap(bw, bh)
    pp.drawOn(c, bx, Y(by + bh / 2 + ph / 2))
    add_link(bx, by, bw, bh, "nodes", on=["tabla"], off=others("tabla"))

    # leyenda
    x = 1650
    c.setFont("Noto", 12.5)
    for key in ["politica", "valor", "taxo", "metodo", "fund"]:
        cat = CATS[key]
        x -= stringWidth(cat["nombre"], "Noto", 12.5)
        c.setFillColor(INK)
        c.drawString(x, Y(1038), cat["nombre"])
        x -= 16
        c.setFillColor(hexc(cat["color"]))
        c.rect(x, Y(1038) - 1, 12, 12, stroke=0, fill=1)
        x -= 24
    c.setFont("Noto", 11)
    c.setFillColor(MUTED)
    if MAP_NOTE:
        c.drawString(60, Y(1076), MAP_NOTE)


# ------------------------------------------------------------------ panel (hoja que se abre sobre el mapa)
PX, PY, PW, PH = 70, 40, 1560, 1020
INNER = 46
LX, LW = PX + INNER, 860
RX = LX + LW + 52
RW = PX + PW - INNER - RX
SEC_GAP = 26


def styles(s):
    return dict(
        defn=st("defn", 19.5 * s, 28 * s, font="Noto"),
        bul=st(
            "bul",
            16.5 * s,
            23.5 * s,
            leftIndent=20 * s,
            bulletIndent=2,
            spaceAfter=7 * s,
            bulletFontName="Noto-Bold",
            bulletFontSize=16.5 * s,
        ),
        cell=st("cell", 14.5 * s, 19.5 * s),
        form=st("form", 18.5 * s, 31 * s, font="Serif", spaceBefore=3),
        flab=st("flab", 12.5, 16, color=MUTED, font="Noto-Italic", spaceBefore=15),
        ej=st("ej", 16 * s, 23.5 * s, font="Serif-Italic"),
        rel=st("rel", 15.5 * s, 21 * s),
        step=st(
            "step",
            16 * s,
            22.5 * s,
            leftIndent=28 * s,
            bulletIndent=0,
            spaceAfter=5 * s,
            bulletFontName="Noto-Bold",
            bulletFontSize=16 * s,
        ),
        sp=st("sp", 6, 12),
    )


class Sec:
    """Sección con rótulo en versalitas y filete, sin tarjeta."""

    def __init__(self, label, flows, boxed=False, targets=None):
        self.label, self.flows, self.boxed, self.targets = label, flows, boxed, targets

    @property
    def pad(self):
        return 16 if self.boxed else 0

    def measure(self, w):
        self.hs = [f.wrap(w - 2 * self.pad, 5000)[1] for f in self.flows]
        head = 30 if self.label else 0
        return 2 * self.pad + head + sum(self.hs)

    def draw(self, c, x, ytop, w, color, owner):
        total = self.measure(w)
        if self.boxed:
            box(c, x, ytop, w, total, 2, stroke=hexc(color), lw=1.2)
        xi, yy = x + self.pad, ytop + self.pad
        if self.label:
            spaced(
                c, xi, yy + 12, self.label.upper(), "Noto-Bold", 11.5, hexc(color), 1.4
            )
            c.saveState()
            c.setStrokeColor(RULE)
            c.setLineWidth(0.8)
            c.line(xi, Y(yy + 20), x + w - self.pad, Y(yy + 20))
            c.restoreState()
            yy += 30
        for i, (f, h) in enumerate(zip(self.flows, self.hs)):
            f.drawOn(c, xi, Y(yy + h))
            if self.targets:
                add_link(
                    xi,
                    yy - 2,
                    w - 2 * self.pad,
                    h + 4,
                    owner,
                    on=["n:" + self.targets[i]],
                    off=others("n:" + self.targets[i]),
                )
            yy += h
        return total


def make_table(spec, width, S):
    data = [[P("<b>%s</b>" % h if h else "", S["cell"]) for h in spec["header"]]]
    for r in spec["rows"]:
        data.append([P(cell, S["cell"]) for cell in r])
    t = Table(data, colWidths=[width * f for f in spec["widths"]])
    t.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LINEABOVE", (0, 0), (-1, 0), 1.3, INK),
                ("LINEBELOW", (0, 0), (-1, 0), 0.7, INK),
                ("LINEBELOW", (0, 1), (-1, -2), 0.4, RULE),
                ("LINEBELOW", (0, -1), (-1, -1), 1.3, INK),
            ]
        )
    )
    return t


def total_h(secs, w):
    return sum(sc.measure(w) for sc in secs) + SEC_GAP * (len(secs) - 1)


def plan(n, s):
    S = styles(s)
    left = [
        Sec(None, [P(n["defn"], S["defn"])]),
        Sec(
            "Ideas clave",
            [Paragraph(fx(b), S["bul"], bulletText="•") for b in n["bullets"]],
        ),
    ]
    forms = []
    for i, (lab, expr) in enumerate(n["formulas"]):
        if i:
            forms.append(
                Paragraph("&nbsp;", S["sp"])
            )  # aire entre fórmulas (sub/superíndices anidados)
        forms += [P(lab, S["flab"]), P(expr, S["form"])]
    right = [
        Sec("Fórmulas", forms, boxed=True),
        Sec("Ejemplo", [P(n["ejemplo"], S["ej"])]),
        Sec(
            "Relacionado  ·  clic para abrir",
            [
                P(
                    "<u><font color='%s'>%s</font></u> <font color='#6B645A' size=%d>— %s</font>"
                    % (
                        CATS[NODE[r]["cat"]]["color"],
                        NODE[r]["corto"],
                        int(14 * s),
                        ph,
                    ),
                    S["rel"],
                )
                for r, ph in n["rel"]
            ],
            targets=[r for r, _ in n["rel"]],
        ),
    ]
    steps = tabla = None
    if "steps" in n:
        steps = Sec(
            "Paso a paso",
            [
                Paragraph(fx(x), S["step"], bulletText="%d." % (i + 1))
                for i, x in enumerate(n["steps"])
            ],
        )
    if "tabla" in n:
        tabla = Sec(n["tabla"]["titulo"], [make_table(n["tabla"], LW, S)])
    base_left = left + ([tabla] if tabla else [])
    base_right = right
    if steps:
        opts = [
            (left + [steps] + ([tabla] if tabla else []), right),
            (base_left, [right[0], steps] + right[1:]),
        ]
        base_left, base_right = min(
            opts, key=lambda o: max(total_h(o[0], LW), total_h(o[1], RW))
        )
    return base_left, base_right, total_h(base_left, LW), total_h(base_right, RW)


def panel_frame(c, color, owner, label, title, sub):
    """Fondo oscurecido, hoja, encabezado y botón Cerrar. Devuelve la y donde empieza el cuerpo."""
    if BACKDROP:  # solo en la versión desplegable: oscurece el mapa de fondo
        c.saveState()
        c.setFillColor(HexColor("#1B1814"))
        c.setFillAlpha(0.62)
        c.rect(0, 0, W, H, stroke=0, fill=1)
        c.restoreState()
        box(c, PX + 5, PY + 6, PW, PH, 4, fill=HexColor("#000000"), alpha=0.25)
    box(c, PX, PY, PW, PH, 4, fill=SHEET, stroke=INK, lw=1.2)
    pt = P(
        title,
        ParagraphStyle(
            "ht", fontName="Serif-Bold", fontSize=36, leading=42, textColor=INK
        ),
    )
    _, h = pt.wrap(PW - 2 * INNER - 170, 200)
    pt.drawOn(c, LX, Y(PY + 36 + h))
    ps = P(
        sub,
        ParagraphStyle(
            "hs", fontName="Serif-Italic", fontSize=18, leading=24, textColor=MUTED
        ),
    )
    _, hs = ps.wrap(PW - 2 * INNER - 170, 100)
    ps.drawOn(c, LX, Y(PY + 36 + h + 4 + hs))
    y_rule = PY + 36 + h + 4 + hs + 16
    c.saveState()
    c.setStrokeColor(INK)
    c.setLineWidth(0.8)
    c.line(LX, Y(y_rule), PX + PW - INNER, Y(y_rule))
    c.restoreState()
    # botón cerrar
    bw, bh = CLOSE_W, 36
    bx, by = PX + PW - INNER - bw, PY + 30
    box(c, bx, by, bw, bh, 3, stroke=INK, lw=1.2)
    cp = P(
        CLOSE_LABEL,
        ParagraphStyle(
            "cl",
            fontName="Noto-Bold",
            fontSize=14.5,
            leading=18,
            alignment=TA_CENTER,
            textColor=INK,
        ),
    )
    _, ph = cp.wrap(bw, bh)
    cp.drawOn(c, bx, Y(by + bh / 2 + ph / 2))
    CLOSE_BTN["rect"] = (bx, by, bw, bh)
    return y_rule + 26


def draw_panel(c, n, idx):
    cat = CATS[n["cat"]]
    owner = "n:" + n["id"]
    begin_layer(c, "n_" + n["id"])
    body_top = panel_frame(
        c,
        cat["color"],
        owner,
        "%s  ·  concepto %d de %d" % (cat["nombre"], idx, len(ORDEN)),
        n["titulo"],
        n["sub"],
    )
    body_bottom = PY + PH - 34
    avail = body_bottom - body_top
    chosen = None
    for s in [
        1.4,
        1.35,
        1.3,
        1.25,
        1.2,
        1.15,
        1.1,
        1.05,
        1.0,
        0.95,
        0.9,
        0.85,
        0.8,
        0.75,
    ]:
        l, r, hl, hr = plan(n, s)
        chosen = (s, l, r, hl, hr)
        if max(hl, hr) <= avail:
            break
    s, l, r, hl, hr = chosen
    if max(hl, hr) > avail:
        print("AVISO: no cabe", n["id"], hl, hr, avail)
    y = body_top
    for sc in l:
        y += sc.draw(c, LX, y, LW, cat["color"], owner) + SEC_GAP
    y = body_top
    for sc in r:
        y += sc.draw(c, RX, y, RW, cat["color"], owner) + SEC_GAP
    print(
        "  %-9s escala %.2f  izq %.0f  der %.0f  (disp. %.0f)"
        % (n["id"], s, hl, hr, avail)
    )
    end_layer(c)


def draw_tabla(c):
    comp = COMPARATIVO
    owner = "tabla"
    begin_layer(c, "tabla")
    body_top = panel_frame(c, "#262320", owner, "Síntesis", comp["titulo"], comp["sub"])
    body_bottom = PY + PH - 34
    tw = PW - 2 * INNER
    ink_cols = None
    for fs in [18.5, 17.5, 16.5, 15.5, 14.5]:
        S_C = st("cc", fs, fs * 1.36)
        S_H = st("ch", fs, fs * 1.3, font="Noto-Bold")
        data = [[P(h, S_H) for h in comp["header"]]] + [
            [P(x, S_C) for x in r] for r in comp["rows"]
        ]
        colw = [tw * f for f in comp["widths"]]
        t = Table(data, colWidths=colw)
        t.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("LINEABOVE", (0, 0), (-1, 0), 1.3, INK),
                    ("LINEBELOW", (0, 0), (-1, 0), 0.7, INK),
                    ("LINEBELOW", (0, 1), (-1, -2), 0.4, RULE),
                    ("LINEBELOW", (0, -1), (-1, -1), 1.3, INK),
                    ("LINEBELOW", (0, 3), (-1, 3), 0.9, MUTED),
                    ("LINEBELOW", (0, 6), (-1, 6), 0.9, MUTED),
                ]
            )
        )
        _, th = t.wrap(tw, 3000)
        S_K = st("kk", fs, fs * 1.36)
        S_KB = st("kb", fs, fs * 1.36, font="Noto-Bold")
        kt = Table(
            [[P(a, S_KB), P(b, S_K)] for a, b in comp["claves"]],
            colWidths=[tw * 0.34, tw * 0.66],
        )
        kt.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("LINEABOVE", (0, 0), (-1, 0), 1.3, INK),
                    ("LINEBELOW", (0, 0), (-1, -2), 0.4, RULE),
                    ("LINEBELOW", (0, -1), (-1, -1), 1.3, INK),
                ]
            )
        )
        _, kh = kt.wrap(tw, 3000)
        if th + 24 + 30 + 20 + kh <= body_bottom - body_top - 24:
            break
    t.drawOn(c, LX, Y(body_top + th))
    # filas clicables (primera columna) → abre el concepto
    row_ids = ["dp", "mc", "td", "sarsa", "qlearn", "dqn", "pg", "a2c", "a3c"]
    ry = body_top + t._rowHeights[0]
    for rid, rh in zip(row_ids, t._rowHeights[1:]):
        add_link(LX, ry, colw[0], rh, owner, on=["n:" + rid], off=others("n:" + rid))
        ry += rh
    c.setFont("Noto-Italic", 12.5)
    c.setFillColor(MUTED)
    c.drawString(
        LX,
        Y(body_top + th + 20),
        "IS = importance sampling.  Clic en el nombre de un algoritmo para abrir su explicación.",
    )
    gy = body_top + th + 62
    spaced(
        c,
        LX,
        gy,
        "GUÍA RÁPIDA PARA ELEGIR UN ALGORITMO",
        "Noto-Bold",
        11.5,
        hexc("#A96B14"),
        1.4,
    )
    kt.drawOn(c, LX, Y(gy + 14 + kh))
    print(
        "  tabla     fuente %.1f  termina %.0f / %.0f" % (fs, gy + 14 + kh, body_bottom)
    )
    end_layer(c)


# ------------------------------------------------------------------ ensamblado
def build():
    tmp = OUT + ".tmp"
    c = canvas.Canvas(tmp, pagesize=(W, H), pageCompression=1)
    draw_map(c)
    for i, nid in enumerate(ORDEN, start=1):
        draw_panel(c, NODE[nid], i)
    draw_tabla(c)
    c.showPage()
    c.save()

    r = PdfReader(tmp)
    w = PdfWriter(clone_from=r)
    page = w.pages[0]

    def new_ocg(name):
        return w._add_object(
            DictionaryObject(
                {
                    NameObject("/Type"): NameObject("/OCG"),
                    NameObject("/Name"): TextStringObject(name),
                }
            )
        )

    keys = ["n:" + i for i in ORDEN] + ["tabla"]
    ocg = {
        k: new_ocg(
            "Detalle: "
            + (NODE[k[2:]]["corto"] if k.startswith("n:") else "Cuadro comparativo")
        )
        for k in keys
    }
    ocg["nodes"] = new_ocg("Mapa (enlaces)")

    props = DictionaryObject()
    for k in keys:
        props[NameObject("/oc_" + ("n_" + k[2:] if k.startswith("n:") else k))] = ocg[k]
    res = page["/Resources"].get_object()
    res[NameObject("/Properties")] = props

    abierta = None if not OPEN else ("tabla" if OPEN == "tabla" else "n:" + OPEN)
    off = [ocg[k] for k in keys if k != abierta]
    w._root_object[NameObject("/OCProperties")] = DictionaryObject(
        {
            NameObject("/OCGs"): ArrayObject(list(ocg.values())),
            NameObject("/D"): DictionaryObject(
                {
                    NameObject("/BaseState"): NameObject("/ON"),
                    NameObject("/OFF"): ArrayObject(off),
                    NameObject("/Name"): TextStringObject("Mapa conceptual"),
                }
            ),
        }
    )

    # Cierre compartido: UNA anotación por zona, sin capa propia (siempre activa) y que apaga todos
    # los paneles. Las zonas no se solapan con ningún cuadro del mapa, así que no estorban cerradas.
    bx, by, bw, bh = CLOSE_BTN["rect"]
    for rx, ry, rw, rh in [
        (bx, by, bw, bh),
        (0, 0, W, PY),
        (0, PY + PH, W, H - PY - PH),
        (0, PY, PX, PH),
        (PX + PW + 15, PY, W - PX - PW - 15, PH),
    ]:
        add_link(rx, ry, rw, rh, None, on=["nodes"], off=list(PANEL_KEYS))

    annots = ArrayObject()
    for a in ANN:
        x, yt, ww, hh = a["rect"]
        state = ArrayObject()
        if a["on"]:
            state.append(NameObject("/ON"))
            state.extend(ocg[k] for k in a["on"])
        if a["off"]:
            state.append(NameObject("/OFF"))
            state.extend(ocg[k] for k in a["off"])
        action = DictionaryObject(
            {
                NameObject("/Type"): NameObject("/Action"),
                NameObject("/S"): NameObject("/SetOCGState"),
                NameObject("/State"): state,
            }
        )
        annot = DictionaryObject(
            {
                NameObject("/Type"): NameObject("/Annot"),
                NameObject("/Subtype"): NameObject("/Link"),
                NameObject("/Rect"): ArrayObject(
                    [FloatObject(round(v, 2)) for v in (x, Y(yt + hh), x + ww, Y(yt))]
                ),
                NameObject("/Border"): ArrayObject([NumberObject(0)] * 3),
                NameObject("/F"): NumberObject(4),
                NameObject("/A"): action,
            }
        )
        if a["owner"]:
            annot[NameObject("/OC")] = ocg[a["owner"]]
        annots.append(w._add_object(annot))
    page[NameObject("/Annots")] = annots

    w._root_object[NameObject("/PageLayout")] = NameObject("/SinglePage")
    w._root_object[NameObject("/OpenAction")] = ArrayObject(
        [page.indirect_reference, NameObject("/Fit")]
    )
    w.add_metadata(
        {
            "/Title": "Mapa conceptual interactivo · Aprendizaje por Refuerzo",
            "/Subject": "Aprendizaje por Refuerzo · Universidad Gran Rosario",
            "/Author": ", ".join(INTEGRANTES),
        }
    )
    with open(OUT, "wb") as f:
        w.write(f)
    os.remove(tmp)
    print(
        "PDF generado:", OUT, "· %d capas · %d zonas clicables" % (len(keys), len(ANN))
    )


if __name__ == "__main__":
    build()
