# Reporte Semanal — Semana 04
## RA: Nicolas Jimenez | Dataset: Egresados y Retirados

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

### Tarea 1a — Completar Master Dataset de Personas (Egresados) — versión final

**Script:** `02_masterpersonas_Egresados_NJ.[ext]`
**Output en Drive:** `DatosArmonizados/keys/MASTER_PERSONAS_EGRESADOS_PII.csv`

- `[x]` Incluir `fecha_nacimiento` — buscarla en los archivos de Egresados y registrarla en formato `YYYY-MM-DD`; si no existe, dejar la columna como `NA` y documentarlo
- `[x]` Verificar que `tipo_documento` aplica el mapeo canónico completo (CC, CE, PA, TI, PEP, OTRO)
- `[x]` Verificar que `sexo` aplica el mapeo canónico completo (M, F, X, NA)
- `[x]` Verificar que `nombre_completo` está en mayúsculas y sin tildes ni caracteres especiales
- `[x]` Verificar longitud válida de `numero_documento` por tipo
- `[x]` Confirmar que el output tiene **una fila por `correo`** — sin duplicados
- `[x]` Guardar `MASTER_PERSONAS_EGRESADOS_PII.csv` en `DatosArmonizados/keys/` (solo Drive, nunca a GitHub)
- `[x]` Hacer **commit y push** del script actualizado

---

### Tarea 1b — Completar Master Dataset de Personas (Retirados) — versión final

**Script:** `02_masterpersonas_Retirados_NJ.[ext]`
**Output en Drive:** `DatosArmonizados/keys/MASTER_PERSONAS_RETIRADOS_PII.csv`

- `[x]` Incluir `fecha_nacimiento` — buscarla en `Retirados_desde_2009.xlsx` y registrarla en formato `YYYY-MM-DD`; si no existe, dejar como `NA` y documentarlo
- `[x]` Verificar que `tipo_documento` aplica el mapeo canónico completo
- `[x]` Verificar que `sexo` aplica el mapeo canónico completo
- `[x]` Verificar que `nombre_completo` está en mayúsculas y sin caracteres especiales
- `[x]` Verificar longitud válida de `numero_documento` por tipo
- `[x]` Confirmar que el output tiene **una fila por `correo`** — sin duplicados
- `[x]` Guardar `MASTER_PERSONAS_RETIRADOS_PII.csv` en `DatosArmonizados/keys/` (solo Drive, nunca a GitHub)
- `[x]` Hacer **commit y push** del script actualizado
- `[x]` **Notificar a Jeronimo Jimenez** que ambos archivos (Egresados y Retirados) están disponibles en Drive

---

### Tarea 2 — Continuar limpieza: armonizar variables categóricas (Egresados)

**Script:** `03_limpieza_Egresados_NJ.[ext]` (continuar desde semana 03)
**Input:** archivos originales de `DatosOriginales/Egresados/`
**Output:** `DatosArmonizados/2_DatosLimpios/Egresados/Egresados_[YYYY-NS]_limpio.csv`

- `[x]` Armonizar `tipo_titulo` o `nivel_titulo` — identificar todos los valores únicos y mapear a categorías canónicas (ej. pregrado, especialización, maestría, doctorado); documentar el mapeo en este reporte
- `[x]` Armonizar `modalidad` si existe — identificar variantes y colapsar
- `[x]` Estandarizar `cod_plan` — verificar formato consistente entre semestres
- `[x]` Verificar que el output **no contiene PII** (ver regla de privacidad en WORKPLAN Fase 3): confirmar que nombre, correo, cédula, nombre del director de tesis, título de la tesis y cualquier identificador directo o indirecto fue eliminado
- `[ ]` Guardar un CSV limpio **por semestre** en `DatosArmonizados/2_DatosLimpios/Egresados/`
- `[x]` Hacer **commit y push** del script

---

### Tarea 3 — Continuar limpieza: armonizar variables categóricas (Retirados)

**Script:** `03_limpieza_Retirados_NJ.[ext]` (continuar desde semana 03)
**Input:** `DatosOriginales/Retirados/Retirados_desde_2009.xlsx`
**Output:** `DatosArmonizados/2_DatosLimpios/Retirados/Retirados_limpio.csv` (archivo único)

- `[x]` Armonizar `tipo_retiro` o `causal_retiro` — identificar todos los valores únicos y mapear a categorías canónicas; documentar el mapeo en este reporte
- `[x]` Verificar que el período de retiro está en formato `YYYY-NS`; corregir variantes
- `[x]` Verificar que el output **no contiene PII** (ver regla de privacidad en WORKPLAN Fase 3)
- `[ ]` Guardar `Retirados_limpio.csv` en `DatosArmonizados/2_DatosLimpios/Retirados/`
- `[ ]` Hacer **commit y push** del script

> Nicolas tiene cuatro tareas esta semana. Si no alcanza ambas limpiezas, priorizar Egresados y documentar en problemas.

---

## Archivos creados o modificados

| Archivo | Acción | Observación |
|---|---|---|
| `1_LimpiezaDatos/02_masterpersonas_Egresados_NJ.[ext]` | Modificado | Versión final con `fecha_nacimiento` |
| `1_LimpiezaDatos/02_masterpersonas_Retirados_NJ.[ext]` | Modificado | Versión final con `fecha_nacimiento` |
| `DatosArmonizados/keys/MASTER_PERSONAS_EGRESADOS_PII.csv` | Actualizado | Solo Drive — nunca a GitHub |
| `DatosArmonizados/keys/MASTER_PERSONAS_RETIRADOS_PII.csv` | Actualizado | Solo Drive — nunca a GitHub |
| `1_LimpiezaDatos/03_limpieza_Egresados_NJ.[ext]` | Modificado | Armonización de variables categóricas |
| `1_LimpiezaDatos/03_limpieza_Retirados_NJ.[ext]` | Modificado | Armonización de variables categóricas |
| `DatosArmonizados/2_DatosLimpios/Egresados/` | Actualizado | CSVs limpios por semestre |
| `DatosArmonizados/2_DatosLimpios/Retirados/` | Actualizado | CSV único limpio |

---

## Problemas encontrados

| # | Descripción del problema | Dato o archivo afectado | Estado |
|---|---|---|---|
| | | | |

---

## Preguntas para el PI/CoPI
Existen columnas que no sé si debo retirar en los archivos limpios, estas son: hist_academica, SNIES, y diploma.


---

## Comentarios adicionales
Aún no se elimina la columna correo en los archivos de limpieza, esto para realizar posteriormente el proceso de anonimización.
**¿Se encontró `fecha_nacimiento` en Egresados?** Sí 

**¿Se encontró `fecha_nacimiento` en Retirados?** No

**Valores únicos de `tipo_titulo` / `nivel_titulo` encontrados en Egresados:** (completar)
La columna NIVEL en ambos módulos tiene 5 valores: PREGRADO, ESPECIALIZACIÓN, ESPECIALIDAD, MAESTRÍA, DOCTORADO
**Mapeo aplicado para `tipo_titulo`:** (completar)
Argumento que especialidad y especialización son lo mismo, por lo que todos los valores de ESPECIALIDAD fueron convertidos a ESPECIALIZACIÓN
**Valores únicos de `tipo_retiro` / `causal_retiro` encontrados en Retirados:** (completar)
9
**Mapeo aplicado para `tipo_retiro`:** (completar)
Ninguno, ya que se verifica que entre la columna BLOQUEO (descripción del bloqueo) y la columna COD_BLOQUEO no hay inconsistencias, hay una relación 1 a 1, por lo que no vi necesario un mapeo.
**N personas únicas en MASTER_PERSONAS_EGRESADOS_PII.csv:** (completar)
79.948
**N personas únicas en MASTER_PERSONAS_RETIRADOS_PII.csv:** (completar)
41.394
---

## Horas trabajadas (estimado)

| Actividad | Horas |
|---|---|
| Completar `02_masterpersonas_Egresados_NJ` (con `fecha_nacimiento`) |0|
| Completar `02_masterpersonas_Retirados_NJ` (con `fecha_nacimiento`) |1|
| Armonizar variables categóricas en `03_limpieza_Egresados_NJ` |2|
| Armonizar variables categóricas en `03_limpieza_Retirados_NJ` |2|
| **Total** |5|
