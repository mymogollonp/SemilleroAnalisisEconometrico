# Plan de trabajo 2026-2S — Manuela Carrillo Castro
## Proyecto: 202602_03_ModalidadTrabajoGrado

**Correo:** mcarrilloca@unal.edu.co · **Rama:** `ra/mcarrillo` · **Código:** `Proyectos/202602_03_ModalidadTrabajoGrado/`
**Carpeta Drive:** `SemilleroMicroeconometriaProyectos/202602_03_ModalidadTrabajoGrado/`
**Supervisión:** Monica Mogollon · **Soporte de datos:** Jeronimo Jimenez (y Nicolas Jimenez, que conoce la base de Egresados)

---

## ⚠ Reglas de datos e IA (obligatorias)

- **Nunca subas datos del proyecto a ningún agente de IA, chatbot o plataforma agéntica** (ChatGPT, Claude, Gemini, Copilot, Cursor, NotebookLM, etc.). Esto incluye bases, extractos, filas de ejemplo, tablas con microdatos y capturas de pantalla de datos. Usa IA solo con código y con documentos públicos (normativa, papers).
- Si usas un agente de código, debe trabajar **solo dentro de la carpeta del código del proyecto**: nunca debe buscar ni explorar otras carpetas del computador, ni **leer datos** sin autorización manual de la PI/CoPI. Ver [CLAUDE.md](../../CLAUDE.md) y la [Guía de RAs §4](../README.md#4-reglas-del-semestre).

---

## Objetivo del semestre

Describir **cómo se distribuyen los estudiantes por modalidad de trabajo de grado** (pasantía, trabajo investigativo o monografía, asignaturas de posgrado, otras) y **cómo les fue en términos académicos**: tiempo hasta el grado, PAPA, créditos y continuación a posgrado. Antes de seguir con el proyecto hay que verificar si existe variación suficiente; en la FCE, por ejemplo, casi nadie hace monografía. Además, revisar la **normativa sobre modalidades y criterios de selección** por facultad.

## Entregables finales (16 dic)

1. `data/base_modalidad_grado.csv`: una fila por egresado de pregrado con modalidad, facultad, cohorte y resultados académicos
2. `output/`: tablas y gráficas de la distribución de modalidades por facultad y período, y de los resultados por modalidad
3. `Revision_normativa/base_normativa.csv`: normas generales y de facultad sobre modalidades de trabajo de grado y requisitos de acceso
4. Documento corto con resultados y viabilidad del proyecto

---

## Semana 1 (3 – 6 nov) — Arranque y solicitud de datos

- `[ ]` Firmar el acuerdo de confidencialidad; pedir acceso a GitHub y Drive
- `[ ]` Clonar el repo, crear la rama `ra/mcarrillo` y el archivo `00_config`; primer commit y push
- `[ ]` Leer la [Introducción](../INTRODUCCION_2026-2S.md) y la [Guía de RAs](../README.md)
- `[ ]` **Solicitar a Jeronimo** (issue `solicitud-datos`) la variable de **trabajo de grado o modalidad** de los datos armonizados de Egresados, anonimizada por `id_unal`. Nicolas confirmó que existe en los datos armonizados pero no en las bases finales
- `[ ]` Buscar literatura sobre modalidades de grado, tesis de pregrado y resultados (posgrado, mercado laboral) y empezar `Literatura/notas_lectura.md`

## Semana 2 (9 – 13 nov) — Explorar las fuentes de modalidad

- `[ ]` Explorar `BASE_CURSADAS`: la variable `creditos_cursados_periodo_trabajo_de_grado` y los créditos de posgrado o `tesis` pueden indicar la modalidad
- `[ ]` Cuando llegue la variable de Egresados: tabular sus valores únicos y proponer un **mapeo a categorías canónicas** (pasantía, trabajo investigativo, asignaturas de posgrado, emprendimiento, otra)
- `[ ]` Normativa general: ubicar el acuerdo del Consejo Académico que reglamenta las modalidades de trabajo de grado en pregrado (verificar si es el Acuerdo 026 de 2012 del Consejo Académico y sus modificaciones) en [legal.unal.edu.co](http://www.legal.unal.edu.co)

## Semana 3 (17 – 20 nov) — Base de modalidad v0

- `[ ]` Script `01_base_modalidad_MC`: unir egresados (`BASE_EGRESADOS_RETIRADOS`, `graduado == 1`) con la modalidad, `BASE_MATRICULADOS` (facultad, cohorte, características) y `BASE_CURSADAS` (PAPA y créditos acumulados)
- `[ ]` Calcular la **duración hasta el grado** (períodos entre el ingreso y el grado)
- `[ ]` Primera tabla: distribución de modalidades por facultad y por año de grado
- `[ ]` Normativa por facultad: requisitos para cada modalidad (PAPA mínimo, avance en créditos, cupos de pasantía, aval de tutor)

## Semana 4 (23 – 27 nov) — Avance de mitad de camino

- `[ ]` Evaluar la **variación disponible**: ¿en qué facultades o programas hay suficientes estudiantes en cada modalidad?
- `[ ]` **Presentación corta (10 min):** distribución de modalidades y viabilidad

## Semana 5 (30 nov – 4 dic) — Resultados por modalidad

- `[ ]` Comparar por modalidad: PAPA de grado, duración, créditos y características de entrada (PBM, puntaje de admisión, sexo). Distinguir **selección** de resultado, porque los mejores estudiantes pueden escoger monografía
- `[ ]` **Continuación a posgrado:** identificar egresados de pregrado que luego aparecen matriculados en un plan de posgrado (`tipo_nivel`) y comparar por modalidad
- `[ ]` Complementar la base de normativa con los criterios de selección por facultad

## Semana 6 (9 – 11 dic) — Documento y presentación final

- `[ ]` Documento corto: datos, distribución, resultados descriptivos, normativa y viabilidad o propuesta de identificación
- `[ ]` **Presentación final**

## Cierre (14 – 16 dic)

- `[ ]` Código reproducible desde `00_config`; `README.md` del proyecto
- `[ ]` **Pull request** de `ra/mcarrillo` → `Proyectos2026-2S`
- `[ ]` Pendientes para 2027-1S

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
| | Modalidad / trabajo de grado (Egresados armonizados) | |
