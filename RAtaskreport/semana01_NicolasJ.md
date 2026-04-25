# Reporte Semanal — Semana 01
## RA: Nicolas Jimenez | Dataset: Egresados y Retirados

**Semana:** 01 (2026-04-13 → 2026-04-26)
**Fecha de entrega del reporte:** 2026-04-26
**Fase del proyecto:** Fase 0 — Inventario y Master Personas

---

## Reglas del proyecto

> Ver [RULES_RA.md](../RULES_RA.md) para la versión completa.

**R1:** Hacer commit y push al terminar cada script.
**R2:** Actualizar este reporte cuando termines, avances o bloquees una tarea (`[ ]` → `[x]`, `[-]`, o `[!]`).
**R3:** No subir datos a GitHub (`.csv`, `.xlsx`, `.zip`).
**R4:** Un script por tarea — no combinar tareas en un mismo script.
**R5:** Todas las rutas en el archivo de configuración (`00_config.R` o `00_config.py`). Nunca hardcodear paths.
**R6:** `DatosOriginales/` es de solo lectura — los scripts solo leen, nunca escriben allí.
**R7:** Documentar la semilla en todo script que use aleatoriedad.

---

## Tareas asignadas

> Nicolas Jimenez cubre dos módulos: **Egresados** y **Retirados**. Entregar un script de inventario y un script de master personas por módulo (4 scripts en total).

### Infraestructura

- `[x]` Leer `WORKPLAN.md`, `requirements-spec.md` y `RULES_RA.md` completos
- `[x]` Firmar el acuerdo de confidencialidad
- `[x]` Clonar el repositorio y verificar acceso a `DatosOriginales/Egresados/` y `DatosOriginales/Retirados/`

---

### Tarea 1a — Inventario de Egresados

**Script a entregar:** `01_Inventario_Egresados_NJ.R` (o `.py`)
**Referencia:** `1_LimpiezaDatos/Example_Inventario.R`
**Ubicación en repo:** `1_LimpiezaDatos/`

- `[x]` **Carga de archivos** — cargar todos los archivos de `DatosOriginales/Egresados/`
- `[x]` **Estructura general** — filas, columnas, missings por variable
- `[x]` **Duplicados** — filas duplicadas en cada archivo
- `[x]` **Consistencia de variables entre semestres** — ¿qué variables cambian entre archivos?
- `[x]` **Clave única** — ¿a qué nivel hay unicidad? (¿una variable? ¿combinación?)
- `[x]` Hacer **commit y push** del script

Documentar en "Comentarios adicionales": campo de ID personal, lista de variables, formato de fecha de grado, variables que cambian, clave única.

---

### Tarea 1b — Inventario de Retirados

**Script a entregar:** `01_Inventario_Retirados_NJ.R` (o `.py`)
**Referencia:** `1_LimpiezaDatos/Example_Inventario.R`
**Ubicación en repo:** `1_LimpiezaDatos/`

> Retirados es un único archivo (`Retirados_desde_2009.xlsx`). El script igualmente debe reportar estructura, duplicados y clave única.

- `[x]` **Carga del archivo** — cargar `Retirados_desde_2009.xlsx`
- `[x]` **Estructura general** — filas, columnas, missings por variable
- `[x]` **Duplicados** — filas duplicadas
- `[x]` **Clave única** — ¿a qué nivel hay unicidad?
- `[x]` Hacer **commit y push** del script

---

### Tarea 2a — Master Dataset de Personas (Egresados)

**Script a entregar:** `02_masterpersonas_Egresados_NJ.R` (o `.py`)
**Referencia:** `1_LimpiezaDatos/Example_masterpersonas.R`
**Ubicación en repo:** `1_LimpiezaDatos/`
**Output en Drive:** `DatosArmonizados/keys/MASTER_PERSONAS_EGRESADOS_PII.csv`

- `[x]` Iterar sobre **todos** los archivos de Egresados
- `[x]` Extraer y armonizar: `correo`, `tipo_documento`, `numero_documento`, `nombre_completo`, `sexo`
- `[x]` Conservar todos los valores distintos de sexo/género por persona (con período)
- `[x]` Validar tipos y formatos de documento
- `[x]` Guardar en `DatosArmonizados/keys/MASTER_PERSONAS_EGRESADOS_PII.csv` (solo Drive)
- `[x]` Hacer **commit y push** del script

---

### Tarea 2b — Master Dataset de Personas (Retirados)

**Script a entregar:** `02_masterpersonas_Retirados_NJ.R` (o `.py`)
**Referencia:** `1_LimpiezaDatos/Example_masterpersonas.R`
**Ubicación en repo:** `1_LimpiezaDatos/`
**Output en Drive:** `DatosArmonizados/keys/MASTER_PERSONAS_RETIRADOS_PII.csv`

- `[x]` Cargar `Retirados_desde_2009.xlsx`
- `[x]` Extraer y armonizar: `correo`, `tipo_documento`, `numero_documento`, `nombre_completo`, `sexo`
- `[x]` Validar tipos y formatos de documento
- `[x]` Guardar en `DatosArmonizados/keys/MASTER_PERSONAS_RETIRADOS_PII.csv` (solo Drive)
- `[x]` Hacer **commit y push** del script

---

## Archivos creados o modificados

| Archivo | Acción | Observación |
|---|---|---|
| `1_LimpiezaDatos/01_Inventario_Egresados_NJ.[ext]` | Creado | Inventario Egresados |
| `1_LimpiezaDatos/01_Inventario_Retirados_NJ.[ext]` | Creado | Inventario Retirados |
| `1_LimpiezaDatos/02_masterpersonas_Egresados_NJ.[ext]` | Creado | Master Personas Egresados |
| `1_LimpiezaDatos/02_masterpersonas_Retirados_NJ.[ext]` | Creado | Master Personas Retirados |
| `DatosArmonizados/keys/MASTER_PERSONAS_EGRESADOS_PII.csv` | Creado | Solo Drive — nunca a GitHub |
| `DatosArmonizados/keys/MASTER_PERSONAS_RETIRADOS_PII.csv` | Creado | Solo Drive — nunca a GitHub |

---

## Problemas encontrados

| # | Descripción del problema | Dato o archivo afectado | Estado |
|---|---|---|---|
## Problemas identificados en los datos

| # | Descripción del problema | Dato o archivo afectado | Estado |
|---|---|---|---|
| 1 | `tipo_documento` solo aparece desde 2022-1S en Egresados. | Egresados | Mitigado: se armonizó y se completó cuando existía información posterior para la misma persona/documento. |
| 2 | No hay una unidad de observación única evidente en Egresados. | Egresados | Documentado: `EMAIL + COD_PLAN` alcanza ~95% de unicidad, pero no es llave estricta. |
| 3 | Retirados no contiene `tipo_documento`. | Retirados | Documentado: se conserva como `NA` en el master. |
| 4 | Existen múltiples estructuras de columnas entre semestres. | Egresados | Documentado: se identificaron 3 estructuras con cambios en variables personales y académicas. |
| 5 | Diferencias de codificación en columna sexo. | Egresados | Mitigado: se creó `sexo` armonizado y se conservó `sexo_raw` |
| 6 | Registros sin correo o con inconsistencias correo-documento. | Masters PII | Documentado: Egresados tiene 1 fila sin correo; Retirados tiene 6 filas sin correo y 1 correo asociado a 2 documentos. |
| 7 | Repeticiones por cambios documentales válidos (ej. TI → CC). | Master Egresados | Documentado: 4 casos que se conservan por trazabilidad histórica. |
---

## Preguntas para el PI/CoPI

-

---

## Comentarios adicionales

**Campo de ID personal en Egresados:** (completar)
Tanto correo como numero de documento

**Lista de variables — Egresados:** (completar)
<details>
<summary>Ver variables</summary>
- `COD_SEDE`
- `SEDE`
- `NOMBRES`
- `PRIMER_APELLIDO`
- `SEGUNDO_APELLIDO`
- `DOCUMENTO`
- `COD_PLAN`
- `DESC_PLAN`
- `CONVENIO_PLAN`
- `HIST_ACADEMICA`
- `EMAIL`
- `SEXO`
- `FECHA_NACIMIENTO`
- `CONVOCATORIA`
- `APERTURA`
- `COD_ACCESO`
- `ACCESO`
- `COD_SUBACCESO`
- `SUBACCESO`
- `COD_FACULTAD`
- `FACULTAD`
- `COD_PROGRAMA`
- `PROGRAMA`
- `COD_NIVEL`
- `TIPO_NIVEL`
- `NIVEL`
- `SNIES`
- `DIPLOMA`
- `TITULOOBT`
- `FOLIO`
- `LIBRO`
- `ACTA`
- `PERIODO_TERMINACION`
- `PAPA_SIN_REDONDEO`
- `PAPA`
- `PROM_ACAD_SIN_REDONDEO`
- `PROM_ACADEMICO`
- `PROM_GRADUADO_SIN_REDONDEDO`
- `PROM_GRADUADO`
- `COD_NOD_INI`
- `NODO_INI`
- `COD_NODO_FIN`
- `NODO_FIN`
- `PER_NODO_GRADUACION`
- `FECHA_GRADUADO`
- `MODALIDAD_TG`
- `NOMBRE_TRABAJO_GR`
- `DOC_DIRECTOR`
- `DIRECTOR`
- `INST_DIRECTOR`
- `DOC_CODIRECTOR`
- `CODIRECTOR`
- `INST_CODIRECTOR`
- `DEP_PROCEDENCIA`
- `NOMBRE_DEPTO_PROCEDENCIA`
- `MUNICIPIO_PROCEDENCIA`
- `NOMBRE_MUNICIPIO_PROCEDENCIA`
- `NUM_MATRICULAS`
- `NUM_CANCELACIONES`
- `DIRECCION_PROCEDENCIA`
- `TEL_PROCEDENCIA`
- `CONVENIO_PLAN.1`
- `PROM_GRADUADO_SIN_REDONDEDO.1`
- `PROM_GRADUADO.1`
- `PBM`
- `CRED_CONSEGUIDOS`
- `CRED_NIVELACION`
- `CRED_CONSEGUIDOS_PLAN`
- `CARNET_UN`
- `archivo_origen`
- `T_DOCUMENTO`
- `NOMBRES_LEGAL`
- `APELLIDO1_LEGAL`
- `APELLIDO2_LEGAL`
- `SEXO_LEGAL`
- `GENERO`
</details>
  
**Formato de fecha de grado:** (completar — ejemplos de valores reales)
En Excel se observa como d-mmm-aa, por ejemplo 5-sep-14. En Python se lee como fecha tipo Timestamp/datetime, representada como YYYY-MM-DD o YYYY-MM-DD 00:00:00.

**Variables que cambian entre semestres — Egresados:** (completar)
Variables que cambian entre semestres — Egresados:
Se encontraron 3 estructuras de columnas. Los cambios principales ocurren a partir de 2022-1S con la incorporación de T_DOCUMENTO, y a partir de 2024-2S con el cambio de variables personales antiguas (NOMBRES, PRIMER_APELLIDO, SEGUNDO_APELLIDO, SEXO) por variables legales/nuevas (NOMBRES_LEGAL, APELLIDO1_LEGAL, APELLIDO2_LEGAL, SEXO_LEGAL, GENERO). También se observa CONVENIO_PLAN.1 (columna repetida, la columna CONVENIO_PLAN siempre se conserva) en la estructura inicial, que no aparece en las posteriores.

**Clave única — Egresados:** (completar)
La combinación EMAIL + COD_PLAN presenta un nivel de unicidad del 95%, por lo que no puede considerarse una llave única estricta. El 5% restante de los casos corresponde principalmente a registros donde varían variables asociadas al trabajo de grado.

**Campo de ID personal en Retirados:** (completar)
Documento, excepto por 1 persona que registra 2 documentos.

**Lista de variables — Retirados:** (completar)
<details>
<summary>Ver variables</summary>
- `COD_SEDE`
- `SEDE`
- `COD_FACULTAD`
- `FACULTAD`
- `COD_UAB`
- `UAB`
- `COD_PROGRAMA`
- `PROGRAMA`
- `COD_SNIES`
- `COD_PLAN`
- `PLAN`
- `CONVENIO_PLAN`
- `NIVEL`
- `DOCUMENTO`
- `HIST_ACADEMICA`
- `NOMBRES_LEGAL`
- `APELLIDO1_LEGAL`
- `APELLIDO2_LEGAL`
- `SEXO_LEGAL`
- `GENERO`
- `CORREO`
- `CONVOCATORIA`
- `APERTURA`
- `NUM_MATRICULAS`
- `FECHA_BLOQUEO`
- `PERIODO_BLOQUEO`
- `TIPO_BLOQUEO`
- `COD_BLOQUEO`
- `BLOQUEO`
- `CAUSA_ACTIVA`
- `ESTADO_ACTUAL`
- `ESTRATO`
- `PBM`
- `COD_ACCESO`
- `NOMBRE_ACCESO`
- `COD_SUBACCESO`
- `NOMBRE_SUBACCESO`
- `DEPTO_PROCEDENCIA`
- `MUN_PROCEDENCIA`
- `PORCENTAJE_AVANCE`
- `COD_NODO_INICIO`
- `NODO_INICIO`
- `EDAD`
- `COD_PAIS_NACIMIENTO`
- `PAIS_NACIMIENTO`
- `COD_DEPTO_NACIMIENTO`
- `DEPTO_NACIMIENTO`
- `COD_MUN_NACIMIENTO`
- `MUN_NACIMIENTO`
- `NUMHIJOSDEPENDIENTES`
- `TIPOPROVIVIENDA`
- `PAPA`
- `PROM_ACADEMICO`
- `COD_COLEGIO`
- `COLEGIO`
- `COD_DEPARTAMENTO_COLEGIO`
- `DEPARTAMENTO_COLEGIO`
- `COD_MUNICIPIO_COLEGIO`
- `MUNICIPIO_COLEGIO`
</details>
**Clave única — Retirados:** (completar)
CORREO + COD_PLAN + PERIODO_BLOQUEO + COD_BLOQUEO

**Personas únicas en MASTER_PERSONAS_EGRESADOS_PII:** (completar)
74.949 identificadores únicos, usando `correo` como identificador principal y `numero_documento` como respaldo. El master final contiene 74.953 filas porque conserva algunos registros múltiples asociados a cambios documentales válidos.

**Personas únicas en MASTER_PERSONAS_RETIRADOS_PII:** (completar)
41394

**Tipos de documento encontrados (Egresados):** (completar)
CC, TI, CE, PA, OTRO, NA.

**Tipos de documento encontrados (Retirados):** (completar)
No existe tipo_documento en la base original de Retirados, se deja como NA.

**Personas con más de un valor de sexo/género:** (completar — N casos Egresados / N casos Retirados)
0 casos egresados
0 casos retirados

## Horas trabajadas (estimado)

| Actividad | Horas |
|---|---|
| Lectura de documentación | |
| `01_Inventario_Egresados_NJ` |6|
| `01_Inventario_Retirados_NJ` |1|
| `02_masterpersonas_Egresados_NJ` |2|
| `02_masterpersonas_Retirados_NJ` |2|
| **Total** |11|
