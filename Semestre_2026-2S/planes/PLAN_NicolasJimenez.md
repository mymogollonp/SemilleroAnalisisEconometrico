# Plan de trabajo 2026-2S — Nicolas Jimenez Castaneda
## Proyecto: 202602_04_AdmisionPandemia

**Correo:** nijimenezca@unal.edu.co · **Rama:** `ra/njimenez` · **Código:** `Proyectos/202602_04_AdmisionPandemia/`
**Carpeta Drive:** `SemilleroMicroeconometriaProyectos/202602_04_AdmisionPandemia/`
**Supervisión:** Monica Mogollon y Karoll Gomez · **Coordinación:** Karen Daniela Castillo (trabajo de grado en este proyecto)
**Rol transversal:** coadministrador del repositorio de datos (acceso completo, junto con Jeronimo)

---

## ⚠ Reglas de datos e IA (obligatorias)

- **Nunca subas datos del proyecto a ningún agente de IA, chatbot o plataforma agéntica** (ChatGPT, Claude, Gemini, Copilot, Cursor, NotebookLM, etc.). Esto incluye bases, extractos, filas de ejemplo, tablas con microdatos y capturas de pantalla de datos. Usa IA solo con código y con documentos públicos (normativa, papers). El prototipo de dashboard no debe usar servicios de IA sobre los datos.
- Si usas un agente de código, debe trabajar **solo dentro de la carpeta del código del proyecto**: nunca debe buscar ni explorar otras carpetas del computador, ni **leer datos** sin autorización manual de la PI/CoPI. Ver [CLAUDE.md](../../CLAUDE.md) y la [Guía de RAs §4](../README.md#4-reglas-del-semestre).

---

## Objetivo del semestre

Durante el COVID la UNAL suspendió su examen de admisión y admitió con base en el **Saber 11 (ICFES)**. Nicolas debe:
1. **Construir la base de trabajo del proyecto**, que identifica a los admitidos por examen UNAL y por Saber 11.
2. **Describir la composición** (sexo, estrato, PBM, tipo de colegio, territorio) y los **resultados académicos** (PAPA, créditos, retiro, permanencia) de ambos grupos.
3. **Definir con rigor los indicadores** que la profesora Karoll necesita para su **dashboard** y dejar un prototipo.

La pregunta de fondo es si el examen propio funciona como barrera de entrada y qué tan bien predice el desempeño (validez predictiva). Esto es insumo para la evaluación de impacto del proyecto más amplio de Karoll: efectos de largo plazo sobre deserción y trayectoria.

## Entregables finales (16 dic)

1. `data/base_admision_pandemia.csv`: cohortes de ingreso con el mecanismo de admisión, composición y resultados
2. `Revision_normativa/base_normativa.csv`: normas de admisión durante la pandemia (períodos, instrumento, ponderaciones)
3. `Semestre_2026-2S/definiciones_indicadores_dashboard.md`: catálogo de indicadores con definición, fórmula, fuente y desagregaciones
4. Prototipo de dashboard con los indicadores principales
5. Documento corto con descriptivas de composición y desempeño por mecanismo de admisión

---

## Semana 1 (3 – 6 nov) — Arranque

- `[ ]` **Revisar el incidente de seguridad** en [logs/INCIDENTE_llave_id_unal_en_git.md](../../logs/INCIDENTE_llave_id_unal_en_git.md): la llave `LLAVE_ID_UNAL_FCE.csv` se subió a GitHub en el commit `be11291` (2026-06-01) desde tu usuario. Con Jeronimo:
  - `[ ]` Explicar cómo ocurrió (qué comando, desde qué carpeta) y registrarlo en la nota del incidente
  - `[ ]` Revisar tus commits anteriores para confirmar que no se subió ningún otro archivo de datos
  - `[ ]` Revisar que la copia de la llave en tu computador esté solo en `DatosArmonizados/keys/` en Drive
  - `[ ]` Después de la purga del historial, borrar tu clon local y volver a clonar el repositorio

- `[ ]` Recibir de Monica la propuesta y la estructura del proyecto de Karoll y leerlas
- `[ ]` Crear la rama `ra/njimenez` y el `00_config` del proyecto; primer commit y push
- `[ ]` Reunión con Karen Daniela para **repartir tareas** entre su trabajo de grado y este plan, y no duplicar esfuerzos
- `[ ]` Confirmar con Karoll el estado del proyecto de **nivelación** (en espera mientras llegan datos más granulares) y cuánto tiempo se le dedica este semestre

## Semana 2 (9 – 13 nov) — Normativa y períodos afectados

- `[ ]` Identificar con la normativa **qué períodos de admisión usaron Saber 11** en lugar del examen UNAL y en qué condiciones (ponderaciones, pruebas, programas especiales)
- `[ ]` Verificar si `convocatoria`, `cod_acceso` o `puntaje_admision` en `BASE_MATRICULADOS` permiten identificar el **mecanismo de admisión** de cada estudiante; si no, pedir la variable (como administrador, documentar la extracción en el log de solicitudes)
- `[ ]` Revisar con Julian las funciones de **indicadores de composición** para usar las mismas definiciones

## Semana 3 (17 – 20 nov) — Base de trabajo v0

- `[ ]` Script `01_base_admision_pandemia_NJ`: cohortes de ingreso a pregrado alrededor de la pandemia (por ejemplo 2018–2023), con el mecanismo de admisión, características de entrada y resultados en los 1, 2 y 4 primeros semestres (PAPA, créditos aprobados, retiro)
- `[ ]` Primer borrador de `definiciones_indicadores_dashboard.md`: lista de indicadores que Karoll necesita (acceso, composición, permanencia, desempeño, graduación) con una **definición rigurosa** de cada uno

## Semana 4 (23 – 27 nov) — Descriptivas y avance

- `[ ]` Composición de las cohortes Saber 11 frente a las cohortes de examen UNAL: ¿entraron más mujeres? ¿más diversidad de estrato, colegio o región?
- `[ ]` **Validez predictiva:** correlación y regresión del PAPA del primer año sobre el puntaje de admisión, por mecanismo, controlando por programa
- `[ ]` **Presentación corta (10 min)** junto con Karen Daniela

## Semana 5 (30 nov – 4 dic) — Indicadores y dashboard

- `[ ]` Validar las definiciones de indicadores con Karoll y Monica
- `[ ]` Prototipo de dashboard (Quarto, Shiny, Streamlit o similar) con los indicadores definidos, alimentado solo por datos agregados (sin microdatos, sin celdas de menos de 10)
- `[ ]` Explorar si se necesitan datos de **personas que no entraron a la universidad** (aspirantes, resultados ICFES) para la evaluación de impacto, y documentar qué se pediría

## Semana 6 (9 – 11 dic) — Documento y presentación final

- `[ ]` Documento corto con descriptivas, validez predictiva y catálogo de indicadores
- `[ ]` **Presentación final**

## Cierre (14 – 16 dic)

- `[ ]` Código reproducible; `README.md` del proyecto
- `[ ]` **Pull request** de `ra/njimenez` → `Proyectos2026-2S`
- `[ ]` Pendientes para 2027-1S: datos de aspirantes y evaluación de impacto

## Tareas transversales (todo el semestre)

- `[ ]` Apoyar a Jeronimo en la administración del repositorio, sobre todo en preguntas de Egresados y Retirados, que Nicolas construyó
- `[ ]` Apoyar a Manuela con la variable de modalidad de trabajo de grado

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
