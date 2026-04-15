# Reporte Semanal — Semana 01
## RA: Nicolas Camacho | Dataset: Matriculados

**Semana:** 01 (2026-04-13 → 2026-04-19)
**Fecha de entrega del reporte:** 2026-04-19
**Fase del proyecto:** Fase 0 — Infraestructura y Llave de Anonimización

---

## Tareas asignadas esta semana

### Tareas comunes del equipo (Fase 0 — Infraestructura)

- `[ ]` Leer `WORKPLAN.md` y `requirements-spec.md` completos y confirmar entendimiento
- `[ ]` Firmar el acuerdo de confidencialidad (`Acuerdo de confidencialidad Semillero Analisis Econometrico.docx`)
- `[ ]` Clonar el repositorio de código en tu máquina local
- `[ ]` Verificar acceso a la carpeta de datos en Drive (`DatosOriginales/`)
- `[ ]` Crear las carpetas de salida en Drive si no existen: `DatosArmonizados/keys/`, `1_DatosAnonimizados/Matriculado/`
- `[ ]` Abrir `00_configuracion.do`, agregar tu bloque de rutas con `c(username)` y las rutas reales de tu PC, hacer **commit y push**

### Tareas específicas — Inventario de Matriculados

> El do-file `inventario_matriculados.do` fue generado por Claude. Tu tarea es revisarlo, entenderlo y ejecutarlo.

- `[ ]` Leer y entender `1_LimpiezaDatos/02_inventario_matriculados.do` antes de ejecutarlo
- `[ ]` Ejecutar `inventario_matriculados.do` y revisar el log generado en `logs/`
- `[ ]` Documentar en "Comentarios adicionales": nombre exacto del campo de ID personal, lista de variables, si los nombres cambian entre años
- `[ ]` Identificar la(s) variable(s) que identifican de forma única una observación en Matriculados y documentarlo en "Comentarios adicionales"
- `[ ]` Hacer **commit y push** del log generado (si no está excluido por `.gitignore`)

### Tareas específicas — Llave de anonimización

> El do-file `01_crear_llave_idunal.do` fue generado por Claude. Debes revisarlo y ajustar el placeholder antes de ejecutarlo.

- `[ ]` Leer y entender `1_LimpiezaDatos/01_crear_llave_idunal.do`
- `[ ]` Actualizar el placeholder `VAR_ID_PERSONAL` (línea `local var_id`) con el nombre real encontrado en el inventario
- `[ ]` Ejecutar `01_crear_llave_idunal.do` y verificar que:
  - El número de estudiantes únicos es razonable
  - No hay duplicados en `id_unal`
  - El archivo `LLAVE_ID_UNAL_FCE.csv` fue creado en `DatosArmonizados/keys/`
- `[ ]` Reportar el número total de estudiantes únicos en la llave
- `[ ]` Notificar al equipo (PI/CoPI y demás RAs) que la llave está disponible
- `[ ]` Hacer **commit y push** del do-file actualizado

> **Nota:** la llave es prerequisito para todos los demás RAs. Priorizar esta tarea.

---

## Archivos creados o modificados

| Archivo | Acción | Observación |
|---|---|---|
| `00_configuracion.do` | Modificado | Agregar bloque de rutas para tu PC |
| `1_LimpiezaDatos/01_crear_llave_idunal.do` | Modificado | Actualizar `VAR_ID_PERSONAL` con nombre real |
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

**Número de estudiantes únicos en la llave:** (completar)

**¿El campo de ID cambia de nombre entre años?** (completar — Sí / No / Parcialmente; si Sí, listar qué nombres encontró)

**Variables en Matriculados:** (completar — pegar la lista de variables del log del inventario)

**¿Inconsistencias de variables entre archivos?** (completar — Sí / No; si Sí, detallar)

**Clave única de observación en Matriculados:** (completar — ej. "La variable `correo_unal` identifica de forma única cada fila" o "La clave compuesta es (`correo_unal`, `cod_plan`)")

---

## Horas trabajadas (estimado)

| Actividad | Horas |
|---|---|
| Lectura de documentación y configuración | |
| Configurar `00_configuracion.do` | |
| Revisar y ejecutar `inventario_matriculados.do` | |
| Revisar, ajustar y ejecutar `01_crear_llave_idunal.do` | |
| **Total** | |
