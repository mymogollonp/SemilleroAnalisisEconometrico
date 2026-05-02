# Reporte Semanal — Semana 03
## RA: Maria Jose Cadena | Dataset: Cancelaciones

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

### Tarea 1 — Finalizar Master Dataset de Personas (Cancelaciones)

**Script:** `02_masterpersonas_Cancelaciones_MJC.[ext]` (continuar o completar)
**Output en Drive:** `DatosArmonizados/keys/MASTER_PERSONAS_CANCELACIONES_PII.csv`

- `[X]` Verificar que el script aplica todos los mapeos canónicos de `tipo_documento` y `sexo` (ver WORKPLAN Paso 1b)
- `[X]` Verificar que `nombre_completo` está en mayúsculas y sin caracteres especiales
- `[X]` Verificar longitud válida de `numero_documento` por tipo
- `[X]` Crear columnas adicionales (`tipo_documento2`, `sexo2`, etc.) si hay cambios entre semestres
- `[X]` Incluir `fecha_nacimiento` si existe en los archivos de Cancelaciones
- `[X]` Guardar `MASTER_PERSONAS_CANCELACIONES_PII.csv` en `DatosArmonizados/keys/` (solo Drive)
- `[X]` Hacer **commit y push** del script
- `[X]` **Notificar a Jeronimo Jimenez** que el archivo está disponible en Drive

---

### Tarea 2 — Iniciar script de Limpieza de Datos (Cancelaciones)

**Script a crear:** `03_limpieza_Cancelaciones_MJC.[ext]`
**Ubicación en repo:** `1_LimpiezaDatos/`
**Input:** archivos originales de `DatosOriginales/Cancelaciones/`

Basado en los hallazgos del inventario (semana 01), iniciar el script de limpieza que:

- `[X]` Carga todos los archivos de Cancelaciones
- `[X]` Estandariza nombres de variables al nombre canónico
- `[X]` Estandariza el formato del período de cancelación a `YYYY-NS`
- `[X]` Detecta y documenta duplicados en el output limpio
- `[X]` Hacer **commit y push** del script (aunque esté incompleto)

---

## Archivos creados o modificados

| Archivo | Acción | Observación |
|---|---|---|
| `1_LimpiezaDatos/02_masterpersonas_Cancelaciones_MJC.[ext]` | Modificado | Versión final con todos los mapeos |
| `DatosArmonizados/keys/MASTER_PERSONAS_CANCELACIONES_PII.csv` | Creado/Actualizado | Solo Drive — nunca a GitHub |
| `1_LimpiezaDatos/03_limpieza_Cancelaciones_MJC.[ext]` | Creado | Inicio del script de limpieza |

---

## Problemas encontrados

| # | Descripción del problema | Dato o archivo afectado | Estado |
|---|---|---|---|
| | | | |

---

## Preguntas para el PI/CoPI

- Hay duplicados exactos (mismo estudiante, mismo semestre, mismo plan, misma materia). En un caso solo cambia el tipo de cancelación, eso es posible? En otros no cambia el tipo de cancelación.

---

## Comentarios adicionales

**¿Se encontró `fecha_nacimiento` en Cancelaciones?** (Sí/No)

No

**Formato del período de cancelación confirmado:** (completar)

YYYY-NS

**Avance del script de limpieza:** (describir hasta dónde llegaste esta semana)

Se creó el script 03_limpieza_Cancelaciones_MJC.py en 1_LimpiezaDatos/. El script carga los 32 archivos .xlsx de DatosOriginales/Cancelaciones/ (manejando el caso especial de Cancelaciones_2024-2S que usa Sheet2), los apila en un DataFrame único de 354.801 filas, y aplica las siguientes transformaciones: (1) armoniza los nombres canónicos de variables PII (CORREO_INSTITUCIONAL → correo, DOCUMENTO → numero_documento, NOMBRES_APELLIDOS → nombre_completo), crea las columnas tipo_documento, sexo y fecha_nacimiento como vacías dado que no existen en esta fuente, y normaliza nombre_completo eliminando tildes, reemplazando Ñ por N y convirtiendo a mayúsculas; (2) valida que el formato de PERIODO cumpla YYYY-NS en todos los archivos; (3) estandariza tipos de dato por columna; (4) normaliza COD_PLAN a string; (5) aplica strip de espacios en variables de texto; (6) reporta cobertura de las 6 variables intermitentes; y (7) detecta duplicados usando la llave correo + PERIODO + COD_PLAN + COD_ASIGNATURA. El script genera un log con todos los diagnósticos y guarda el output consolidado en DatosArmonizados/Cancelaciones/Cancelaciones_limpio.csv. El script corre sin errores y produce el CSV de salida.

---

## Horas trabajadas (estimado)

| Actividad | Horas |
|---|---|
| Finalizar `02_masterpersonas_Cancelaciones_MJC` | 30 min|
| Iniciar `03_limpieza_Cancelaciones_MJC` | 2 horas|
| **Total** | |
