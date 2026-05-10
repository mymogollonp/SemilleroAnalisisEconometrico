# Reporte Semanal — Semana 04
## RA: Jeronimo Jimenez | Dataset: Cursadas + Consolidación Master Personas

**Semana:** 04 (2026-05-04 → 2026-05-10)
**Fecha de entrega del reporte:** 2026-05-10
**Fase del proyecto:** Fase 1 — Master Personas PII (versión final + consolidación) | Fase 3 — Limpieza de variables categóricas

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

### Tarea 1 — Completar Master Dataset de Personas (Cursadas) — versión final

**Script:** `02_masterpersonas_Cursadas_JJ.[ext]`
**Output en Drive:** `DatosArmonizados/keys/MASTER_PERSONAS_CURSADAS_PII.csv`

- `[ ]` Incluir `fecha_nacimiento` — buscarla en los archivos de Cursadas y registrarla en formato `YYYY-MM-DD`; si no existe en ningún archivo, dejar la columna como `NA` y documentarlo
- `[ ]` Verificar que `tipo_documento` aplica el mapeo canónico completo (CC, CE, PA, TI, PEP, OTRO)
- `[ ]` Verificar que `sexo` aplica el mapeo canónico completo (M, F, X, NA)
- `[ ]` Verificar que `nombre_completo` está en mayúsculas y sin tildes ni caracteres especiales
- `[ ]` Verificar longitud válida de `numero_documento` por tipo
- `[ ]` Confirmar que el output tiene **una fila por `correo`** — sin duplicados
- `[ ]` Guardar `MASTER_PERSONAS_CURSADAS_PII.csv` en `DatosArmonizados/keys/` (solo Drive, nunca a GitHub)
- `[ ]` Hacer **commit y push** del script actualizado

---

### Tarea 2 — Consolidar Master Dataset de Personas (todos los módulos)

**Script:** `03_consolidacion_masterpersonas_JJ.[ext]`
**Prerequisito:** confirmación de los cuatro RAs de que sus archivos están disponibles en Drive
**Output en Drive:** `DatosArmonizados/keys/MASTER_PERSONAS_PII.csv`

- `[ ]` Esperar notificación de **Nicolas Camacho**, **Maria Jose Cadena** y **Nicolas Jimenez** (los cuatro confirman disponibilidad antes de consolidar)
- `[ ]` Cargar los cinco archivos: `MASTER_PERSONAS_MATRICULADOS_PII.csv`, `MASTER_PERSONAS_CURSADAS_PII.csv`, `MASTER_PERSONAS_CANCELACIONES_PII.csv`, `MASTER_PERSONAS_EGRESADOS_PII.csv`, `MASTER_PERSONAS_RETIRADOS_PII.csv`
- `[ ]` Verificar que todos los archivos tienen las columnas canónicas: `correo`, `tipo_documento`, `numero_documento`, `nombre_completo`, `fecha_nacimiento`, `sexo`
- `[ ]` Apilar todos los archivos usando los nombres canónicos
- `[ ]` Deduplicar por `correo` — si una persona tiene valores distintos entre módulos para `tipo_documento`, `numero_documento`, `sexo` o `fecha_nacimiento`, crear columnas numeradas (`tipo_documento1`, `tipo_documento2`, etc.) en lugar de descartar
- `[ ]` Guardar `MASTER_PERSONAS_PII.csv` en `DatosArmonizados/keys/` (solo Drive, nunca a GitHub)
- `[ ]` Hacer **commit y push** del script
- `[ ]` **Notificar al PI/CoPI** que `MASTER_PERSONAS_PII.csv` está disponible

---

### Tarea 3 — Reporte estadístico de inconsistencias del Master consolidado

**Script:** `04_reporte_inconsistencias_masterpersonas_JJ.[ext]`
**Input:** `DatosArmonizados/keys/MASTER_PERSONAS_PII.csv`
**Output:** `logs/reporte_inconsistencias_master_YYYY-MM-DD.md` (en el repo)

Generar un reporte que documente la calidad y consistencia del master consolidado. Este reporte es insumo para que el PI/CoPI tome decisiones antes de la anonimización.

- `[ ]` **Cobertura por módulo** — N personas únicas aportadas por cada módulo (Matriculados, Cursadas, Cancelaciones, Egresados, Retirados)
- `[ ]` **Personas en más de un módulo** — N personas que aparecen en 2, 3, 4 o 5 módulos simultáneamente
- `[ ]` **Inconsistencias de `tipo_documento`** — N personas con más de un tipo de documento registrado; tabla de pares de tipos más frecuentes (ej. CC + CE)
- `[ ]` **Inconsistencias de `numero_documento`** — N personas con más de un número de documento; N documentos con formato inválido por tipo
- `[ ]` **Inconsistencias de `fecha_nacimiento`** — N personas con más de una fecha de nacimiento registrada entre módulos; rango de fechas observado
- `[ ]` **Inconsistencias de `sexo`** — N personas con más de un valor de sexo registrado; distribución de valores canónicos (M / F / X / NA)
- `[ ]` **Personas sin `correo`** — N registros sin correo (excluidos del master)
- `[ ]` Guardar el reporte como `logs/reporte_inconsistencias_master_YYYY-MM-DD.md`
- `[ ]` Hacer **commit y push** del script y del reporte

---

### Tarea 4 — Continuar limpieza: armonizar variables categóricas (Cursadas)

**Script:** `04_limpieza_Cursadas_JJ.[ext]` (continuar desde semana 03)
**Input:** archivos originales de `DatosOriginales/Cursadas/`
**Output:** `DatosArmonizados/2_DatosLimpios/Cursadas/Cursadas_[YYYY-NS]_limpio.csv`

- `[ ]` Armonizar `tipo_calificacion` — identificar todos los valores únicos y mapear a categorías canónicas
- `[ ]` Verificar escala de calificaciones 0–5 en todos los archivos; documentar valores fuera de rango
- `[ ]` Armonizar `nivel_formacion` si existe — colapsar variantes
- `[ ]` Verificar que el output **no contiene PII** (ver regla de privacidad en WORKPLAN Fase 3)
- `[ ]` Guardar un CSV limpio **por semestre** en `DatosArmonizados/2_DatosLimpios/Cursadas/`
- `[ ]` Hacer **commit y push** del script

> Jeronimo tiene tres tareas esta semana además de la limpieza. Si no alcanza la Tarea 4, documentarlo en problemas y priorizarlo la semana siguiente.

---

## Archivos creados o modificados

| Archivo | Acción | Observación |
|---|---|---|
| `1_LimpiezaDatos/02_masterpersonas_Cursadas_JJ.[ext]` | Modificado | Versión final con `fecha_nacimiento` |
| `DatosArmonizados/keys/MASTER_PERSONAS_CURSADAS_PII.csv` | Actualizado | Solo Drive — nunca a GitHub |
| `1_LimpiezaDatos/03_consolidacion_masterpersonas_JJ.[ext]` | Creado/Modificado | Consolidación de los 5 módulos |
| `DatosArmonizados/keys/MASTER_PERSONAS_PII.csv` | Creado | Solo Drive — nunca a GitHub |
| `1_LimpiezaDatos/04_reporte_inconsistencias_masterpersonas_JJ.[ext]` | Creado | Reporte de inconsistencias |
| `logs/reporte_inconsistencias_master_YYYY-MM-DD.md` | Creado | Reporte en el repo (sin datos) |
| `1_LimpiezaDatos/04_limpieza_Cursadas_JJ.[ext]` | Creado/Modificado | Armonización de variables categóricas |
| `DatosArmonizados/2_DatosLimpios/Cursadas/` | Actualizado | CSVs limpios por semestre |

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

**RAs que notificaron disponibilidad de su archivo (antes de consolidar):** (completar — NC / MJC / NJ)

**¿Se encontró `fecha_nacimiento` en Cursadas?** (Sí / No / Parcialmente)

**N personas únicas en MASTER_PERSONAS_PII.csv consolidado:** (completar)

**N personas con inconsistencias de `fecha_nacimiento` entre módulos:** (completar)

**N personas con inconsistencias de `tipo_documento` entre módulos:** (completar)

**Valores únicos de `tipo_calificacion` encontrados en Cursadas:** (completar)

---

## Horas trabajadas (estimado)

| Actividad | Horas |
|---|---|
| Completar `02_masterpersonas_Cursadas_JJ` (con `fecha_nacimiento`) | |
| `03_consolidacion_masterpersonas_JJ` | |
| `04_reporte_inconsistencias_masterpersonas_JJ` | |
| Armonizar variables categóricas en `04_limpieza_Cursadas_JJ` | |
| **Total** | |
