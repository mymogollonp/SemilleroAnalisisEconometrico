# Reporte Semanal — Semana 03
## RA: Nicolas Camacho | Dataset: Matriculados

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

### Tarea 1 — Finalizar Master Dataset de Personas (Matriculados)

**Script:** `02_masterpersonas_Matriculados_NC.[ext]` (continuar o completar)
**Output en Drive:** `DatosArmonizados/keys/MASTER_PERSONAS_MATRICULADOS_PII.csv`

- `[ ]` Verificar que el script aplica todos los mapeos canónicos de `tipo_documento` y `sexo` (ver WORKPLAN Paso 1b)
- `[ ]` Verificar que `nombre_completo` está en mayúsculas y sin caracteres especiales
- `[ ]` Verificar longitud válida de `numero_documento` por tipo
- `[ ]` Crear columnas adicionales (`tipo_documento2`, `sexo2`, etc.) si hay cambios entre semestres
- `[ ]` Incluir `fecha_nacimiento` si existe en los archivos de Matriculados
- `[ ]` Guardar `MASTER_PERSONAS_MATRICULADOS_PII.csv` en `DatosArmonizados/keys/` (solo Drive)
- `[ ]` Hacer **commit y push** del script
- `[ ]` **Notificar a Jeronimo Jimenez** que el archivo está disponible en Drive

---

### Tarea 2 — Iniciar script de Limpieza de Datos (Matriculados)

**Script a crear:** `03_limpieza_Matriculados_NC.[ext]`
**Ubicación en repo:** `1_LimpiezaDatos/`
**Input:** archivos originales de `DatosOriginales/Matriculado/`

Basado en los hallazgos del inventario (semana 01), iniciar el script de limpieza que:

- `[ ]` Carga todos los archivos de Matriculados
- `[ ]` Estandariza nombres de variables al nombre canónico (resolver los cambios de nombre identificados en el inventario)
- `[ ]` Estandariza el formato del período académico a `YYYY-NS`
- `[ ]` Estandariza variables de programa (`cod_plan`, `cod_programa`) — aplicar los casos identificados en el inventario
- `[ ]` Detecta y documenta duplicados en el output limpio
- `[ ]` Hacer **commit y push** del script (aunque esté incompleto — el progreso también se versiona)

> Este script será la base para la construcción del panel en fases posteriores. Priorizar la estandarización de variables que cambian entre semestres.

---

## Archivos creados o modificados

| Archivo | Acción | Observación |
|---|---|---|
| `1_LimpiezaDatos/02_masterpersonas_Matriculados_NC.[ext]` | Modificado | Versión final con todos los mapeos |
| `DatosArmonizados/keys/MASTER_PERSONAS_MATRICULADOS_PII.csv` | Creado/Actualizado | Solo Drive — nunca a GitHub |
| `1_LimpiezaDatos/03_limpieza_Matriculados_NC.[ext]` | Creado | Inicio del script de limpieza |

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

**¿Se encontró `fecha_nacimiento` en Matriculados?** (Sí/No)

**Variables que cambiaron de nombre entre semestres (hallazgos del inventario):** (completar)

**Avance del script de limpieza:** (describir hasta dónde llegaste esta semana)

---

## Horas trabajadas (estimado)

| Actividad | Horas |
|---|---|
| Finalizar `02_masterpersonas_Matriculados_NC` | |
| Iniciar `03_limpieza_Matriculados_NC` | |
| **Total** | |
