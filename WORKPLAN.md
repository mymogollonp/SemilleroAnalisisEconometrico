# Workplan: Armonización de Datos UNAL
## Semillero de Análisis Econométrico

**PI:** Karoll Gomez, Hernando Bayona
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

> **Regla global de outputs:** todos los archivos de datos se guardan en formato **CSV**. No se generan archivos `.dta`.

---

> Las reglas del proyecto para RAs están documentadas en [RULES_RA.md](RULES_RA.md).

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
C:\Drive2023\UNAL_Docente\SemilleroAnalisisEconometrico\
├── DatosOriginales\             ← READ-ONLY: nunca modificar
│   ├── Matriculado\
│   ├── Cursadas\
│   ├── Cancelaciones\
│   ├── Egresados\
│   └── Retirados\
├── Diccionarios\                ← diccionarios de variables por módulo (creados por Mauricio Hernandez)
│   ├── Diccionario_Cancelaciones.xlsx
│   ├── Diccionario_Columnas.xlsx
│   ├── Diccionario_Cursadas.xlsx
│   ├── Diccionario_Egresados.xlsx
│   ├── Dicionario_Matriculados.xlsx
│   └── Dicionario_Retirados.xlsx
├── HeredadoMarcos\
└── DatosArmonizados\
    ├── keys\                    ← crosswalks de anonimización (confidencial, nunca a GitHub)
    │   ├── MASTER_PERSONAS_MATRICULADOS_PII.csv
    │   ├── MASTER_PERSONAS_CURSADAS_PII.csv
    │   ├── MASTER_PERSONAS_CANCELACIONES_PII.csv
    │   ├── MASTER_PERSONAS_EGRESADOS_PII.csv
    │   ├── MASTER_PERSONAS_RETIRADOS_PII.csv
    │   ├── MASTER_PERSONAS_PII.csv     ← consolidado (generado por PI/Data Scientist)
    │   └── LLAVE_ID_UNAL_FCE.csv       ← crosswalk id_real ↔ id_unal
    ├── 1_DatosAnonimizados\     ← archivos originales anonimizados, un CSV por archivo fuente
    │   ├── MASTER_PERSONAS_ANON.csv
    │   ├── Matriculado\
    │   ├── Cursadas\
    │   ├── Cancelaciones\
    │   ├── Egresados\
    │   └── Retirados\
    ├── 2_DatosLimpios\          ← outputs de limpieza (un CSV limpio por módulo)
    ├── panel\                   ← panel maestro
    ├── muestras\                ← muestras
    └── outputs\                 ← tablas y figuras
```

---

## Fase 0 — Infraestructura

**Objetivo:** dejar el repositorio operativo con rutas configuradas en todas las máquinas antes de ejecutar cualquier código sobre los datos.

### Infraestructura
- [ ] Actualizar `README.md` con descripción del proyecto
- [ ] Actualizar `.gitignore` para excluir todos los formatos de datos (`*.csv`, `*.xlsx`, `*.zip`)
- [ ] Crear `code/00_configuracion.do` con globales de rutas
- [ ] Crear carpetas de salida en Drive (ver estructura arriba)
- [ ] Crear `logs/.gitkeep` para versionar la carpeta vacía
- [ ] Primer commit y push a GitHub con estructura base

### Scripts de referencia

> `1_LimpiezaDatos/Example_Inventario.R` y `1_LimpiezaDatos/Example_masterpersonas.R` son scripts de referencia en R. Cada RA adapta estos ejemplos a su módulo y los entrega con su nombre y módulo: `01_Inventario_[modulo]_[iniciales].R` y `02_masterpersonas_[modulo]_[iniciales].R`.

| Script de referencia | Tarea |
|---|---|
| `1_LimpiezaDatos/Example_Inventario.R` | Cargar todos los archivos del módulo; estructura general; duplicados; consistencia de variables entre semestres; clave única de observación |
| `1_LimpiezaDatos/Example_masterpersonas.R` | Master Dataset de Personas por módulo (con PII): extrae y armoniza correo, tipo/número de documento, nombre, sexo; registra historia completa de sexo/género; valida formatos |

### Productos esperados — Semana 1

Cada RA entrega **dos scripts** en `1_LimpiezaDatos/` con commit y push:

| RA | Script 1 — Inventario | Script 2 — Master Personas | Output en Drive (keys/) |
|---|---|---|---|
| Nicolas Camacho | `01_Inventario_Matriculados_NC.[ext]` | `02_masterpersonas_Matriculados_NC.[ext]` | `MASTER_PERSONAS_MATRICULADOS_PII.csv` |
| Jeronimo Jimenez | `01_Inventario_Cursadas_JJ.[ext]` | `02_masterpersonas_Cursadas_JJ.[ext]` | `MASTER_PERSONAS_CURSADAS_PII.csv` |
| Maria Jose Cadena | `01_Inventario_Cancelaciones_MJC.[ext]` | `02_masterpersonas_Cancelaciones_MJC.[ext]` | `MASTER_PERSONAS_CANCELACIONES_PII.csv` |
| Nicolas Jimenez | `01_Inventario_Egresados_NJ.[ext]` + `01_Inventario_Retirados_NJ.[ext]` | `02_masterpersonas_Egresados_NJ.[ext]` + `02_masterpersonas_Retirados_NJ.[ext]` | `MASTER_PERSONAS_EGRESADOS_PII.csv` + `MASTER_PERSONAS_RETIRADOS_PII.csv` |

### Paso 1b — Master Dataset de Personas por Módulo (con PII)

Cada RA construye su propio Master Personas iterando sobre **todos** los archivos de su módulo. El objetivo es capturar, por cada persona única, **todos los valores observados** de identificadores, tipo y número de documento, sexo/género y nombre — no tomar un único valor, sino la historia completa.

#### Variables canónicas del output

| Nombre canónico | Descripción | Notas de construcción |
|---|---|---|
| `correo` | Correo institucional (@unal.edu.co) | Llave principal de deduplicación |
| `tipo_documento` | Tipo de ID — valores canónicos: CC, CE, PA, TI, PEP, OTRO | Homogeneizar desde los valores originales (ver tabla de mapeo abajo). Si una persona registra más de un tipo a lo largo de los semestres, crear columnas adicionales: `tipo_documento1`, `tipo_documento2`, etc. |
| `numero_documento` | Número del documento de identidad | Verificar longitud válida por tipo (ver tabla abajo). Si cambia entre semestres, crear `numero_documento1`, `numero_documento2`, etc. |
| `nombre_completo` | Nombre del estudiante | Convertir a **mayúsculas** y eliminar caracteres especiales (tildes, ñ → N, etc.). Si varía entre archivos, conservar todas las variantes. |
| `fecha_nacimiento` | Fecha de nacimiento (si existe en la fuente) | Registrar en formato `YYYY-MM-DD`. Si no existe en ningún archivo del módulo, omitir la columna. |
| `sexo` | Sexo/género — valores canónicos: M, F, X, NA | Homogeneizar desde los valores originales (ver tabla de mapeo abajo). Si una persona registra más de un valor a lo largo de los semestres, crear columnas adicionales: `sexo1`, `sexo2`, etc. |

#### Mapeo de valores — `tipo_documento`

Homogeneizar el campo original al valor canónico antes de guardar:

| Valor original (en mayúsculas) | Valor canónico |
|---|---|
| `CEDULA`, `CEDULA DE CIUDADANIA` | `CC` |
| `TARJETA DE IDENTIDAD` | `TI` |
| `CEDULA DE EXTRANJERIA` | `CE` |
| `PASAPORTE` | `PA` |
| `PERMISO ESPECIAL DE PERMANENCIA` | `PEP` |
| `PERMISO DE RESIDENCIA Y TRABAJO`, `OTROS` | `OTRO` |

#### Mapeo de valores — `sexo`

Homogeneizar el campo original al valor canónico antes de guardar:

| Valor original (en mayúsculas) | Valor canónico |
|---|---|
| `H`, `MASCULINO` | `M` |
| `D`, `FEMENINO`, `MUJER` | `F` |
| `X`, `NO BINARIO` | `X` |
| `NO DISPONIBLE`, vacío | `NA` (valor nulo) |

#### Longitud válida del número de documento

| Tipo | Formato esperado |
|---|---|
| `CC` | Numérico, 6–10 dígitos |
| `TI` | Numérico, 10–11 dígitos |
| `CE` | Alfanumérico, longitud variable |
| `PA` | Alfanumérico, longitud variable |

Anotar en el reporte semanal todo número de documento que no cumpla el formato esperado para su tipo.

#### Reglas de construcción

1. **Iterar sobre todos los archivos del módulo** — no trabajar solo con el más reciente.
2. **Armonizar nombres de variables**: si la fuente usa `CORREO_UNAL`, `email`, `GENERO`, `SEXO_BIO`, etc., renombrar a los nombres canónicos antes de apilar.
3. **Columnas múltiples para variables que cambian**: si una persona registra distintos valores de `tipo_documento`, `numero_documento` o `sexo` en diferentes semestres, no colapsar a un único valor — crear columnas adicionales numeradas (`tipo_documento1`, `tipo_documento2`, `sexo1`, `sexo2`, etc.) ordenadas cronológicamente. Reportar el número de personas con más de un valor observado.
4. **Homogeneizar `tipo_documento`** usando la tabla de mapeo antes de guardar.
5. **Homogeneizar `sexo`** usando la tabla de mapeo antes de guardar.
6. **Estandarizar `nombre_completo`**: convertir a mayúsculas y eliminar caracteres especiales (reemplazar tildes y ñ por sus equivalentes sin acento).
7. **Verificar longitud del número de documento** según la tabla de longitudes válidas.
8. **Guardar como** `DatosArmonizados/keys/MASTER_PERSONAS_[MODULO]_PII.csv` (confidencial, solo en Drive — nunca a GitHub).
9. **Reportar en el reporte semanal**: N personas únicas, distribución de tipos de documento, N personas con más de un valor de sexo/género, N documentos con formato inválido.

| RA | Archivo de salida (en `DatosArmonizados/keys/`) |
|---|---|
| Nicolas Camacho | `MASTER_PERSONAS_MATRICULADOS_PII.csv` |
| Jeronimo Jimenez | `MASTER_PERSONAS_CURSADAS_PII.csv` |
| Maria Jose Cadena | `MASTER_PERSONAS_CANCELACIONES_PII.csv` |
| Nicolas Jimenez | `MASTER_PERSONAS_EGRESADOS_PII.csv` y `MASTER_PERSONAS_RETIRADOS_PII.csv` |

---

### Paso 1c — Consolidación del Master Dataset de Personas (con PII)

**Responsable:** Jeronimo Jimenez
**Prerequisito:** todos los RAs han entregado su `MASTER_PERSONAS_[MODULO]_PII.csv`
**Salida:** `DatosArmonizados/keys/MASTER_PERSONAS_PII.csv` (confidencial, solo en Drive)

Una vez todos los módulos estén disponibles, Jeronimo Jimenez consolida los cinco archivos en una única base maestra de personas:

1. Cargar los cinco archivos: Matriculados, Cursadas, Cancelaciones, Egresados, Retirados
2. Apilar (union) todas las filas usando los nombres canónicos como columnas comunes
3. Deduplicar por `correo` — conservar todas las variantes de tipo/número de documento, nombre y sexo tal como fueron registradas por módulo
4. Resolver conflictos: si el mismo correo tiene valores contradictorios en distintos módulos, crear columnas numeradas (`tipo_documento1`, `tipo_documento2`, etc.) en lugar de colapsar
5. Guardar como `MASTER_PERSONAS_PII.csv`
6. Reportar: N personas únicas totales, N personas que aparecen en más de un módulo, N conflictos de tipo/número de documento resueltos

> **Decisión de diseño:** se genera `id_unal` fresco para este proyecto. No se intenta cruzar con la llave heredada de `BASE_DATOS_REGISTRO_UNAL_BOGOTA`.

---

## Fase 1 — Anonimización de Archivos Originales

**Objetivo:** importar cada archivo Excel original, reemplazar el ID real por `id_unal` usando la llave de Fase 0, eliminar todas las columnas con datos personales, y guardar como CSV en `DatosArmonizados/1_DatosAnonimizados/`. Al finalizar esta fase, ningún archivo fuera de `keys/` contiene identificadores personales.

### Regla de oro
> Todo el trabajo posterior a Fase 1 opera exclusivamente sobre los CSVs anonimizados. Nunca se vuelve a abrir un archivo original para análisis.

**Objetivo:** crear un dataset maestro a nivel de persona completamente anonimizado, que contenga `id_unal` más las variables socioeconómicas e invariantes en el tiempo.

**Script:** `1_LimpiezaDatos/04_master_personas_anon` (`.do`, `.R` o `.py`) *(por crear — responsable: Nicolas Camacho)*
**Salida:** `DatosArmonizados/1_DatosAnonimizados/MASTER_PERSONAS_ANON.csv`

### Contenido del dataset

> Los RAs escriben sus propios scripts de anonimización en el lenguaje de su preferencia (Stata, R o Python). Usar los inventarios como guía para conocer los nombres exactos de las variables antes de escribir el código. Los scripts en `1_LimpiezaDatos/07_anonimizar_*.do` son referencia, no obligación.

1. **Importar** el archivo Excel (`import excel using ..., firstrow`)
2. **Merge con la llave** — `merge m:1 <id_real> using LLAVE_ID_UNAL_FCE.csv`, verificar que todos los registros cruzan (`_merge==3`)
3. **Eliminar columnas con datos personales** — nombre, correo, cédula, fecha de nacimiento y cualquier otro identificador directo
4. **Verificar** que no queden variables con identificadores personales residuales
5. **Guardar como CSV** en la subcarpeta correspondiente de `1_DatosAnonimizados/`, conservando el nombre original del archivo (ej. `Matriculados_2009-1S.csv`)

> Los archivos que se procesan en loop (múltiples semestres) guardan un CSV por archivo fuente dentro del loop y hacen `clear` entre iteraciones para no acumular datos en memoria.

---

## Fase 2 — Inventario, Perfilado y Diccionario

**Objetivo:** documentar qué hay en cada fuente; identificar inconsistencias de nomenclatura entre archivos del mismo módulo y entre módulos; completar el diccionario de variables.

### Tareas por RA

Cada RA trabaja sobre los archivos originales de su módulo en `DatosOriginales/`. Para cada dataset debe:

1. **Perfilar variables** — listar variables disponibles, tipos, rangos, tasas de missings, número de observaciones por período (salida del script de inventario)
2. **Detectar inconsistencias de nombres** — comparar encabezados entre todos los archivos del mismo módulo (ej. ¿`CODIGO_PROGRAMA` en 2009 se llama `COD_PLAN` en 2020?)
3. **Completar el diccionario de su módulo** — actualizar el archivo Excel correspondiente en `Diccionarios/`

### Diccionarios de variables (`Diccionarios/` en Drive)

Los diccionarios ya fueron creados por Mauricio Hernandez. Cada RA debe **completar y verificar** el archivo de su módulo con base en su propio inventario:

| RA | Archivo a completar | Ruta en Drive |
|---|---|---|
| Nicolas Camacho | `Dicionario_Matriculados.xlsx` | `Diccionarios/Dicionario_Matriculados.xlsx` |
| Jeronimo Jimenez | `Diccionario_Cursadas.xlsx` | `Diccionarios/Diccionario_Cursadas.xlsx` |
| Maria Jose Cadena | `Diccionario_Cancelaciones.xlsx` | `Diccionarios/Diccionario_Cancelaciones.xlsx` |
| Nicolas Jimenez | `Diccionario_Egresados.xlsx` y `Dicionario_Retirados.xlsx` | `Diccionarios/` |

> `Diccionario_Columnas.xlsx` es el diccionario de columnas comunes entre módulos — revisarlo para evitar duplicar descripciones ya existentes.

> **Tarea crítica:** anotar explícitamente cuando un nombre de variable cambia entre años dentro del mismo módulo. El PI y CoPI asignarán el nombre canónico antes de iniciar Fase 3.

---

## Fase 3 — Limpieza por Dataset

Un do-file por fuente en `2_LimpiezaDatos/`. Cada uno lee los CSVs anonimizados de `1_DatosAnonimizados/`, aplica la limpieza y guarda un CSV consolidado en `DatosArmonizados/2_DatosLimpios/`.
**Regla:** nunca modificar los archivos de `1_DatosAnonimizados/`.

| Script de referencia (Stata) | Tarea central | RA |
|---|---|---|
| `2_LimpiezaDatos/08_limpiar_matriculados.do` | Estandarizar variables de programa, período, estrato, PBM; detectar duplicados | Nicolas Camacho |
| `2_LimpiezaDatos/09_limpiar_cursadas.do` | Estandarizar código de asignatura, calificación, créditos; verificar escala 0–5 | Jeronimo Jimenez |
| `2_LimpiezaDatos/10_limpiar_cancelaciones.do` | Fecha de cancelación → período `YYYY-NS`; cruce con matriculados | Maria Jose Cadena |
| `2_LimpiezaDatos/11_limpiar_egresados.do` | Fecha de grado → período; cruce con matriculados para validar | Nicolas Jimenez |
| `2_LimpiezaDatos/12_limpiar_retirados.do` | Período de retiro; tipo de retiro; cruce con estados académicos | Nicolas Jimenez |

---

## Fase 7 — Armonización de IDs y Períodos

**Scripts:** `3_Armonizacion/13_armonizar_ids`, `3_Armonizacion/14_armonizar_periodos`

### IDs entre datasets
- Verificar que todos los datasets limpios tienen `id_unal` correctamente asignado
- Documentar estudiantes que aparecen en datasets secundarios pero no en Matriculados

### Formato de períodos
- Formato canónico: `YYYY-NS` (ej. `2016-1S`, `2023-2S`)
- Manejar variantes: `20161`, `2016-I`, `2016S1`
- Generar `periodo_num` (entero ordinal) para ordenamiento correcto en el panel

---

## Fase 8 — Construcción del Panel Maestro

**Do-file:** `4_BasesdeTrabajo/15_construir_panel.do`
**Backbone:** `Matriculados` (define quién es estudiante activo en cada período)

```
Panel maestro: id_unal × periodo × cod_plan
│
├── join PERSONAS          → variables socioeconómicas e invariantes
├── join CURSADAS          → desempeño académico por período
├── join CANCELACIONES     → indicador cancelo_semestre
├── join EGRESADOS         → indicador graduado, fecha_grado, titulo
└── join RETIRADOS         → indicador retirado, periodo_retiro
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

## Fase 9 — Control de Calidad

**Script:** `4_BasesdeTrabajo/16_control_calidad`
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

**Script:** `4_BasesdeTrabajo/17_crear_muestra`

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

*Última actualización: 2026-04-17 — Reglas de RAs extraídas a `RULES_RA.md`; cada RA construye su propio `MASTER_PERSONAS_[MODULO]_PII.csv`; consolidación por PI/Data Scientist; los scripts generados son referencia, no obligación; diccionarios ya creados por Mauricio Hernandez en `Diccionarios/` — RAs solo completan*
