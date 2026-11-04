# Plan de trabajo 2026-2S — Julian Esteban Bermudez Chiguasuque
## Proyecto: 202602_02_TimingAdmision · Componente: composición de estudiantes

**Correo:** jbermudezch@unal.edu.co · **Rama:** `ra/jbermudez` · **Código:** `Proyectos/202602_02_TimingAdmision/composicion/`
**Carpeta Drive:** `SemilleroMicroeconometriaProyectos/202602_02_TimingAdmision/`
**Compañero de proyecto:** Dilan Tovar (doble titulación y normativa) · **Supervisión:** Monica Mogollon

---

## ⚠ Reglas de datos e IA (obligatorias)

- **Nunca subas datos del proyecto a ningún agente de IA, chatbot o plataforma agéntica** (ChatGPT, Claude, Gemini, Copilot, Cursor, NotebookLM, etc.). Esto incluye bases, extractos, filas de ejemplo, tablas con microdatos y capturas de pantalla de datos. Usa IA solo con código y con documentos públicos (normativa, papers).
- Si usas un agente de código, debe trabajar **solo dentro de la carpeta del código del proyecto**: nunca debe buscar ni explorar otras carpetas del computador, ni **leer datos** sin autorización manual de la PI/CoPI. Ver [CLAUDE.md](../../CLAUDE.md) y la [Guía de RAs §4](../README.md#4-reglas-del-semestre).

---

## Objetivo del semestre

Describir la **composición histórica de los estudiantes que ingresan**, por programa y facultad, **antes y después** del cambio en el *timing* de la admisión: sexo, estrato, PBM, tipo de colegio, origen territorial, etnia, edad y puntaje de admisión. Un ejemplo de la hipótesis es la distribución por género, que según los profesores cambió sustancialmente en algunos programas.

Julian además **lidera la estandarización de los indicadores de composición** del semillero. Las mismas definiciones y el mismo código se usarán en el proyecto *Admisión Pandemia* (Nicolas), así que deben quedar como funciones reutilizables.

## Entregables finales (16 dic)

1. `Proyectos/202602_02_TimingAdmision/composicion/indicadores_composicion.[R|py]`: funciones documentadas que reciben una base y devuelven indicadores de composición por grupo
2. `Semestre_2026-2S/definiciones_indicadores_composicion.md`: definición formal de cada indicador
3. `data/composicion_programa_periodo.csv`: panel de indicadores programa × período de ingreso
4. `output/`: gráficas de evolución y tablas antes/después; índices de segregación por programa
5. Documento corto con resultados

---

## Semana 1 (3 – 6 nov) — Arranque

- `[ ]` Firmar el acuerdo de confidencialidad; pedir acceso a GitHub y Drive
- `[ ]` Clonar el repo, crear la rama `ra/jbermudez` y el archivo `00_config`; primer commit y push
- `[ ]` Leer la [Introducción](../INTRODUCCION_2026-2S.md) y la [Guía de RAs](../README.md)
- `[ ]` Leer el artículo del profesor Hernando Bayona (pedirlo a Monica) y resumirlo en `Literatura/notas_lectura.md`
- `[ ]` Reunión con Dilan para acordar la división del trabajo y el período de corte antes/después

## Semana 2 (9 – 13 nov) — Cohortes de ingreso y variables

- `[ ]` Script `01_cohortes_ingreso_JB`: identificar el **primer período** de cada `id_unal` × `cod_plan` en `BASE_MATRICULADOS`. Esa es la cohorte de ingreso
- `[ ]` Revisar la cobertura de las variables de composición por período: `sexo`, `estrato`, `pbm_consolidado`, `tipo_colegio`, `cod_mpio_residencia`, `etnia`, `edad_periodo`, `puntaje_admision`, `cod_acceso`. Hacer tabla de missings por período
- `[ ]` Restringir a **pregrado** y documentar cómo se distinguen los admitidos regulares de los de programas especiales (PAES, PEAMA) usando `cod_acceso` y `cod_subacceso`

## Semana 3 (17 – 20 nov) — Definir indicadores

- `[ ]` Redactar `definiciones_indicadores_composicion.md`: % mujeres, distribución por estrato, PBM medio y cuartiles, % colegio oficial, % fuera de Bogotá, % grupo étnico, edad media de ingreso y puntaje de admisión medio
- `[ ]` Agregar un indicador de **segregación o concentración** por programa, por ejemplo el índice de disimilitud de Duncan por sexo entre programas
- `[ ]` Programar las funciones en `indicadores_composicion.[ext]` y **compartirlas con Nicolas** para validarlas en su proyecto

## Semana 4 (23 – 27 nov) — Panel de composición y avance

- `[ ]` Construir `composicion_programa_periodo.csv` para todos los programas de pregrado y todos los períodos de ingreso
- `[ ]` Gráficas de evolución 2009–2025 para toda la universidad y por facultad, marcando el período del cambio (fecha aportada por Dilan)
- `[ ]` **Presentación corta (10 min)** junto con Dilan

## Semana 5 (30 nov – 4 dic) — Antes y después

- `[ ]` Comparar las cohortes antes y después del cambio (ventanas de 2, 4 y 6 semestres): diferencias de medias por programa y una primera regresión descriptiva del indicador sobre `post × programa` con efectos fijos
- `[ ]` Identificar los **programas con mayores cambios** de composición, por ejemplo en género
- `[ ]` Cuidar que ninguna tabla publique celdas con menos de 10 estudiantes

## Semana 6 (9 – 11 dic) — Documento y presentación final

- `[ ]` Documento corto: definiciones, evolución de la composición y resultados antes/después
- `[ ]` **Presentación final** conjunta con Dilan

## Cierre (14 – 16 dic)

- `[ ]` Código reproducible y funciones documentadas; `README.md` de la subcarpeta
- `[ ]` **Pull request** de `ra/jbermudez` → `Proyectos2026-2S`
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
| | | |
