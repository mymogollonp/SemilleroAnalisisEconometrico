# Reporte Semanal — Semana 03
## RA: Jeronimo Jimenez | Dataset: Cursadas

**Semana:** 03 (2026-04-27 → 2026-05-03)
**Fecha de entrega del reporte:** 2026-05-03
**Fase del proyecto:** Fase 1 — Master Personas PII + Consolidación (Paso 1c) | Fase 3 — Inicio Limpieza

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

### Tarea 1 — Finalizar Master Dataset de Personas (Cursadas)

**Script:** `02_masterpersonas_Cursadas_JJ.[ext]` (continuar o completar)
**Output en Drive:** `DatosArmonizados/keys/MASTER_PERSONAS_CURSADAS_PII.csv`

- `[ ]` Verificar que el script aplica todos los mapeos canónicos de `tipo_documento` y `sexo` (ver WORKPLAN Paso 1b)
- `[ ]` Verificar que `nombre_completo` está en mayúsculas y sin caracteres especiales
- `[ ]` Verificar longitud válida de `numero_documento` por tipo
- `[ ]` Crear columnas adicionales (`tipo_documento2`, `sexo2`, etc.) si hay cambios entre semestres
- `[ ]` Incluir `fecha_nacimiento` si existe en los archivos de Cursadas
- `[ ]` Guardar `MASTER_PERSONAS_CURSADAS_PII.csv` en `DatosArmonizados/keys/` (solo Drive)
- `[ ]` Hacer **commit y push** del script

---

### Tarea 1c — Consolidación del Master Dataset de Personas (Paso 1c)

**Script a crear:** `03_consolidacion_masterpersonas_JJ.[ext]`
**Ubicación en repo:** `1_LimpiezaDatos/`
**Prerequisito:** confirmar que los tres RAs han notificado que su archivo está disponible en Drive
**Output en Drive:** `DatosArmonizados/keys/MASTER_PERSONAS_PII.csv`

- `[ ]` Esperar confirmación de Nicolas Camacho, Maria Jose Cadena y Nicolas Jimenez
- `[ ]` Cargar los cinco archivos: `MASTER_PERSONAS_MATRICULADOS_PII.csv`, `MASTER_PERSONAS_CURSADAS_PII.csv`, `MASTER_PERSONAS_CANCELACIONES_PII.csv`, `MASTER_PERSONAS_EGRESADOS_PII.csv`, `MASTER_PERSONAS_RETIRADOS_PII.csv`
- `[ ]` Apilar todos los archivos usando los nombres canónicos como columnas comunes
- `[ ]` Deduplicar por `correo`; conservar todas las variantes de tipo/número/sexo en columnas numeradas si hay conflictos
- `[ ]` Guardar `MASTER_PERSONAS_PII.csv` en `DatosArmonizados/keys/` (solo Drive, nunca a GitHub)
- `[ ]` Reportar: N personas únicas totales, N personas en más de un módulo, N conflictos resueltos
- `[ ]` Hacer **commit y push** del script
- `[ ]` **Notificar al PI/CoPI** que `MASTER_PERSONAS_PII.csv` está disponible

---

### Tarea 2 — Iniciar script de Limpieza de Datos (Cursadas)

**Script a crear:** `04_limpieza_Cursadas_JJ.[ext]`
**Ubicación en repo:** `1_LimpiezaDatos/`
**Input:** archivos originales de `DatosOriginales/Cursadas/`

Basado en los hallazgos del inventario (semana 01), iniciar el script de limpieza que:

- `[ ]` Carga todos los archivos de Cursadas
- `[ ]` Estandariza nombres de variables al nombre canónico
- `[ ]` Estandariza el formato del período académico a `YYYY-NS`
- `[ ]` Verifica que la escala de calificaciones está en 0–5 en todos los archivos
- `[ ]` Detecta y documenta duplicados en el output limpio
- `[ ]` Hacer **commit y push** del script (aunque esté incompleto)

> Jeronimo tiene dos responsabilidades esta semana (consolidación + limpieza). Si no alcanza a iniciar la limpieza, documentarlo en problemas y priorizarlo la semana siguiente.

---

## Archivos creados o modificados

| Archivo | Acción | Observación |
|---|---|---|
| `1_LimpiezaDatos/02_masterpersonas_Cursadas_JJ.[ext]` | Modificado | Versión final con todos los mapeos |
| `DatosArmonizados/keys/MASTER_PERSONAS_CURSADAS_PII.csv` | Creado/Actualizado | Solo Drive — nunca a GitHub |
| `1_LimpiezaDatos/03_consolidacion_masterpersonas_JJ.[ext]` | Creado | Script de consolidación Paso 1c |
| `DatosArmonizados/keys/MASTER_PERSONAS_PII.csv` | Creado | Solo Drive — nunca a GitHub |
| `1_LimpiezaDatos/04_limpieza_Cursadas_JJ.[ext]` | Creado | Inicio del script de limpieza |

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

**¿Se encontró `fecha_nacimiento` en Cursadas?** (Sí/No)

**RAs que notificaron disponibilidad de su archivo:** (completar — NC / MJC / NJ)

**Personas únicas en MASTER_PERSONAS_PII.csv consolidado:** (completar)

**Avance del script de limpieza:** (describir hasta dónde llegaste esta semana)

---

## Horas trabajadas (estimado)

| Actividad | Horas |
|---|---|
| Finalizar `02_masterpersonas_Cursadas_JJ` | |
| `03_consolidacion_masterpersonas_JJ` (Paso 1c) | |
| `04_limpieza_Cursadas_JJ` | |
| **Total** | |
