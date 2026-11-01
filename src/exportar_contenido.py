# -*- coding: utf-8 -*-
"""Exporta la estructura del mapa y el contenido de cada concepto a Markdown (y .docx si hay pandoc)."""
import re
import subprocess
import shutil
import sys

_argv, sys.argv = sys.argv, [sys.argv[0]]
import build_interactivo as B  # noqa: E402
sys.argv = _argv

OUT = str(B.RAIZ / "docs" / "Contenido_y_estructura_mapa_conceptual.md")


def md(t):
    t = t.replace("<br/>", "\n")
    t = re.sub(r"<sub>(.*?)</sub>", r"_{\1}", t)
    t = re.sub(r"<super>(.*?)</super>", r"^{\1}", t)
    t = re.sub(r"<sup>(.*?)</sup>", r"^{\1}", t)
    t = re.sub(r"<b>(.*?)</b>", r"**\1**", t)
    t = re.sub(r"<i>(.*?)</i>", r"*\1*", t)
    t = re.sub(r"<[^>]+>", "", t)
    return t.replace("&nbsp;", " ").replace("|", "\\|") if False else t.replace("&nbsp;", " ")


def cell(t):
    return md(t).replace("|", "\\|").replace("\n", " ")


L = []
L += ["# Aprendizaje por Refuerzo — Mapa conceptual", "",
      "**%s** · %s" % (B.UNIVERSIDAD, B.MATERIA), "",
      "**Integrantes:** " + "; ".join(B.INTEGRANTES), "",
      "**Profesores:** " + "; ".join(B.PROFESORES), "",
      "Contenido y estructura del mapa (17 conceptos de la consigna + cuadro comparativo).", ""]

# ---------------------------------------------------------------- estructura
L += ["## 1. Estructura del mapa", "", "### Grupos (zonas del mapa)", ""]
grupos = {}
for n in B.NODOS:
    grupos.setdefault(n["cat"], []).append(n["corto"])
zonas = [("fund", "Fundamentos"), ("metodo", "Métodos de solución"), ("taxo", "Conceptos transversales"),
         ("valor", "Familia basada en valor (algoritmos)"), ("politica", "Familia basada en política (algoritmos)")]
for key, nombre in zonas:
    L.append("- **%s:** %s" % (nombre, "; ".join(grupos[key])))
L += ["", "### Relaciones entre conceptos (flechas del mapa)", "",
      "| Desde | Relación | Hacia |", "|---|---|---|"]
for a, b, text, t, style in B.EDGES:
    rel = text or "(relación directa)"
    if style == "dash":
        rel += " (línea punteada, sin dirección)"
    L.append("| %s | %s | %s |" % (B.NODE[a]["corto"], rel, B.NODE[b]["corto"]))

L += ["", "### Lectura del mapa en forma de árbol", "",
      "```",
      "Componentes del RL ── se formalizan como ──> Procesos de decisión de Markov (MDP)",
      "   MDP ── define ──> Función estado-valor V(s)   <── V = Σ π·Q ──   Función acción-valor Q(s,a) <── define ── MDP",
      "   V(s)  ── predicción ──┐",
      "   Q(s,a) ── control ────┴─> Predicción vs Control",
      "   MDP ── modelo conocido ──> Programación dinámica",
      "   MDP ── sin modelo ───────> Monte Carlo ┄┄ TD = MC + DP ┄┄ Diferencia temporal  <── sin modelo ── MDP",
      "   Diferencia temporal ── control on-policy ──> SARSA ──> On-Policy vs Off-Policy <── Q-Learning",
      "   Diferencia temporal ── control off-policy ─> Q-Learning ── + red neuronal ──> DQN",
      "   Epsilon-Greedy ── explora con ε ──> SARSA y Q-Learning",
      "   Basado en valores vs. políticas ── valor ──> SARSA | ── política ──> Policy Gradient/REINFORCE | ── híbrido ──> A2C",
      "   Monte Carlo ── retorno completo ──> Policy Gradient/REINFORCE ── + crítico ──> A2C ── + workers asíncronos ──> A3C",
      "```", ""]

# ---------------------------------------------------------------- contenido
L += ["## 2. Contenido de cada concepto", ""]
for i, n in enumerate(B.NODOS, start=1):
    cat = B.CATS[n["cat"]]["nombre"]
    L += ["### %d. %s" % (i, re.sub(r"<[^>]+>", "", n["titulo"])), "",
          "*Grupo: %s · %s*" % (cat, md(n["sub"])), "",
          "**Definición.** " + md(n["defn"]), "", "**Ideas clave**", ""]
    L += ["- " + md(b) for b in n["bullets"]]
    if "steps" in n:
        L += ["", "**Paso a paso**", ""]
        L += ["%d. %s" % (k, md(s)) for k, s in enumerate(n["steps"], start=1)]
    if "tabla" in n:
        t = n["tabla"]
        L += ["", "**%s**" % t["titulo"], "",
              "| " + " | ".join(cell(h) or " " for h in t["header"]) + " |",
              "|" + "---|" * len(t["header"])]
        L += ["| " + " | ".join(cell(c) for c in r) + " |" for r in t["rows"]]
    L += ["", "**Fórmulas**", ""]
    L += ["- *%s:* %s" % (md(lab), md(expr).replace("\n", " ;  ")) for lab, expr in n["formulas"]]
    L += ["", "**Ejemplo.** " + md(n["ejemplo"]), "", "**Se relaciona con:** " +
          "; ".join("%s (%s)" % (B.NODE[r]["corto"], md(p)) for r, p in n["rel"]), "", "---", ""]

# ---------------------------------------------------------------- cuadro comparativo
C = B.COMPARATIVO
L += ["## 3. %s" % C["titulo"], "", "| " + " | ".join(C["header"]) + " |", "|" + "---|" * len(C["header"])]
L += ["| " + " | ".join(cell(x) for x in r) + " |" for r in C["rows"]]
L += ["", "*IS = importance sampling.*", "", "### Guía rápida para elegir un algoritmo", ""]
L += ["- **%s** %s" % (md(a), md(b)) for a, b in C["claves"]]

open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
print("Generado:", OUT, "(%d líneas)" % len(L))
if shutil.which("pandoc"):
    subprocess.run(["pandoc", OUT, "-o", OUT.replace(".md", ".docx")], check=True)
    print("Generado también:", OUT.replace(".md", ".docx"))
