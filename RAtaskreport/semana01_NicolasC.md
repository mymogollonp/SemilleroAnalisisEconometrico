# Reporte Semanal — Semana 01
## RA: Nicolas Camacho | Dataset: Matriculados

**Semana:** 01 (2026-04-13 → 2026-04-19)
**Fecha de entrega del reporte:** 2026-04-19
**Fase del proyecto:** Fase 0 — Infraestructura y Llave de Anonimización

---

## Reglas del proyecto

> Ver [RULES_RA.md](../RULES_RA.md) para la versión completa.

**R1:** Hacer commit y push al terminar cada script.
**R2:** Actualizar este reporte cuando termines, avances o bloquees una tarea (`[ ]` → `[x]`, `[-]`, o `[!]`).
**R3:** No subir datos a GitHub (`.csv`, `.xlsx`, `.zip`).
**R4:** Un script por tarea — no combinar fases.
**R5:** Todas las rutas en el archivo de configuración (`00_configuracion.do`, `00_config.R` o `00_config.py`). Nunca hardcodear paths.
**R6:** `DatosOriginales/` es de solo lectura — los scripts solo leen, nunca escriben allí.
**R7:** Documentar la semilla en todo script que use aleatoriedad.

---

## Tareas asignadas esta semana

### Tarea inicial — Script de exploración propio

> Antes de ejecutar los scripts generados por Claude, escribe tu propio código de exploración en el lenguaje de tu preferencia (R, Python o Stata).

- `[ ]` Escribir un script `EX_Matriculados_NC.[ext]` que abra uno de los archivos de tu módulo, liste las variables, muestre las primeras filas y reporte el número de observaciones
- `[ ]` Hacer **commit y push** del script

### Tareas comunes del equipo (Fase 0 — Infraestructura)

- `[ ]` Leer `WORKPLAN.md` y `requirements-spec.md` completos y confirmar entendimiento
- `[ ]` Firmar el acuerdo de confidencialidad (`Acuerdo de confidencialidad Semillero Analisis Econometrico.docx`)
- `[ ]` Clonar el repositorio de código en tu máquina local
- `[ ]` Verificar acceso a la carpeta de datos en Drive (`DatosOriginales/`)
- `[ ]` Crear las carpetas de salida en Drive si no existen: `DatosArmonizados/keys/`, `1_DatosAnonimizados/Matriculado/`
- `[ ]` Abrir `00_configuracion.do`, agregar tu bloque de rutas con `c(username)` y las rutas reales de tu PC, hacer **commit y push**

### Tareas específicas — Inventario de Matriculados

> El script `1_LimpiezaDatos/02_inventario_matriculados.do` es un **script de referencia** generado previamente. No estás obligado a ejecutarlo — escribe tu propio script de inventario en el lenguaje de tu preferencia (R, Python o Stata).

- `[ ]` Escribir tu propio script de inventario para Matriculados
- `[ ]` El script debe: abrir cada archivo, listar variables y tipos, contar missings, comparar encabezados entre años, reportar N observaciones por archivo
- `[ ]` Documentar en "Comentarios adicionales": nombre exacto del campo de ID personal, lista de variables, si los nombres cambian entre años
- `[ ]` Identificar la(s) variable(s) que identifican de forma única una observación en Matriculados
- `[ ]` Hacer **commit y push** del script de inventario

### Tareas específicas — Master Dataset de Personas (Matriculados)

- `[ ]` A partir del inventario, identificar las variables de: correo/email, tipo de documento, número de documento, nombre completo, sexo/género
- `[ ]` Escribir un script que itere sobre **todos** los archivos Matriculados (no solo el más reciente)
- `[ ]` Armonizar nombres de variables en el output: usar `correo`, `tipo_documento`, `numero_documento`, `nombre_completo`, `sexo` como nombres canónicos
- `[ ]` **Sexo/género**: registrar **todos los valores distintos observados por persona** — una persona puede cambiar de género entre períodos; conservar todos los pares `(correo, sexo, periodo)`, no reducir a uno
- `[ ]` **Tipo de documento**: registrar todos los tipos encontrados (CC, CE, PA, TI, NUIP, PEP u otros); reportar cualquier código no reconocido
- `[ ]` **Verificar formato de número de documento**: CC (6–10 dígitos numéricos), CE (alfanumérico), PA (alfanumérico), TI (10–11 dígitos); anotar registros con formato inesperado
- `[ ]` Guardar como `DatosArmonizados/keys/MASTER_PERSONAS_MATRICULADOS_PII.csv` (solo en Drive, nunca a GitHub)
- `[ ]` Hacer **commit y push** del script

### Tareas específicas — Diccionario de variables

- `[ ]` Abrir `Diccionarios/Dicionario_Matriculados.xlsx` en Drive
- `[ ]` Completar las filas faltantes y verificar la información existente con base en el inventario
- `[ ]` Documentar en "Comentarios adicionales" cualquier variable no documentada o discrepancia encontrada

### Tareas específicas — Llave de anonimización

> **Prerequisito:** esta tarea depende de que el PI o Data Scientist haya consolidado todos los `MASTER_PERSONAS_[MODULO]_PII.csv` en `MASTER_PERSONAS_PII.csv`. Esperar confirmación antes de proceder.

> El script `1_LimpiezaDatos/01_crear_llave_idunal.do` es un **script de referencia**. Escribe tu propio script de generación de llave en el lenguaje de tu preferencia.

- `[ ]` Esperar confirmación del PI/Data Scientist de que `MASTER_PERSONAS_PII.csv` está disponible
- `[ ]` Escribir un script que:
  - Lea `DatosArmonizados/keys/MASTER_PERSONAS_PII.csv`
  - Genere `id_unal` mediante permutación aleatoria con semilla `20260223`, formato `UNAL000001`
  - Guarde el crosswalk como `LLAVE_ID_UNAL_FCE.csv` en `DatosArmonizados/keys/`
- `[ ]` Verificar que no hay duplicados en `id_unal` y que todos los registros tienen llave asignada
- `[ ]` Reportar el número total de personas únicas en la llave
- `[ ]` Notificar al equipo (PI/CoPI y demás RAs) que `LLAVE_ID_UNAL_FCE.csv` está disponible
- `[ ]` Hacer **commit y push** del script

> **Nota:** la llave es prerequisito para la anonimización de todos los módulos. Priorizar esta tarea una vez que `MASTER_PERSONAS_PII.csv` esté listo.

---

## Archivos creados o modificados

| Archivo | Acción | Observación |
|---|---|---|
| `00_configuracion.do` / `00_config.R` / `00_config.py` | Modificado | Agregar bloque de rutas para tu PC |
| `EX_Matriculados_NC.[ext]` | Creado | Script de exploración inicial |
| `[tu_script_inventario_NC].[ext]` | Creado | Script de inventario propio |
| `[tu_script_master_personas_NC].[ext]` | Creado | Script que genera MASTER_PERSONAS_MATRICULADOS_PII |
| `DatosArmonizados/keys/MASTER_PERSONAS_MATRICULADOS_PII.csv` | Creado | PII confidencial — solo en Drive, nunca a GitHub |
| `[tu_script_llave_NC].[ext]` | Creado | Script de generación de llave (solo si MASTER_PERSONAS_PII está disponible) |
| `DatosArmonizados/keys/LLAVE_ID_UNAL_FCE.csv` | Creado | Crosswalk confidencial — solo en Drive, nunca a GitHub |

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

**Campo de ID personal identificado:** (completar — ej. "El campo se llama `correo_unal` en todos los archivos")

**¿El campo de ID cambia de nombre entre años?** (completar — Sí / No / Parcialmente; si Sí, listar qué nombres encontró)

**Variables en Matriculados:** (completar — pegar la lista de variables del inventario)

**¿Inconsistencias de variables entre archivos?** (completar — Sí / No; si Sí, detallar)

**Clave única de observación en Matriculados:** (completar — ej. "La variable `correo_unal` identifica de forma única cada fila" o "La clave compuesta es (`correo_unal`, `cod_plan`)")

**Número de personas únicas en MASTER_PERSONAS_MATRICULADOS_PII:** (completar)

**Tipos de documento encontrados en Matriculados:** (completar — ej. "CC: 94%, CE: 5%, PA: 1%")

**Personas con más de un valor de sexo/género registrado:** (completar — N casos; describir brevemente si es posible)

**Registros con formato de documento inválido:** (completar — N registros; describir el problema)

**Discrepancias o variables no documentadas en `Dicionario_Matriculados.xlsx`:** (completar)

**Número total de personas en la llave (`LLAVE_ID_UNAL_FCE.csv`):** (completar — solo si la tarea se completó esta semana)

---

## Horas trabajadas (estimado)

| Actividad | Horas |
|---|---|
| Lectura de documentación y configuración | |
| Escritura de script de exploración (`EX_Matriculados_NC`) | |
| Configurar archivo de rutas | |
| Escritura y ejecución de script de inventario propio | |
| Escritura de script Master Personas Matriculados PII | |
| Completar `Dicionario_Matriculados.xlsx` | |
| Escritura de script de generación de llave (si aplica) | |
| **Total** | |
