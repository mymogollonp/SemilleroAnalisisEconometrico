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

- `[X]` Agregar columna `fecha_nacimiento` con valor `NA` en todos los registros (Cancelaciones no tiene esta variable — documentarlo en el reporte)
- `[X]` Verificar nuevamente que `tipo_documento`, `sexo` y `nombre_completo` aplican los mapeos canónicos
- `[X]` Confirmar que el output tiene **una fila por `correo`** — sin duplicados
- `[X]` Guardar `MASTER_PERSONAS_CANCELACIONES_PII.csv` actualizado en `DatosArmonizados/keys/` (solo Drive, nunca a GitHub)
- `[X]` Hacer **commit y push** del script actualizado
- `[X]` **Notificar a Jeronimo Jimenez** que el archivo actualizado está disponible en Drive

---

### Tarea 2 — Continuar limpieza: armonizar variables categóricas (Cancelaciones)

**Script:** `03_limpieza_Cancelaciones_MJC.[ext]` (continuar desde semana 03)
**Input:** archivos originales de `DatosOriginales/Cancelaciones/`
**Output:** `DatosArmonizados/2_DatosLimpios/Cancelaciones/Cancelaciones_[YYYY-NS]_limpio.csv`

Semana 03 dejó el script con la estructura básica. Esta semana el foco es armonizar las variables que toman un conjunto reducido de valores.

- `[X]` Armonizar `tipo_cancelacion` — identificar todos los valores únicos presentes en los 32 archivos y mapear a categorías canónicas; documentar el mapeo en este reporte
- `[X]` Armonizar `cod_plan` — estandarizar formato (verificar si hay variantes: con ceros, sin ceros, con guiones)
- `[X]` Armonizar `nivel_formacion` si existe en Cancelaciones — colapsar variantes
- `[X]` Resolver los duplicados identificados en semana 03 (mismo estudiante, mismo semestre, misma materia): documentar la regla de desempate aplicada y consultarle al PI/CoPI si es necesario
- `[X]` Verificar que el output **no contiene PII** (ver regla de privacidad en WORKPLAN Fase 3): confirmar que nombre, correo, cédula y cualquier identificador directo o indirecto fue eliminado
- `[X]` Guardar un CSV limpio **por semestre** en `DatosArmonizados/2_DatosLimpios/Cancelaciones/`
- `[X]` Hacer **commit y push** del script

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

- Tomé la decisión de eliminar los duplicados exactos (aquellos que tuvieran todas las columnas idénticas) y mantuve solo la primera ocurrencia.
- Identifiqué duplicados por llave natural, definidos como registros con la misma combinación de correo electrónico, período, código de plan y código de asignatura, pero con diferencias en alguna de las demás variables. Estos casos se consideraron potencialmente problemáticos, ya que no corresponden a simples copias exactas sino a observaciones inconsistentes o ambiguas. Por esta razón, todos los grupos detectados se exportaron a un archivo independiente (duplicados_llave_natural.csv) para su revisión y validación posterior con el PI/CoPI. Por ahora, deje solo la primera observación de estos casos.

---

## Comentarios adicionales

**`fecha_nacimiento` en Cancelaciones:** No existe en la fuente — columna agregada como `NA`.

**Valores únicos de `tipo_cancelacion` encontrados:**

ANULADA_SIN_PERDIDA_CREDITOS
CANCELADA_CON_PERDIDA_CREDITOS

**Mapeo aplicado para `tipo_cancelacion`:**

No se aplicó recodificación adicional, ya que los valores encontrados ya corresponden a categorías consistentes y mutuamente excluyentes.

**Regla de desempate aplicada para duplicados:**

Se eliminaron duplicados exactos conservando la primera ocurrencia (keep='first'). Para duplicados por llave natural (correo + PERIODO + COD_PLAN + COD_ASIGNATURA), se conservó provisionalmente la primera ocurrencia (keep='first') y los casos fueron exportados a duplicados_llave_natural.csv para revisión posterior con PI/CoPI.

**N personas únicas en MASTER_PERSONAS_CANCELACIONES_PII.csv:**

76,415 estudiantes únicos (identificados por correo institucional).

---

## Horas trabajadas (estimado)

| Actividad | Horas |
|---|---|
| Actualizar `02_masterpersonas_Cancelaciones_MJC` (agregar `fecha_nacimiento`) | 20 min|
| Armonizar variables categóricas en `03_limpieza_Cancelaciones_MJC` | 1 hora |
| **Total** | 1h 20min|
