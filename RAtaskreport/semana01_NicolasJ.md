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

- `[ ]` Leer `WORKPLAN.md`, `requirements-spec.md` y `RULES_RA.md` completos
- `[ ]` Firmar el acuerdo de confidencialidad
- `[ ]` Clonar el repositorio y verificar acceso a `DatosOriginales/Egresados/` y `DatosOriginales/Retirados/`

---

### Tarea 1a — Inventario de Egresados

**Script a entregar:** `01_Inventario_Egresados_NJ.R` (o `.py`)
**Referencia:** `1_LimpiezaDatos/Example_Inventario.R`
**Ubicación en repo:** `1_LimpiezaDatos/`

- `[ ]` **Carga de archivos** — cargar todos los archivos de `DatosOriginales/Egresados/`
- `[ ]` **Estructura general** — filas, columnas, missings por variable
- `[ ]` **Duplicados** — filas duplicadas en cada archivo
- `[ ]` **Consistencia de variables entre semestres** — ¿qué variables cambian entre archivos?
- `[ ]` **Clave única** — ¿a qué nivel hay unicidad? (¿una variable? ¿combinación?)
- `[ ]` Hacer **commit y push** del script

Documentar en "Comentarios adicionales": campo de ID personal, lista de variables, formato de fecha de grado, variables que cambian, clave única.

---

### Tarea 1b — Inventario de Retirados

**Script a entregar:** `01_Inventario_Retirados_NJ.R` (o `.py`)
**Referencia:** `1_LimpiezaDatos/Example_Inventario.R`
**Ubicación en repo:** `1_LimpiezaDatos/`

> Retirados es un único archivo (`Retirados_desde_2009.xlsx`). El script igualmente debe reportar estructura, duplicados y clave única.

- `[ ]` **Carga del archivo** — cargar `Retirados_desde_2009.xlsx`
- `[ ]` **Estructura general** — filas, columnas, missings por variable
- `[ ]` **Duplicados** — filas duplicadas
- `[ ]` **Clave única** — ¿a qué nivel hay unicidad?
- `[ ]` Hacer **commit y push** del script

---

### Tarea 2a — Master Dataset de Personas (Egresados)

**Script a entregar:** `02_masterpersonas_Egresados_NJ.R` (o `.py`)
**Referencia:** `1_LimpiezaDatos/Example_masterpersonas.R`
**Ubicación en repo:** `1_LimpiezaDatos/`
**Output en Drive:** `DatosArmonizados/keys/MASTER_PERSONAS_EGRESADOS_PII.csv`

- `[ ]` Iterar sobre **todos** los archivos de Egresados
- `[ ]` Extraer y armonizar: `correo`, `tipo_documento`, `numero_documento`, `nombre_completo`, `sexo`
- `[ ]` Conservar todos los valores distintos de sexo/género por persona (con período)
- `[ ]` Validar tipos y formatos de documento
- `[ ]` Guardar en `DatosArmonizados/keys/MASTER_PERSONAS_EGRESADOS_PII.csv` (solo Drive)
- `[ ]` Hacer **commit y push** del script

---

### Tarea 2b — Master Dataset de Personas (Retirados)

**Script a entregar:** `02_masterpersonas_Retirados_NJ.R` (o `.py`)
**Referencia:** `1_LimpiezaDatos/Example_masterpersonas.R`
**Ubicación en repo:** `1_LimpiezaDatos/`
**Output en Drive:** `DatosArmonizados/keys/MASTER_PERSONAS_RETIRADOS_PII.csv`

- `[ ]` Cargar `Retirados_desde_2009.xlsx`
- `[ ]` Extraer y armonizar: `correo`, `tipo_documento`, `numero_documento`, `nombre_completo`, `sexo`
- `[ ]` Validar tipos y formatos de documento
- `[ ]` Guardar en `DatosArmonizados/keys/MASTER_PERSONAS_RETIRADOS_PII.csv` (solo Drive)
- `[ ]` Hacer **commit y push** del script

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
| | | | |

---

## Preguntas para el PI/CoPI

-

---

## Comentarios adicionales

**Campo de ID personal en Egresados:** (completar)

**Lista de variables — Egresados:** (completar)

**Formato de fecha de grado:** (completar — ejemplos de valores reales)

**Variables que cambian entre semestres — Egresados:** (completar)

**Clave única — Egresados:** (completar)

**Campo de ID personal en Retirados:** (completar)

**Lista de variables — Retirados:** (completar)

**Clave única — Retirados:** (completar)

**Personas únicas en MASTER_PERSONAS_EGRESADOS_PII:** (completar)

**Personas únicas en MASTER_PERSONAS_RETIRADOS_PII:** (completar)

**Tipos de documento encontrados (Egresados):** (completar)

**Tipos de documento encontrados (Retirados):** (completar)

**Personas con más de un valor de sexo/género:** (completar — N casos Egresados / N casos Retirados)

---

## Horas trabajadas (estimado)

| Actividad | Horas |
|---|---|
| Lectura de documentación | |
| `01_Inventario_Egresados_NJ` | |
| `01_Inventario_Retirados_NJ` | |
| `02_masterpersonas_Egresados_NJ` | |
| `02_masterpersonas_Retirados_NJ` | |
| **Total** | |
