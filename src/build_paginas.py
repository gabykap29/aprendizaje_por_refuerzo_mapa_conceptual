# -*- coding: utf-8 -*-
"""Versión de PÁGINAS del mapa conceptual (celular, tablet y cualquier visor de PDF).

Mismo diseño que build_interactivo.py, pero cada cuadro del mapa es un enlace a su propia página
(enlaces internos estándar, que funcionan en Drive, Chrome, iPhone/iPad, Acrobat, etc.) y cada
página tiene un botón «Volver al mapa».

Uso:  python src/build_paginas.py [salida.pdf]
"""
import os
import re
import sys

from reportlab.pdfgen import canvas

sys.argv, _argv = [sys.argv[0]], sys.argv  # build_interactivo lee sys.argv al importarse
import build_interactivo as B  # noqa: E402

OUT = (
    _argv[1]
    if len(_argv) > 1
    else str(B.RAIZ / "pdf" / "Mapa_Conceptual_Aprendizaje_por_Refuerzo_PAGINAS.pdf")
)

# Ajustes de esta versión
B.BACKDROP = False
B.CLOSE_LABEL = "←  Volver al mapa"
B.CLOSE_W = 190
B.MAP_NOTE = "Tocá un cuadro para abrir su página; en cada página, «Volver al mapa» regresa acá."
B.begin_layer = lambda c, key: None  # aquí no hay capas
B.end_layer = lambda c: None


def destino(on):
    k = on[0]
    return "p_tabla" if k == "tabla" else "p_" + k[2:]


def volcar_enlaces(c, extra=()):
    for a in B.ANN:
        x, yt, w, h = a["rect"]
        c.linkRect("", destino(a["on"]), (x, B.Y(yt + h), x + w, B.Y(yt)), relative=0, thickness=0)
    B.ANN.clear()
    for rect, dest in extra:
        x, yt, w, h = rect
        c.linkRect("", dest, (x, B.Y(yt + h), x + w, B.Y(yt)), relative=0, thickness=0)


def pagina(c, nombre, titulo, nivel=0):
    c.bookmarkPage(nombre)
    c.addOutlineEntry(titulo, nombre, level=nivel)
    c.setFillColor(B.PAPER)
    c.rect(0, 0, B.W, B.H, stroke=0, fill=1)


def main():
    c = canvas.Canvas(OUT, pagesize=(B.W, B.H), pageCompression=1)
    c.setTitle("Mapa conceptual · Aprendizaje por Refuerzo")
    c.setAuthor(", ".join(B.INTEGRANTES))
    c.setSubject("Aprendizaje por Refuerzo · Universidad Gran Rosario")

    pagina(c, "mapa", "Mapa conceptual")
    B.draw_map(c)
    volcar_enlaces(c)
    c.showPage()

    for i, nid in enumerate(B.ORDEN, start=1):
        n = B.NODE[nid]
        pagina(c, "p_" + nid, re.sub(r"<[^>]+>", "", n["titulo"]), 1)
        B.draw_panel(c, n, i)
        volcar_enlaces(c, extra=[(B.CLOSE_BTN["rect"], "mapa")])
        c.showPage()

    pagina(c, "p_tabla", "Cuadro comparativo de algoritmos")
    B.draw_tabla(c)
    volcar_enlaces(c, extra=[(B.CLOSE_BTN["rect"], "mapa")])
    c.showPage()

    c.save()
    print("PDF generado:", OUT, "(%d páginas)" % (len(B.ORDEN) + 2))


if __name__ == "__main__":
    main()
