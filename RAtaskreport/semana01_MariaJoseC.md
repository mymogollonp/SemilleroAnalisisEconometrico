# Reporte Semanal — Semana 01
## RA: Maria Jose Cadena | Dataset: Cancelaciones

**Semana:** 01 (2026-04-13 → 2026-04-19)
**Fecha de entrega del reporte:** 2026-04-19
**Fase del proyecto:** Fase 0 — Infraestructura / inicio Fase 1 — Anonimización

---

## Tareas asignadas esta semana

### Tarea inicial — Script de exploración propio

> Antes de ejecutar los scripts generados por Claude, escribe tu propio código de exploración en el lenguaje de tu preferencia (R, Python o Stata).

- `[ ]` Escribir un script `EX_Cancelaciones_MJC.[ext]` que abra uno de los archivos de tu módulo, liste las variables, muestre las primeras filas y reporte el número de observaciones
- `[ ]` Hacer **commit y push** del script

### Tareas comunes del equipo (Fase 0 — Infraestructura)

- `[ ]` Leer `WORKPLAN.md` y `requirements-spec.md` completos y confirmar entendimiento
- `[ ]` Firmar el acuerdo de confidencialidad (`Acuerdo de confidencialidad Semillero Analisis Econometrico.docx`)
- `[ ]` Clonar el repositorio de código en tu máquina local
- `[ ]` Verificar acceso a la carpeta de datos en Drive (`DatosOriginales/`)
- `[ ]` Crear la subcarpeta `DatosArmonizados/1_DatosAnonimizados/Cancelaciones/` en Drive
- `[ ]` Abrir `00_configuracion.do`, agregar tu bloque de rutas con `c(username)` y las rutas reales de tu PC, hacer **commit y push**

### Tareas específicas — Inventario de Cancelaciones

> El do-file `inventario_cancelaciones.do` fue generado por Claude. Tu tarea es revisarlo, entenderlo y ejecutarlo.

- `[ ]` Leer y entender `1_LimpiezaDatos/02_inventario_cancelaciones.do` antes de ejecutarlo
- `[ ]` Ejecutar `inventario_cancelaciones.do` y revisar el log generado en `logs/`
- `[ ]` Documentar en "Comentarios adicionales":
  - Nombre exacto del campo de ID personal
  - Lista completa de variables
  - Si los nombres de variables cambian entre años
  - Cómo está codificada la fecha o período de cancelación (el do-file muestra ejemplos de valores)
  - Verificar que el primer archivo es `Cancelaciones_2009-2S.xlsx` (no existe 2009-1S)
  - La(s) variable(s) que identifican de forma única una observación
- `[ ]` Hacer **commit y push** del log generado

### Tareas específicas — Anonimización de Cancelaciones

> Dependencia: requiere que Nicolas Camacho haya generado y compartido `LLAVE_ID_UNAL_FCE.csv`.

- `[ ]` Esperar confirmación de Nicolas Camacho de que la llave está disponible
- `[ ]` Si la llave está disponible esta semana: crear `1_LimpiezaDatos/09_anonimizar_cancelaciones.do` siguiendo el patrón del workplan, hacer **commit y push**

---

## Archivos creados o modificados

| Archivo | Acción | Observación |
|---|---|---|
| `00_configuracion.do` | Modificado | Agregar bloque de rutas para tu PC |
| `1_LimpiezaDatos/09_anonimizar_cancelaciones.do` | Crear | Solo si la llave está disponible esta semana |

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

**Campo de ID personal en Cancelaciones:** (completar)

**Variables identificadas en Cancelaciones:** (completar — pegar lista del log del inventario)

**Formato de la fecha/período de cancelación:** (completar — el inventario muestra ejemplos de valores string; documentar si es fecha completa, YYYY-NS, otro)

**¿Cambian nombres de variables entre años?** (completar — el inventario reporta inconsistencias automáticamente)

**Clave única de observación en Cancelaciones:** (completar — ej. "La variable `correo_unal` identifica de forma única cada fila" o indicar clave compuesta)

---

## Horas trabajadas (estimado)

| Actividad | Horas |
|---|---|
| Lectura de documentación y configuración | |
| Escritura de script de exploración (`EX_Cancelaciones_MJC`) | |
| Configurar `00_configuracion.do` | |
| Revisar y ejecutar `inventario_cancelaciones.do` | |
| Escritura de `09_anonimizar_cancelaciones.do` (si aplica) | |
| **Total** | |
