# Requirements Specification: Armonización de Datos UNAL
## Semillero de Análisis Econométrico

**PI:** Karoll Gomez, Hernando Bayona
**CoPI:** Monica Mogollon
**Data Scientist:** Mauricio Hernandez
**Date:** 2026-04-13
**Status:** APPROVED

---

## Objective

Build a clean, harmonized, and anonymized working database from the original UNAL (Universidad Nacional de Colombia) administrative datasets, following reproducible research standards. All code is version-controlled in GitHub; all data files reside exclusively in Google Drive.

---

## Directories

| Role | Path |
|---|---|
| Code repository | `C:\code\SemilleroAnalisisEconometrico` |
| Data folder | `C:\Drive2023\UNAL_Docente\SemilleroAnalisisEconometrico` |

**Never navigate above either root directory.** Do not read or write files outside these two trees without explicit documented justification.

---

## Rule 1 — Never Delete Data

> **No data file is ever deleted.**

- Files with extensions `.csv`, `.xlsx`, `.zip`, or any other data format are **permanent and unmodifiable in their original version**.
- If a file requires transformation, generate a **new derived file** whose name reflects the processing step.
- The original file remains untouched as the source of truth.
- Never use destructive commands on data: no unconditional `drop`, no `keep` without saving first, no overwriting of original files.
- If a data value appears erroneous, document it in the session log but **do not delete it**.
- **Do not delete any original file without explicit written permission from the PI.**

---

## Rule 2 — Never Delete Code

> **No script or code file is ever deleted.**

- All scripts (`.do`, `.R`, `.py`), notebooks, and code files are **permanent**.
- If a program becomes obsolete or is superseded by an improved version, keep the original and create the new one with a different name or incremented version number.
  - Example: `07_anonimizar_matriculados_v1.R` → `07_anonimizar_matriculados_v2.R` (do not delete v1).
- Fixes are made by creating new files, not by overwriting previous ones without a backup.
- This rule applies regardless of language: Stata, R, Python, Jupyter notebooks, or any other analysis code.

---

## Rule 3 — Stay Within Project Directories

> **All project work happens inside the two root directories defined above.**

- All paths in code must use the variables defined in the project configuration file (`00_configuracion.do` for Stata, `00_config.R` for R, `00_config.py` for Python) for portability across machines. Never hardcode absolute paths outside of these configuration files.
- Never read or write files outside these directories without documenting the exception in the session log.
- Outputs (tables, figures, logs) are saved inside designated subdirectories:
  - `logs/` — session logs and inventario logs
  - `DatosArmonizados/outputs/` — tables and figures
  - `DatosArmonizados/panel/` — processed panel datasets
  - `DatosArmonizados/muestras/` — samples
  - `DatosArmonizados/keys/` — anonymization crosswalks (confidential)

---

## Rule 4 — No Data in GitHub

> **The code repository contains code, documentation, and logs only — never data.**

- The `.gitignore` must exclude all data formats: `*.csv`, `*.xlsx`, `*.xls`, `*.zip`, `*.rar`.
- Anonymization keys and any file containing personal identifiers must never be committed.
- Large binary files (Word documents, PDFs) go in Google Drive, not in the repo.

---

## Rule 5 — Anonymization Before Analysis

> **No working file outside `DatosArmonizados/keys/` may contain personal identifiers.**

- Personal identifiers include: full name, email address, national ID (cédula), student code, and date of birth.
- All shared or published datasets use `id_unal` (anonymous, randomly permuted, format `UNAL000001`).
- The `id_unal` identifier is generated fresh for this project using a documented random permutation with seed `20260223`. It is not derived from or linked to identifiers in inherited datasets from prior projects.
- The crosswalk `id_unal ↔ real identifier` is stored only in `DatosArmonizados/keys/LLAVE_ID_UNAL_FCE.csv` and is never shared outside PI authorization.
- The anonymization seed must be documented explicitly in the script that generates it.

---

## Rule 6 — CSV-Only Outputs

> **All output data files are saved in CSV format. No `.dta` or `.xlsx` output files are generated.**

- Every script that writes data must produce CSV. Language-specific equivalents:
  - Stata: `export delimited using "...", replace`
  - R: `write.csv(df, "...", row.names = FALSE)` or `readr::write_csv(df, "...")`
  - Python: `df.to_csv("...", index=False)`
- This applies to all intermediate and final outputs: anonymized files, cleaned files, panel datasets, samples, and crosswalks.
- Reading `.xlsx` originals is allowed. Writing `.xlsx` is not.

---

## Rule 7 — Session Log Required

> **Every working session produces a session log.**

- Log file: `logs/session_YYYY-MM-DD.md`
- Minimum content: datasets opened, transformations applied, decisions made, anomalies found, next steps.
- If multiple sessions occur on the same date, append to the existing log with a timestamp header.

---

## Rule 8 — Never Modify DatosOriginales

> **The `DatosOriginales/` folder is read-only.**

- No script (in any language) or manual action may create, edit, rename, or delete files inside `DatosOriginales/`.
- Scripts only **read** from `DatosOriginales/` — they never write to it.
- All outputs (anonymized, cleaned, processed) are saved in `DatosArmonizados/` or its subdirectories.
- If an original file appears incorrect or incomplete, document it in the weekly report and notify the PI/CoPI. Do not modify the file.

---

## Inventario Requirements

Each inventario script (`02_inventario_*` — Stata `.do`, R `.R`, or Python `.py`) must produce a log that documents:

1. **Total number of files** found in the source folder and whether it matches the expected count.
2. **Variable list** for each file: Stata name, type, and Excel header label.
3. **Missing values** per variable.
4. **Variable consistency across years**: which variables appear in all files vs. only some; auto-detected differences flagged with `⚠`.
5. **Unique observation key**: which variable(s) uniquely identify a row. The Stata reference script uses `capture isid` to auto-detect single-variable keys; R/Python equivalents should test uniqueness with `n_distinct()` / `df.nunique()`. If no single variable is unique, the RA must identify the composite key manually and document it.
6. **Dataset-specific checks**:
   - Cursadas: numeric variables outside the 0–5 grade scale flagged with `⚠`.
   - Cancelaciones / Egresados: string examples shown for date/period variables to identify format.
   - Retirados: summary statistics and string examples for period variables.

The RA must document all findings in their weekly task report (`RAtaskreport/semana01_*.md`) before proceeding to anonymization.

---

## File Naming Conventions

| File type | Convention | Example |
|---|---|---|
| Path-config script | `00_configuracion.do` / `00_config.R` / `00_config.py` | `00_config.R` |
| Main script (any language) | `NN_descripcion.[do\|R\|py]` | `07_anonimizar_matriculados.R` |
| Versioned script | `NN_descripcion_vK.[do\|R\|py]` | `07_anonimizar_matriculados_v2.py` |
| Exploration script | `EX_MODULO_INICIALES.[do\|R\|py]` | `EX_Cursadas_JJ.R` |
| Original data | `NOMBRE_ORIGINAL.ext` | `Matriculados_2023-2S.xlsx` |
| Anonymized output | `NOMBRE_anon.csv` | `Matriculados_2023-2S_anon.csv` |
| Processed data | `NOMBRE_descriptor.csv` | `BASE_FCE_ARMONIZADA.csv` |
| Anonymization key | `LLAVE_*.csv` | `LLAVE_ID_UNAL_FCE.csv` |
| Session log | `session_YYYY-MM-DD.md` | `session_2026-04-13.md` |
| Inventario log | `inventario_MODULO_YYYY-MM-DD.log` | `inventario_matriculados_2026-04-14.log` |
| QC report | `QC_report_YYYY-MM-DD.md` | `QC_report_2026-04-13.md` |
| RA task report | `semanaNN_NombreA.md` | `semana01_NicolasC.md` |

---

## Directory Structure

```
C:\code\SemilleroAnalisisEconometrico\              ← GitHub repo (code only)
├── requirements-spec.md                            ← this file
├── README.md
├── WORKPLAN.md
├── .gitignore                                      ← excludes *.csv, *.xlsx, *.zip, etc.
├── 00_configuracion.do                             ← global path macros; one block per machine
├── 1_LimpiezaDatos\
│   ├── 01_crear_llave_idunal.do                   ← Phase 0: generate id_unal crosswalk
│   ├── 02_inventario_matriculados.do              ← Phase 0: profile Matriculados files
│   ├── 02_inventario_cursadas.do                  ← Phase 0: profile Cursadas files
│   ├── 02_inventario_cancelaciones.do             ← Phase 0: profile Cancelaciones files
│   ├── 02_inventario_egresados.do                 ← Phase 0: profile Egresados files
│   ├── 02_inventario_retirados.do                 ← Phase 0: profile Retirados file
│   ├── 07_anonimizar_matriculados.do              ← Phase 1: anonymize Matriculados
│   ├── 08_anonimizar_cursadas.do                  ← Phase 1: anonymize Cursadas
│   ├── 09_anonimizar_cancelaciones.do             ← Phase 1: anonymize Cancelaciones
│   ├── 10_anonimizar_egresados.do                 ← Phase 1: anonymize Egresados
│   └── 11_anonimizar_retirados.do                 ← Phase 1: anonymize Retirados
├── 2_LimpiezaDatos\                               ← Phase 3: cleaning (per dataset)
├── 3_Armonizacion\                                ← Phase 4: ID and period harmonization
├── 4_BasesdeTrabajo\                              ← Phases 5–7: panel, QC, sample
├── RAtaskreport\                                  ← weekly progress reports per RA
│   ├── semana01_NicolasC.md
│   ├── semana01_JeronimoJ.md
│   ├── semana01_MariaJoseC.md
│   └── semana01_NicolasJ.md
└── logs\
    └── .gitkeep

C:\Drive2023\UNAL_Docente\SemilleroAnalisisEconometrico\   ← Google Drive (data only)
├── Acuerdo de confidencialidad Semillero Analisis Econometrico.docx
├── DatosOriginales\                               ← READ-ONLY; never modified
│   ├── Matriculado\                               ← Matriculados_2009-1S.xlsx … 2025-2S.xlsx (34 files)
│   ├── Cursadas\                                  ← Cursadas_2009-1S.xlsx … 2025-1S.xlsx (33 files)
│   ├── Cancelaciones\                             ← Cancelaciones_2009-2S.xlsx … 2025-1S.xlsx (32 files)
│   ├── Egresados\                                 ← Egresados_2009-1S.xlsx … 2025-1S.xlsx (33 files)
│   └── Retirados\
│       └── Retirados_desde_2009.xlsx              ← single file covering full period
├── HeredadoMarcos\                                ← inherited from prior project (read-only reference)
│   ├── Panel registro.zip
│   └── ProcesadosMarcos\
│       ├── BASE_DATOS_REGISTRO_UNAL_BOGOTA.csv    ← prior panel (not used directly)
│       ├── LLAVE_DATOS_REGISTRO_UNAL_BOGOTA.csv   ← prior crosswalk (confidential)
│       └── DICCIONARIO.xlsx
└── DatosArmonizados\
    ├── keys\                                      ← LLAVE_ID_UNAL_FCE.csv (confidential, never to GitHub)
    ├── 1_DatosAnonimizados\                       ← Phase 1 outputs (one CSV per source file)
    │   ├── Matriculado\
    │   ├── Cursadas\
    │   ├── Cancelaciones\
    │   ├── Egresados\
    │   └── Retirados\
    ├── 2_DatosLimpios\                            ← Phase 3 outputs (one CSV per module)
    ├── panel\                                     ← master panel
    ├── muestras\                                  ← stratified sample
    └── outputs\                                   ← tables and figures
```

---

## Script Numbering Convention

Scripts within the same processing phase share the same two-digit prefix. The extension (`.do`, `.R`, `.py`) depends on the language chosen by the RA.

| Prefix | Phase | Description |
|---|---|---|
| `00` | Configuration | Path macros; one file only |
| `01` | Phase 0 — Key generation | Anonymization crosswalk |
| `02` | Phase 0 — Inventario | One file per dataset; all run in parallel |
| `07–11` | Phase 1 — Anonymization | One file per dataset |
| `12–16` | Phase 3 — Cleaning | One file per dataset (TBD) |
| `17–18` | Phase 4 — Harmonization | IDs and periods (TBD) |
| `19` | Phase 5 — Panel | Master panel construction (TBD) |
| `20` | Phase 6 — QC | Quality control report (TBD) |
| `21` | Phase 7 — Sample | Stratified sample (TBD) |

> Exploration scripts (`EX_*`) are not numbered — they are free-form and personal to each RA.

---

## Approval

[x] Research Director approved: 2026-04-13

*Última actualización: 2026-04-14 — Reflects actual do-file structure; adds CSV-only rule, inventario requirements (unique key identification), and do-file numbering convention*
