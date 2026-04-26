# Reporte Semanal — Semana 01
## RA: Maria Jose Cadena | Dataset: Cancelaciones

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

- `[X]` Escribir un script `EX_Cancelaciones_MJC.[py]` que abra uno de los archivos de tu módulo, liste las variables, muestre las primeras filas y reporte el número de observaciones
- `[X]` Hacer **commit y push** del script

### Tareas comunes del equipo (Fase 0 — Infraestructura)

- `[X]` Leer `WORKPLAN.md` y `requirements-spec.md` completos y confirmar entendimiento
- `[X]` Firmar el acuerdo de confidencialidad (`Acuerdo de confidencialidad Semillero Analisis Econometrico.docx`)
- `[X]` Clonar el repositorio de código en tu máquina local
- `[X]` Verificar acceso a la carpeta de datos en Drive (`DatosOriginales/`)
- `[X]` Crear la subcarpeta `DatosArmonizados/1_DatosAnonimizados/Cancelaciones/` en Drive
- `[X]` Abrir `00_configuracion.do`, agregar tu bloque de rutas con `c(username)` y las rutas reales de tu PC, hacer **commit y push**

### Tareas específicas — Inventario de Cancelaciones

> El script `1_LimpiezaDatos/02_inventario_cancelaciones.do` es un **script de referencia** generado previamente. No estás obligada a ejecutarlo — escribe tu propio script de inventario en el lenguaje de tu preferencia (R, Python o Stata).

- `[X]` Escribir tu propio script de inventario para Cancelaciones
- `[X]` El script debe: abrir cada archivo, listar variables y tipos, contar missings, comparar encabezados entre años, mostrar ejemplos de valores para la variable de fecha/período de cancelación, reportar N observaciones por archivo
- `[X]` Documentar en "Comentarios adicionales":
  - Nombre exacto del campo de ID personal
  - Lista completa de variables
  - Si los nombres de variables cambian entre años
  - Cómo está codificada la fecha o período de cancelación
  - Confirmar que el primer archivo es `Cancelaciones_2009-2S.xlsx` (no existe 2009-1S)
  - La(s) variable(s) que identifican de forma única una observación
- `[X]` Hacer **commit y push** del script de inventario

### Tareas específicas — Master Dataset de Personas (Cancelaciones)

- `[X]` A partir del inventario, identificar las variables de: correo/email, tipo de documento, número de documento, nombre completo, sexo/género
- `[X]` Escribir un script que itere sobre **todos** los archivos Cancelaciones (no solo el más reciente)
- `[X]` Armonizar nombres de variables en el output: usar `correo`, `tipo_documento`, `numero_documento`, `nombre_completo`, `sexo` como nombres canónicos
- `[!]` **Sexo/género**: registrar **todos los valores distintos observados por persona** — una persona puede cambiar de género entre períodos; conservar todos los pares `(correo, sexo, periodo)`, no reducir a uno
- `[!]` **Tipo de documento**: registrar todos los tipos encontrados (CC, CE, PA, TI, NUIP, PEP u otros); reportar cualquier código no reconocido
- `[X]` **Verificar formato de número de documento**: CC (6–10 dígitos numéricos), CE (alfanumérico), PA (alfanumérico), TI (10–11 dígitos); anotar registros con formato inesperado
- `[X]` Guardar como `DatosArmonizados/keys/MASTER_PERSONAS_CANCELACIONES_PII.csv` (solo en Drive, nunca a GitHub)
- `[X]` Hacer **commit y push** del script

### Tareas específicas — Diccionario de variables

- `[X]` Abrir `Diccionarios/Diccionario_Cancelaciones.xlsx` en Drive
- `[X]` Completar las filas faltantes y verificar la información existente con base en el inventario
- `[X]` Documentar en "Comentarios adicionales" cualquier variable no documentada o discrepancia encontrada

### Tareas específicas — Anonimización de Cancelaciones

> Dependencia: requiere que Nicolas Camacho haya generado y compartido `LLAVE_ID_UNAL_FCE.csv`.

- `[ ]` Esperar confirmación de Nicolas Camacho de que la llave está disponible
- `[ ]` Si la llave está disponible esta semana: escribir tu propio script `1_LimpiezaDatos/09_anonimizar_cancelaciones.[ext]`, hacer **commit y push**

---

## Archivos creados o modificados

| Archivo | Acción | Observación |
|---|---|---|
| `00_configuracion.do` / `00_config.R` / `00_config.py` | Modificado | Agregar bloque de rutas para tu PC |
| `EX_Cancelaciones_MJC.[ext]` | Creado | Script de exploración inicial |
| `[01_inventario_cancelaciones_MJCS].[py]` | Creado | Script de inventario propio |
| `[tu_script_master_personas_MJC].[ext]` | Creado | Script que genera MASTER_PERSONAS_CANCELACIONES_PII |
| `DatosArmonizados/keys/MASTER_PERSONAS_CANCELACIONES_PII.csv` | Creado | PII confidencial — solo en Drive, nunca a GitHub |
| `1_LimpiezaDatos/09_anonimizar_cancelaciones.[ext]` | Creado | Solo si la llave está disponible esta semana |

---

## Problemas encontrados

| # | Descripción del problema | Dato o archivo afectado | Estado |
|---|---|---|---|
| | | | |

---

## Preguntas para el PI/CoPI

- Crear la variable tipo de documento a partir CC (6–10 dígitos numéricos), CE (alfanumérico), PA (alfanumérico), TI (10–11 dígitos); anotar registros con formato inesperado, no se si sea correcto (choque con CC y TI, CE y PA)? Por ahora quedaron como NAN (junto a género)
- hay un salto notable en el volumen de cancelaciones a partir de 2020-1S (de ~9K a ~24K registros por semestre), que se mantiene elevado hasta 2022-1S y luego baja. Probablemente refleja el efecto pandemia + medidas de flexibilización académica de la UNAL en ese período — no es un problema de datos, pero vale la pena que quede documentado.

---

## Comentarios adicionales

**Campo de ID personal en Cancelaciones:** (completar)

El correo institucional es más estable como identificador académico (un estudiante puede cambiar de documento por naturalización, pero su correo UNAL no cambia). 

**Variables identificadas en Cancelaciones:** (completar — pegar lista del inventario)

45 variables en total. Las 39 presentes en todos los archivos son: ACCESO, ADMISION, APERTURA, ASIGNATURA, CAUSA_ANULA, COD_ACCESO, COD_ASIGNATURA, COD_FACULTAD, COD_FACULTAD_ASIGNATURA, COD_NODO_INICIO, COD_PLAN, COD_SEDE_ASIGNATURA, COD_SUBACCESO, COD_UAB_ASIGNATURA, CONVENIO_PLAN, CORRECIÓN DE CRED. PERDIDA, CORREO_INSTITUCIONAL, CREDITOS, DOCUMENTO, FACULTAD, FACULTAD_ASIGNATURA, FECHA, GRUP_ACTA, GRUP_ACTI, HIST_ACAD, LOGIN_USUARIO_ESTUDIANTE, NODO_INICIO, NOMBRES_APELLIDOS, NOTA_ALFABETICA, NOTA_NUMERICA, PERIODO, PLAN, SEDE, SUBACCESO, TIPO_CANCELACION, TIPO_NIVEL, TIPO_USUARIO, UAB_ASIGNATURA, USUARIO_CANCELACION.

**Formato de la fecha/período de cancelación:** (completar — documentar si es fecha completa, YYYY-NS, otro; mostrar ejemplos de valores)

La variable PERIODO usa formato YYYY-NS (ej. 2009-2S, 2010-1S) de forma consistente en los 32 archivos. No hay variantes de formato. Adicionalmente existe la variable FECHA con tipo datetime64[ns] en todos los archivos, que registra la fecha exacta de cancelación.

**¿Cambian nombres de variables entre años?** (completar — Sí / No; si Sí, detallar)

No. Los nombres de columna no cambian entre semestres. Las 39 variables base mantienen exactamente el mismo nombre en todos los archivos. 

**¿El primer archivo es `Cancelaciones_2009-2S.xlsx`?** (completar — confirmar que no existe 2009-1S)

Si.

**Clave única de observación en Cancelaciones:** (completar — ej. "La variable `correo_unal` identifica de forma única cada fila" o indicar clave compuesta)

Ninguna combinación evaluada identifica de forma única cada fila. El dataset es a nivel cancelación de asignatura, no de estudiante ni de semestre. La llave CORREO_INSTITUCIONAL + PERIODO + COD_PLAN alcanza solo 64.49% de unicidad (72.284 llaves repetidas sobre 354.801 filas). Los repetidos son filas genuinamente distintas — un estudiante puede cancelar múltiples asignaturas en el mismo semestre. Las columnas que más diferencian los repetidos son COD_ASIGNATURA (varía en 69.384 llaves) y ASIGNATURA (69.379), lo que confirma que la llave única es CORREO_INSTITUCIONAL + PERIODO + COD_PLAN + COD_ASIGNATURA. 

**Número de personas únicas en MASTER_PERSONAS_CANCELACIONES_PII:** (completar)

**Tipos de documento encontrados en Cancelaciones:** (completar — ej. "CC: 94%, CE: 5%, PA: 1%")

No existe la variable de tipo de documento.

**Personas con más de un valor de sexo/género registrado:** (completar — N casos)

No existe variable de sexo/género en Cancelaciones. 

**Registros con formato de documento inválido:** (completar — N registros; describir el problema)

**Discrepancias o variables no documentadas en `Diccionario_Cancelaciones.xlsx`:** (completar)

Algunas variables cambian de tipo a lo largo del periodo:
COD_PLAN
COD_PROG_CURRICULAR
COD_UAB_ASIGNATURA
CONVENIO_PLAN
CONVOCATORIA
DESC_PROG_CURRICULAR
DES_GR_ACTIV
DOCUMENTO
GRUP_ACTI
NOTA_ALFABETICA
PBM
PUNTAJE_ADMISION

---

## Horas trabajadas (estimado)

| Actividad | Horas |
|---|---|
| Lectura de documentación y configuración |1 hora|
| Escritura de script de exploración (`EX_Cancelaciones_MJC`) | 30 min|
| Configurar archivo de rutas |5 min|
| Escritura y ejecución de script de inventario propio |5 horas|
| Escritura de script Master Personas Cancelaciones PII | 3 horas|
| Completar `Diccionario_Cancelaciones.xlsx` |1 hora|
| Escritura de `09_anonimizar_cancelaciones.[ext]` (si aplica) | |
| **Total** | |
