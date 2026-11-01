# -*- coding: utf-8 -*-
"""Comprueba que los enlaces de los PDF generados llevan donde deben.

Uso:  python src/verificar_enlaces.py
  - pdf/..._PAGINAS.pdf : cada cuadro/enlace debe ir a la página de su concepto.
  - pdf/Mapa_Conceptual_Aprendizaje_por_Refuerzo.pdf : 18 capas, todas apagadas al abrir salvo el mapa,
    y cada enlace con una acción SetOCGState.
"""
import sys
from pathlib import Path

from pypdf import PdfReader

sys.path.insert(0, str(Path(__file__).resolve().parent))
from contenido import NODOS  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
errores = 0


def chequear(ok, msg):
    global errores
    print(("  OK   " if ok else "  FALLA ") + msg)
    errores += 0 if ok else 1


# ---------------------------------------------------------------- versión de páginas
r = PdfReader(RAIZ / "pdf" / "Mapa_Conceptual_Aprendizaje_por_Refuerzo_PAGINAS.pdf")
print("Versión de páginas:", len(r.pages), "páginas")
ids = [n["id"] for n in NODOS]
pagina = {i: 2 + k for k, i in enumerate(ids)}
pagina["tabla"] = len(ids) + 2


def destino(a):
    return r.get_page_number(a["/Dest"][0].get_object()) + 1


mapa = [destino(a.get_object()) for a in r.pages[0]["/Annots"]]
chequear(mapa == [pagina[i] for i in ids] + [pagina["tabla"]], "mapa: 17 cuadros + botón del cuadro comparativo")
for k, n in enumerate(NODOS):
    got = [destino(a.get_object()) for a in r.pages[1 + k]["/Annots"]]
    chequear(got == [pagina[x] for x, _ in n["rel"]] + [1], "página %2d (%s): relacionados + volver al mapa" % (2 + k, n["id"]))
tabla = [destino(a.get_object()) for a in r.pages[-1]["/Annots"]]
chequear(tabla[-1] == 1 and len(tabla) == 10, "cuadro comparativo: 9 algoritmos + volver al mapa")

# ---------------------------------------------------------------- versión desplegable (capas)
r = PdfReader(RAIZ / "pdf" / "Mapa_Conceptual_Aprendizaje_por_Refuerzo.pdf")
print("Versión desplegable:", len(r.pages), "página")
oc = r.trailer["/Root"]["/OCProperties"]
chequear(len(oc["/OCGs"]) == len(ids) + 2, "%d capas (17 conceptos + cuadro comparativo + enlaces del mapa)" % len(oc["/OCGs"]))
chequear(len(oc["/D"]["/OFF"]) == len(ids) + 1, "al abrir: los 18 paneles apagados")
acciones = [a.get_object().get("/A", {}).get("/S") for a in r.pages[0]["/Annots"]]
chequear(all(x == "/SetOCGState" for x in acciones), "%d zonas clicables, todas SetOCGState" % len(acciones))

print("\n%s" % ("Todo correcto." if not errores else "%d comprobaciones fallaron." % errores))
sys.exit(1 if errores else 0)
