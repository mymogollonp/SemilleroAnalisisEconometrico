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
    ├── 2_DatosLimpios\          ← outputs de limpieza (un CSV limpio por semestre por módulo)
    │   ├── Matriculado\         ← Matriculados_[YYYY-NS]_limpio.csv (34 archivos)
    │   ├── Cursadas\            ← Cursadas_[YYYY-NS]_limpio.csv (33 archivos)
    │   ├── Cancelaciones\       ← Cancelaciones_[YYYY-NS]_limpio.csv (32 archivos)
    │   ├── Egresados\           ← Egresados_[YYYY-NS]_limpio.csv (33 archivos)
    │   └── Retirados\           ← Retirados_limpio.csv (archivo único — sin semestres)
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

Un script por fuente en `1_LimpiezaDatos/`. Cada uno lee los archivos originales de `DatosOriginales/`, aplica la limpieza y guarda un CSV limpio **por semestre** en `DatosArmonizados/2_DatosLimpios/[modulo]/`.
**Regla:** nunca modificar los archivos de `DatosOriginales/`.

### Regla de privacidad — Sin PII en archivos limpios

> **Los archivos limpios no pueden contener ninguna variable que identifique directamente o indirectamente a un estudiante.**

Esto incluye, pero no se limita a:

| Tipo | Ejemplos de variables a eliminar |
|---|---|
| Identificadores directos | nombre, correo, cédula, código de estudiante, fecha de nacimiento |
| Identificadores indirectos | dirección de residencia, teléfono, municipio de residencia a nivel detallado |
| Variables académicas con identificación | nombre del director de tesis, título de la tesis |

Las variables indirectas **no se pierden** — se conservan en los archivos originales en `DatosOriginales/` y podrán limpiarse y armonizarse en una fase posterior cuando el equipo decida incluirlas. **No eliminar del archivo original; solo excluir del output limpio.**

Si un RA detecta una variable que podría identificar estudiantes y no está listada arriba, debe documentarla en su reporte semanal y consultarle al PI/CoPI antes de decidir si incluirla o excluirla.

| RA | Tarea central | Script | Output en `DatosArmonizados/2_DatosLimpios/` |
|---|---|---|---|
| Nicolas Camacho | Estandarizar variables de programa, período, estrato, PBM; detectar duplicados | `03_limpieza_Matriculados_NC.[ext]` | `Matriculado/Matriculados_[YYYY-NS]_limpio.csv` — un CSV por semestre |
| Jeronimo Jimenez | Estandarizar código de asignatura, calificación, créditos; verificar escala 0–5 | `04_limpieza_Cursadas_JJ.[ext]` | `Cursadas/Cursadas_[YYYY-NS]_limpio.csv` — un CSV por semestre |
| Maria Jose Cadena | Estandarizar fecha de cancelación → período `YYYY-NS`; cruce con matriculados | `03_limpieza_Cancelaciones_MJC.[ext]` | `Cancelaciones/Cancelaciones_[YYYY-NS]_limpio.csv` — un CSV por semestre |
| Nicolas Jimenez | Estandarizar fecha de grado → período; cruce con matriculados para validar | `03_limpieza_Egresados_NJ.[ext]` | `Egresados/Egresados_[YYYY-NS]_limpio.csv` — un CSV por semestre |
| Nicolas Jimenez | Estandarizar período de retiro; tipo de retiro | `03_limpieza_Retirados_NJ.[ext]` | `Retirados/Retirados_limpio.csv` — archivo único |

---

## Fase 7 — Armonización de IDs y Períodos

**Scripts:** `3_Armonizacion/13_armonizar_ids`, `3_Armonizacion/14_armonizar_periodos`

### IDs entre datasets
- Verificar que todos los datasets limpios tienen `id_unal` correctamente asignado
- Documentar estudiantes que aparecen en datasets secundarios pero no en Matriculados

### Formato de períodos y columnas de tiempo
- Formato canónico del período: `YYYY-NS` (ej. `2016-1S`, `2023-2S`)
- Manejar variantes: `20161`, `2016-I`, `2016S1`
- Generar `periodo_num` (entero ordinal) para ordenamiento correcto en el panel
- **Añadir a cada dataset armonizado:**
  - `academic_anio` — año académico extraído del período (ej. `2016`)
  - `academic_semester` — semestre extraído del período (`1` o `2`)

### Diccionario de variables
- Completar el diccionario de cada módulo con categorías bien definidas usando normativas y definiciones oficiales de la Universidad Nacional de Colombia (Acuerdo 008 de 2008, reglamentos estudiantiles, sistema SIA)
- Documentar explícitamente los códigos numéricos de variables categóricas: `cod_acceso`, `cod_subacceso`, `cod_nodo_inicio`, `cod_nodo_fin`, `cod_facultad`, `cod_nivel`, `tipo_nivel`, `cod_etnia`, `cod_estado_civil`

### Retirados — división por semestres
- Evaluar si `Retirados_desde_2009.xlsx` contiene una variable de período de retiro que permita dividir en archivos por semestre (igual que las demás bases)
- Si existe período de retiro: generar un CSV por semestre en `DatosArmonizados/2_DatosLimpios/Retirados/Retirados_[YYYY-NS]_limpio.csv`
- Si no existe: documentar en el diccionario y conservar como archivo único

---

## Fase 8 — Construcción de Bases de Trabajo

**Destino:** `FinalWorkingDataSets/`
**Clave de observación en todas las bases:** `(id_unal, periodo, cod_plan)`
**Regla:** cada base contiene exclusivamente las variables especificadas — no añadir columnas adicionales sin aprobación del PI/CoPI. Eliminar variables de texto que dupliquen categorías ya codificadas numéricamente.

---

### Base Matriculados

**Script:** `3_BasesdeTrabajo/01_base_matriculados.[ext]`
**Output:** `FinalWorkingDataSets/BASE_MATRICULADOS.csv`
**Consolidar para todos los períodos disponibles.**

Completar variables con información faltante cruzando con otras bases (Cursadas, Egresados). No incluir créditos cursados, promedios ni PAPA — se recalcularán en fases posteriores.

#### Variables

| Grupo | Variable | Descripción |
|---|---|---|
| **Clave** | `id_unal` | ID anónimo del estudiante |
| **Clave** | `periodo` | Período académico (`YYYY-NS`) |
| **Clave** | `academic_año` | Año académico |
| **Clave** | `academic_semestre` | Semestre (`1` o `2`) |
| **Clave** | `cod_plan` | Código del plan de estudios |
| **Programa** | `cod_programa` | Código del programa curricular |
| **Programa** | `cod_sede` | Código de sede |
| **Programa** | `sede` | Nombre de sede |
| **Programa** | `cod_facultad` | Código de facultad |
| **Programa** | `facultad` | Nombre de facultad |
| **Programa** | `cod_nivel` | Código de nivel (pregrado/posgrado) |
| **Programa** | `tipo_nivel` | Descripción del nivel |
| **Inicio** | `puntaje_admision` | Puntaje de admisión |
| **Inicio** | `convocatoria` | Convocatoria de admisión |
| **Inicio** | `cod_acceso` | Código de modalidad de acceso |
| **Inicio** | `acceso` | Descripción de modalidad de acceso |
| **Inicio** | `cod_subacceso` | Código de sub-modalidad de acceso |
| **Inicio** | `cod_nodo_inicio` | Código de nodo de inicio (nivelación o no) |
| **Inicio** | `nodo_inicio` | Descripción del nodo de inicio |
| **Inicio** | `fecha_inscripcion` | Fecha de carga de inscripción |
| **Socioeconómica** | `sexo` | Sexo/género (valor canónico: M, F, X) |
| **Socioeconómica** | `fecha_nacimiento` | Fecha de nacimiento (`YYYY-MM-DD`) |
| **Socioeconómica** | `edad_periodo` | Edad del estudiante en el período |
| **Socioeconómica** | `cod_estado_civil` | Código de estado civil |
| **Socioeconómica** | `cod_departamento_residencia` | Código DANE del departamento de residencia |
| **Socioeconómica** | `departamento_residencia` | departamento de residencia |
| **Socioeconómica** | `municipio_residencia` | Municipio de residencia |
| **Socioeconómica** | `cod_municipio_residencia` | Código DANE del municipio de residencia |
| **Socioeconómica** | `pais_nacimiento` | País de nacimiento |
| **Socioeconómica** | `municipio_nacimiento` | Municipio de nacimiento |
| **Socioeconómica** | `cod_municipio_nacimiento` | Código DANE del municipio de nacimiento |
| **Socioeconómica** | `etnia` | Pertenencia étnica |
| **Socioeconómica** | `tipo_colegio` | Tipo de colegio de origen (oficial / no oficial) |
| **Socioeconómica** | `cod_colegio` | Código del colegio de origen |
| **Socioeconómica** | `anio_terminacion_colegio` | Año de terminación del bachillerato |
| **Socioeconómica** | `pbm_consolidado` | Puntaje Básico de Matrícula consolidado |
| **Socioeconómica** | `pbm_*` | Puntajes PBM por categoría (una columna por categoría disponible) |
| **Socioeconómica** | `estrato` | Estrato socioeconómico |

---

### Base Cursadas

**Script:** `3_BasesdeTrabajo/02_base_cursadas.[ext]`
**Output:** `FinalWorkingDataSets/BASE_CURSADAS.csv`
**Consolidar para todos los períodos disponibles.**

No incluir variables distintas a las especificadas.

#### Variables

| Grupo | Variable | Descripción |
|---|---|---|
| **Clave** | `id_unal` | ID anónimo del estudiante |
| **Clave** | `periodo` | Período académico (`YYYY-NS`) |
| **Clave** | `academic_año` | Año académico |
| **Clave** | `academic_semestre` | Semestre (`1` o `2`) |
| **Clave** | `cod_plan` | Código del plan de estudios |
| **Créditos período** | `creditos_cursados_periodo` | Total de créditos cursados en el período-plan |
| **Créditos período** | `creditos_cursados_periodo_*` | Créditos cursados por tipología  |
| **Créditos período** | `creditos_aprobados_periodo` | Créditos aprobados (nota ≥ 3.0) en el período |
| **Créditos período** | `creditos_reprobados_periodo` | Créditos reprobados (nota < 3.0) en el período |
| **Créditos acumulados** | `creditos_cursados_acumulados` | Créditos cursados acumulados desde el inicio |
| **Créditos plan** | `creditos_requeridos_plan` | Total de créditos requeridos por el plan para graduarse *(pendiente confirmar disponibilidad)* |
| **Promedios** | `promedio_simple_periodo` | Promedio simple de calificaciones del período |
| **Promedios** | `promedio_simple_acumulado` | Promedio simple acumulado hasta el período |
| **Promedios** | `papa_periodo` | PAPA del período  |

---

### Base Cancelaciones

**Script:** `3_BasesdeTrabajo/03_base_cancelaciones.[ext]`
**Output:** `FinalWorkingDataSets/BASE_CANCELACIONES.csv`
**Consolidar para todos los períodos disponibles.**

No incluir variables distintas a las especificadas.

#### Variables

| Grupo | Variable | Descripción |
|---|---|---|
| **Clave** | `id_unal` | ID anónimo del estudiante |
| **Clave** | `periodo` | Período académico (`YYYY-NS`) |
| **Clave** | `academic_anio` | Año académico |
| **Clave** | `academic_semester` | Semestre (`1` o `2`) |
| **Clave** | `cod_plan` | Código del plan de estudios |
| **Cancelaciones período** | `creditos_cancelados_periodo` | Total de créditos cancelados en el período-plan |
| **Cancelaciones período** | `materias_canceladas_periodo` | Número de materias canceladas en el período |
| **Cancelaciones período** | `materias_canceladas_periodo_*` | Número de materias canceladas por tipo de cancelación |
| **Cancelaciones acumuladas** | `creditos_cancelados_acumulados` | Créditos cancelados acumulados desde el inicio |
| **Cancelaciones acumuladas** | `materias_canceladas_acumuladas` | Número de materias canceladas acumuladas hasta el período |

---

### Base Egresados-Retirados

**Script:** `3_BasesdeTrabajo/04_base_egresados_retirados.[ext]`
**Output:** `FinalWorkingDataSets/BASE_EGRESADOS_RETIRADOS.csv`
**Consolidar para todos los períodos disponibles.**

No incluir variables distintas a las especificadas.

#### Variables

| Grupo | Variable | Descripción |
|---|---|---|
| **Clave** | `id_unal` | ID anónimo del estudiante |
| **Clave** | `periodo` | Período académico (`YYYY-NS`) |
| **Clave** | `academic_anio` | Año académico |
| **Clave** | `academic_semester` | Semestre (`1` o `2`) |
| **Clave** | `cod_plan` | Código del plan de estudios |
| **Estado** | `graduado` | Binaria: 1 si se graduó en este período-plan, 0 si no |
| **Estado** | `retirado` | Binaria: 1 si se retiró en este período-plan, 0 si no |
| **Graduación** | `papa_acumulado_graduacion` | PAPA con el que se graduó |
| **Graduación** | `creditos_cursados_acumulados_graduacion` | Total de créditos cursados al momento de graduación |
| **Graduación** | `graduacion_con_meritos` | Binaria: 1 si se graduó con mérito |
| **Graduación** | `graduacion_normal` | Binaria: 1 si se graduó sin distinción especial |
| **Retiro** | `motivo_retiro` | Motivo de retiro del programa |
| **Cohorte** | `cohorte_admision` | Período de admisión al programa (`YYYY-NS`) |
| **Cohorte** | `percentil_cohorte_admision` | Percentil promedio papa entre la cohorte de admisión dentro de la cohorte |

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


---

## Fase 10 — Muestra y Entregables

**Script:** `4_BasesdeTrabajo/17_crear_muestra`

Muestra aleatoria estratificada 5%, estratificada por período y programa. Semilla documentada para replicabilidad.

### Archivos finales

| Archivo | Ubicación en Drive | Descripción |
|---|---|---|
| `MASTER_PERSONAS_ANON.csv` | `DatosArmonizados/1_DatosAnonimizados/` | Dataset maestro de personas anonimizado |
| `[Modulo]_[YYYY-NS]_limpio.csv` | `DatosArmonizados/2_DatosLimpios/[Modulo]/` | Un CSV limpio por semestre por módulo (Matriculados, Cursadas, Cancelaciones, Egresados) |
| `Retirados_limpio.csv` | `DatosArmonizados/2_DatosLimpios/Retirados/` | Archivo único limpio para Retirados |
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
