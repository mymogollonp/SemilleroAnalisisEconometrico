# Reporte Semanal — Semana 01
## RA: Jeronimo Jimenez | Dataset: Cursadas

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
- `[ ]` Crear la subcarpeta `DatosArmonizados/1_DatosAnonimizados/Cursadas/` en Drive
- `[ ]` Abrir `00_configuracion.do`, agregar tu bloque de rutas con `c(username)` y las rutas reales de tu PC, hacer **commit y push**

### Tareas específicas — Inventario de Cursadas

> El do-file `inventario_cursadas.do` fue generado por Claude. Tu tarea es revisarlo, entenderlo y ejecutarlo.

- `[ ]` Leer y entender `1_LimpiezaDatos/02_inventario_cursadas.do` antes de ejecutarlo
- `[ ]` Ejecutar `inventario_cursadas.do` y revisar el log generado en `logs/`
- `[ ]` Documentar en "Comentarios adicionales":
  - Nombre exacto del campo de ID personal
  - Lista completa de variables
  - Si los nombres de variables cambian entre años
  - Si la escala de calificaciones es 0–5 en todos los archivos (el do-file lo reporta automáticamente)
  - La(s) variable(s) que identifican de forma única una observación
- `[ ]` Hacer **commit y push** del log generado

### Tareas específicas — Anonimización de Cursadas

> Dependencia: requiere que Nicolas Camacho haya generado y compartido `LLAVE_ID_UNAL_FCE.csv`.

- `[ ]` Esperar confirmación de Nicolas Camacho de que la llave está disponible
- `[ ]` Una vez disponible la llave, revisar la estructura de `1_LimpiezaDatos/02_inventario_cursadas.do` para entender el patrón que seguirá el do-file de anonimización
- `[ ]` Si la llave está disponible esta semana: crear `1_LimpiezaDatos/08_anonimizar_cursadas.do` siguiendo el patrón del workplan, hacer **commit y push**

---

## Archivos creados o modificados

| Archivo | Acción | Observación |
|---|---|---|
| `00_configuracion.do` | Modificado | Agregar bloque de rutas para tu PC |
| `1_LimpiezaDatos/08_anonimizar_cursadas.do` | Crear | Solo si la llave está disponible esta semana |

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

**Variables identificadas en Cursadas:** (completar — pegar lista del log del inventario)

**¿Escala de calificaciones es 0–5 en todos los archivos?** (completar — el inventario reporta automáticamente las variables fuera de rango)

**¿Cambian nombres de variables entre años?** (completar — el inventario reporta inconsistencias automáticamente)

**Clave única de observación en Cursadas:** (completar — ej. "Ninguna variable individual es clave única; la clave compuesta es (`correo_unal`, `cod_asignatura`, `grupo`)")

---

## Horas trabajadas (estimado)

| Actividad | Horas |
|---|---|
| Lectura de documentación y configuración | |
| Configurar `00_configuracion.do` | |
| Revisar y ejecutar `inventario_cursadas.do` | |
| Escritura de `08_anonimizar_cursadas.do` (si aplica) | |
| **Total** | |
