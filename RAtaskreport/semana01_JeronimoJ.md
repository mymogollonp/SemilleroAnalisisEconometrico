# Reporte Semanal — Semana 01
## RA: Jeronimo Jimenez | Dataset: Cursadas

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

- `[ ]` Escribir un script `EX_Cursadas_JJ.[ext]` que abra uno de los archivos de tu módulo, liste las variables, muestre las primeras filas y reporte el número de observaciones
- `[ ]` Hacer **commit y push** del script

### Tareas comunes del equipo (Fase 0 — Infraestructura)

- `[ ]` Leer `WORKPLAN.md` y `requirements-spec.md` completos y confirmar entendimiento
- `[ ]` Firmar el acuerdo de confidencialidad (`Acuerdo de confidencialidad Semillero Analisis Econometrico.docx`)
- `[ ]` Clonar el repositorio de código en tu máquina local
- `[ ]` Verificar acceso a la carpeta de datos en Drive (`DatosOriginales/`)
- `[ ]` Crear la subcarpeta `DatosArmonizados/1_DatosAnonimizados/Cursadas/` en Drive
- `[ ]` Abrir `00_configuracion.do`, agregar tu bloque de rutas con `c(username)` y las rutas reales de tu PC, hacer **commit y push**

### Tareas específicas — Inventario de Cursadas

> El script `1_LimpiezaDatos/02_inventario_cursadas.do` es un **script de referencia** generado previamente. No estás obligado a ejecutarlo — escribe tu propio script de inventario en el lenguaje de tu preferencia (R, Python o Stata).

- `[ ]` Escribir tu propio script de inventario para Cursadas
- `[ ]` El script debe: abrir cada archivo, listar variables y tipos, contar missings, comparar encabezados entre años, reportar N observaciones por archivo, verificar que las calificaciones están en escala 0–5
- `[ ]` Documentar en "Comentarios adicionales":
  - Nombre exacto del campo de ID personal
  - Lista completa de variables
  - Si los nombres de variables cambian entre años
  - Si la escala de calificaciones es 0–5 en todos los archivos
  - La(s) variable(s) que identifican de forma única una observación
- `[ ]` Hacer **commit y push** del script de inventario

### Tareas específicas — Master Dataset de Personas (Cursadas)

- `[ ]` A partir del inventario, identificar las variables con datos personales (nombre, correo, cédula)
- `[ ]` Escribir un script que extraiga personas únicas de todos los archivos Cursadas
- `[ ]` Guardar como `DatosArmonizados/keys/MASTER_PERSONAS_CURSADAS_PII.csv` (solo en Drive, nunca a GitHub)
- `[ ]` Reportar el número de personas únicas en "Comentarios adicionales"
- `[ ]` Hacer **commit y push** del script

### Tareas específicas — Diccionario de variables

- `[ ]` Abrir `Diccionarios/Diccionario_Cursadas.xlsx` en Drive
- `[ ]` Completar las filas faltantes y verificar la información existente con base en el inventario
- `[ ]` Documentar en "Comentarios adicionales" cualquier variable no documentada o discrepancia encontrada

### Tareas específicas — Anonimización de Cursadas

> Dependencia: requiere que Nicolas Camacho haya generado y compartido `LLAVE_ID_UNAL_FCE.csv`.

- `[ ]` Esperar confirmación de Nicolas Camacho de que la llave está disponible
- `[ ]` Si la llave está disponible esta semana: escribir tu propio script `1_LimpiezaDatos/08_anonimizar_cursadas.[ext]`, hacer **commit y push**

---

## Archivos creados o modificados

| Archivo | Acción | Observación |
|---|---|---|
| `00_configuracion.do` / `00_config.R` / `00_config.py` | Modificado | Agregar bloque de rutas para tu PC |
| `EX_Cursadas_JJ.[ext]` | Creado | Script de exploración inicial |
| `[tu_script_inventario_JJ].[ext]` | Creado | Script de inventario propio |
| `[tu_script_master_personas_JJ].[ext]` | Creado | Script que genera MASTER_PERSONAS_CURSADAS_PII |
| `DatosArmonizados/keys/MASTER_PERSONAS_CURSADAS_PII.csv` | Creado | PII confidencial — solo en Drive, nunca a GitHub |
| `1_LimpiezaDatos/08_anonimizar_cursadas.[ext]` | Creado | Solo si la llave está disponible esta semana |

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

**Campo de ID personal en Cursadas:** (completar — ej. "Se llama `correo_unal`, igual que en Matriculados")

**Variables identificadas en Cursadas:** (completar — pegar lista del inventario)

**¿Escala de calificaciones es 0–5 en todos los archivos?** (completar — Sí / No; si No, detallar qué archivos tienen valores fuera de rango)

**¿Cambian nombres de variables entre años?** (completar — Sí / No; si Sí, detallar)

**Clave única de observación en Cursadas:** (completar — ej. "Ninguna variable individual es clave única; la clave compuesta es (`correo_unal`, `cod_asignatura`, `grupo`)")

**Número de personas únicas en MASTER_PERSONAS_CURSADAS_PII:** (completar)

**Discrepancias o variables no documentadas en `Diccionario_Cursadas.xlsx`:** (completar)

---

## Horas trabajadas (estimado)

| Actividad | Horas |
|---|---|
| Lectura de documentación y configuración | |
| Escritura de script de exploración (`EX_Cursadas_JJ`) | |
| Configurar archivo de rutas | |
| Escritura y ejecución de script de inventario propio | |
| Escritura de script Master Personas Cursadas PII | |
| Completar `Diccionario_Cursadas.xlsx` | |
| Escritura de `08_anonimizar_cursadas.[ext]` (si aplica) | |
| **Total** | |
