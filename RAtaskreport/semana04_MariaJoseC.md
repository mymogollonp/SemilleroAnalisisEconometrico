# Reporte Semanal — Semana 04
## RA: Maria Jose Cadena | Dataset: Cancelaciones

**Semana:** 04 (2026-05-04 → 2026-05-10)
**Fecha de entrega del reporte:** 2026-05-10
**Fase del proyecto:** Fase 1 — Master Personas PII (versión final) | Fase 3 — Limpieza de variables categóricas

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

### Tarea 1 — Completar Master Dataset de Personas (Cancelaciones) — versión final

**Script:** `02_masterpersonas_Cancelaciones_MJC.[ext]`
**Output en Drive:** `DatosArmonizados/keys/MASTER_PERSONAS_CANCELACIONES_PII.csv`

El master de semana 03 no incluía `fecha_nacimiento` porque no existe en Cancelaciones. Esta semana se cierra formalmente el archivo con esa columna explícita como `NA` para que la consolidación de Jeronimo sea consistente entre módulos.

- `[ ]` Agregar columna `fecha_nacimiento` con valor `NA` en todos los registros (Cancelaciones no tiene esta variable — documentarlo en el reporte)
- `[ ]` Verificar nuevamente que `tipo_documento`, `sexo` y `nombre_completo` aplican los mapeos canónicos
- `[ ]` Confirmar que el output tiene **una fila por `correo`** — sin duplicados
- `[ ]` Guardar `MASTER_PERSONAS_CANCELACIONES_PII.csv` actualizado en `DatosArmonizados/keys/` (solo Drive, nunca a GitHub)
- `[ ]` Hacer **commit y push** del script actualizado
- `[ ]` **Notificar a Jeronimo Jimenez** que el archivo actualizado está disponible en Drive

---

### Tarea 2 — Continuar limpieza: armonizar variables categóricas (Cancelaciones)

**Script:** `03_limpieza_Cancelaciones_MJC.[ext]` (continuar desde semana 03)
**Input:** archivos originales de `DatosOriginales/Cancelaciones/`
**Output:** `DatosArmonizados/2_DatosLimpios/Cancelaciones/Cancelaciones_[YYYY-NS]_limpio.csv`

Semana 03 dejó el script con la estructura básica. Esta semana el foco es armonizar las variables que toman un conjunto reducido de valores.

- `[ ]` Armonizar `tipo_cancelacion` — identificar todos los valores únicos presentes en los 32 archivos y mapear a categorías canónicas; documentar el mapeo en este reporte
- `[ ]` Armonizar `cod_plan` — estandarizar formato (verificar si hay variantes: con ceros, sin ceros, con guiones)
- `[ ]` Armonizar `nivel_formacion` si existe en Cancelaciones — colapsar variantes
- `[ ]` Resolver los duplicados identificados en semana 03 (mismo estudiante, mismo semestre, misma materia): documentar la regla de desempate aplicada y consultarle al PI/CoPI si es necesario
- `[ ]` Verificar que el output **no contiene PII** (ver regla de privacidad en WORKPLAN Fase 3): confirmar que nombre, correo, cédula y cualquier identificador directo o indirecto fue eliminado
- `[ ]` Guardar un CSV limpio **por semestre** en `DatosArmonizados/2_DatosLimpios/Cancelaciones/`
- `[ ]` Hacer **commit y push** del script

---

## Archivos creados o modificados

| Archivo | Acción | Observación |
|---|---|---|
| `1_LimpiezaDatos/02_masterpersonas_Cancelaciones_MJC.[ext]` | Modificado | Agrega `fecha_nacimiento = NA` |
| `DatosArmonizados/keys/MASTER_PERSONAS_CANCELACIONES_PII.csv` | Actualizado | Solo Drive — nunca a GitHub |
| `1_LimpiezaDatos/03_limpieza_Cancelaciones_MJC.[ext]` | Modificado | Armonización de variables categóricas |
| `DatosArmonizados/2_DatosLimpios/Cancelaciones/` | Actualizado | CSVs limpios por semestre |

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

**`fecha_nacimiento` en Cancelaciones:** No existe en la fuente — columna agregada como `NA`.

**Valores únicos de `tipo_cancelacion` encontrados:** (completar — pegar lista)

**Mapeo aplicado para `tipo_cancelacion`:** (completar)

**Regla de desempate aplicada para duplicados:** (completar — ej. "Se conservó el registro con el tipo de cancelación más reciente")

**N personas únicas en MASTER_PERSONAS_CANCELACIONES_PII.csv:** (completar)

---

## Horas trabajadas (estimado)

| Actividad | Horas |
|---|---|
| Actualizar `02_masterpersonas_Cancelaciones_MJC` (agregar `fecha_nacimiento`) | |
| Armonizar variables categóricas en `03_limpieza_Cancelaciones_MJC` | |
| **Total** | |
