# Reporte Semanal — Semana 01
## RA: Nicolas Jimenez | Dataset: Egresados y Retirados

**Semana:** 01 (2026-04-13 → 2026-04-19)
**Fecha de entrega del reporte:** 2026-04-19
**Fase del proyecto:** Fase 0 — Infraestructura / inicio Fase 1 — Anonimización

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

- `[ ]` Escribir un script `EX_Egresados_NJ.[ext]` (o `EX_Retirados_NJ.[ext]`) que abra uno de los archivos de tu módulo, liste las variables, muestre las primeras filas y reporte el número de observaciones
- `[ ]` Hacer **commit y push** del script

### Tareas comunes del equipo (Fase 0 — Infraestructura)

- `[ ]` Leer `WORKPLAN.md` y `requirements-spec.md` completos y confirmar entendimiento
- `[ ]` Firmar el acuerdo de confidencialidad (`Acuerdo de confidencialidad Semillero Analisis Econometrico.docx`)
- `[ ]` Clonar el repositorio de código en tu máquina local
- `[ ]` Verificar acceso a la carpeta de datos en Drive (`DatosOriginales/`)
- `[ ]` Crear las subcarpetas `DatosArmonizados/1_DatosAnonimizados/Egresados/` y `.../Retirados/` en Drive
- `[ ]` Abrir `00_configuracion.do`, agregar tu bloque de rutas con `c(username)` y las rutas reales de tu PC, hacer **commit y push**

### Tareas específicas — Inventario de Egresados

> El script `1_LimpiezaDatos/02_inventario_egresados.do` es un **script de referencia** generado previamente. No estás obligado a ejecutarlo — escribe tu propio script de inventario en el lenguaje de tu preferencia (R, Python o Stata).

- `[ ]` Escribir tu propio script de inventario para Egresados
- `[ ]` El script debe: abrir cada archivo, listar variables y tipos, contar missings, comparar encabezados entre años, mostrar ejemplos de valores para la fecha de grado, reportar N observaciones por archivo
- `[ ]` Documentar en "Comentarios adicionales":
  - Nombre exacto del campo de ID personal
  - Lista completa de variables
  - Si los nombres de variables cambian entre años
  - Cómo está codificada la fecha de grado (ejemplos de valores)
  - La(s) variable(s) que identifican de forma única una observación
- `[ ]` Hacer **commit y push** del script de inventario

### Tareas específicas — Inventario de Retirados

> El script `1_LimpiezaDatos/02_inventario_retirados.do` es un **script de referencia** generado previamente. No estás obligado a ejecutarlo — escribe tu propio script de inventario.

- `[ ]` Escribir tu propio script de inventario para Retirados (archivo único: `Retirados_desde_2009.xlsx`)
- `[ ]` El script debe: listar variables y tipos, contar missings, mostrar ejemplos de valores para el período de retiro, reportar N total de observaciones
- `[ ]` Documentar en "Comentarios adicionales":
  - Nombre del campo de ID personal
  - Variables disponibles
  - Cómo está codificado el período de retiro (ejemplos)
  - Número total de observaciones
  - La(s) variable(s) que identifican de forma única una observación
- `[ ]` Hacer **commit y push** del script de inventario

### Tareas específicas — Master Dataset de Personas (Egresados y Retirados)

- `[ ]` A partir de los inventarios, identificar las variables de: correo/email, tipo de documento, número de documento, nombre completo, sexo/género en cada módulo
- `[ ]` Escribir un script que itere sobre **todos** los archivos Egresados y construya el Master Personas de Egresados
- `[ ]` Escribir un script para Retirados (archivo único `Retirados_desde_2009.xlsx`) que construya el Master Personas de Retirados
- `[ ]` En ambos scripts: armonizar nombres de variables al output canónico: `correo`, `tipo_documento`, `numero_documento`, `nombre_completo`, `sexo`
- `[ ]` **Sexo/género**: registrar **todos los valores distintos observados por persona** — una persona puede cambiar de género entre períodos; conservar todos los pares `(correo, sexo, periodo)`, no reducir a uno
- `[ ]` **Tipo de documento**: registrar todos los tipos encontrados (CC, CE, PA, TI, NUIP, PEP u otros); reportar cualquier código no reconocido
- `[ ]` **Verificar formato de número de documento**: CC (6–10 dígitos numéricos), CE (alfanumérico), PA (alfanumérico), TI (10–11 dígitos); anotar registros con formato inesperado
- `[ ]` Guardar: `DatosArmonizados/keys/MASTER_PERSONAS_EGRESADOS_PII.csv` y `MASTER_PERSONAS_RETIRADOS_PII.csv` (solo en Drive, nunca a GitHub)
- `[ ]` Hacer **commit y push** de los scripts

### Tareas específicas — Diccionario de variables

- `[ ]` Abrir `Diccionarios/Diccionario_Egresados.xlsx` en Drive y completar las filas faltantes
- `[ ]` Abrir `Diccionarios/Dicionario_Retirados.xlsx` en Drive y completar las filas faltantes
- `[ ]` Documentar en "Comentarios adicionales" cualquier variable no documentada o discrepancia encontrada

### Tareas específicas — Anonimización

> Dependencia: requiere que Nicolas Camacho haya generado y compartido `LLAVE_ID_UNAL_FCE.csv`.

- `[ ]` Esperar confirmación de Nicolas Camacho de que la llave está disponible
- `[ ]` Si la llave está disponible esta semana:
  - Escribir tu propio script `1_LimpiezaDatos/10_anonimizar_egresados.[ext]`, hacer **commit y push**
  - Escribir tu propio script `1_LimpiezaDatos/11_anonimizar_retirados.[ext]`, hacer **commit y push**

> **Nota:** Retirados tiene un solo archivo — una vez disponible la llave, `11_anonimizar_retirados.[ext]` puede completarse rápidamente.

---

## Archivos creados o modificados

| Archivo | Acción | Observación |
|---|---|---|
| `00_configuracion.do` / `00_config.R` / `00_config.py` | Modificado | Agregar bloque de rutas para tu PC |
| `EX_Egresados_NJ.[ext]` o `EX_Retirados_NJ.[ext]` | Creado | Script de exploración inicial |
| `[tu_script_inventario_egresados_NJ].[ext]` | Creado | Script de inventario propio — Egresados |
| `[tu_script_inventario_retirados_NJ].[ext]` | Creado | Script de inventario propio — Retirados |
| `[tu_script_master_egresados_NJ].[ext]` | Creado | Script que genera MASTER_PERSONAS_EGRESADOS_PII |
| `[tu_script_master_retirados_NJ].[ext]` | Creado | Script que genera MASTER_PERSONAS_RETIRADOS_PII |
| `DatosArmonizados/keys/MASTER_PERSONAS_EGRESADOS_PII.csv` | Creado | PII confidencial — solo en Drive, nunca a GitHub |
| `DatosArmonizados/keys/MASTER_PERSONAS_RETIRADOS_PII.csv` | Creado | PII confidencial — solo en Drive, nunca a GitHub |
| `1_LimpiezaDatos/10_anonimizar_egresados.[ext]` | Creado | Solo si la llave está disponible esta semana |
| `1_LimpiezaDatos/11_anonimizar_retirados.[ext]` | Creado | Solo si la llave está disponible esta semana |

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

**Campo de ID personal en Egresados:** (completar)

**Variables identificadas en Egresados:** (completar — pegar lista del inventario)

**Formato de la fecha de grado en Egresados:** (completar — mostrar ejemplos de valores)

**¿Cambian nombres de variables entre años en Egresados?** (completar — Sí / No; si Sí, detallar)

**Clave única de observación en Egresados:** (completar — ej. "`correo_unal` es clave única" o indicar clave compuesta)

**Número de personas únicas en MASTER_PERSONAS_EGRESADOS_PII:** (completar)

**Tipos de documento encontrados en Egresados:** (completar — ej. "CC: 94%, CE: 5%, PA: 1%")

**Personas con más de un valor de sexo/género en Egresados:** (completar — N casos)

**Registros con formato de documento inválido en Egresados:** (completar — N registros; describir el problema)

**Campo de ID personal en Retirados:** (completar)

**Variables identificadas en Retirados:** (completar)

**Cómo está codificado el período de retiro:** (completar — mostrar ejemplos de valores)

**Número de observaciones en `Retirados_desde_2009.xlsx`:** (completar)

**Clave única de observación en Retirados:** (completar — ej. "`correo_unal` es clave única" o indicar clave compuesta)

**Número de personas únicas en MASTER_PERSONAS_RETIRADOS_PII:** (completar)

**Tipos de documento encontrados en Retirados:** (completar)

**Personas con más de un valor de sexo/género en Retirados:** (completar — N casos)

**Registros con formato de documento inválido en Retirados:** (completar)

**Discrepancias en `Diccionario_Egresados.xlsx` o `Dicionario_Retirados.xlsx`:** (completar)

---

## Horas trabajadas (estimado)

| Actividad | Horas |
|---|---|
| Lectura de documentación y configuración | |
| Escritura de script de exploración (`EX_Egresados_NJ` o `EX_Retirados_NJ`) | |
| Configurar archivo de rutas | |
| Escritura y ejecución de script de inventario — Egresados | |
| Escritura y ejecución de script de inventario — Retirados | |
| Escritura de scripts Master Personas (Egresados + Retirados) | |
| Completar diccionarios (Egresados + Retirados) | |
| Escritura de scripts de anonimización (si aplica) | |
| **Total** | |
