# Reporte Semanal — Semana 04
## RA: Nicolas Camacho | Dataset: Matriculados

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

### Tarea 1 — Completar Master Dataset de Personas (Matriculados) — versión final

**Script:** `02_masterpersonas_Matriculados_NC.[ext]`
**Output en Drive:** `DatosArmonizados/keys/MASTER_PERSONAS_MATRICULADOS_PII.csv`

El objetivo esta semana es entregar la versión **definitiva** del master de personas de Matriculados, lista para que Jeronimo la consolide con los demás módulos.

- `[ ]` Incluir `fecha_nacimiento` — buscarla en los archivos de Matriculados y registrarla en formato `YYYY-MM-DD`; si no existe en ningún archivo, dejar la columna como `NA` y documentarlo
- `[ ]` Verificar que `tipo_documento` aplica el mapeo canónico completo (CC, CE, PA, TI, PEP, OTRO)
- `[ ]` Verificar que `sexo` aplica el mapeo canónico completo (M, F, X, NA)
- `[ ]` Verificar que `nombre_completo` está en mayúsculas y sin tildes ni caracteres especiales
- `[ ]` Verificar longitud válida de `numero_documento` por tipo; anotar en problemas cualquier documento fuera de rango
- `[ ]` Confirmar que el output tiene **una fila por `correo`** — sin duplicados
- `[ ]` Guardar `MASTER_PERSONAS_MATRICULADOS_PII.csv` en `DatosArmonizados/keys/` (solo Drive, nunca a GitHub)
- `[ ]` Hacer **commit y push** del script actualizado
- `[ ]` **Notificar a Jeronimo Jimenez** que el archivo está disponible en Drive

---

### Tarea 2 — Continuar limpieza: armonizar variables categóricas (Matriculados)

**Script:** `03_limpieza_Matriculados_NC.[ext]` (continuar desde semana 03)
**Input:** archivos originales de `DatosOriginales/Matriculado/`
**Output:** `DatosArmonizados/2_DatosLimpios/Matriculado/Matriculados_[YYYY-NS]_limpio.csv`

Esta semana el foco es estandarizar las variables que toman un conjunto reducido de valores (categóricas). Estas son las más fáciles de armonizar y forman la base del panel.

- `[ ]` Armonizar `tipo_admision` — identificar todos los valores únicos presentes y mapear a categorías canónicas; documentar el mapeo en este reporte
- `[ ]` Armonizar `nivel_formacion` (pregrado, especialización, maestría, doctorado) — identificar variantes y colapsar
- `[ ]` Armonizar `sede` — verificar que todos los registros corresponden a Bogotá; documentar cualquier excepción
- `[ ]` Armonizar `estrato` — verificar rango 1–6; documentar valores fuera de rango
- `[ ]` Verificar que el output **no contiene PII** (ver regla de privacidad en WORKPLAN Fase 3): eliminar nombre, correo, cédula, dirección y cualquier variable de identificación directa o indirecta
- `[ ]` Guardar un CSV limpio **por semestre** en `DatosArmonizados/2_DatosLimpios/Matriculado/`
- `[ ]` Hacer **commit y push** del script

---

## Archivos creados o modificados

| Archivo | Acción | Observación |
|---|---|---|
| `1_LimpiezaDatos/02_masterpersonas_Matriculados_NC.[ext]` | Modificado | Versión final con `fecha_nacimiento` |
| `DatosArmonizados/keys/MASTER_PERSONAS_MATRICULADOS_PII.csv` | Actualizado | Solo Drive — nunca a GitHub |
| `1_LimpiezaDatos/03_limpieza_Matriculados_NC.[ext]` | Modificado | Armonización de variables categóricas |
| `DatosArmonizados/2_DatosLimpios/Matriculado/` | Actualizado | CSVs limpios por semestre |

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

**¿Se encontró `fecha_nacimiento` en Matriculados?** (Sí / No / Parcialmente — indicar en qué archivos)

**Valores únicos de `tipo_admision` encontrados:** (completar — pegar lista)

**Valores únicos de `nivel_formacion` encontrados:** (completar — pegar lista)

**Mapeo aplicado para `tipo_admision`:** (completar — ej. "REGULAR → Regular, PEAMA → PEAMA")

**N personas únicas en MASTER_PERSONAS_MATRICULADOS_PII.csv:** (completar)

---

## Horas trabajadas (estimado)

| Actividad | Horas |
|---|---|
| Completar `02_masterpersonas_Matriculados_NC` (con `fecha_nacimiento`) | |
| Armonizar variables categóricas en `03_limpieza_Matriculados_NC` | |
| **Total** | |
