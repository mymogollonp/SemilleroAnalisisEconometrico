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
| PI | Hernando Bayona | — |
| CoPI | Monica Mogollon | — |
| Data Scientist | Mauricio Hernandez | Todos (referente técnico) |
| RA | Nicolas Camacho | Matriculados |
| RA | Jeronimo Jimenez | Cursadas |
| RA | Maria Jose Cadena | Cancelaciones |
| RA | Nicolas Jimenez | Egresados y Retirados |

> **Rol del Data Scientist:** Mauricio Hernandez ha trabajado previamente con estos datos y está disponible para resolver dudas técnicas de los RAs sobre estructura, variables y codificación de los archivos. No tiene tareas asignadas en el workplan.

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

## Fase 0 — Infraestructura

**Objetivo:** dejar el repositorio operativo con rutas configuradas en todas las máquinas antes de ejecutar cualquier código sobre los datos.

### Tareas
- [ ] Todos los RAs clonan el repositorio y completan su bloque de rutas en `00_configuracion.do` → commit + push
- [ ] Todos los RAs firman el acuerdo de confidencialidad
- [ ] Verificar acceso a la carpeta de datos en Drive (`DatosOriginales/`)
- [ ] Crear subcarpetas de salida en `DatosArmonizados/` (ver estructura arriba)

### Do-files
| Do-file | Responsable | Descripción |
|---|---|---|
| `00_configuracion.do` | Todos | Globales de rutas — cada RA agrega su bloque y hace commit+push |

---

## Fase 1 — Master Dataset de Personas (con PII) y Llave de Anonimización

**Objetivo:** construir un dataset maestro a nivel de persona con todos los identificadores personales (PII), a partir de los archivos fuente. Sobre ese dataset maestro generar la llave de anonimización `id_unal`.

### Paso 1a — Inventarios (prerequisito)

Antes de construir el dataset maestro cada RA debe explorar sus archivos para identificar el campo de ID personal y la estructura de variables.

> Los do-files de inventario fueron generados por Claude Code como punto de partida. Cada RA debe **leerlos, entenderlos y ejecutarlos** antes de continuar. Ante dudas sobre variables o codificación, consultar a **Mauricio Hernandez**.

| Do-file | Responsable | Descripción |
|---|---|---|
| `1_LimpiezaDatos/02_inventario_matriculados.do` | Nicolas Camacho | Perfila todos los archivos Matriculados; identifica campo de ID, consistencia de variables, y clave única de observación |
| `1_LimpiezaDatos/02_inventario_cursadas.do` | Jeronimo Jimenez | Idem Cursadas; verifica escala de calificaciones 0–5; identifica clave única |
| `1_LimpiezaDatos/02_inventario_cancelaciones.do` | Maria Jose Cadena | Idem Cancelaciones; identifica formato de fecha de cancelación y clave única |
| `1_LimpiezaDatos/02_inventario_egresados.do` | Nicolas Jimenez | Idem Egresados; identifica formato de fecha de grado y clave única |
| `1_LimpiezaDatos/02_inventario_retirados.do` | Nicolas Jimenez | Perfila el archivo único Retirados_desde_2009.xlsx; identifica clave única |

### Paso 1b — Master Dataset de Personas (con PII)

**Do-file:** `1_LimpiezaDatos/03_master_personas_pii.do` *(por crear — responsable: Nicolas Camacho con apoyo de Mauricio Hernandez)*
**Salida:** `DatosArmonizados/keys/MASTER_PERSONAS_PII.csv` (confidencial — nunca a GitHub)

Compilar todos los identificadores personales únicos a partir de Matriculados (fuente primaria) y complementar con personas que aparezcan en otros módulos pero no en Matriculados:

1. Leer en loop todos los archivos `Matriculados_YYYY-NS.xlsx`, apilar IDs únicos
2. Revisar si existen personas en Cursadas / Cancelaciones / Egresados / Retirados sin registro en Matriculados; documentar
3. Consolidar una fila por persona con: ID real, nombre (si disponible), y variables de identificación disponibles
4. Guardar como `MASTER_PERSONAS_PII.csv` en `DatosArmonizados/keys/`

### Paso 1c — Llave de Anonimización

**Do-file:** `1_LimpiezaDatos/01_crear_llave_idunal.do`
**Responsable:** Nicolas Camacho
**Salida:** `DatosArmonizados/keys/LLAVE_ID_UNAL_FCE.csv` (confidencial)

1. Leer `MASTER_PERSONAS_PII.csv`
2. Generar `id_unal` mediante permutación aleatoria con semilla `20260223`, formato `UNAL000001`
3. Guardar crosswalk `id_real ↔ id_unal` como `LLAVE_ID_UNAL_FCE.csv`
4. Notificar al equipo que la llave está disponible

> **Decisión de diseño:** se genera `id_unal` fresco para este proyecto. No se intenta cruzar con la llave heredada de `BASE_DATOS_REGISTRO_UNAL_BOGOTA`. Si en el futuro se necesita vincular ambos proyectos, ese cruce se hará como paso explícito y documentado.

### Secuencia de ejecución en Fase 1

1. Todos los RAs ejecutan sus inventarios en paralelo (Paso 1a)
2. Nicolas Camacho consolida el Master Dataset de Personas con PII (Paso 1b)
3. Nicolas Camacho genera la llave y notifica al equipo (Paso 1c)

---

## Fase 2 — Master Dataset de Personas Anonimizado + Variables Clave

**Objetivo:** crear un dataset maestro a nivel de persona completamente anonimizado, que contenga `id_unal` más las variables socioeconómicas e invariantes en el tiempo. Este dataset será la tabla de personas de referencia para todo el análisis posterior.

**Do-file:** `1_LimpiezaDatos/04_master_personas_anon.do` *(por crear — responsable: Nicolas Camacho)*
**Salida:** `DatosArmonizados/1_DatosAnonimizados/MASTER_PERSONAS_ANON.csv`

### Contenido del dataset

| Tipo de variable | Ejemplos | Fuente |
|---|---|---|
| Identificador anónimo | `id_unal` | Llave (Fase 1) |
| Características de admisión | `puntaje_admision`, `pbm` | Matriculados |
| Variables socioeconómicas | `estrato`, `municipio_procedencia` | Matriculados |
| Variables académicas invariantes | `cod_plan`, `nombre_programa`, `sede` | Matriculados (primer registro) |

> **Variables invariantes en el tiempo:** si una variable cambia de valor entre períodos para el mismo estudiante, documentar la decisión de qué valor retener (primer registro, último, moda) antes de incluirla.

### Pasos
1. Leer `LLAVE_ID_UNAL_FCE.csv`
2. Leer Matriculados anonimizados; hacer merge con la llave para reemplazar ID real por `id_unal`
3. Eliminar todas las columnas con PII (nombre, correo, cédula, fecha de nacimiento)
4. Retener una fila por persona con las variables clave (resolver duplicados según criterio acordado)
5. Guardar como `MASTER_PERSONAS_ANON.csv`

---

## Fase 3 — Exploración y Diccionario

**Objetivo:** completar los archivos de diccionario ya iniciados por Mauricio Hernandez con los hallazgos de la exploración de cada dataset. Acordar nombres canónicos de variables antes de proceder a la limpieza.

> **Punto de partida:** Mauricio Hernandez ha trabajado previamente con estos datos y ha creado los archivos base de diccionario en Drive. Los RAs deben completarlos con la información que emerja de sus inventarios (Fase 1) y la exploración de los archivos originales.

### Tareas por RA

| RA | Módulo | Tarea |
|---|---|---|
| Nicolas Camacho | Matriculados | Completar diccionario; documentar cambios de nombres entre años |
| Jeronimo Jimenez | Cursadas | Completar diccionario; documentar escala de calificaciones y cambios |
| Maria Jose Cadena | Cancelaciones | Completar diccionario; documentar formato de fechas/períodos |
| Nicolas Jimenez | Egresados y Retirados | Completar diccionario de ambos módulos |

### Diccionario colaborativo (`DatosArmonizados/DICCIONARIO_VARIABLES.xlsx`)

Estructura mínima por variable:

| nombre_variable_original | módulo | tipo | descripción | valores_ejemplo | nombre_canónico_propuesto | cambia_entre_años | notas |
|---|---|---|---|---|---|---|---|
| `COD_PLAN` | Matriculados | string | código del programa académico | `2879` | `cod_plan` | No | |
| `CODIGO_PROGRAMA` | Matriculados | string | igual a COD_PLAN en archivos pre-2015 | `2879` | `cod_plan` | Sí — renombrado en 2015 | verificar con Mauricio |

> **Tarea crítica:** anotar explícitamente cuando un nombre de variable cambia entre años. El PI/CoPI y Mauricio Hernandez asignarán el nombre canónico antes de iniciar Fase 5.

---

## Fase 4 — Diseño de Tablas y Relaciones

**Objetivo:** antes de limpiar o consolidar datos, definir explícitamente el modelo relacional del proyecto: qué tablas existirán, cuál es la clave de cada una, y cómo se relacionan entre sí. Este diseño guía todas las fases de limpieza y construcción del panel.

**Responsables:** PI + CoPI + Mauricio Hernandez, con insumos de los RAs
**Salida:** `docs/modelo_relacional.md` en el repositorio

### Preguntas a resolver en esta fase

1. **Unidad de análisis del panel maestro:** ¿`id_unal × periodo`? ¿`id_unal × periodo × cod_plan`? ¿Ambas?
2. **Tabla de personas:** ¿qué variables son realmente invariantes en el tiempo para todos los estudiantes?
3. **Tabla de trayectorias:** ¿cómo manejar a un estudiante con múltiples programas simultáneos?
4. **Relaciones entre tablas:**
   - Cursadas: ¿se une al panel por `id_unal + periodo` o por `id_unal + periodo + cod_plan`?
   - Cancelaciones, Egresados, Retirados: ¿a qué nivel de granularidad?
5. **Estudiantes que aparecen en módulos secundarios pero no en Matriculados:** ¿se incluyen o excluyen?

### Esquema preliminar de tablas

```
PERSONAS           → id_unal (PK), variables invariantes
MATRICULADOS       → id_unal × periodo × cod_plan (PK)
CURSADAS           → id_unal × periodo × cod_asignatura × grupo (PK tentativa)
CANCELACIONES      → id_unal × periodo (PK tentativa — verificar si puede cancelar más de una vez)
EGRESADOS          → id_unal × cod_plan (PK tentativa — puede haber doble titulación)
RETIRADOS          → id_unal (PK tentativa — verificar si puede retirarse y reingresar)
```

> Las claves tentativas deben confirmarse contra los hallazgos de unicidad reportados por los inventarios (Fase 1).

---

## Fase 5 — Anonimización de Archivos Originales

**Objetivo:** importar cada archivo Excel original, reemplazar el ID real por `id_unal` usando la llave de Fase 1, eliminar todas las columnas con datos personales, y guardar como CSV en `DatosArmonizados/1_DatosAnonimizados/`. Al finalizar esta fase, ningún archivo fuera de `keys/` contiene identificadores personales.

### Regla de oro
> Todo el trabajo posterior a Fase 5 opera exclusivamente sobre los CSVs anonimizados. Nunca se vuelve a abrir un archivo original para análisis.

### Do-files y responsables

| Do-file | Dataset | Archivos fuente | Destino | RA |
|---|---|---|---|---|
| `1_LimpiezaDatos/07_anonimizar_matriculados.do` | Matriculados | `DatosOriginales/Matriculado/*.xlsx` (34) | `1_DatosAnonimizados/Matriculado/` | Nicolas Camacho |
| `1_LimpiezaDatos/08_anonimizar_cursadas.do` | Cursadas | `DatosOriginales/Cursadas/*.xlsx` (33) | `1_DatosAnonimizados/Cursadas/` | Jeronimo Jimenez |
| `1_LimpiezaDatos/09_anonimizar_cancelaciones.do` | Cancelaciones | `DatosOriginales/Cancelaciones/*.xlsx` (32) | `1_DatosAnonimizados/Cancelaciones/` | Maria Jose Cadena |
| `1_LimpiezaDatos/10_anonimizar_egresados.do` | Egresados | `DatosOriginales/Egresados/*.xlsx` (33) | `1_DatosAnonimizados/Egresados/` | Nicolas Jimenez |
| `1_LimpiezaDatos/11_anonimizar_retirados.do` | Retirados | `DatosOriginales/Retirados/Retirados_desde_2009.xlsx` | `1_DatosAnonimizados/Retirados/` | Nicolas Jimenez |

### Pasos por do-file (estructura común)

> Los do-files de anonimización serán escritos por cada RA en la Semana 2, después de haber ejecutado los inventarios y recibido la llave. Usar los inventarios y el diccionario como guía para los nombres exactos de variables.

1. **Importar** el archivo Excel (`import excel using ..., firstrow`)
2. **Merge con la llave** — `merge m:1 <id_real> using LLAVE_ID_UNAL_FCE.csv`, verificar que todos los registros cruzan (`_merge==3`)
3. **Eliminar columnas con datos personales** — nombre, correo, cédula, fecha de nacimiento y cualquier otro identificador directo
4. **Verificar** que no queden variables con identificadores personales residuales
5. **Guardar como CSV** en la subcarpeta correspondiente de `1_DatosAnonimizados/`

> Los archivos que se procesan en loop guardan un CSV por archivo fuente dentro del loop y hacen `clear` entre iteraciones para no acumular datos en memoria.

---

## Fase 6 — Limpieza por Dataset

Un do-file por fuente en `2_LimpiezaDatos/`. Cada uno lee los CSVs anonimizados de `1_DatosAnonimizados/`, aplica la limpieza según los nombres canónicos aprobados en Fase 3, y guarda un CSV consolidado en `DatosArmonizados/2_DatosLimpios/`.

**Regla:** nunca modificar los archivos de `1_DatosAnonimizados/`.

| Do-file | Tarea central | RA |
|---|---|---|
| `2_LimpiezaDatos/08_limpiar_matriculados.do` | Estandarizar variables de programa, período, estrato, PBM; detectar duplicados | Nicolas Camacho |
| `2_LimpiezaDatos/09_limpiar_cursadas.do` | Estandarizar código de asignatura, calificación, créditos; verificar escala 0–5 | Jeronimo Jimenez |
| `2_LimpiezaDatos/10_limpiar_cancelaciones.do` | Fecha de cancelación → período `YYYY-NS`; cruce con matriculados | Maria Jose Cadena |
| `2_LimpiezaDatos/11_limpiar_egresados.do` | Fecha de grado → período; cruce con matriculados para validar | Nicolas Jimenez |
| `2_LimpiezaDatos/12_limpiar_retirados.do` | Período de retiro; tipo de retiro; cruce con estados académicos | Nicolas Jimenez |

---

## Fase 7 — Armonización de IDs y Períodos

**Do-files:** `3_Armonizacion/13_armonizar_ids.do`, `3_Armonizacion/14_armonizar_periodos.do`

### IDs entre datasets (`13_armonizar_ids.do`)
- Verificar que todos los datasets limpios tienen `id_unal` correctamente asignado
- Documentar estudiantes que aparecen en datasets secundarios pero no en Matriculados

### Formato de períodos (`14_armonizar_periodos.do`)
- Formato canónico: `YYYY-NS` (ej. `2016-1S`, `2023-2S`)
- Manejar variantes: `20161`, `2016-I`, `2016S1`
- Generar `periodo_num` (entero ordinal) para ordenamiento correcto en el panel

---

## Fase 8 — Construcción del Panel Maestro

**Do-file:** `4_BasesdeTrabajo/15_construir_panel.do`
**Backbone:** tabla `MATRICULADOS` limpia (define quién es estudiante activo en cada período)

```
Panel maestro: id_unal × periodo × cod_plan
│
├── join PERSONAS          → variables socioeconómicas e invariantes
├── join CURSADAS          → desempeño académico por período
├── join CANCELACIONES     → indicador cancelo_semestre
├── join EGRESADOS         → indicador graduado, fecha_grado, titulo
└── join RETIRADOS         → indicador retirado, periodo_retiro
```

**Clave del panel:** `(id_unal, periodo, cod_plan)` — a confirmar según Fase 4
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

## Fase 9 — Control de Calidad

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

## Fase 10 — Muestra y Entregables

**Do-file:** `4_BasesdeTrabajo/17_crear_muestra.do`

Muestra aleatoria estratificada 5%, estratificada por período y programa. Semilla documentada para replicabilidad.

### Archivos finales

| Archivo | Ubicación en Drive | Descripción |
|---|---|---|
| `MASTER_PERSONAS_ANON.csv` | `DatosArmonizados/1_DatosAnonimizados/` | Dataset maestro de personas anonimizado |
| `BASE_FCE_ARMONIZADA.csv` | `FinalWorkingDataSets/` | Panel maestro completo |
| `MUESTRA_FCE_5PCT.csv` | `DatosArmonizados/muestras/` | Muestra para uso en curso |
| `LLAVE_ID_UNAL_FCE.csv` | `DatosArmonizados/keys/` | Crosswalk `id_unal` ↔ ID real (confidencial) |
| `DICCIONARIO_FCE.md` | `docs/` (repo) | Diccionario de todas las variables |

---

## Cronograma

| Semana | Fase | Responsables |
|---|---|---|
| 1 | Fase 0 — Infraestructura | Todos los RAs |
| 1–2 | Fase 1 — Master Personas (PII) + Llave | Nicolas Camacho (llave); todos los RAs (inventarios) |
| 2 | Fase 2 — Master Personas Anonimizado | Nicolas Camacho |
| 2 | Fase 3 — Exploración y Diccionario | Todos los RAs (insumos de Mauricio Hernandez) |
| 2–3 | Fase 4 — Diseño de Tablas y Relaciones | PI + CoPI + Mauricio Hernandez |
| 3–4 | Fase 5 — Anonimización de archivos originales | RAs según asignación |
| 4–5 | Fase 6 — Limpieza por dataset | RAs según asignación |
| 5 | Fase 7 — Armonización de IDs y períodos | Todos los RAs |
| 6 | Fase 8 — Panel maestro | PI + CoPI |
| 6 | Fase 9 — Control de calidad | Todos los RAs |
| 7 | Fase 10 — Muestra y entregables | PI + CoPI |

---

*Última actualización: 2026-04-17 — Restructuración de fases: nueva Fase 1 (Master Personas PII + llave), nueva Fase 2 (Master Personas Anonimizado), nueva Fase 3 (Diccionario), nueva Fase 4 (Diseño Relacional); adición de PI Hernando Bayona y Data Scientist Mauricio Hernandez*
