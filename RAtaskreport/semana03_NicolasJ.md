# Reporte Semanal — Semana 03
## RA: Nicolas Jimenez | Dataset: Egresados y Retirados

**Semana:** 03 (2026-04-27 → 2026-05-03)
**Fecha de entrega del reporte:** 2026-05-03
**Fase del proyecto:** Fase 1 — Master Personas PII | Fase 3 — Inicio Limpieza

---

## Reglas del proyecto

> Ver [RULES_RA.md](../RULES_RA.md) para la versión completa.

**R1:** Hacer commit y push al terminar cada script.
**R2:** Actualizar este reporte cuando termines, avances o bloquees una tarea.
**R3:** No subir datos a GitHub (`.csv`, `.xlsx`, `.zip`).
**R4:** Un script por tarea — no combinar tareas en un mismo script.
**R5:** Todas las rutas en el archivo de configuración. Nunca hardcodear paths.
**R6:** `DatosOriginales/` es de solo lectura.

---

## Tareas asignadas

### Tarea 1a — Finalizar Master Dataset de Personas (Egresados)

**Script:** `02_masterpersonas_Egresados_NJ.[ext]` (continuar o completar)
**Output en Drive:** `DatosArmonizados/keys/MASTER_PERSONAS_EGRESADOS_PII.csv`

- `[ ]` Verificar que el script aplica todos los mapeos canónicos de `tipo_documento` y `sexo` (ver WORKPLAN Paso 1b)
- `[ ]` Verificar que `nombre_completo` está en mayúsculas y sin caracteres especiales
- `[ ]` Verificar longitud válida de `numero_documento` por tipo
- `[ ]` Crear columnas adicionales (`tipo_documento2`, `sexo2`, etc.) si hay cambios entre semestres
- `[ ]` Incluir `fecha_nacimiento` si existe en los archivos de Egresados
- `[ ]` Guardar `MASTER_PERSONAS_EGRESADOS_PII.csv` en `DatosArmonizados/keys/` (solo Drive)
- `[ ]` Hacer **commit y push** del script

---

### Tarea 1b — Finalizar Master Dataset de Personas (Retirados)

**Script:** `02_masterpersonas_Retirados_NJ.[ext]` (continuar o completar)
**Output en Drive:** `DatosArmonizados/keys/MASTER_PERSONAS_RETIRADOS_PII.csv`

- `[ ]` Verificar que el script aplica todos los mapeos canónicos de `tipo_documento` y `sexo`
- `[ ]` Verificar que `nombre_completo` está en mayúsculas y sin caracteres especiales
- `[ ]` Verificar longitud válida de `numero_documento` por tipo
- `[ ]` Incluir `fecha_nacimiento` si existe en Retirados
- `[ ]` Guardar `MASTER_PERSONAS_RETIRADOS_PII.csv` en `DatosArmonizados/keys/` (solo Drive)
- `[ ]` Hacer **commit y push** del script
- `[ ]` **Notificar a Jeronimo Jimenez** que ambos archivos están disponibles en Drive

---

### Tarea 2 — Iniciar scripts de Limpieza de Datos (Egresados y Retirados)

**Scripts a crear:**
- `03_limpieza_Egresados_NJ.[ext]`
- `03_limpieza_Retirados_NJ.[ext]`

**Ubicación en repo:** `1_LimpiezaDatos/`
**Input:** archivos originales de `DatosOriginales/Egresados/` y `DatosOriginales/Retirados/`

Para cada módulo, iniciar el script de limpieza que:

- `[ ]` Carga todos los archivos del módulo
- `[ ]` Estandariza nombres de variables al nombre canónico
- `[ ]` Estandariza el formato del período académico a `YYYY-NS`
- `[ ]` Estandariza el formato de fecha de grado/retiro (si existe)
- `[ ]` Detecta y documenta duplicados en el output limpio
- `[ ]` Hacer **commit y push** de cada script (aunque estén incompletos)

> Nicolas tiene cuatro scripts esta semana (dos Master Personas + dos limpiezas). Si no alcanza ambas limpiezas, priorizar Egresados y documentar en problemas.

---

## Archivos creados o modificados

| Archivo | Acción | Observación |
|---|---|---|
| `1_LimpiezaDatos/02_masterpersonas_Egresados_NJ.[ext]` | Modificado | Versión final con todos los mapeos |
| `1_LimpiezaDatos/02_masterpersonas_Retirados_NJ.[ext]` | Modificado | Versión final con todos los mapeos |
| `DatosArmonizados/keys/MASTER_PERSONAS_EGRESADOS_PII.csv` | Creado/Actualizado | Solo Drive — nunca a GitHub |
| `DatosArmonizados/keys/MASTER_PERSONAS_RETIRADOS_PII.csv` | Creado/Actualizado | Solo Drive — nunca a GitHub |
| `1_LimpiezaDatos/03_limpieza_Egresados_NJ.[ext]` | Creado | Inicio del script de limpieza |
| `1_LimpiezaDatos/03_limpieza_Retirados_NJ.[ext]` | Creado | Inicio del script de limpieza |

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

**¿Se encontró `fecha_nacimiento` en Egresados?** (Sí/No)

**¿Se encontró `fecha_nacimiento` en Retirados?** (Sí/No)

**Avance del script de limpieza — Egresados:** (describir hasta dónde llegaste)

**Avance del script de limpieza — Retirados:** (describir hasta dónde llegaste)

---

## Horas trabajadas (estimado)

| Actividad | Horas |
|---|---|
| Finalizar `02_masterpersonas_Egresados_NJ` | |
| Finalizar `02_masterpersonas_Retirados_NJ` | |
| `03_limpieza_Egresados_NJ` | |
| `03_limpieza_Retirados_NJ` | |
| **Total** | |
