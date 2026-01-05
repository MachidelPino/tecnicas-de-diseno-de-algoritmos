# TDA — Aprendizajes y estrategia (mi recorrido técnico)

> Este documento es un destilado **práctico** de Técnicas de Diseño de Algoritmos (TDA): qué tipos de problemas aparecen, cómo aprendí a encararlos, en qué me equivocaba y qué heurísticas me destrabaron.  
> **No es** un apunte teórico completo. **Sí es** una guía de razonamiento y ejecución: **modelado → técnica → correctitud → complejidad → (si aplica) reconstrucción**.

---

## 1) Qué evalúa realmente TDA

Con el tiempo entendí que TDA no premia “saber algoritmos sueltos”, sino poder sostener un ciclo consistente:

1. **Modelar**: convertir el enunciado en un objeto manipulable (subproblemas, estados, grafo/DAG, red de flujo, etc.).
2. **Elegir técnica por propiedad**, no por costumbre: “¿qué estructura me habilita un argumento de correctitud?”
3. **Definir con precisión** qué calcula mi algoritmo (semántica del estado / subproblema / objeto).
4. **Probar correctitud** con una idea que cierre (invariante, inducción, intercambio, ⇔, etc.).
5. **Analizar complejidad** de forma honesta: estructura + implementación + costo real de operaciones.
6. **Reconstruir** si lo piden: no solo el valor óptimo, también “cómo llego”.

Mi cambio más grande fue dejar de pensar “¿qué algoritmo me acuerdo?” y pasar a pensar:
**“¿qué propiedad del problema me habilita una técnica que puedo justificar?”**

---

## 2) Cómo reconozco el molde del problema

Aprender a “oler el molde” valió más que memorizar.

### 2.1 Antes de elegir técnica: qué tipo de salida pide
Esta clasificación me ordena el modelado:

- **Decisión**: “¿existe solución?”
- **Construcción**: “devolveme una solución”
- **Optimización**: “mejor valor” (min/max)
- **Conteo**: “cuántas soluciones”

La técnica suele caer del cruce **(tipo de salida) + (estructura)**.

### 2.2 Moldes típicos (paradigmas)
**Secuencias / arreglos**
- subsecuencias, intervalos, particiones, costos por orden
- *señal*: hay un orden natural (índices) y decisiones “hacia adelante”

**Subconjuntos / combinatoria**
- elegir/no elegir, restricciones acumulativas, conteo de configuraciones
- *señal*: explosión combinatoria por decisiones binarias repetidas

**Grillas / caminos con restricciones**
- coordenadas + transición local + condición (vida, mod, etc.)
- *señal*: estado = (posición, recurso, “modo”)

**Scheduling / selección**
- “orden importa” o “costo depende del orden”
- *señal*: aparece una regla local plausible o una estructura tipo “merge óptimo”

### 2.3 Moldes típicos (grafos)
**Recorridos (BFS/DFS)**
- componentes, ciclos, bipartito, puentes/articulaciones, “distancia en #aristas”
- *huele a*: extraer estructura, no optimizar pesos

**AGM (Prim/Kruskal)**
- “conectar todo con costo mínimo”, “infraestructura mínima”, “subred barata”
- *huele a*: elegir aristas sin ciclos (propiedades de corte/ciclo)

**Camino mínimo (BFS/Dijkstra/Bellman-Ford)**
- “ruta óptima”, “menor costo/tiempo”
- *señal*: pesos no negativos → Dijkstra; negativos → Bellman-Ford; todos iguales → BFS

**DAG + DP (orden topológico)**
- dependencias, prerrequisitos, “solo depende de anteriores”, “no puedo volver atrás”
- *huele a*: DP sobre un orden (transición segura)

**Flujo**
- asignaciones con restricciones, matching, capacidades, caminos disjuntos
- *huele a*: “pasar unidades” respetando límites (capacidad + conservación)

---

## 3) Mi evolución (técnica y verificable)

### Etapa 1: cuando todavía “adivinaba” técnicas
- Veía recursión y asumía **Divide & Conquer** aunque hubiera superposición.
- En DP escribía recurrencias que “parecían” funcionar, pero **sin semántica del estado**.
- Cuando algo no cerraba, intentaba “arreglarlo agregando parámetros” (estado inmanejable).
- En greedy proponía reglas razonables, pero **sin prueba** o con pruebas circulares.
- En correctitud mezclaba intuición con afirmaciones sin justificar.

**Lo que me destrabó**: obligarme a escribir la semántica en una frase y a elegir una plantilla de prueba.

### Etapa 2: cuando el mismo pipeline se volvió general (y me sostuvo en grafos/flujo)
- Dejé de saltar al algoritmo (“esto parece Dijkstra”) y pasé a preguntar:
  **¿qué estoy optimizando? ¿qué condición garantiza que aplica?**
- Empecé a justificar representación/operaciones (listas vs matriz, heap, etc.).
- En modelados “lindos” (especialmente flujo) dejé de conformarme con el dibujo:
  ahora cierro con la doble implicación **solución válida ⇔ flujo/modelo válido**.
- En demostraciones, pasé de párrafos largos a **1–3 lemas cortos** con objetos nombrados.

---

## 4) Pipeline universal para resolver (y para escribir la solución)

Este es mi checklist estable, independientemente del tema:

1. **Objetos**: ¿cuáles son las entidades? (índices, estados, vértices/aristas, capas, unidades)
2. **Salida exacta**: decisión / construcción / optimización / conteo
3. **Propiedad clave** que “regala” el enunciado:
   - aciclicidad, pesos no negativos, capacidad, bipartición, monotonicidad, etc.
4. **Técnica candidata** + **qué invariante/argumento** la sostiene
5. **Definición formal**:
   - DP: semántica de `f(...)`
   - grafo: qué es vértice/arista/peso/capacidad
6. **Correctitud** en lemas chicos (no “parece obvio”)
7. **Complejidad**:
   - DP: `#estados × costo(transición)`
   - grafos: en función de `n=|V|`, `m=|E|` + estructura de datos
8. **Reconstrucción** si aplica: qué guardo (padre/decisión) y cómo leo la solución

**Plantilla de entrega** (casi siempre):
- **Modelo**
- **Algoritmo**
- **Correctitud**
- **Complejidad**
- **Reconstrucción** (si aplica)

---

## 5) Toolbox: lo mínimo que necesito recordar (y por qué funciona)

### 5.1 Divide & Conquer (D&C)
**Idea**: partir en subproblemas *independientes* y combinar.

**Chequeos que ahora hago**
- ¿Hay superposición fuerte de subproblemas? → entonces no es D&C “puro”: pensar DP.
- ¿La recurrencia refleja el algoritmo real? (tamaños + costo de combinar)
- Teorema Maestro solo si la forma es `T(n)=aT(n/c)+f(n)` *y sé qué significan `a,c,f`*.

### 5.2 Backtracking (BT) + podas
**Estructura que siempre escribo**
1. qué es una **solución candidata** (hoja)
2. qué es una **solución parcial** (nodo)
3. cómo genero **sucesores**
4. **podas**:
   - factibilidad: ya es imposible completar
   - optimalidad (branch & bound): aun completando perfecto no supero lo mejor

**Error que dejé atrás**: podar “por intuición”.  
Ahora, toda poda que mata ramas debe ser **segura** (no corta soluciones válidas).

### 5.3 Programación Dinámica (DP): mi regla de oro
> Si no puedo explicar `f(...)` en una frase precisa, el estado está mal.

**Receta que me funciona**
1. estado con semántica (qué representa)
2. transición como “primera decisión + subproblema”
3. casos base coherentes con la semántica
4. memoización o tabla
5. complejidad como `#estados × transición`

**Error clásico mío**: “agrego un parámetro más y sale”.  
Ahora lo tomo como síntoma de:
- semántica incorrecta, o
- parámetro redundante, o
- dos problemas mezclados en un solo DP.

### 5.4 Bottom-up + reconstrucción
**Bottom-up** = orden de cómputo donde dependencias ya están listas.

**Reconstrucción** (lo que antes subestimaba)
- guardar `choice[state]` o `parent[state]`
- o reconstruir comparando valores si la transición lo permite sin ambigüedad

**Memoria**
- si depende de “fila anterior” puedo comprimir
- si necesito reconstrucción, el tradeoff es real: más memoria vs más recomputación

### 5.5 Greedy: proponer es fácil, probar es el trabajo
**Señales de que puede haber greedy**
- orden natural claro
- la decisión “no se arrepiente” (monotonicidad)
- puedo describir un intercambio local

**Dos plantillas que uso (y no improviso)**
- **Stays ahead**: paso a paso, mi solución no va peor según una métrica explícita.
- **Intercambio**: tomo una óptima cualquiera y la transformo para que empiece con la elección greedy sin empeorar.

**Error que dejé**: “funciona en ejemplos”.  
Ahora, si no tengo plantilla, asumo que **no está demostrado**.

---

## 6) Grafos: el kit que realmente uso (con criterios, no recetas)

### 6.1 Representación: elegir bien te ahorra todo lo demás
La pregunta no es “cómo se representa”, sino **qué operaciones** necesito.

- iterar vecinos muchas veces → **lista de adyacencia** (casi siempre)
- consultar arista en O(1) → matriz (caro en memoria)

Aprendí a justificarlo en la complejidad: recorrer vecinos en lista suma `O(n+m)`.

### 6.2 BFS/DFS: “extractores” de estructura
- **BFS**:
  - distancias en cantidad de aristas
  - árbol geodésico y capas (paridad/bipartición cuando aplica)
- **DFS**:
  - estructura padre/hijo, ancestros
  - back edges (ciclos)
  - base para puentes/articulaciones y clasificaciones

Mi chequeo rápido:
**¿la distancia mide #aristas o pesos?**  
Ese filtro me evitó forzar BFS donde no corresponde.

### 6.3 AGM (Prim/Kruskal): conectar barato ≠ caminos baratos
Para mí, AGM dejó de ser “un algoritmo” y pasó a ser una propiedad:

- objetivo: **conectar** minimizando **suma de costos** → suena a AGM
- “subred barata” suele esconder lo mismo

Punto clave que internalicé:
- un AGM **no** garantiza caminos mínimos entre pares

### 6.4 Caminos mínimos: cuándo aplica cada uno (y por qué)
Mi checklist:

- **BFS**: todas las aristas equivalen (mismo costo) → distancia en #aristas
- **Dijkstra**: pesos **no negativos**
- **Bellman-Ford**: admite negativos y detecta ciclos negativos alcanzables

Lo importante para mí fue entender la condición como **invariante**:
en Dijkstra, “lo que sale de la PQ queda fijo” se rompe si un negativo puede mejorar tarde.

### 6.5 DAG + DP: el atajo cuando lo detecto
Cuando hay aciclicidad, muchas cosas se vuelven limpias:
- camino mínimo/máximo en DAG con DP sobre orden topológico
- conteo de caminos, dependencias

Me entrené a detectar DAG aunque no lo digan:
dependencias, “solo depende de anteriores”, “no hay vuelta atrás”, o aciclicidad por construcción.

### 6.6 Flujo: modelar restricciones como capacidades (sin autoengañarme)
Frase que me ordenó todo:

> Un buen modelo de flujo es uno donde **una unidad de flujo tiene significado**, y **cada restricción del enunciado aparece como capacidad/conservación**.

Dos moldes recurrentes:
- **Asignación / matching**: a lo sumo uno ↔ capacidad 1; a lo sumo C ↔ capacidad C
- **Caminos disjuntos**: capacidad 1 por arista ↔ no repetir arista (cada unidad es un camino)

Lo que me cambió la vida fue exigir el cierre formal:
- **solución válida ⇒ construyo un flujo**
- **flujo ⇒ leo una solución válida**

Sin ese ⇔, el modelo queda “lindo” pero no probado.

---

## 7) Correctitud: cómo aprendí a escribir demostraciones que cierran

### 7.1 Estructura mínima que sigo
1. qué pruebo
2. definiciones (estado, óptimo, alcanzable, etc.)
3. técnica elegida (inducción / invariante / intercambio / ⇔)
4. cierre explícito (por qué eso implica lo pedido)

### 7.2 Mis tres mejoras más concretas
- **Dejar de buscar “la idea mágica”**: primero formalizo y elijo técnica por forma.
- **Nombrar objetos**: “sea i el primer índice donde difieren…”, “sea e la arista máxima…”.
  Esto convierte narración en verificación.
- **Convertir frases puente en lemas**:
  “si saco esta arista el árbol se parte”, “el orden topológico habilita la transición”, etc.

### 7.3 Plantillas que más uso
- **Inducción** sobre una medida bien definida (tamaño/índice/nivel/cantidad restante)
- **Invariante** (recorridos, relajación, estructuras mantenidas)
- **Intercambio / stays-ahead** (greedy)
- **⇔** (modelados: flujo/asignación, transformaciones de problema)

---

## 8) Checklist de autopsia (cuando algo no cierra)

### 8.1 Modelado
- ¿definí bien vértices/aristas/estados?
- ¿peso/costo/capacidad significan lo correcto?
- ¿me faltó una restricción escondida en una frase?
- ¿estoy optimizando exactamente lo que piden?

### 8.2 Elección de técnica
- ¿estoy usando un algoritmo que requiere una condición que no tengo?
  - Dijkstra con negativos
  - BFS con pesos distintos
  - DP sin orden/aciclicidad cuando hace falta
  - flujo sin semántica de unidad

### 8.3 Correctitud
- ¿enuncié el invariante o el lema clave?
- ¿si corresponde, probé ambas direcciones (⇔)?
- ¿mi argumento depende de “claramente” más de una vez?

### 8.4 Complejidad
- ¿depende de la representación elegida?
- ¿cuento operaciones reales (push/pop heap, recorrer vecinos, construir grafo auxiliar)?
- ¿la cota es compatible con los límites del enunciado?

### 8.5 Reconstrucción
- ¿guardé decisión/padre o solo el valor?
- ¿qué pasa con empates? ¿definí criterio?

**Red flags que ahora tomo en serio**
- “no sé explicar qué significa mi estado”
- “agrego un parámetro y sigo sin cerrar”
- “solo tengo ejemplos para la prueba”
- “la complejidad me da algo absurdo para los límites”

---

## 9) Estrategia de parcial (en modo productivo)

### 9.1 Triage
1. barrido rápido: clasificar por molde (DP/BT/D&C/greedy/grafos/flujo)
2. asegurar puntos: resolver primero lo que tenga pipeline claro
3. volver a lo difícil con la cabeza ya “caliente”

### 9.2 Cómo escribo para que corrijan rápido
- semántica del estado/modelo en **una línea**
- algoritmo en pasos + estructura de datos
- correctitud en 1–3 lemas/invariante
- complejidad cerrada
- reconstrucción si aplica (qué guardo y cómo leo)

### 9.3 Plan B para sumar sin completar
Si no llego al final, intento dejar:
- **modelo correcto** (aunque falten detalles)
- transición principal / idea del algoritmo
- casos base (si DP) o invariante (si grafo)
- complejidad razonable

Eso suele rendir más que mucho pseudocódigo sin semántica.

---

## 10) Qué habilidades reales me dejó TDA

- **Modelar bajo presión**: texto → estructura formal
- **Elegir técnicas por invariantes** (y saber cuándo NO aplican)
- **Demostrar sin humo**: objetos nombrados, lemas cortos, cierre claro
- **Complejidad honesta**: operaciones reales + costo de construir estructuras auxiliares
- **Reconstrucción**: no solo “cuánto vale” sino “cómo llego”
- **Debug de ideas**: sé dónde mirar cuando algo no cierra (modelo / técnica / invariante / cota)

Si tuviera que resumir mi cambio en una frase:

> Pasé de intentar *adivinar el algoritmo* a construirlo desde una definición precisa de qué estoy calculando, qué propiedad lo justifica y cómo se prueba.
