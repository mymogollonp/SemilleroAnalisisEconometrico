# Reporte Semanal — Semana 01
## RA: Jeronimo Jimenez | Dataset: Cursadas

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

### Infraestructura

- `[ ]` Leer `WORKPLAN.md`, `requirements-spec.md` y `RULES_RA.md` completos
- `[ ]` Firmar el acuerdo de confidencialidad
- `[ ]` Clonar el repositorio y verificar acceso a `DatosOriginales/Cursadas/`

---

### Tarea 1 — Inventario de Cursadas

**Script a entregar:** `01_Inventario_Cursadas_JJ.R` (o `.py`)
**Referencia:** `1_LimpiezaDatos/Example_Inventario.R`
**Ubicación en repo:** `1_LimpiezaDatos/`

El script debe producir un reporte con:

- `[ ]` **Carga de archivos** — cargar todos los archivos de la carpeta `DatosOriginales/Cursadas/`
- `[ ]` **Estructura general** — número de filas y columnas por archivo; missings por variable
- `[ ]` **Duplicados** — identificar filas duplicadas en cada archivo
- `[ ]` **Consistencia de nombres de variables entre semestres** — ¿qué variables cambian de nombre entre archivos?
- `[ ]` **Clave única** — identificar a qué nivel hay unicidad en los datos (¿una variable? ¿combinación?)
- `[ ]` Hacer **commit y push** del script

Documentar en "Comentarios adicionales":
- Nombre exacto del campo de ID personal (correo, cédula u otro)
- Lista completa de variables
- Variables que cambian entre semestres
- Clave única de observación (variable simple o compuesta)
- ¿La escala de calificaciones es 0–5 en todos los archivos?

---

### Tarea 2 — Master Dataset de Personas (Cursadas)

**Script a entregar:** `02_masterpersonas_Cursadas_JJ.R` (o `.py`)
**Referencia:** `1_LimpiezaDatos/Example_masterpersonas.R`
**Ubicación en repo:** `1_LimpiezaDatos/`
**Output en Drive:** `DatosArmonizados/keys/MASTER_PERSONAS_CURSADAS_PII.csv`

El script debe:

- `[ ]` Iterar sobre **todos** los archivos de Cursadas (no solo el más reciente)
- `[ ]` Extraer y armonizar a nombres canónicos: `correo`, `tipo_documento`, `numero_documento`, `nombre_completo`, `sexo`
- `[ ]` Conservar **todos los valores distintos de sexo/género observados** por persona (con el período correspondiente)
- `[ ]` Registrar todos los tipos de documento encontrados; reportar cualquier código no reconocido (válidos: CC, CE, PA, TI, NUIP, PEP)
- `[ ]` Verificar formato de número de documento (CC: 6–10 dígitos; TI: 10–11 dígitos; CE/PA: alfanumérico)
- `[ ]` Guardar en `DatosArmonizados/keys/MASTER_PERSONAS_CURSADAS_PII.csv` (solo Drive, nunca a GitHub)
- `[ ]` Hacer **commit y push** del script (no del CSV)

---

## Archivos creados o modificados

| Archivo | Acción | Observación |
|---|---|---|
| `1_LimpiezaDatos/01_Inventario_Cursadas_JJ.[ext]` | Creado | Script de inventario |
| `1_LimpiezaDatos/02_masterpersonas_Cursadas_JJ.[ext]` | Creado | Script que genera MASTER_PERSONAS_CURSADAS_PII |
| `DatosArmonizados/keys/MASTER_PERSONAS_CURSADAS_PII.csv` | Creado | Solo en Drive — nunca a GitHub |

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

**Campo de ID personal en Cursadas:** (completar)

**Lista de variables:** (completar — pegar output del inventario)

**Variables que cambian entre semestres:** (completar — Sí/No; si Sí, listar)

**Clave única de observación:** (completar — variable simple o compuesta)

**¿Escala de calificaciones es 0–5 en todos los archivos?** (completar)

**Personas únicas en MASTER_PERSONAS_CURSADAS_PII:** (completar)

**Tipos de documento encontrados:** (completar — ej. CC: 94%, CE: 5%)

**Personas con más de un valor de sexo/género:** (completar — N casos)

**Registros con formato de documento inválido:** (completar — N registros)

---

## Horas trabajadas (estimado)

| Actividad | Horas |
|---|---|
| Lectura de documentación | |
| `01_Inventario_Cursadas_JJ` | |
| `02_masterpersonas_Cursadas_JJ` | |
| **Total** | |
