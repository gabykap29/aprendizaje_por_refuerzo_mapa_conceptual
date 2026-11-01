# -*- coding: utf-8 -*-
"""Contenido del mapa conceptual de Aprendizaje por Refuerzo.
Editá este archivo para cambiar textos; luego ejecutá build_mapa.py.
Marcado permitido: <b>, <i>, <sub>, <super>, <br/>.
"""

CATS = {
    "fund":     dict(nombre="Fundamentos",           color="#2563EB", tint="#DBEAFE"),
    "metodo":   dict(nombre="Métodos de solución",   color="#0F766E", tint="#CCFBF1"),
    "taxo":     dict(nombre="Conceptos transversales", color="#B45309", tint="#FEF3C7"),
    "valor":    dict(nombre="Basados en valor",      color="#15803D", tint="#DCFCE7"),
    "politica": dict(nombre="Basados en política",   color="#6D28D9", tint="#EDE9FE"),
}

# Posición en el mapa: (cx, cy, ancho, alto) sobre un lienzo de 1700 x 1100
NODOS = [
 dict(id="comp", cat="fund", pos=(230, 215, 300, 96),
      corto="Componentes del aprendizaje por refuerzo",
      mapsub="Agente · Entorno · Estado · Acción · Política · Recompensa · Descuento",
      titulo="Componentes del aprendizaje por refuerzo",
      sub="Los ingredientes de cualquier problema de RL",
      defn="El <b>aprendizaje por refuerzo (RL)</b> es un paradigma en el que un <b>agente</b> aprende a decidir "
           "<b>interactuando con un entorno</b>, por prueba y error, para maximizar la <b>recompensa acumulada</b> "
           "a largo plazo. No hay respuestas correctas etiquetadas (como en el aprendizaje supervisado): solo una señal "
           "de recompensa que dice qué tan bien se está actuando.",
      bullets=[
        "<b>Ciclo de interacción:</b> en cada paso t el agente observa el estado S<sub>t</sub>, elige una acción A<sub>t</sub>, "
        "y el entorno responde con una recompensa R<sub>t+1</sub> y un nuevo estado S<sub>t+1</sub>.",
        "<b>Objetivo:</b> no maximizar la recompensa inmediata, sino el <b>retorno</b> G<sub>t</sub> "
        "(suma de recompensas futuras descontadas).",
        "<b>Dilema exploración–explotación:</b> probar acciones nuevas (explorar) vs. usar la mejor conocida (explotar).",
        "<b>Episodio:</b> secuencia completa de interacción desde un estado inicial hasta uno terminal. "
        "Las tareas pueden ser <i>episódicas</i> o <i>continuas</i>.",
      ],
      tabla=dict(titulo="Los siete componentes",
        header=["Componente", "Qué es", "Notación"],
        rows=[
          ["<b>Agente</b>", "Quien aprende y toma decisiones (el «cerebro»).", "—"],
          ["<b>Entorno</b>", "Todo lo externo al agente; responde a cada acción con un nuevo estado y una recompensa.", "—"],
          ["<b>Estado</b>", "Descripción de la situación del entorno en un instante dado.", "s ∈ S"],
          ["<b>Acción</b>", "Decisión que el agente puede tomar en un estado.", "a ∈ A(s)"],
          ["<b>Política</b>", "Regla de comportamiento del agente: qué acción elegir en cada estado. Es lo que se quiere aprender.", "π(a|s)"],
          ["<b>Recompensa</b>", "Señal escalar inmediata que evalúa la acción tomada; define el objetivo.", "r = R(s,a,s')"],
          ["<b>Descuento</b>", "Factor que pondera el futuro: γ≈0 → agente «miope»; γ≈1 → visión a largo plazo.", "γ ∈ [0,1]"],
        ], widths=[0.17, 0.62, 0.21]),
      formulas=[
        ("Retorno descontado", "G<sub>t</sub> = R<sub>t+1</sub> + γ R<sub>t+2</sub> + γ² R<sub>t+3</sub> + … = Σ<sub>k=0</sub><super>∞</super> γ<super>k</super> R<sub>t+k+1</sub>"),
        ("Política estocástica", "π(a|s) = P( A<sub>t</sub> = a | S<sub>t</sub> = s )"),
      ],
      ejemplo="<b>Robot aspiradora.</b> Agente: el robot. Entorno: la casa. Estado: posición + nivel de batería. "
              "Acciones: avanzar, girar, volver a la base. Recompensa: +1 por superficie limpiada, −10 por chocar. "
              "γ = 0,95 para que valore llegar a cargarse antes de quedarse sin batería.",
      rel=[("mdp", "se formalizan como un MDP"), ("v", "el retorno define el valor de un estado"),
           ("egreedy", "exploración vs. explotación")]),

 dict(id="mdp", cat="fund", pos=(640, 215, 250, 84),
      corto="Procesos de decisión de Markov", mapsub="MDP = (S, A, P, R, γ)",
      titulo="Procesos de decisión de Markov (MDP)",
      sub="El marco matemático del aprendizaje por refuerzo",
      defn="Un <b>MDP</b> es el modelo matemático formal de un problema de decisión secuencial: describe estados, "
           "acciones, cómo evoluciona el entorno y qué recompensas se reciben. Casi todo el RL se plantea "
           "como la búsqueda de una buena política en un MDP.",
      bullets=[
        "<b>Tupla (S, A, P, R, γ):</b> conjunto de estados, de acciones, dinámica de transición P(s'|s,a), "
        "función de recompensa R(s,a,s') y factor de descuento γ.",
        "<b>Propiedad de Markov:</b> el futuro depende solo del estado y la acción actuales, no de toda la historia. "
        "El estado resume todo lo relevante del pasado.",
        "<b>Objetivo:</b> hallar la política óptima π* que maximiza el retorno esperado desde cualquier estado.",
        "<b>Con modelo vs. sin modelo:</b> si P y R se conocen, el MDP se resuelve por <i>programación dinámica</i>; "
        "si no se conocen, el agente aprende de la experiencia (<i>Monte Carlo, Diferencia Temporal</i>).",
        "<b>Variantes:</b> MDP parcialmente observable (POMDP), donde el agente no ve el estado completo.",
      ],
      formulas=[
        ("Propiedad de Markov", "P( S<sub>t+1</sub> | S<sub>t</sub>, A<sub>t</sub> ) = P( S<sub>t+1</sub> | S<sub>1</sub>, A<sub>1</sub>, …, S<sub>t</sub>, A<sub>t</sub> )"),
        ("Ecuación de Bellman (esperanza)", "V<super>π</super>(s) = Σ<sub>a</sub> π(a|s) Σ<sub>s'</sub> P(s'|s,a) [ R + γ V<super>π</super>(s') ]"),
        ("Ecuación de Bellman (optimalidad)", "V*(s) = max<sub>a</sub> Σ<sub>s'</sub> P(s'|s,a) [ R + γ V*(s') ]"),
      ],
      ejemplo="<b>Gridworld.</b> Una cuadrícula 4×4: cada celda es un estado, las acciones son ↑ ↓ ← →, "
              "cada paso cuesta −1 y llegar a la meta termina el episodio. Si el piso es resbaloso, P(s'|s,a) "
              "es estocástica: ir «↑» a veces te desvía a un costado.",
      rel=[("comp", "formaliza sus componentes"), ("v", "define la función estado-valor"),
           ("q", "define la función acción-valor"), ("dp", "se resuelve con el modelo conocido"),
           ("mc", "o aprendiendo de episodios"), ("td", "o aprendiendo paso a paso")]),

 dict(id="v", cat="fund", pos=(1060, 150, 260, 76),
      corto="Función estado-valor", mapsub="V(s)",
      titulo="Función estado-valor  V(s)",
      sub="¿Qué tan bueno es estar en este estado?",
      defn="La <b>función estado-valor</b> V<super>π</super>(s) es el <b>retorno esperado</b> si el agente parte del estado s "
           "y sigue la política π de ahí en adelante. Resume el «futuro prometedor» de un estado en un solo número.",
      bullets=[
        "Depende de la política: una misma situación vale distinto según cómo se actúe después.",
        "<b>Recursividad de Bellman:</b> el valor de un estado = recompensa inmediata + valor descontado del siguiente estado.",
        "<b>Valor óptimo V*(s):</b> el mayor valor alcanzable por cualquier política; de él se deduce π*.",
        "<b>Relación con Q:</b> V es el promedio de Q ponderado por la política.",
        "<b>Limitación para controlar:</b> con solo V, para elegir acción hace falta conocer el modelo (a qué estado lleva cada acción). "
        "Por eso, en control sin modelo se prefiere Q(s,a).",
        "<b>Cómo se estima:</b> programación dinámica (con modelo), promedio de retornos en Monte Carlo, o TD(0).",
      ],
      formulas=[
        ("Definición", "V<super>π</super>(s) = E<sub>π</sub>[ G<sub>t</sub> | S<sub>t</sub> = s ]"),
        ("Bellman", "V<super>π</super>(s) = E<sub>π</sub>[ R<sub>t+1</sub> + γ V<super>π</super>(S<sub>t+1</sub>) | S<sub>t</sub> = s ]"),
        ("Desde Q", "V<super>π</super>(s) = Σ<sub>a</sub> π(a|s) · Q<super>π</super>(s,a)"),
        ("Actualización TD(0)", "V(s) ← V(s) + α [ r + γ V(s') − V(s) ]"),
      ],
      ejemplo="<b>Gridworld.</b> Con recompensa −1 por paso, una celda adyacente a la meta tiene V ≈ −1 y una celda lejana V ≈ −14: "
              "el valor «mide» cuántos pasos faltan. El agente aprende que moverse hacia celdas de mayor V es bueno.",
      rel=[("q", "su versión que incluye la acción"), ("mdp", "se define sobre un MDP"),
           ("predctrl", "estimarla es el problema de predicción"), ("td", "se estima con TD(0)"),
           ("a2c", "es el «crítico» en actor-crítico")]),

 dict(id="q", cat="fund", pos=(1060, 280, 260, 76),
      corto="Función acción-valor", mapsub="Q(s, a)",
      titulo="Función acción-valor  Q(s, a)",
      sub="¿Qué tan buena es esta acción en este estado?",
      defn="La <b>función acción-valor</b> Q<super>π</super>(s,a) es el retorno esperado si el agente, estando en s, "
           "<b>toma la acción a</b> y luego sigue la política π. Es la función central del aprendizaje basado en valores.",
      bullets=[
        "<b>Permite decidir sin modelo:</b> la política greedy es simplemente π(s) = argmax<sub>a</sub> Q(s,a).",
        "<b>Q*(s,a)</b> es el valor óptimo; conocer Q* equivale a conocer cómo actuar de forma óptima.",
        "<b>Forma tabular:</b> una «Q-table» con una fila por estado y una columna por acción. "
        "Cuando los estados son demasiados, se aproxima con una red neuronal (DQN).",
        "<b>Función de ventaja:</b> A(s,a) = Q(s,a) − V(s) mide cuánto mejor es una acción que el promedio en ese estado "
        "(es la que usan A2C/A3C).",
        "<b>Es lo que estiman</b> SARSA (Q<super>π</super>) y Q-Learning (Q*).",
      ],
      formulas=[
        ("Definición", "Q<super>π</super>(s,a) = E<sub>π</sub>[ G<sub>t</sub> | S<sub>t</sub>=s, A<sub>t</sub>=a ]"),
        ("Óptima (Bellman)", "Q*(s,a) = Σ<sub>s'</sub> P(s'|s,a) [ R + γ max<sub>a'</sub> Q*(s',a') ]"),
        ("Política greedy", "π(s) = argmax<sub>a</sub> Q(s,a)"),
        ("Ventaja", "A(s,a) = Q(s,a) − V(s)"),
      ],
      ejemplo="<b>Q-table.</b> En una celda con meta a la derecha: Q(s,→) = −2, Q(s,↑) = −5, Q(s,←) = −9, Q(s,↓) = −6. "
              "La política greedy elige «→». Nunca hizo falta saber a dónde lleva cada acción: basta comparar valores.",
      rel=[("v", "V es el promedio de Q según π"), ("sarsa", "la estima on-policy"),
           ("qlearn", "la estima off-policy"), ("dqn", "la aproxima con una red neuronal"),
           ("egreedy", "se usa para elegir acciones a partir de Q")]),

 dict(id="predctrl", cat="taxo", pos=(1480, 215, 260, 84),
      corto="Predicción vs Control", mapsub="evaluar una π  ·  encontrar π*",
      titulo="Predicción vs Control",
      sub="Dos preguntas distintas sobre una política",
      defn="Los problemas de RL se separan en dos tareas: la <b>predicción</b> (o evaluación de política) estima "
           "<b>qué tan buena es</b> una política dada; el <b>control</b> busca <b>la mejor política</b>. "
           "Casi todos los algoritmos de control combinan ambas.",
      bullets=[
        "<b>Predicción:</b> dada una política fija π, estimar V<super>π</super> o Q<super>π</super>. No se cambia el comportamiento, solo se mide.",
        "<b>Control:</b> encontrar π* (y V*, Q*). Se logra alternando <i>evaluar</i> y <i>mejorar</i> la política.",
        "<b>Iteración generalizada de la política (GPI):</b> evaluación y mejora conviven: la evaluación acerca la función de valor "
        "a la política actual y la mejora vuelve la política greedy respecto del valor.",
        "<b>Control necesita explorar</b> (por ejemplo con ε-greedy); la predicción pura no.",
      ],
      tabla=dict(titulo="Predicción vs Control",
        header=["", "Predicción", "Control"],
        rows=[
          ["<b>Pregunta</b>", "¿Qué tan buena es esta política?", "¿Cuál es la mejor política?"],
          ["<b>Entrada</b>", "Una política π fija", "Ninguna (se parte de una política cualquiera)"],
          ["<b>Salida</b>", "V<super>π</super>(s) o Q<super>π</super>(s,a)", "π*, V*(s), Q*(s,a)"],
          ["<b>Ejemplos</b>", "Evaluación de política (DP), MC de predicción, TD(0)", "Iteración de políticas/valores (DP), MC control, SARSA, Q-Learning"],
        ], widths=[0.16, 0.42, 0.42]),
      formulas=[
        ("Predicción (TD)", "V(s) ← V(s) + α [ r + γ V(s') − V(s) ]"),
        ("Control (Q-Learning)", "Q(s,a) ← Q(s,a) + α [ r + γ max<sub>a'</sub> Q(s',a') − Q(s,a) ]"),
      ],
      ejemplo="<b>Dos preguntas en un videojuego.</b> Predicción: «si siempre juego de forma defensiva, ¿qué puntaje esperado tengo?». "
              "Control: «¿qué estrategia me da el mayor puntaje posible?».",
      rel=[("v", "predicción estima V"), ("q", "control suele estimar Q"),
           ("dp", "resuelve ambos con modelo"), ("mc", "resuelve ambos con episodios"),
           ("td", "resuelve ambos paso a paso")]),

 dict(id="dp", cat="metodo", pos=(230, 470, 270, 84),
      corto="Programación dinámica", mapsub="con modelo · bootstrapping",
      titulo="Programación dinámica (DP)",
      sub="Planificar cuando el modelo del entorno es conocido",
      defn="La <b>programación dinámica</b> resuelve MDPs <b>cuando se conoce el modelo completo</b> (P y R). "
           "Convierte las ecuaciones de Bellman en reglas de actualización que se aplican iterativamente "
           "hasta converger. Es la base teórica de todo el RL.",
      bullets=[
        "<b>Bootstrapping:</b> actualiza una estimación a partir de otras estimaciones (el valor de s se calcula con el valor de s').",
        "<b>Barridos completos:</b> recorre <i>todos</i> los estados y todas las transiciones posibles (sin muestrear).",
        "<b>Evaluación de política:</b> calcula V<super>π</super> aplicando Bellman de esperanza hasta converger.",
        "<b>Mejora de política:</b> hace la política greedy respecto del valor actual.",
        "<b>Iteración de políticas:</b> alterna evaluación completa y mejora. <b>Iteración de valores:</b> fusiona ambos pasos con la ecuación de optimalidad.",
        "<b>Limitaciones:</b> requiere un modelo (casi nunca disponible) y su costo crece con el número de estados (maldición de la dimensionalidad).",
      ],
      formulas=[
        ("Evaluación de política", "V<sub>k+1</sub>(s) = Σ<sub>a</sub> π(a|s) Σ<sub>s'</sub> P(s'|s,a) [ R + γ V<sub>k</sub>(s') ]"),
        ("Iteración de valores", "V<sub>k+1</sub>(s) = max<sub>a</sub> Σ<sub>s'</sub> P(s'|s,a) [ R + γ V<sub>k</sub>(s') ]"),
      ],
      ejemplo="<b>Planificar una ruta con mapa completo.</b> Si conocés las probabilidades de cada transición, "
              "podés calcular V* para todas las celdas sin ni siquiera «jugar» una vez: solo iterando la fórmula hasta que los valores dejan de cambiar.",
      rel=[("mdp", "requiere el MDP completo"), ("mc", "alternativa sin modelo"),
           ("td", "TD hereda su bootstrapping"), ("predctrl", "evaluación = predicción; iteración = control")]),

 dict(id="mc", cat="metodo", pos=(640, 470, 250, 84),
      corto="Monte Carlo", mapsub="episodios completos · sin modelo",
      titulo="Métodos Monte Carlo (MC)",
      sub="Aprender promediando retornos de episodios completos",
      defn="Los métodos <b>Monte Carlo</b> aprenden <b>directamente de la experiencia</b> sin necesitar el modelo. "
           "Esperan a que el episodio termine, calculan el retorno real G<sub>t</sub> de cada estado visitado y "
           "estiman el valor como el <b>promedio de esos retornos</b>.",
      bullets=[
        "<b>Sin bootstrapping:</b> usa retornos reales completos, no estimaciones de otros estados.",
        "<b>Solo tareas episódicas:</b> necesita que el episodio termine para poder actualizar.",
        "<b>Sin sesgo, alta varianza:</b> el retorno real es una estimación insesgada, pero varía mucho entre episodios.",
        "<b>First-visit vs. every-visit:</b> promediar el retorno solo de la primera visita al estado en el episodio, o de todas.",
        "<b>MC control:</b> estima Q y mejora la política; necesita explorar (exploring starts o ε-greedy).",
        "<b>Ventaja:</b> puede aprender de simulaciones o experiencia real, y no se ve afectado por violaciones de Markov.",
      ],
      formulas=[
        ("Estimación por promedio", "V(s) ≈ ( G<sup>(1)</sup> + G<sup>(2)</sup> + … + G<sup>(N)</sup> ) / N"),
        ("Actualización incremental", "V(S<sub>t</sub>) ← V(S<sub>t</sub>) + α [ G<sub>t</sub> − V(S<sub>t</sub>) ]"),
      ],
      ejemplo="<b>Blackjack.</b> Se juegan muchas manos; al terminar cada una se conoce el resultado final (+1, 0, −1) "
              "y se actualiza el valor de todos los estados por los que pasó esa mano. No hace falta conocer las probabilidades del mazo.",
      rel=[("td", "TD actualiza sin esperar al final"), ("dp", "DP necesita modelo; MC no"),
           ("pg", "REINFORCE usa retornos Monte Carlo"), ("predctrl", "sirve para predicción y control")]),

 dict(id="td", cat="metodo", pos=(1060, 470, 270, 84),
      corto="Diferencia temporal", mapsub="TD(0) · paso a paso · bootstrapping",
      titulo="Aprendizaje por diferencia temporal (TD)",
      sub="Aprender paso a paso, sin esperar al final del episodio",
      defn="El aprendizaje por <b>diferencia temporal</b> combina lo mejor de Monte Carlo (aprende de la experiencia, sin modelo) "
           "y de la programación dinámica (hace bootstrapping). Actualiza el valor de un estado <b>después de cada paso</b>, "
           "usando la estimación del siguiente estado.",
      bullets=[
        "<b>Objetivo TD:</b> r + γ·V(s'). En vez del retorno completo G<sub>t</sub>, usa la recompensa inmediata más el valor estimado del siguiente estado.",
        "<b>Error TD (δ):</b> diferencia entre el objetivo y la estimación actual; es la señal de aprendizaje.",
        "<b>Funciona en tareas continuas</b> y en episodios inconclusos.",
        "<b>Menos varianza que MC</b> pero con algo de sesgo (porque se apoya en estimaciones).",
        "<b>Base de los grandes algoritmos:</b> SARSA, Q-Learning, DQN y el «crítico» de A2C/A3C.",
        "<b>Extensiones:</b> n-step TD y TD(λ) interpolan entre TD(0) y Monte Carlo.",
      ],
      tabla=dict(titulo="Comparación DP · MC · TD",
        header=["", "Prog. dinámica", "Monte Carlo", "Diferencia temporal"],
        rows=[
          ["<b>¿Necesita modelo?</b>", "Sí", "No", "No"],
          ["<b>¿Bootstrapping?</b>", "Sí", "No", "Sí"],
          ["<b>¿Muestrea?</b>", "No (barrido completo)", "Sí", "Sí"],
          ["<b>Actualiza…</b>", "Cada iteración", "Al final del episodio", "Cada paso"],
          ["<b>Sesgo / Varianza</b>", "— / —", "Sin sesgo / alta varianza", "Algo de sesgo / baja varianza"],
        ], widths=[0.24, 0.24, 0.26, 0.26]),
      formulas=[
        ("TD(0)", "V(S<sub>t</sub>) ← V(S<sub>t</sub>) + α [ R<sub>t+1</sub> + γ V(S<sub>t+1</sub>) − V(S<sub>t</sub>) ]"),
        ("Error TD", "δ<sub>t</sub> = R<sub>t+1</sub> + γ V(S<sub>t+1</sub>) − V(S<sub>t</sub>)"),
      ],
      ejemplo="<b>Volver a casa en auto.</b> Estimás 30 min de viaje. Tras 5 min topás con tráfico y la nueva estimación sube a 40 min: "
              "TD corrige ya mismo la estimación inicial. MC esperaría a llegar a casa para ajustar.",
      rel=[("mc", "comparte el muestreo, no el bootstrapping"), ("dp", "comparte el bootstrapping, no el modelo"),
           ("sarsa", "control on-policy basado en TD"), ("qlearn", "control off-policy basado en TD"),
           ("a2c", "el crítico se aprende con TD")]),

 dict(id="vspol", cat="taxo", pos=(640, 735, 310, 96),
      corto="Aprendizaje basado en valores vs. basado en políticas", mapsub="¿qué aprende el agente?",
      titulo="Basado en valores vs. basado en políticas",
      sub="Dos formas de llegar a una buena política",
      defn="Hay dos grandes familias: los métodos <b>basados en valores</b> aprenden una función de valor (V o Q) y "
           "<b>derivan</b> la política de ella; los métodos <b>basados en políticas</b> <b>optimizan directamente</b> "
           "la política. Los <b>actor-crítico</b> combinan ambos.",
      bullets=[
        "<b>Basados en valores:</b> la política es implícita (greedy o ε-greedy sobre Q). Ejemplos: SARSA, Q-Learning, DQN.",
        "<b>Basados en políticas:</b> se parametriza π<sub>θ</sub>(a|s) (p. ej. una red con softmax) y se ajusta θ por ascenso del gradiente. Ejemplos: REINFORCE.",
        "<b>Actor-crítico (híbrido):</b> el <i>actor</i> es la política y el <i>crítico</i> es la función de valor que lo guía. Ejemplos: A2C, A3C.",
      ],
      tabla=dict(titulo="Comparación",
        header=["", "Basado en valores", "Basado en políticas"],
        rows=[
          ["<b>Qué aprende</b>", "V(s) o Q(s,a); la política se deriva", "La política π<sub>θ</sub>(a|s) directamente"],
          ["<b>Acciones</b>", "Discretas (necesita un max sobre acciones)", "Discretas y <b>continuas</b>"],
          ["<b>Política</b>", "Determinista (con ε para explorar)", "Estocástica de forma natural"],
          ["<b>Convergencia</b>", "Puede oscilar o divergir con redes", "Más suave, pero a óptimos locales"],
          ["<b>Varianza</b>", "Baja", "Alta (se reduce con crítico/baseline)"],
          ["<b>Eficiencia de datos</b>", "Mayor (off-policy, replay)", "Menor (suele ser on-policy)"],
        ], widths=[0.22, 0.39, 0.39]),
      formulas=[
        ("Valor → política", "π(s) = argmax<sub>a</sub> Q(s,a)"),
        ("Política directa", "θ ← θ + α ∇<sub>θ</sub> J(θ)"),
      ],
      ejemplo="<b>Conducir un auto.</b> Basado en valor: calcular cuán bueno es cada giro posible y elegir el mejor. "
              "Basado en política: la red entrega directamente «girar el volante 3,2°»: no se puede hacer un argmax sobre infinitos ángulos.",
      rel=[("sarsa", "valor"), ("qlearn", "valor"), ("dqn", "valor profundo"),
           ("pg", "política"), ("a2c", "híbrido actor-crítico"), ("a3c", "híbrido asíncrono")]),

 dict(id="onoff", cat="taxo", pos=(1265, 640, 210, 100),
      corto="On-Policy vs Off-Policy", mapsub="política de comportamiento vs objetivo",
      titulo="On-Policy vs Off-Policy",
      sub="¿La política que explora es la misma que se aprende?",
      defn="Se distinguen dos políticas: la de <b>comportamiento</b> b (la que genera los datos) y la <b>objetivo</b> π (la que se evalúa y mejora). "
           "En <b>on-policy</b> son la misma; en <b>off-policy</b> son distintas.",
      bullets=[
        "<b>On-policy:</b> aprende sobre la política que está ejecutando, exploración incluida. Es más simple y estable, pero descarta los datos viejos.",
        "<b>Off-policy:</b> puede aprender la política óptima (greedy) mientras explora con otra, <b>reutilizar experiencia pasada</b> "
        "(experience replay) o aprender de datos de otros agentes o de humanos.",
        "<b>Corrección:</b> cuando b ≠ π en métodos de muestreo (p. ej. Monte Carlo) se usa <i>importance sampling</i>, que reescala por el cociente π/b.",
        "<b>Costo:</b> off-policy + bootstrapping + aproximación de funciones puede ser inestable (la «tríada mortal»).",
      ],
      tabla=dict(titulo="Clasificación de los algoritmos",
        header=["Algoritmo", "Tipo", "Por qué"],
        rows=[
          ["<b>SARSA</b>", "On-policy", "Su objetivo usa la acción a' realmente elegida por la política ε-greedy."],
          ["<b>Q-Learning</b>", "Off-policy", "Su objetivo usa max Q(s',·), sin importar qué acción se tome luego."],
          ["<b>DQN</b>", "Off-policy", "Hereda de Q-Learning y reutiliza datos del replay buffer."],
          ["<b>REINFORCE</b>", "On-policy", "Aprende con trayectorias generadas por la política actual."],
          ["<b>A2C / A3C</b>", "On-policy", "Los gradientes se calculan con datos de la política vigente."],
        ], widths=[0.22, 0.17, 0.61]),
      formulas=[
        ("Importance sampling", "ρ<sub>t</sub> = π(A<sub>t</sub>|S<sub>t</sub>) / b(A<sub>t</sub>|S<sub>t</sub>)"),
      ],
      ejemplo="<b>Aprender a cocinar.</b> On-policy: aprendés solo de lo que vos mismo cocinás con tu receta actual. "
              "Off-policy: aprendés de recetas de otros y de tus intentos viejos, pero apuntando a cocinar la mejor versión posible.",
      rel=[("sarsa", "ejemplo on-policy"), ("qlearn", "ejemplo off-policy"),
           ("dqn", "off-policy con replay"), ("egreedy", "política de comportamiento típica")]),

 dict(id="sarsa", cat="valor", pos=(1010, 640, 230, 84),
      corto="Algoritmo SARSA", mapsub="control TD on-policy",
      titulo="Algoritmo SARSA",
      sub="State – Action – Reward – State – Action",
      defn="<b>SARSA</b> es un algoritmo de <b>control TD on-policy</b>. Aprende Q<super>π</super>(s,a) usando la quíntupla "
           "(s, a, r, s', a') y su objetivo incluye la acción a' <b>realmente elegida</b> por la política (ε-greedy) en el siguiente estado.",
      bullets=[
        "<b>Es on-policy:</b> evalúa y mejora la misma política que usa para explorar; por eso «paga» por sus propios errores de exploración.",
        "<b>Conducta cautelosa:</b> en Cliff Walking, SARSA aprende un camino seguro, alejado del acantilado, porque sabe que a veces explorará.",
        "<b>Convergencia:</b> converge a π* si todos los pares (s,a) se visitan infinitamente y ε → 0 gradualmente (condición GLIE).",
      ],
      steps=[
        "Inicializar Q(s,a) arbitrariamente.",
        "En el estado s elegir a con política ε-greedy sobre Q.",
        "Ejecutar a; observar r y s'.",
        "Elegir a' en s' con la <b>misma</b> política ε-greedy.",
        "Actualizar Q(s,a) con el objetivo r + γ Q(s',a').",
        "s ← s', a ← a'. Repetir hasta fin del episodio.",
      ],
      formulas=[
        ("Actualización", "Q(s,a) ← Q(s,a) + α [ r + γ Q(s',a') − Q(s,a) ]"),
        ("Objetivo TD", "r + γ Q(s',a')   (a' ~ ε-greedy)"),
      ],
      ejemplo="<b>Cliff Walking.</b> Una cuadrícula con un acantilado junto al camino más corto. Con ε = 0,1, SARSA aprende la ruta "
              "más larga y segura, porque contempla que una acción aleatoria cerca del borde podría hacerlo caer.",
      rel=[("td", "es TD aplicado a control"), ("onoff", "ejemplo on-policy"),
           ("egreedy", "elige acciones con ε-greedy"), ("qlearn", "su contraparte off-policy"),
           ("q", "estima Q<super>π</super>")]),

 dict(id="qlearn", cat="valor", pos=(1520, 640, 230, 84),
      corto="Algoritmo Q-Learning", mapsub="control TD off-policy",
      titulo="Algoritmo Q-Learning",
      sub="Aprender la política óptima mientras se explora",
      defn="<b>Q-Learning</b> (Watkins, 1989) es un algoritmo de <b>control TD off-policy</b>. Su objetivo usa el <b>máximo</b> valor de Q en el "
           "siguiente estado, es decir, asume que a partir de ahí se actuará de forma óptima, <b>aunque el comportamiento real sea otro</b>.",
      bullets=[
        "<b>Es off-policy:</b> la política de comportamiento (ε-greedy) explora; la política objetivo (greedy) es la que se aprende.",
        "<b>Aprende Q* directamente</b> sin importar cómo se recolecten los datos, siempre que todos los pares (s,a) se visiten con frecuencia.",
        "<b>Más audaz:</b> en Cliff Walking aprende el camino óptimo pegado al acantilado, aunque durante el entrenamiento cae a veces.",
        "<b>Limitaciones:</b> la Q-table no escala a espacios grandes (→ DQN) y el operador max produce <i>sobreestimación</i> (→ Double Q-Learning).",
      ],
      steps=[
        "Inicializar Q(s,a) arbitrariamente.",
        "En s elegir a con ε-greedy sobre Q.",
        "Ejecutar a; observar r y s'.",
        "Calcular el objetivo r + γ max<sub>a'</sub> Q(s',a') (sin elegir a' realmente).",
        "Actualizar Q(s,a) hacia ese objetivo.",
        "s ← s'. Repetir hasta fin del episodio.",
      ],
      tabla=dict(titulo="SARSA vs Q-Learning",
        header=["", "SARSA", "Q-Learning"],
        rows=[
          ["<b>Tipo</b>", "On-policy", "Off-policy"],
          ["<b>Objetivo</b>", "r + γ Q(s',a')", "r + γ max Q(s',·)"],
          ["<b>Aprende</b>", "Q<super>π</super> (de la política ε-greedy)", "Q* (de la política greedy)"],
          ["<b>Estilo</b>", "Cauteloso", "Óptimo pero arriesgado al entrenar"],
        ], widths=[0.2, 0.4, 0.4]),
      formulas=[
        ("Actualización", "Q(s,a) ← Q(s,a) + α [ r + γ max<sub>a'</sub> Q(s',a') − Q(s,a) ]"),
        ("Política objetivo", "π(s) = argmax<sub>a</sub> Q(s,a)"),
      ],
      ejemplo="<b>Cliff Walking.</b> Q-Learning converge a la ruta más corta junto al borde del acantilado (la óptima). "
              "Durante el entrenamiento, por la exploración ε, se cae más veces que SARSA; una vez entrenado y con ε = 0, su recorrido es mejor.",
      rel=[("td", "es TD aplicado a control"), ("onoff", "ejemplo off-policy"),
           ("egreedy", "explora con ε-greedy"), ("sarsa", "su contraparte on-policy"),
           ("dqn", "se extiende con redes neuronales"), ("q", "estima Q*")]),

 dict(id="egreedy", cat="taxo", pos=(1265, 830, 240, 84),
      corto="Epsilon-Greedy", mapsub="exploración vs explotación",
      titulo="Epsilon-Greedy (ε-greedy)",
      sub="La estrategia más simple para equilibrar explorar y explotar",
      defn="Con probabilidad <b>1 − ε</b> el agente <b>explota</b>: elige la acción de mayor valor estimado; "
           "con probabilidad <b>ε</b> <b>explora</b>: elige una acción al azar. Garantiza que todas las acciones se sigan probando.",
      bullets=[
        "<b>Dilema:</b> explotar maximiza la recompensa ahora; explorar puede descubrir algo mejor. Hace falta un equilibrio.",
        "<b>Decaimiento de ε:</b> se empieza con ε alto (≈ 1,0) para explorar mucho y se reduce (≈ 0,01–0,1) a medida que el agente aprende.",
        "<b>Dónde se usa:</b> SARSA, Q-Learning, DQN y MC control.",
        "<b>Alternativas:</b> softmax/Boltzmann (elige según probabilidades proporcionales al valor), UCB (optimismo ante la incertidumbre), inicialización optimista.",
      ],
      formulas=[
        ("Política ε-greedy", "π(a|s) = 1 − ε + ε/|A|   si a = argmax Q(s,·)<br/>π(a|s) = ε/|A|   en otro caso"),
        ("Decaimiento exponencial", "ε<sub>t</sub> = max( ε<sub>min</sub>, ε<sub>0</sub> · d<super>t</super> )"),
      ],
      ejemplo="<b>Elegir restaurante.</b> Con ε = 0,1: el 90 % de las veces vas a tu favorito (explotar) y el 10 % probás uno nuevo al azar (explorar). "
              "Si nunca probás, jamás sabrás si existe uno mejor.",
      rel=[("sarsa", "lo usa para elegir a y a'"), ("qlearn", "lo usa como política de comportamiento"),
           ("dqn", "lo usa para recolectar experiencia"), ("onoff", "define la política de comportamiento"),
           ("comp", "dilema exploración–explotación")]),

 dict(id="dqn", cat="valor", pos=(1520, 880, 240, 84),
      corto="Algoritmo DQN (Deep Q-Network)", mapsub="Q-Learning + red neuronal",
      titulo="Algoritmo DQN (Deep Q-Network)",
      sub="Q-Learning con redes neuronales profundas",
      defn="<b>DQN</b> (DeepMind, 2013/2015) reemplaza la Q-table por una <b>red neuronal profunda</b> Q(s,a;θ) que aproxima la función acción-valor. "
           "Permite aprender directamente de entradas de alta dimensión, como los <b>píxeles</b> de un videojuego Atari.",
      bullets=[
        "<b>Experience Replay:</b> las transiciones (s,a,r,s',done) se guardan en un buffer y se entrena con <i>minibatches aleatorios</i>. "
        "Rompe la correlación entre muestras consecutivas y reutiliza datos.",
        "<b>Target Network:</b> una copia de la red con parámetros congelados θ<super>−</super> calcula el objetivo y se actualiza cada C pasos. "
        "Evita perseguir un objetivo que se mueve en cada paso.",
        "<b>Off-policy y basado en valores;</b> acciones discretas; explora con ε-greedy.",
        "<b>Extensiones:</b> Double DQN (reduce la sobreestimación), Dueling DQN, Prioritized Replay, Rainbow.",
      ],
      steps=[
        "Observar s, elegir a con ε-greedy usando la red Q(s,·;θ).",
        "Ejecutar a, observar r, s'; guardar (s,a,r,s') en el buffer.",
        "Muestrear un minibatch aleatorio del buffer.",
        "Calcular el objetivo y = r + γ max Q(s',·;θ<super>−</super>) con la red objetivo.",
        "Minimizar (y − Q(s,a;θ))² por descenso del gradiente.",
        "Cada C pasos copiar θ<super>−</super> ← θ.",
      ],
      formulas=[
        ("Función de pérdida", "L(θ) = E<sub>(s,a,r,s')~D</sub> [ ( r + γ max<sub>a'</sub> Q(s',a';θ<super>−</super>) − Q(s,a;θ) )² ]"),
      ],
      ejemplo="<b>Atari (Breakout, Pong…).</b> La entrada son 4 fotogramas de 84×84 píxeles apilados; la red convolucional devuelve un Q para cada botón del joystick. "
              "DQN superó el nivel humano en muchos juegos con el mismo algoritmo y la misma arquitectura.",
      rel=[("qlearn", "es Q-Learning con red neuronal"), ("q", "aproxima Q(s,a)"),
           ("onoff", "off-policy gracias al replay"), ("egreedy", "explora con ε-greedy"),
           ("vspol", "basado en valores")]),

 dict(id="pg", cat="politica", pos=(230, 640, 300, 96),
      corto="Policy Gradient y algoritmo REINFORCE", mapsub="∇θ log πθ · Monte Carlo",
      titulo="Policy Gradient y algoritmo REINFORCE",
      sub="Optimizar la política directamente por ascenso del gradiente",
      defn="Los métodos de <b>gradiente de la política</b> parametrizan la política π<sub>θ</sub>(a|s) (típicamente una red neuronal) y ajustan θ "
           "para <b>aumentar el retorno esperado</b> J(θ). <b>REINFORCE</b> (Williams, 1992) es el algoritmo más simple: usa retornos Monte Carlo de episodios completos.",
      bullets=[
        "<b>Intuición:</b> si una acción llevó a un buen retorno, aumentar su probabilidad; si llevó a uno malo, reducirla.",
        "<b>Teorema del gradiente de la política:</b> el gradiente se puede estimar sin conocer el modelo, solo con ∇ log π y retornos.",
        "<b>Ventajas:</b> maneja acciones continuas, aprende políticas estocásticas y su convergencia es suave.",
        "<b>Desventajas:</b> alta varianza, baja eficiencia de muestras y necesita episodios completos; converge a óptimos locales.",
        "<b>Baseline:</b> restar b(s) al retorno reduce la varianza sin introducir sesgo. Llevarlo al extremo da el actor-crítico (A2C).",
      ],
      steps=[
        "Inicializar los parámetros θ de la política.",
        "Generar un episodio completo siguiendo π<sub>θ</sub>: (S<sub>0</sub>,A<sub>0</sub>,R<sub>1</sub>, …, S<sub>T</sub>).",
        "Para cada paso t calcular el retorno G<sub>t</sub>.",
        "Actualizar θ ← θ + α · G<sub>t</sub> · ∇<sub>θ</sub> log π<sub>θ</sub>(A<sub>t</sub>|S<sub>t</sub>).",
        "Repetir con un nuevo episodio.",
      ],
      formulas=[
        ("Objetivo", "J(θ) = E<sub>π<sub>θ</sub></sub>[ G<sub>0</sub> ]"),
        ("Gradiente de la política", "∇<sub>θ</sub> J(θ) = E<sub>π<sub>θ</sub></sub>[ ∇<sub>θ</sub> log π<sub>θ</sub>(a|s) · G<sub>t</sub> ]"),
        ("REINFORCE", "θ ← θ + α · G<sub>t</sub> · ∇<sub>θ</sub> log π<sub>θ</sub>(A<sub>t</sub>|S<sub>t</sub>)"),
        ("Con baseline", "θ ← θ + α · ( G<sub>t</sub> − b(S<sub>t</sub>) ) · ∇<sub>θ</sub> log π<sub>θ</sub>(A<sub>t</sub>|S<sub>t</sub>)"),
      ],
      ejemplo="<b>CartPole.</b> Una red con softmax da la probabilidad de empujar el carro a la izquierda o derecha. Al terminar cada episodio, "
              "las acciones de los episodios largos (que mantuvieron el palo en equilibrio) ven aumentar su probabilidad.",
      rel=[("vspol", "familia basada en políticas"), ("mc", "usa retornos Monte Carlo"),
           ("a2c", "se mejora agregando un crítico"), ("onoff", "es on-policy")]),

 dict(id="a2c", cat="politica", pos=(230, 815, 300, 96),
      corto="A2C (Advantage Actor-Critic)", mapsub="actor + crítico · síncrono",
      titulo="A2C — Advantage Actor-Critic",
      sub="Actor-crítico con función de ventaja, actualización síncrona",
      defn="<b>A2C</b> combina dos redes (o dos cabezas de una misma red): el <b>actor</b> π<sub>θ</sub>(a|s), que decide, y el <b>crítico</b> V<sub>w</sub>(s), "
           "que evalúa los estados y se aprende por TD. El crítico permite calcular la <b>ventaja</b>, que reemplaza al retorno en el gradiente y reduce mucho la varianza.",
      bullets=[
        "<b>Ventaja A(s,a):</b> cuánto mejor fue la acción que el valor promedio del estado. Se estima con el error TD: A ≈ r + γV(s') − V(s).",
        "<b>Actor:</b> sube la probabilidad de acciones con ventaja positiva y baja las de ventaja negativa.",
        "<b>Crítico:</b> se entrena para predecir bien V(s) minimizando el error TD cuadrático.",
        "<b>Síncrono:</b> varios entornos paralelos avanzan n pasos; se esperan todos, se promedian los gradientes y se hace <b>una</b> actualización.",
        "<b>Compromiso:</b> menos varianza que REINFORCE a cambio de algo de sesgo (por el bootstrapping del crítico). Es on-policy.",
        "<b>Pérdida total:</b> pérdida de política + c<sub>1</sub>·pérdida del crítico − c<sub>2</sub>·entropía (la entropía fomenta explorar).",
      ],
      formulas=[
        ("Ventaja (error TD)", "A(s,a) ≈ r + γ V<sub>w</sub>(s') − V<sub>w</sub>(s)"),
        ("Actor", "θ ← θ + α<sub>θ</sub> · A · ∇<sub>θ</sub> log π<sub>θ</sub>(a|s)"),
        ("Crítico", "w ← w − α<sub>w</sub> ∇<sub>w</sub> ( r + γ V<sub>w</sub>(s') − V<sub>w</sub>(s) )²"),
      ],
      ejemplo="<b>Actor y crítico.</b> El actor es un jugador; el crítico, su entrenador: no le dice qué hacer, "
              "sino «esa jugada salió mejor (o peor) de lo que esperaba». El jugador ajusta su estilo según esa retroalimentación.",
      rel=[("pg", "mejora REINFORCE con un crítico"), ("a3c", "su versión asíncrona"),
           ("td", "el crítico se aprende con TD"), ("v", "el crítico estima V(s)"),
           ("vspol", "método híbrido valor + política")]),

 dict(id="a3c", cat="politica", pos=(230, 990, 300, 96),
      corto="A3C (Asynchronous Advantage Actor-Critic)", mapsub="actor-crítico con workers asíncronos",
      titulo="A3C — Asynchronous Advantage Actor-Critic",
      sub="Actor-crítico entrenado por muchos trabajadores en paralelo",
      defn="<b>A3C</b> (Mnih et al., DeepMind, 2016) lanza varios <b>workers asíncronos</b>. Cada uno tiene una copia local de la red y su propio entorno, "
           "calcula gradientes con su experiencia y los aplica a una <b>red global compartida</b> <b>sin esperar</b> a los demás.",
      bullets=[
        "<b>Decorrelación sin replay buffer:</b> como cada worker explora situaciones distintas, los datos son diversos sin necesidad de guardar experiencia.",
        "<b>Eficiente en CPU multinúcleo;</b> no requiere GPU. Entrenó bien juegos Atari en menos tiempo que DQN.",
        "<b>Ciclo de cada worker:</b> copiar parámetros globales → jugar n pasos → calcular gradientes con ventajas → enviarlos a la red global.",
        "<b>Es on-policy,</b> usa retornos de n pasos y suele agregar entropía para fomentar la exploración.",
        "<b>A2C vs A3C:</b> A2C es la versión síncrona; en la práctica, con GPU, A2C suele rendir igual o mejor y es más fácil de reproducir.",
      ],
      tabla=dict(titulo="A2C vs A3C",
        header=["", "A2C", "A3C"],
        rows=[
          ["<b>Actualización</b>", "Síncrona: espera a todos los workers", "Asíncrona: cada worker actualiza cuando termina"],
          ["<b>Parámetros</b>", "Una sola red, un solo update por lote", "Red global + copias locales"],
          ["<b>Hardware ideal</b>", "GPU (lotes grandes)", "CPU multinúcleo"],
          ["<b>Reproducibilidad</b>", "Alta (determinista)", "Menor (orden de actualización variable)"],
          ["<b>Política</b>", "On-policy", "On-policy"],
        ], widths=[0.22, 0.39, 0.39]),
      formulas=[
        ("Retorno de n pasos", "R<sub>t</sub> = Σ<sub>i=0</sub><super>n−1</super> γ<super>i</super> r<sub>t+i</sub> + γ<super>n</super> V(s<sub>t+n</sub>)"),
        ("Ventaja", "A<sub>t</sub> = R<sub>t</sub> − V(s<sub>t</sub>)"),
        ("Gradiente por worker", "dθ ← dθ + ∇<sub>θ</sub> log π<sub>θ</sub>(a<sub>t</sub>|s<sub>t</sub>) · A<sub>t</sub>"),
      ],
      ejemplo="<b>Equipo de exploradores.</b> Varios exploradores recorren partes distintas de un territorio y cada uno actualiza un mapa común "
              "apenas descubre algo útil, sin esperar a los otros. El mapa mejora más rápido que con un solo explorador.",
      rel=[("a2c", "su versión síncrona"), ("pg", "heredan el gradiente de la política"),
           ("onoff", "es on-policy"), ("dqn", "otra vía de estabilizar el aprendizaje profundo")]),
]

# Cuadro comparativo final
COMPARATIVO = dict(
    titulo="Cuadro comparativo de algoritmos",
    sub="Resumen para integrar los contenidos",
    header=["Algoritmo", "Familia", "Política", "Qué aprende", "Regla de actualización (resumen)", "Acciones", "¿Modelo?"],
    widths=[0.11, 0.12, 0.10, 0.12, 0.35, 0.12, 0.08],
    rows=[
      ["<b>Prog. dinámica</b>", "Valor (planificación)", "—", "V*, Q*, π*", "V(s) ← max<sub>a</sub> Σ P(s'|s,a)[ r + γ V(s') ]", "Discretas", "Sí"],
      ["<b>Monte Carlo</b>", "Valor", "On / off (con IS)", "V<super>π</super>, Q<super>π</super>", "V(s) ← V(s) + α [ G<sub>t</sub> − V(s) ]", "Discretas", "No"],
      ["<b>TD(0)</b>", "Valor", "On / off", "V<super>π</super>", "V(s) ← V(s) + α [ r + γ V(s') − V(s) ]", "Discretas", "No"],
      ["<b>SARSA</b>", "Valor", "On-policy", "Q<super>π</super> → Q*", "Q(s,a) ← Q(s,a) + α [ r + γ Q(s',a') − Q(s,a) ]", "Discretas", "No"],
      ["<b>Q-Learning</b>", "Valor", "Off-policy", "Q*", "Q(s,a) ← Q(s,a) + α [ r + γ max Q(s',·) − Q(s,a) ]", "Discretas", "No"],
      ["<b>DQN</b>", "Valor (profundo)", "Off-policy", "Q(s,a;θ) con red", "min ( r + γ max Q(s',·;θ<super>−</super>) − Q(s,a;θ) )² con replay y red objetivo", "Discretas", "No"],
      ["<b>REINFORCE</b>", "Política", "On-policy", "π<sub>θ</sub>", "θ ← θ + α G<sub>t</sub> ∇ log π<sub>θ</sub>(a|s)", "Disc. y cont.", "No"],
      ["<b>A2C</b>", "Híbrido actor-crítico", "On-policy", "π<sub>θ</sub> y V<sub>w</sub>", "θ ← θ + α A ∇ log π<sub>θ</sub>;  A = r + γ V(s') − V(s);  síncrono", "Disc. y cont.", "No"],
      ["<b>A3C</b>", "Híbrido actor-crítico", "On-policy", "π<sub>θ</sub> y V<sub>w</sub>", "Igual que A2C pero con workers asíncronos sobre una red global", "Disc. y cont.", "No"],
    ],
    claves=[
      ("¿Tengo el modelo del entorno?", "Sí → programación dinámica. No → Monte Carlo, TD y derivados."),
      ("¿Episodios cortos, o tareas continuas?", "Episodios: MC o TD. Continuas: TD."),
      ("¿Acciones discretas o continuas?", "Discretas: SARSA, Q-Learning, DQN. Continuas: métodos de política (REINFORCE, A2C/A3C)."),
      ("¿Estados enormes (imágenes)?", "Aproximar con redes: DQN (valor) o A2C/A3C (política + valor)."),
      ("¿Quiero reutilizar experiencia?", "Off-policy: Q-Learning, DQN. Si no, on-policy: SARSA, REINFORCE, A2C/A3C."),
    ],
)
