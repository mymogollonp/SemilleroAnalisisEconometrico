# Plan de trabajo 2026-2S — Dilan Thomas Tovar Roa
## Proyecto: 202602_02_TimingAdmision · Componente: doble titulación, reingresos, cupos y normativa

**Correo:** ditovarr@unal.edu.co · **Rama:** `ra/dtovar` · **Código:** `Proyectos/202602_02_TimingAdmision/dobletitulacion_normativa/`
**Carpeta Drive:** `SemilleroMicroeconometriaProyectos/202602_02_TimingAdmision/`
**Compañero de proyecto:** Julian Bermudez (composición) · **Supervisión:** Monica Mogollon · **Antecedente:** artículo del profesor Hernando Bayona

---

## ⚠ Reglas de datos e IA (obligatorias)

- **Nunca subas datos del proyecto a ningún agente de IA, chatbot o plataforma agéntica** (ChatGPT, Claude, Gemini, Copilot, Cursor, NotebookLM, etc.). Esto incluye bases, extractos, filas de ejemplo, tablas con microdatos y capturas de pantalla de datos. Usa IA solo con código y con documentos públicos (normativa, papers).
- Si usas un agente de código, debe trabajar **solo dentro de la carpeta del código del proyecto**: nunca debe buscar ni explorar otras carpetas del computador, ni **leer datos** sin autorización manual de la PI/CoPI. Ver [CLAUDE.md](../../CLAUDE.md) y la [Guía de RAs §4](../README.md#4-reglas-del-semestre).

---

## Objetivo del semestre

La política cambió el orden de la admisión: antes se escogía el programa y luego se presentaba el examen; ahora se presenta el examen y luego se escoge. Dilan tiene dos tareas:
1. **Sistematizar la normativa de admisión** en una base de datos: cuándo cambió el *timing*, cuántas rondas de admisión hay por semestre, cómo se asignan los cupos y cómo cambiaron las reglas semestre a semestre.
2. **Describir doble titulación, reingresos y ocupación de cupos** antes y después del cambio. La hipótesis es que, si más estudiantes terminan en un programa que no querían, aumentan la doble titulación, los reingresos y los traslados, y el objetivo de "sillas llenas con gente que quiere estar ahí" no se cumple del todo.

## Entregables finales (16 dic)

1. `Revision_normativa/base_normativa.csv`: normas de admisión de pregrado 2009–2025, una fila por norma y período
2. `Revision_normativa/linea_tiempo_admision.md`: línea de tiempo de las reglas de admisión, incluida la fecha exacta del cambio de *timing*
3. `output/`: series antes y después de doble titulación, reingresos, traslados y ocupación de cupos
4. Documento corto con resultados y preguntas abiertas

---

## Semana 1 (3 – 6 nov) — Arranque

- `[ ]` Firmar el acuerdo de confidencialidad; pedir acceso a GitHub y Drive
- `[ ]` Clonar el repo, crear la rama `ra/dtovar` y el archivo `00_config`; primer commit y push
- `[ ]` Leer la [Introducción](../INTRODUCCION_2026-2S.md) y la [Guía de RAs](../README.md)
- `[ ]` Leer el artículo del profesor Hernando Bayona sobre el cambio en la admisión (pedirlo a Monica) y resumirlo en `Literatura/notas_lectura.md`
- `[ ]` Reunión de 30 min con Julian para **acordar la división del trabajo** y el período de corte antes/después

## Semana 2 (9 – 13 nov) — Normativa: búsqueda y diseño de la base

- `[ ]` Identificar la **norma que cambia el *timing*** (acuerdo del CSU o del Consejo Académico, o resolución de la Dirección Nacional de Admisiones) y el **primer período afectado**
- `[ ]` Diseñar el esquema de `base_normativa.csv` (ver [Guía §7](../README.md#7-literatura-y-normativa)) y agregar columnas propias de admisión: `n_rondas`, `momento_eleccion_programa`, `tipo_examen`, `ponderaciones`, `cupos`
- `[ ]` Descargar normas de admisión de [legal.unal.edu.co](http://www.legal.unal.edu.co) y de la página de Admisiones; guardar los PDFs en `Revision_normativa/pdf/`
- `[ ]` Probar un flujo automático (Python más un LLM, o búsqueda de texto) para extraer fecha, órgano y resumen de cada PDF (solo normativa pública, nunca datos); **verificar a mano una muestra**

## Semana 3 (17 – 20 nov) — Normativa v1 y definiciones

- `[ ]` Completar la base de normativa 2009–2025 y redactar `linea_tiempo_admision.md`
- `[ ]` Definir operacionalmente con los datos:
  - **Doble titulación:** `id_unal` con más de un `cod_plan` de pregrado, simultáneo o secuencial, o código de acceso o subacceso de doble titulación en `BASE_MATRICULADOS`
  - **Reingreso:** `id_unal` que vuelve a matricularse tras uno o más períodos de ausencia, o tras un retiro registrado en `BASE_EGRESADOS_RETIRADOS`
  - **Traslado:** cambio de `cod_plan` sin graduación intermedia
- `[ ]` Revisar los valores de `cod_acceso`, `acceso` y `cod_subacceso`: ¿identifican doble titulación, reingreso o traslado? Pedir a Jeronimo variables adicionales si hace falta

## Semana 4 (23 – 27 nov) — Descriptivas v0 y avance

- `[ ]` Script `01_base_trayectorias_DT`: base estudiante–período con plan, estado y eventos (doble titulación, reingreso, traslado, retiro)
- `[ ]` Series por cohorte de ingreso: % con doble titulación, % con reingreso, % con traslado
- `[ ]` **Presentación corta (10 min)** junto con Julian: línea de tiempo normativa y primeras series

## Semana 5 (30 nov – 4 dic) — Antes y después, y cupos

- `[ ]` Comparar las cohortes antes y después del cambio por facultad y programa; probar ventanas de 2, 4 y 6 semestres alrededor del corte
- `[ ]` **Ocupación de cupos:** N de admitidos o matriculados de primer semestre por programa y período, frente a los cupos de la normativa (si están disponibles). Identificar programas que se quedan con sillas vacías
- `[ ]` Coordinarse con Julian para usar el **mismo corte y las mismas definiciones de cohorte**

## Semana 6 (9 – 11 dic) — Documento y presentación final

- `[ ]` Documento corto con resultados de doble titulación, reingresos, cupos y normativa
- `[ ]` **Presentación final** conjunta con Julian

## Cierre (14 – 16 dic)

- `[ ]` Código reproducible desde `00_config`; `README.md` de la subcarpeta
- `[ ]` **Pull request** de `ra/dtovar` → `Proyectos2026-2S`
- `[ ]` Pendientes para 2027-1S, por ejemplo qué se podría hacer con las listas de admisión cuando estén disponibles

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
