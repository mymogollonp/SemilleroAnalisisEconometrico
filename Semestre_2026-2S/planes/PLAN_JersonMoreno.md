# Plan de trabajo 2026-2S — Jerson Stiven Moreno Blanco
## Proyecto: 202602_01_CambioPlanesCurriculares

**Correo:** jmorenobl@unal.edu.co · **Rama:** `ra/jmoreno` · **Código:** `Proyectos/202602_01_CambioPlanesCurriculares/`
**Carpeta Drive:** `SemilleroMicroeconometriaProyectos/202602_01_CambioPlanesCurriculares/`
**Supervisión:** Monica Mogollon · **Soporte de datos:** Jeronimo Jimenez

---

## ⚠ Reglas de datos e IA (obligatorias)

- **Nunca subas datos del proyecto a ningún agente de IA, chatbot o plataforma agéntica** (ChatGPT, Claude, Gemini, Copilot, Cursor, NotebookLM, etc.). Esto incluye bases, extractos, filas de ejemplo, tablas con microdatos y capturas de pantalla de datos. Usa IA solo con código y con documentos públicos (normativa, papers).
- Si usas un agente de código, debe trabajar **solo dentro de la carpeta del código del proyecto**: nunca debe buscar ni explorar otras carpetas del computador, ni **leer datos** sin autorización manual de la PI/CoPI. Ver [CLAUDE.md](../../CLAUDE.md) y la [Guía de RAs §4](../README.md#4-reglas-del-semestre).

---

## Objetivo del semestre

Documentar **todos los cambios en planes de estudio** de la universidad observables entre 2009 y 2025, en los datos y en la normativa. Hay que **clasificarlos** (créditos, flexibilización, solo nombre o código, otros) y **cuantificar cuántos estudiantes se vieron afectados** por cada tipo de cambio. Este inventario es el insumo para estimar el efecto de los cambios sobre el desempeño, siguiendo a Arteaga (2018).

## Entregables finales (16 dic)

1. `data/catalogo_cambios_planes.csv`: una fila por evento de cambio (plan origen → plan destino, período, tipo de cambio, fuente)
2. `Revision_normativa/base_normativa.csv`: normas que crean, modifican o derogan planes de estudio
3. `output/`: tablas de estudiantes afectados por tipo de cambio, facultad y cohorte
4. `Literatura/notas_lectura.md`: Arteaga (2018) y al menos 4 referencias más
5. Documento corto (5–8 páginas) con resultados y una propuesta de estrategia de identificación

---

## Semana 1 (3 – 6 nov) — Arranque

- `[x]` Firmar el acuerdo de confidencialidad; pedir acceso a GitHub y Drive
- `[x]` Clonar el repo, crear la rama `ra/jmoreno` y el archivo `00_config`; primer commit y push
- `[x]` Leer la [Introducción](../INTRODUCCION_2026-2S.md) y la [Guía de RAs](../README.md)
- `[-]` Leer **Arteaga (2018)**, *J. Public Economics* 157: 212–225, y resumirlo en `Literatura/notas_lectura.md`: reforma, datos, método, resultados
- `[ ]` Revisar con Monica el documento de proyecto ya formulado (revisión de literatura de la convocatoria) y anotar preguntas
- `[-]` Explorar `BASE_MATRICULADOS.csv`: N por período; valores de `cod_plan`, `cod_programa`, `facultad` y `tipo_nivel`

## Semana 2 (9 – 13 nov) — Identificar cambios en los datos

- `[ ]` Script `01_historia_planes_JM`: construir la tabla `cod_plan × período` (primer y último período observado, N estudiantes, programa, facultad)
- `[ ]` Identificar **planes que aparecen o desaparecen** y **programas con más de un `cod_plan`** a lo largo del tiempo
- `[ ]` Identificar **estudiantes que cambian de `cod_plan`** dentro del mismo `cod_programa`. Esa transición es la "huella" de un cambio de plan
- `[ ]` Revisar qué se avanzó antes sobre la FCE: preguntar a Monica por los cambios ya conocidos de la Facultad
- `[ ]` Normativa: localizar en [legal.unal.edu.co](http://www.legal.unal.edu.co) los acuerdos de **Consejo Académico y Consejos de Facultad** que aprueban o modifican planes; empezar con la FCE

## Semana 3 (17 – 20 nov) — Catálogo de cambios v0

- `[ ]` Construir `catalogo_cambios_planes.csv` v0 con los eventos detectados en los datos
- `[ ]` Para cada evento, comparar créditos por tipología antes y después usando `BASE_CURSADAS` (créditos cursados por tipología de los graduados de cada plan)
- `[ ]` Proponer **reglas de clasificación**: (a) cambio en créditos totales; (b) cambio en la composición obligatoria/optativa (flexibilización); (c) solo código o nombre; (d) otro
- `[ ]` Ampliar la base de normativa a todas las facultades de Bogotá; usar extracción de texto o LLM para resumir los acuerdos (solo documentos públicos, nunca datos)
- `[ ]` Si se necesitan créditos requeridos por plan (`creditos_requeridos_plan`, que no está en las bases), **pedirlos a Jeronimo**

## Semana 4 (23 – 27 nov) — Avance de mitad de camino

- `[ ]` Cruzar el catálogo de datos con la base de normativa: ¿cada cambio observado tiene norma? ¿cada norma se ve en los datos?
- `[ ]` Clasificar todos los eventos con las reglas acordadas
- `[ ]` **Presentación corta (10 min)** en la reunión: cuántos cambios hay, de qué tipo y en qué facultades

## Semana 5 (30 nov – 4 dic) — Estudiantes afectados

- `[ ]` Script `03_afectados_JM`: para cada evento, contar estudiantes **expuestos** (matriculados en el plan al momento del cambio) y **cohortes antes y después**
- `[ ]` Tablas por tipo de cambio × facultad × nivel; comparar graduación, PAPA y créditos de las cohortes antes y después (descriptivo)
- `[ ]` Identificar los 2–3 cambios más "limpios" para una evaluación de impacto (cambio grande, fecha precisa, cohortes comparables)

## Semana 6 (9 – 11 dic) — Documento y presentación final

- `[ ]` Redactar el documento corto: motivación, datos, catálogo, estadísticas y propuesta de identificación (regresión discontinua por cohorte o diferencias en diferencias)
- `[ ]` **Presentación final** en la reunión

## Cierre (14 – 16 dic)

- `[ ]` Revisar que todo el código corra de principio a fin desde `00_config`
- `[ ]` Abrir **pull request** de `ra/jmoreno` → `Proyectos2026-2S`
- `[ ]` Escribir `Proyectos/202602_01_CambioPlanesCurriculares/README.md`: qué hace cada script, en qué orden se corren y qué outputs produce
- `[ ]` Lista de pendientes para 2027-1S

---

## Bitácora

| Semana | Avances | Problemas o bloqueos | Horas |
|---|---|---|---|
| S1 | | | |
| S2 | | | |
| S3 | | | |
| S4 | | | |
| S5 | | | |
| S6 | | | |

## Solicitudes de datos a Jeronimo

| Fecha | Variable(s) | Estado |
|---|---|---|
| | | |
