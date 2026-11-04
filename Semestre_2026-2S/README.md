# Guía para RAs — Semestre 2026-2S
## Semillero de Microeconometría · UNAL

Esta guía explica **cómo configurar tu entorno, dónde va cada cosa y qué reglas seguir**. Para el contexto general de los proyectos, lee primero la [Introducción al semestre](INTRODUCCION_2026-2S.md).

---

## 1. Tu proyecto, tu rama y tu plan

| RA | Proyecto | Rama de Git | Plan de trabajo |
|---|---|---|---|
| Jerson Stiven Moreno Blanco | 202602_01_CambioPlanesCurriculares | `ra/jmoreno` | [PLAN_JersonMoreno.md](planes/PLAN_JersonMoreno.md) |
| Dilan Thomas Tovar Roa | 202602_02_TimingAdmision | `ra/dtovar` | [PLAN_DilanTovar.md](planes/PLAN_DilanTovar.md) |
| Julian Esteban Bermudez Chiguasuque | 202602_02_TimingAdmision | `ra/jbermudez` | [PLAN_JulianBermudez.md](planes/PLAN_JulianBermudez.md) |
| Manuela Carrillo Castro | 202602_03_ModalidadTrabajoGrado | `ra/mcarrillo` | [PLAN_ManuelaCarrillo.md](planes/PLAN_ManuelaCarrillo.md) |
| Nicolas Jimenez Castaneda | 202602_04_AdmisionPandemia | `ra/njimenez` | [PLAN_NicolasJimenez.md](planes/PLAN_NicolasJimenez.md) |
| Jeronimo Jimenez Castaneda | Administración Repositorio + DANE C600 | `ra/jjimenez` | [PLAN_JeronimoJimenez.md](planes/PLAN_JeronimoJimenez.md) |

### Organización de ramas

```
main                      ← aprobado: documentación, reglas y código revisado
├── BorradoresCodigo      ← solo el repositorio de datos (pipeline; Jeronimo y Nicolas)
└── Proyectos2026-2S      ← rama del semestre: planes y código de los proyectos
    ├── ra/jmoreno   ├── ra/dtovar   ├── ra/jbermudez
    ├── ra/mcarrillo ├── ra/njimenez └── ra/jjimenez
```

Tu rama sale de `Proyectos2026-2S` y tus *pull requests* van hacia `Proyectos2026-2S`. Al final del semestre, después de la revisión, `Proyectos2026-2S` se integra a `main`.

Tu plan tiene tareas semanales con checkboxes. **Actualízalo en tu rama antes de cada reunión semanal**:

- `[x]` completada · `[-]` en progreso · `[ ]` no iniciada · `[!]` bloqueada (explica el bloqueo en la sección *Bitácora* de tu plan)

---

## 2. Dónde va cada cosa

**Código → GitHub** (este repositorio, en tu rama)
```
SemilleroAnalisisEconometrico/            ← repo
├── Semestre_2026-2S/
│   ├── INTRODUCCION_2026-2S.md
│   ├── README.md                          ← esta guía
│   └── planes/PLAN_<Nombre>.md            ← tu plan (lo actualizas tú)
└── Proyectos/
    └── 202602_0X_<Proyecto>/              ← TU código va aquí
        ├── 00_config.[R|py|do]            ← rutas de tu máquina (único lugar con rutas absolutas)
        ├── 01_base_trabajo_<INICIALES>.[ext]
        ├── 02_descriptivas_<INICIALES>.[ext]
        └── ...
```

**Datos, outputs y documentos → Google Drive** (carpeta compartida `SemilleroMicroeconometriaProyectos`)
```
SemilleroMicroeconometriaProyectos/
├── FinalWorkingDataSets/        ← SOLO LECTURA: bases anónimas del repositorio
│   ├── Matriculados/            BASE_MATRICULADOS.csv
│   ├── Cursados/                BASE_CURSADAS_[YYYY-NS].csv (33 archivos)
│   ├── Egresados_Retirados/     BASE_EGRESADOS_RETIRADOS_[YYYY-NS].csv
│   └── diccionario_*.xlsx       diccionarios de las bases de trabajo
├── Diccionarios/                ← diccionarios de los módulos originales
└── 202602_0X_<Proyecto>/
    ├── code/                    ← no guardes scripts aquí; el código vive en GitHub
    ├── data/                    ← tus bases de trabajo derivadas (CSV)
    ├── Literatura/              ← papers y notas de lectura
    ├── output/                  ← tablas y figuras
    └── Revision_normativa/      ← PDFs de normas + base de normativa (CSV)
```

> **Nunca trabajes solo en tu computador personal.** Todo lo que produzcas debe quedar en GitHub (código) o en la carpeta del proyecto (datos y outputs).

---

## 3. Configuración inicial (semana 1)

1. **Firma el acuerdo de confidencialidad** y envíalo a Monica antes de acceder a los datos.
2. **Pide acceso** al repositorio de GitHub (a Jeronimo) y a la carpeta compartida de Drive (a Monica).
3. **Instala Google Drive para escritorio** y sincroniza `SemilleroMicroeconometriaProyectos`.
4. **Clona el repositorio y crea tu rama**:
   ```bash
   git clone https://github.com/mymogollonp/SemilleroAnalisisEconometrico.git
   cd SemilleroAnalisisEconometrico
   git checkout Proyectos2026-2S            # rama del semestre
   git pull
   git checkout -b ra/<tu-usuario>          # ej. ra/jmoreno (sale de Proyectos2026-2S)
   git push -u origin ra/<tu-usuario>
   ```
5. **Crea tu archivo de configuración** en `Proyectos/<tu proyecto>/00_config.[R|py|do]`. Ejemplo en R:
   ```r
   # 00_config.R — una sección por usuario; detecta la máquina por nombre de usuario
   usuario <- Sys.getenv("USERNAME")
   if (usuario == "jerso") {
     dir_proyectos <- "G:/Mi unidad/SemilleroMicroeconometriaProyectos"
   }
   dir_final    <- file.path(dir_proyectos, "FinalWorkingDataSets")
   dir_proyecto <- file.path(dir_proyectos, "202602_01_CambioPlanesCurriculares")
   dir_data     <- file.path(dir_proyecto, "data")
   dir_output   <- file.path(dir_proyecto, "output")
   ```
   Ejemplo en Python:
   ```python
   # 00_config.py
   import getpass
   from pathlib import Path
   if getpass.getuser() == "ditov":
       DIR_PROYECTOS = Path("G:/Mi unidad/SemilleroMicroeconometriaProyectos")
   DIR_FINAL    = DIR_PROYECTOS / "FinalWorkingDataSets"
   DIR_PROYECTO = DIR_PROYECTOS / "202602_02_TimingAdmision"
   ```

---

## 4. Reglas del semestre

| # | Regla |
|---|---|
| **R1** | **Commit y push al terminar cada script**, con mensajes descriptivos (`feat: base de trabajo timing — composición por sexo`). |
| **R2** | **Trabaja solo en tu rama** `ra/<usuario>`. Nunca hagas push a `main`, a `Proyectos2026-2S`, a `BorradoresCodigo` ni a la rama de otro RA. Para integrar tu trabajo, abre un *pull request* hacia **`Proyectos2026-2S`** y Jeronimo lo revisa. |
| **R3** | **Nunca subas datos a GitHub**: nada de `.csv`, `.xlsx`, `.dta`, `.parquet`, `.zip` ni PDFs. Revisa `git status` antes de cada commit. Si subes un dato por error, **avisa de inmediato** a Jeronimo. No intentes borrarlo tú. |
| **R4** | **`FinalWorkingDataSets/` es de solo lectura.** Tus scripts leen de ahí y escriben en `data/` u `output/` de tu proyecto. |
| **R5** | **Rutas solo en `00_config`.** Ningún otro script lleva rutas absolutas. |
| **R6** | **Un script por tarea**, numerados en orden de ejecución (`01_`, `02_`, ...), con tus iniciales al final. |
| **R7** | **Outputs de datos en CSV** (UTF-8). Tablas en CSV o LaTeX; figuras en PNG o PDF. |
| **R8** | **No intentes reidentificar a nadie.** No cruces bases anónimas con fuentes externas para identificar personas. No publiques tablas con celdas de menos de **10 estudiantes**. |
| **R9** | **Actualiza tu plan** antes de cada reunión semanal: checkboxes y bitácora. |
| **R10** | **Lenguaje libre** (R, Python, Stata), pero el código debe correr en otra máquina con solo cambiar `00_config`. |
| **R11** | **Nunca subas datos a ningún agente de IA, chatbot o plataforma agéntica** (ChatGPT, Claude, Gemini, Copilot, Cursor, NotebookLM, etc.). Esto incluye bases, extractos, filas de ejemplo, tablas con microdatos y capturas de pantalla de datos. Usa IA solo con código y con documentos públicos (normativa, papers). |
| **R12** | **Agentes de código solo en la carpeta del código.** Si usas Claude Code, Copilot, Cursor u otro agente, no debe buscar, explorar ni leer carpetas fuera de tu clon del repositorio, y **nunca debe leer datos** salvo autorización manual y explícita de la PI/CoPI. Ver [CLAUDE.md](../CLAUDE.md). |

---

## 5. Cómo pedir datos adicionales

Las bases finales no tienen todas las variables originales. Por ejemplo, la modalidad de trabajo de grado no quedó en ellas. Si necesitas algo más:

1. Abre un **issue en GitHub** con la etiqueta `solicitud-datos` y asígnalo a **Jeronimo Jimenez**. También puedes escribirle por correo a jerjimenezca@unal.edu.co.
2. Incluye:
   - **Proyecto** y **RA**
   - **Variable(s)** solicitada(s), y el módulo y archivo de origen si lo conoces
   - **Períodos** requeridos
   - **Para qué** la necesitas, en una línea
3. Jeronimo extrae la variable **anonimizada** (pegada por `id_unal`), la deja en la carpeta `data/` de tu proyecto y registra la entrega en el log de solicitudes.

Ningún RA, salvo los administradores (Jeronimo y Nicolas), accede a la carpeta `SemilleroAnalisisEconometrico` ni a datos con información personal.

---

## 6. Las bases de trabajo en breve

| Base | Nivel de observación | Variables clave |
|---|---|---|
| `BASE_MATRICULADOS` | estudiante–plan–período | `id_unal`, `periodo`, `cod_plan`, programa, facultad, nivel, acceso/subacceso, `puntaje_admision`, `convocatoria`, sexo, edad, residencia, nacimiento, etnia, colegio, PBM y componentes, estrato |
| `BASE_CURSADAS_[YYYY-NS]` | estudiante–plan–período | créditos cursados, aprobados y reprobados por tipología; promedios simple y PAPA, del período y acumulados |
| `BASE_EGRESADOS_RETIRADOS_[YYYY-NS]` | estudiante–plan–período | `graduado`, `retirado`, causal de bloqueo, créditos conseguidos, promedio, `porcentaje_avance` |

- **Llave de pegue entre bases:** `id_unal` + `periodo` + `cod_plan`. Ojo con las mayúsculas: Egresados usa `ID_UNAL` y `COD_PLAN`.
- **Separador:** las bases usan `;` y codificación UTF-8 con BOM.
- **Diccionarios:** `FinalWorkingDataSets/diccionario_*.xlsx`.
- La base de **Cancelaciones** todavía no está en la carpeta de proyectos. Jeronimo la publicará.

---

## 7. Literatura y normativa

- Guarda los papers en `Literatura/` y mantén un archivo `Literatura/notas_lectura.md` con un resumen de cada uno: pregunta, datos, método, resultado y relevancia para el proyecto.
- La normativa se guarda en `Revision_normativa/` como PDFs y, sobre todo, como una **base sistematizada** `Revision_normativa/base_normativa.csv` con columnas mínimas:

  | columna | descripción |
  |---|---|
  | `id_norma` | identificador propio |
  | `tipo` | Acuerdo, Resolución, Circular… |
  | `numero`, `anio`, `fecha` | identificación de la norma |
  | `organo` | CSU, Consejo Académico, Consejo de Facultad, Dirección de Admisiones… |
  | `alcance` | universidad, sede, facultad o programa (con `cod_plan` si aplica) |
  | `tema` | admisión, plan de estudios, trabajo de grado… |
  | `periodo_vigencia` | primer período académico afectado (`YYYY-NS`) |
  | `resumen` | 2–3 líneas |
  | `deroga_modifica` | normas que modifica o deroga |
  | `url` | enlace a la fuente |

---

## 8. Contactos

| Para… | Escribe a |
|---|---|
| Dudas de investigación y tareas | Monica Mogollon (CoPI) |
| Acceso al repositorio, datos adicionales, problemas con Git | Jeronimo Jimenez — jerjimenezca@unal.edu.co |
| Datos de admisión, indicadores y dashboard | Nicolas Jimenez — nijimenezca@unal.edu.co |

---

*Última actualización: 2026-11-03*
