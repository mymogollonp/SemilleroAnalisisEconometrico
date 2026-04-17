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

### Scripts de referencia para inventario

> Los do-files en `1_LimpiezaDatos/02_inventario_*.do` son scripts de referencia generados previamente. Los RAs **no están obligados a ejecutarlos** — cada RA debe escribir su propio script de inventario en el lenguaje de su preferencia (Stata, R o Python).

| Script de referencia (Stata) | Responsable | Descripción |
|---|---|---|
| `1_LimpiezaDatos/02_inventario_matriculados.do` | Nicolas Camacho | Referencia: perfila Matriculados; identifica campo de ID, consistencia de variables, clave única |
| `1_LimpiezaDatos/02_inventario_cursadas.do` | Jeronimo Jimenez | Referencia: perfila Cursadas; verifica escala 0–5; identifica clave única |
| `1_LimpiezaDatos/02_inventario_cancelaciones.do` | Maria Jose Cadena | Referencia: perfila Cancelaciones; identifica formato de fecha y clave única |
| `1_LimpiezaDatos/02_inventario_egresados.do` | Nicolas Jimenez | Referencia: perfila Egresados; identifica formato de fecha de grado y clave única |
| `1_LimpiezaDatos/02_inventario_retirados.do` | Nicolas Jimenez | Referencia: perfila Retirados_desde_2009.xlsx; identifica clave única |

### Paso 1b — Master Dataset de Personas por Módulo (con PII)

Cada RA construye su propio Master Personas iterando sobre **todos** los archivos de su módulo. El objetivo es capturar, por cada persona única, **todos los valores observados** de identificadores, tipo y número de documento, sexo/género y nombre — no tomar un único valor, sino la historia completa.

#### Variables canónicas del output

| Nombre canónico | Descripción | Notas de construcción |
|---|---|---|
| `correo` | Correo institucional (@unal.edu.co) | Llave principal de deduplicación |
| `tipo_documento` | Tipo de ID (CC, CE, PA, TI, NUIP, PEP…) | Registrar **todos** los tipos observados para la persona |
| `numero_documento` | Número del documento de identidad | Verificar formato (ver abajo) |
| `nombre_completo` | Nombre tal como aparece en la fuente | Puede variar entre archivos; conservar todas las variantes |
| `sexo` | Sexo/género tal como está registrado en la fuente | **Registrar todos los valores distintos observados** — una persona puede cambiar de género entre períodos |

#### Reglas de construcción

1. **Iterar sobre todos los archivos del módulo** — no trabajar solo con el más reciente.
2. **Armonizar nombres de variables**: si la fuente usa `CORREO_UNAL`, `email`, `GENERO`, `SEXO_BIO`, etc., renombrar a los nombres canónicos antes de apilar.
3. **Sexo/género — registrar todos los valores observados**: una persona puede aparecer con valores distintos de sexo/género en distintos semestres. Conservar todos los pares `(correo, sexo, periodo)` distintos; no reducir a un único valor. Reportar el número de personas con más de un valor observado.
4. **Tipo de documento — registrar todos los tipos**: si una persona aparece con CC en algunos archivos y CE en otros, conservar ambos registros. Verificar que los tipos correspondan a códigos reconocidos (CC, CE, PA, TI, NUIP, PEP). Reportar cualquier código desconocido.
5. **Verificar formato del número de documento**:
   - `CC` (Cédula de ciudadanía): numérico, 6–10 dígitos
   - `CE` (Cédula de extranjería): alfanumérico, puede tener prefijos de país
   - `PA` (Pasaporte): alfanumérico, longitud variable
   - `TI` (Tarjeta de identidad): numérico, 10–11 dígitos
   - Anotar en el reporte semanal todo número de documento que no cumpla el formato esperado para su tipo.
6. **Guardar como** `DatosArmonizados/keys/MASTER_PERSONAS_[MODULO]_PII.csv` (confidencial, solo en Drive — nunca a GitHub).
7. **Reportar en el reporte semanal**: N personas únicas, distribución de tipos de documento, N personas con más de un valor de sexo/género, N documentos con formato inválido.

| RA | Archivo de salida (en `DatosArmonizados/keys/`) |
|---|---|
| Nicolas Camacho | `MASTER_PERSONAS_MATRICULADOS_PII.csv` |
| Jeronimo Jimenez | `MASTER_PERSONAS_CURSADAS_PII.csv` |
| Maria Jose Cadena | `MASTER_PERSONAS_CANCELACIONES_PII.csv` |
| Nicolas Jimenez | `MASTER_PERSONAS_EGRESADOS_PII.csv` y `MASTER_PERSONAS_RETIRADOS_PII.csv` |

> **Consolidación:** una vez todos los RAs entreguen sus archivos, el PI o Data Scientist consolida en `MASTER_PERSONAS_PII.csv`. La consolidación debe resolver conflictos de tipo/número de documento y producir un registro de sexo/género por período a nivel de persona única.

### Creación de la llave de anonimización

**Script de referencia (Stata):** `1_LimpiezaDatos/01_crear_llave_idunal.do`
**Responsable:** Nicolas Camacho (una vez que el PI/Data Scientist haya consolidado `MASTER_PERSONAS_PII.csv`)
**Salida:** `DatosArmonizados/keys/LLAVE_ID_UNAL_FCE.csv` (confidencial)

1. Leer `MASTER_PERSONAS_PII.csv` (archivo consolidado — prerequisito: todos los RAs deben haber entregado su MASTER_PERSONAS_[MODULO]_PII.csv)
2. Generar `id_unal` mediante permutación aleatoria con semilla `20260223`, formato `UNAL000001`
3. Guardar crosswalk `id_real ↔ id_unal` como `LLAVE_ID_UNAL_FCE.csv`
4. Notificar al equipo que la llave está disponible

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
