# Reporte Semanal — Semana 01
## RA: Nicolas Jimenez | Dataset: Egresados y Retirados

**Semana:** 01 (2026-04-13 → 2026-04-19)
**Fecha de entrega del reporte:** 2026-04-19
**Fase del proyecto:** Fase 0 — Infraestructura / inicio Fase 1 — Anonimización

---

## Tareas asignadas esta semana

### Tareas comunes del equipo (Fase 0 — Infraestructura)

- `[ ]` Leer `WORKPLAN.md` y `requirements-spec.md` completos y confirmar entendimiento
- `[ ]` Firmar el acuerdo de confidencialidad (`Acuerdo de confidencialidad Semillero Analisis Econometrico.docx`)
- `[ ]` Clonar el repositorio de código en tu máquina local
- `[ ]` Verificar acceso a la carpeta de datos en Drive (`DatosOriginales/`)
- `[ ]` Crear las subcarpetas `DatosArmonizados/1_DatosAnonimizados/Egresados/` y `.../Retirados/` en Drive
- `[ ]` Abrir `00_configuracion.do`, agregar tu bloque de rutas con `c(username)` y las rutas reales de tu PC, hacer **commit y push**

### Tareas específicas — Inventario de Egresados

> El do-file `inventario_egresados.do` fue generado por Claude. Tu tarea es revisarlo, entenderlo y ejecutarlo.

- `[ ]` Leer y entender `1_LimpiezaDatos/02_inventario_egresados.do` antes de ejecutarlo
- `[ ]` Ejecutar `inventario_egresados.do` y revisar el log generado en `logs/`
- `[ ]` Documentar en "Comentarios adicionales":
  - Nombre exacto del campo de ID personal
  - Lista completa de variables
  - Si los nombres de variables cambian entre años
  - Cómo está codificada la fecha de grado (el do-file muestra ejemplos de valores)
  - La(s) variable(s) que identifican de forma única una observación
- `[ ]` Hacer **commit y push** del log generado

### Tareas específicas — Inventario de Retirados

> El do-file `inventario_retirados.do` fue generado por Claude. Tu tarea es revisarlo, entenderlo y ejecutarlo.

- `[ ]` Leer y entender `1_LimpiezaDatos/02_inventario_retirados.do` antes de ejecutarlo
- `[ ]` Ejecutar `inventario_retirados.do` y revisar el log generado en `logs/`
- `[ ]` Documentar en "Comentarios adicionales":
  - Nombre del campo de ID personal
  - Variables disponibles
  - Cómo está codificado el período de retiro
  - Número total de observaciones
  - La(s) variable(s) que identifican de forma única una observación

### Tareas específicas — Anonimización

> Dependencia: requiere que Nicolas Camacho haya generado y compartido `LLAVE_ID_UNAL_FCE.csv`.

- `[ ]` Esperar confirmación de Nicolas Camacho de que la llave está disponible
- `[ ]` Si la llave está disponible esta semana:
  - Crear `1_LimpiezaDatos/10_anonimizar_egresados.do`, hacer **commit y push**
  - Crear `1_LimpiezaDatos/11_anonimizar_retirados.do`, hacer **commit y push**

> **Nota:** Retirados tiene un solo archivo — una vez disponible la llave, `11_anonimizar_retirados.do` puede completarse rápidamente.

---

## Archivos creados o modificados

| Archivo | Acción | Observación |
|---|---|---|
| `00_configuracion.do` | Modificado | Agregar bloque de rutas para tu PC |
| `1_LimpiezaDatos/10_anonimizar_egresados.do` | Crear | Solo si la llave está disponible esta semana |
| `1_LimpiezaDatos/11_anonimizar_retirados.do` | Crear | Solo si la llave está disponible esta semana |

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

**Variables identificadas en Egresados:** (completar — pegar lista del log del inventario)

**Formato de la fecha de grado en Egresados:** (completar — el inventario muestra ejemplos de valores)

**¿Cambian nombres de variables entre años en Egresados?** (completar)

**Campo de ID personal en Retirados:** (completar)

**Variables identificadas en Retirados:** (completar)

**Cómo está codificado el período de retiro:** (completar)

**Número de observaciones en `Retirados_desde_2009.xlsx`:** (completar)

**Clave única de observación en Egresados:** (completar — ej. "`correo_unal` es clave única" o indicar clave compuesta)

**Clave única de observación en Retirados:** (completar — ej. "`correo_unal` es clave única" o indicar clave compuesta)

---

## Horas trabajadas (estimado)

| Actividad | Horas |
|---|---|
| Lectura de documentación y configuración | |
| Configurar `00_configuracion.do` | |
| Revisar y ejecutar `inventario_egresados.do` | |
| Revisar y ejecutar `inventario_retirados.do` | |
| Escritura de do-files de anonimización (si aplica) | |
| **Total** | |
