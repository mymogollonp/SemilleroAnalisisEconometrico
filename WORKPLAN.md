# Workplan: Armonización de Datos UNAL
## Semillero de Análisis Econométrico

**PI:** Karoll Gomez
**CoPI:** Monica Mogollon
**Repositorio de código:** `C:\code\SemilleroAnalisisEconometrico`
**Repositorio de datos:** `C:\Drive2023\UNAL_Docente\SemilleroAnalisisEconometrico`
**Fecha de inicio:** 2026-04-13

### Equipo de investigación

| Rol | Nombre | Dataset a cargo |
|---|---|---|
| PI | Karoll Gomez | — |
| CoPI | Monica Mogollon | — |
| RA | Nicolas Camacho | Matriculados |
| RA | Jeronimo Jimenez | Cursadas |
| RA | Maria Jose Cadena | Cancelaciones |
| RA | Nicolas Jimenez | Egresados y Retirados |

> **Regla global de outputs:** todos los archivos de datos se guardan en formato **CSV**. No se generan archivos `.dta`.

---

## Reglas para RAs

### R1 — Commit y push al terminar código

Cada vez que un RA crea o modifica un do-file, debe:

1. **Hacer commit** del archivo en el repositorio local con un mensaje descriptivo que indique qué hace el do-file y para qué módulo.
   ```
   git add 1_LimpiezaDatos/07_anonimizar_matriculados.do
   git commit -m "feat: anonimizar matriculados - reemplaza correo por id_unal"
   ```
2. **Hacer push** al repositorio remoto en GitHub inmediatamente después del commit.
   ```
   git push
   ```

> El repositorio en GitHub es la única fuente de verdad para el código. Un do-file que no está en GitHub no existe para el equipo.

### R2 — Actualizar el reporte de tareas

Cada vez que un RA completa una tarea (o la avanza/bloquea), debe actualizar su archivo de reporte semanal en `RAtaskreport/semanaNN_NombreA.md`:

- Cambiar el estado de la tarea: `[ ]` → `[x]` (completada), `[-]` (en progreso), o `[!]` (bloqueada)
- Llenar la tabla de archivos creados o modificados
- Anotar cualquier problema encontrado en la tabla de problemas
- Hacer commit y push del reporte actualizado junto con el código o de forma independiente

### R3 — No datos en GitHub

El repositorio solo contiene código, documentación y logs. Nunca subir archivos de datos (`.csv`, `.xlsx`, `.zip`, etc.). El `.gitignore` ya excluye estos formatos.

### R4 — Un do-file por tarea

Cada do-file tiene una sola responsabilidad (anonimizar un módulo, limpiar un módulo, etc.). No combinar tareas de distintas fases en un mismo script.

### R5 — Actualizar las rutas raíz en `00_configuracion.do`

El archivo `00_configuracion.do` define los globales de rutas que todos los do-files usan. Cada RA debe editar su sección local al comenzar a trabajar en una máquina nueva:

```stata
* ============================================================
* 00_configuracion.do — Rutas raíz por usuario
* Editar la sección correspondiente a tu máquina
* ============================================================

local usuario = c(username)

if "`usuario'" == "NicolasC" {
    global dir_datos  "C:/TuRuta/SemilleroAnalisisEconometrico"
    global dir_code   "C:/TuRuta/code/SemilleroAnalisisEconometrico"
}
else if "`usuario'" == "JeronimoJ" {
    global dir_datos  "C:/TuRuta/SemilleroAnalisisEconometrico"
    global dir_code   "C:/TuRuta/code/SemilleroAnalisisEconometrico"
}
* ... agregar bloque para cada RA
```

Pasos para cada RA:
1. Abrir `00_configuracion.do` y agregar un bloque `else if` con tu nombre de usuario (`c(username)`) y las rutas correctas en tu PC
2. Hacer commit y push del archivo actualizado

> Nunca hardcodear rutas absolutas fuera de `00_configuracion.do`. Si un do-file no corre en otra máquina, la causa es casi siempre una ruta mal configurada aquí.

### R6 — Nunca modificar DatosOriginales

La carpeta `DatosOriginales/` es de solo lectura. Ningún do-file, script, ni acción manual puede crear, editar, renombrar o eliminar archivos dentro de ella.

- Los do-files solo **leen** de `DatosOriginales/` — nunca escriben en ella.
- Todos los outputs (anonimizados, limpios, procesados) se guardan en `DatosArmonizados/` o sus subcarpetas.
- Si un archivo original parece incorrecto o incompleto, documentarlo en el reporte semanal y notificar al PI/CoPI. No modificar el archivo.

### R7 — Documentar la semilla y las rutas

Todo do-file que use una semilla aleatoria debe declararla explícitamente con un comentario. Todas las rutas deben usar los globales definidos en `00_configuracion.do`, nunca rutas absolutas hardcodeadas.

---

## Datos disponibles

| Dataset | Archivos | Cobertura | RA responsable |
|---|---|---|---|
| Matriculados | `.xlsx` (34 archivos) | 2009-1S → 2025-2S (panel continuo) | Nicolas Camacho |
| Cursadas | `.xlsx` (33 archivos) | 2009-1S → 2025-1S | Jeronimo Jimenez |
| Cancelaciones | `.xlsx` (32 archivos) | 2009-2S → 2025-1S | Maria Jose Cadena |
| Egresados | `.xlsx` (33 archivos) | 2009-1S → 2025-1S | Nicolas Jimenez |
| Retirados | `.xlsx` (1 archivo) | `Retirados_desde_2009.xlsx` | Nicolas Jimenez |

> **Nota:** No se encontró ningún archivo de Rendimiento Matemáticas Básicas en `DatosOriginales`. Pendiente confirmar si existe esta fuente.

**Datos procesados heredados (`HeredadoMarcos/ProcesadosMarcos/`):**
- `BASE_DATOS_REGISTRO_UNAL_BOGOTA.csv` — panel académico con `id_unal` anónimo (semilla `20260223`)
- `LLAVE_DATOS_REGISTRO_UNAL_BOGOTA.csv` — crosswalk `correo ↔ id_unal` (confidencial)
- `DICCIONARIO.xlsx` — diccionario de variables
- `Panel registro.zip` — archivo comprimido con panel heredado

---

## Estructura de carpetas en Drive (datos)

```
DatosArmonizados/
├── keys/                        ← crosswalks de anonimización (confidencial, nunca a GitHub)
│   └── LLAVE_ID_UNAL_FCE.csv
├── 1_DatosAnonimizados/         ← archivos originales anonimizados, un CSV por archivo fuente
│   ├── Matriculado/
│   ├── Cursadas/
│   ├── Cancelaciones/
│   ├── Egresados/
│   └── Retirados/
├── 2_DatosLimpios/              ← outputs de Fase 3 (un CSV limpio por módulo)
├── panel/                       ← panel maestro
├── muestras/                    ← muestras
└── outputs/                     ← tablas y figuras
```

---

## Fase 0 — Infraestructura y Llave de Anonimización

**Objetivo:** dejar el repositorio operativo y generar la llave de anonimización antes de tocar cualquier archivo original.

### Infraestructura
- [ ] Actualizar `README.md` con descripción del proyecto
- [ ] Actualizar `.gitignore` para excluir todos los formatos de datos (`*.csv`, `*.xlsx`, `*.zip`)
- [ ] Crear `code/00_configuracion.do` con globales de rutas
- [ ] Crear carpetas de salida en Drive (ver estructura arriba)
- [ ] Crear `logs/.gitkeep` para versionar la carpeta vacía
- [ ] Primer commit y push a GitHub con estructura base

### Do-files generados (revisar y ejecutar)

> Los do-files de esta fase fueron generados por Claude Code como punto de partida.
> Cada RA debe **leerlos, entenderlos y ejecutarlos** — no correr código sin revisarlo.
> Si algo no funciona o parece incorrecto, documentarlo en el reporte semanal y notificar al PI/CoPI.

| Do-file | Responsable | Descripción |
|---|---|---|
| `00_configuracion.do` | Todos | Globales de rutas — cada RA agrega su bloque y hace commit+push |
| `1_LimpiezaDatos/02_inventario_matriculados.do` | Nicolas Camacho | Perfila todos los archivos Matriculados; identifica campo de ID, consistencia de variables, y clave única de observación |
| `1_LimpiezaDatos/02_inventario_cursadas.do` | Jeronimo Jimenez | Idem Cursadas; verifica escala de calificaciones 0–5; identifica clave única |
| `1_LimpiezaDatos/02_inventario_cancelaciones.do` | Maria Jose Cadena | Idem Cancelaciones; identifica formato de fecha de cancelación y clave única |
| `1_LimpiezaDatos/02_inventario_egresados.do` | Nicolas Jimenez | Idem Egresados; identifica formato de fecha de grado y clave única |
| `1_LimpiezaDatos/02_inventario_retirados.do` | Nicolas Jimenez | Perfila el archivo único Retirados_desde_2009.xlsx; identifica clave única |
| `1_LimpiezaDatos/01_crear_llave_idunal.do` | Nicolas Camacho | Genera LLAVE_ID_UNAL_FCE.csv — **requiere actualizar `VAR_ID_PERSONAL` con el nombre real encontrado en el inventario** |

### Secuencia de ejecución en Fase 0

1. Todos los RAs completan su bloque en `00_configuracion.do` y hacen commit+push
2. Nicolas Camacho ejecuta `inventario_matriculados.do` → identifica `VAR_ID_PERSONAL`
3. Nicolas Camacho actualiza `01_crear_llave_idunal.do` y lo ejecuta → genera la llave
4. Nicolas Camacho notifica al equipo que `LLAVE_ID_UNAL_FCE.csv` está disponible
5. Los demás RAs ejecutan sus inventarios en paralelo mientras esperan la llave

### Creación de la llave de anonimización
**Do-file:** `1_LimpiezaDatos/01_crear_llave_idunal.do`
**Responsable:** Nicolas Camacho
**Salida:** `DatosArmonizados/keys/LLAVE_ID_UNAL_FCE.csv` (confidencial)

Pasos:
1. Ejecutar `inventario_matriculados.do` primero para confirmar el nombre del campo de ID personal
2. Actualizar el placeholder `VAR_ID_PERSONAL` en el do-file con el nombre real
3. Leer en loop todos los archivos `Matriculados_YYYY-NS.xlsx`, apilar IDs únicos
4. Generar `id_unal` mediante permutación aleatoria con semilla `20260223`, formato `UNAL000001`
5. Guardar crosswalk como `LLAVE_ID_UNAL_FCE.csv` en `DatosArmonizados/keys/`

> **Decisión de diseño:** se genera `id_unal` fresco para este proyecto. No se intenta cruzar con la llave heredada de `BASE_DATOS_REGISTRO_UNAL_BOGOTA`. Si en el futuro se necesita vincular ambos proyectos, ese cruce se hará como paso explícito y documentado.

---

## Fase 1 — Anonimización de Archivos Originales

**Objetivo:** importar cada archivo Excel original, reemplazar el ID real por `id_unal` usando la llave de Fase 0, eliminar todas las columnas con datos personales, y guardar como CSV en `DatosArmonizados/1_DatosAnonimizados/`. Al finalizar esta fase, ningún archivo fuera de `keys/` contiene identificadores personales.

### Regla de oro
> Todo el trabajo posterior a Fase 1 opera exclusivamente sobre los CSVs anonimizados. Nunca se vuelve a abrir un archivo original para análisis.

### Do-files y responsables

| Do-file | Dataset | Archivos fuente | Destino | RA |
|---|---|---|---|---|
| `1_LimpiezaDatos/07_anonimizar_matriculados.do` | Matriculados | `DatosOriginales/Matriculado/*.xlsx` (34) | `1_DatosAnonimizados/Matriculado/` | Nicolas Camacho |
| `1_LimpiezaDatos/08_anonimizar_cursadas.do` | Cursadas | `DatosOriginales/Cursadas/*.xlsx` (33) | `1_DatosAnonimizados/Cursadas/` | Jeronimo Jimenez |
| `1_LimpiezaDatos/09_anonimizar_cancelaciones.do` | Cancelaciones | `DatosOriginales/Cancelaciones/*.xlsx` (32) | `1_DatosAnonimizados/Cancelaciones/` | Maria Jose Cadena |
| `1_LimpiezaDatos/10_anonimizar_egresados.do` | Egresados | `DatosOriginales/Egresados/*.xlsx` (33) | `1_DatosAnonimizados/Egresados/` | Nicolas Jimenez |
| `1_LimpiezaDatos/11_anonimizar_retirados.do` | Retirados | `DatosOriginales/Retirados/Retirados_desde_2009.xlsx` | `1_DatosAnonimizados/Retirados/` | Nicolas Jimenez |

### Pasos por do-file (estructura común)

> Los do-files de anonimización serán generados por cada RA en la Semana 2, después de haber ejecutado los inventarios y recibido la llave. Usar los inventarios como guía para conocer los nombres exactos de las variables antes de escribir el código.

1. **Importar** el archivo Excel (`import excel using ..., firstrow`)
2. **Merge con la llave** — `merge m:1 <id_real> using LLAVE_ID_UNAL_FCE.csv`, verificar que todos los registros cruzan (`_merge==3`)
3. **Eliminar columnas con datos personales** — nombre, correo, cédula, fecha de nacimiento y cualquier otro identificador directo
4. **Verificar** que no queden variables con identificadores personales residuales
5. **Guardar como CSV** en la subcarpeta correspondiente de `1_DatosAnonimizados/`, conservando el nombre original del archivo (ej. `Matriculados_2009-1S.csv`)

> Los archivos que se procesan en loop (múltiples semestres) guardan un CSV por archivo fuente dentro del loop y hacen `clear` entre iteraciones para no acumular datos en memoria.

---

## Fase 2 — Inventario, Perfilado y Diccionario

**Objetivo:** documentar qué hay en cada fuente ya anonimizada; identificar inconsistencias de nomenclatura entre archivos del mismo módulo y entre módulos; producir un diccionario de variables originales.

**Do-file:** `2_LimpiezaDatos/07_inventario_datos.do`
**Salidas:**
- `logs/session_YYYY-MM-DD.md` — hallazgos y decisiones
- `docs/fuentes_datos.md` — ficha técnica de cada fuente
- `docs/DICCIONARIO_VARIABLES_ORIGINALES.xlsx` — diccionario colaborativo (ver abajo)

### Tareas por RA

Cada RA trabaja sobre los CSVs anonimizados de su módulo en `1_DatosAnonimizados/`. Para cada dataset debe:

1. **Perfilar variables** — listar variables disponibles, tipos, rangos, tasas de missings, número de observaciones por período
2. **Detectar inconsistencias de nombres** — comparar encabezados entre todos los archivos del mismo módulo (ej. ¿`CODIGO_PROGRAMA` en 2009 se llama `COD_PLAN` en 2020?)
3. **Completar el diccionario colaborativo** — llenar las filas correspondientes a su módulo en `DICCIONARIO_VARIABLES_ORIGINALES.xlsx`

### Diccionario colaborativo (`docs/DICCIONARIO_VARIABLES_ORIGINALES.xlsx`)

Archivo Excel en Drive. Cada RA llena las columnas de su módulo. Estructura mínima:

| nombre_variable_original | módulo | tipo | descripción | valores_ejemplo | nombre_canónico_propuesto | cambia_entre_años | notas |
|---|---|---|---|---|---|---|---|
| `COD_PLAN` | Matriculados | string | código del programa académico | `2879` | `cod_plan` | No | |
| `CODIGO_PROGRAMA` | Matriculados | string | igual a COD_PLAN en archivos pre-2015 | `2879` | `cod_plan` | Sí — renombrado en 2015 | verificar |

> **Tarea crítica:** anotar explícitamente cuando un nombre de variable cambia entre años dentro del mismo módulo. El PI y CoPI asignarán el nombre canónico antes de iniciar Fase 3.

| RA | Módulo a documentar |
|---|---|
| Nicolas Camacho | Matriculados |
| Jeronimo Jimenez | Cursadas |
| Maria Jose Cadena | Cancelaciones |
| Nicolas Jimenez | Egresados y Retirados |

---

## Fase 3 — Limpieza por Dataset

Un do-file por fuente en `2_LimpiezaDatos/`. Cada uno lee los CSVs anonimizados de `1_DatosAnonimizados/`, aplica la limpieza y guarda un CSV consolidado en `DatosArmonizados/2_DatosLimpios/`.
**Regla:** nunca modificar los archivos de `1_DatosAnonimizados/`.

| Do-file | Tarea central | RA |
|---|---|---|
| `2_LimpiezaDatos/08_limpiar_matriculados.do` | Estandarizar variables de programa, período, estrato, PBM; detectar duplicados | Nicolas Camacho |
| `2_LimpiezaDatos/09_limpiar_cursadas.do` | Estandarizar código de asignatura, calificación, créditos; verificar escala 0–5 | Jeronimo Jimenez |
| `2_LimpiezaDatos/10_limpiar_cancelaciones.do` | Fecha de cancelación → período `YYYY-NS`; cruce con matriculados | Maria Jose Cadena |
| `2_LimpiezaDatos/11_limpiar_egresados.do` | Fecha de grado → período; cruce con matriculados para validar | Nicolas Jimenez |
| `2_LimpiezaDatos/12_limpiar_retirados.do` | Período de retiro; tipo de retiro; cruce con estados académicos | Nicolas Jimenez |

---

## Fase 4 — Armonización de IDs y Períodos

**Do-files:** `3_Armonizacion/13_armonizar_ids.do`, `3_Armonizacion/14_armonizar_periodos.do`

### IDs entre datasets (`13_armonizar_ids.do`)
- Verificar que todos los datasets limpios tienen `id_unal` correctamente asignado
- Documentar estudiantes que aparecen en datasets secundarios pero no en Matriculados

### Formato de períodos (`14_armonizar_periodos.do`)
- Formato canónico: `YYYY-NS` (ej. `2016-1S`, `2023-2S`)
- Manejar variantes: `20161`, `2016-I`, `2016S1`
- Generar `periodo_num` (entero ordinal) para ordenamiento correcto en el panel

---

## Fase 5 — Construcción del Panel Maestro

**Do-file:** `4_BasesdeTrabajo/15_construir_panel.do`
**Backbone:** `Matriculados` (define quién es estudiante activo en cada período)

```
Panel maestro: id_unal × periodo × cod_plan
│
├── join Cursadas       → desempeño académico por período
├── join Cancelaciones  → indicador cancelo_semestre
├── join Egresados      → indicador graduado, fecha_grado, titulo
└── join Retirados      → indicador retirado, periodo_retiro
```

> **Nota:** join de Rendimiento Matemáticas Básicas queda pendiente hasta confirmar existencia y granularidad de esa fuente.

**Clave del panel:** `(id_unal, periodo, cod_plan)`
**Tipo de panel:** desequilibrado — un estudiante con doble titulación genera múltiples filas por período.

### Variables de estado al cierre de cada período

| Variable | Fuente | Descripción |
|---|---|---|
| `papa_periodo` | Cursadas | GPA acumulado al período |
| `promedio_periodo` | Cursadas | Promedio del semestre |
| `creditos_aprob` | Cursadas | Créditos aprobados en el período |
| `creditos_reprob` | Cursadas | Créditos reprobados en el período |
| `cancelo` | Cancelaciones | 1 si canceló el semestre completo |
| `graduado` | Egresados | 1 si se graduó en este período |
| `retirado` | Retirados | 1 si se retiró del programa |

---

## Fase 6 — Control de Calidad

**Do-file:** `4_BasesdeTrabajo/16_control_calidad.do`
**Salida:** `logs/QC_report_YYYY-MM-DD.md`

Checklist automatizado:
- [ ] Unicidad de la clave `(id_unal, periodo, cod_plan)`
- [ ] Ningún `id_unal` con datos personales residuales
- [ ] Calificaciones en rango 0–5 en todas las variables de promedio
- [ ] Períodos en rango 2009-1S a 2025-2S
- [ ] Ningún estudiante con `graduado=1` y `retirado=1` simultáneamente
- [ ] Distribución de estrato consistente con promedios UNAL reportados
- [ ] Conteo de observaciones por período vs. totales en fuentes oficiales

---

## Fase 7 — Muestra y Entregables

**Do-file:** `4_BasesdeTrabajo/17_crear_muestra.do`

Muestra aleatoria estratificada 5%, estratificada por período y programa. Semilla documentada para replicabilidad.

### Archivos finales

| Archivo | Ubicación en Drive | Descripción |
|---|---|---|
| `BASE_FCE_ARMONIZADA.csv` | `FinalWorkingDataSets/` | Panel maestro completo |
| `MUESTRA_FCE_5PCT.csv` | `DatosArmonizados/muestras/` | Muestra para uso en curso |
| `LLAVE_ID_UNAL_FCE.csv` | `DatosArmonizados/keys/` | Crosswalk `id_unal` ↔ ID real (confidencial) |
| `DICCIONARIO_FCE.md` | `docs/` (repo) | Diccionario de todas las variables |

---

## Cronograma

| Semana | Fase | Do-files | Responsables |
|---|---|---|---|
| 1 | Fase 0 — Infraestructura + llave | `01` | PI + CoPI + Nicolas Camacho |
| 1–2 | Fase 1 — Anonimización de archivos originales | `02` – `06` | RAs según asignación |
| 2 | Fase 2 — Inventario, perfilado y diccionario | `07` + Excel colaborativo | Todos los RAs |
| 2–4 | Fase 3 — Limpieza por dataset | `08` – `12` | RAs según asignación |
| 4 | Fase 4 — Armonización de IDs y períodos | `13`, `14` | Todos los RAs |
| 5–6 | Fase 5 — Panel maestro | `15` | PI + CoPI |
| 6 | Fase 6 — Control de calidad | `16` | Todos los RAs |
| 7 | Fase 7 — Muestra y entregables | `17` | PI + CoPI |

---

*Última actualización: 2026-04-14 — Fase 0 incluye creación de llave; Fase 1 anonimiza todos los archivos originales y guarda CSVs en `1_DatosAnonimizados/`; todos los outputs son CSV, sin archivos .dta*
