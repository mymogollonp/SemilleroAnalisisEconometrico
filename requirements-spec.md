# Requirements Specification: Armonización de Datos UNAL
## Semillero de Análisis Econométrico

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

- Files with extensions `.csv`, `.dta`, `.xlsx`, `.zip`, or any other data format are **permanent and unmodifiable in their original version**.
- If a file requires transformation, generate a **new derived file** whose name reflects the processing step (e.g., `BASE_FCE_ARMONIZADA_con_id.dta`).
- The original file remains untouched as the source of truth.
- Never use destructive commands on data: no unconditional `drop`, no `keep` without saving first, no overwriting of original CSVs.
- If a data value appears erroneous, document it in the session log but **do not delete it**.
- **Do not delete any original file without explicit written permission from the Research Director.**

---

## Rule 2 — Never Delete Code

> **No do-file, script, or code file is ever deleted.**

- All do-files (`.do`), scripts, notebooks, and code files are **permanent**.
- If a program becomes obsolete or is superseded by an improved version, keep the original and create the new one with a different name or incremented version number.
  - Example: `02_limpiar_matriculados_v1.do` → `02_limpiar_matriculados_v2.do` (do not delete v1).
- Fixes are made by creating new files, not by overwriting previous ones without a backup.
- This rule applies to all code: Stata do-files, R scripts, Python scripts, Jupyter notebooks, and any other analysis code.

---

## Rule 3 — Stay Within Project Directories

> **All project work happens inside the two root directories defined above.**

- Do-files must set the working directory via `cd` or via the global macro `${dir_datos}` / `${dir_code}` at startup.
- Never read or write files outside these directories without documenting the exception in the session log.
- All paths in code must be **relative** or use the global macros for portability across machines.
- Outputs (tables, figures, logs) are saved inside designated subdirectories:
  - `logs/` — session logs
  - `DatosArmonizados/outputs/` — tables and figures
  - `DatosArmonizados/panel/` — processed panel datasets
  - `DatosArmonizados/muestras/` — samples
  - `DatosArmonizados/keys/` — anonymization crosswalks (confidential)

---

## Rule 4 — No Data in GitHub

> **The code repository contains code, documentation, and logs only — never data.**

- The `.gitignore` must exclude all data formats: `*.csv`, `*.dta`, `*.xlsx`, `*.xls`, `*.zip`, `*.rar`.
- Anonymization keys and any file containing personal identifiers must never be committed.
- Large binary files (Word documents, PDFs) go in Google Drive, not in the repo.

---

## Rule 5 — Anonymization Before Sharing

> **No working file outside `DatosArmonizados/keys/` may contain personal identifiers.**

- Personal identifiers include: full name, email address, national ID (cédula), student code, and date of birth.
- All shared or published datasets use `id_unal` (anonymous, randomly permuted, format `UNAL000001`).
- The crosswalk `id_unal ↔ real identifier` is stored only in `DatosArmonizados/keys/` and is never shared outside the Research Director's authorization.
- Anonymization seed must be documented in the do-file that generates it.

---

## Rule 6 — Session Log Required

> **Every working session produces a session log.**

- Log file: `logs/session_YYYY-MM-DD.md`
- Minimum content: datasets opened, transformations applied, decisions made, anomalies found, next steps.
- If multiple sessions occur on the same date, append to the existing log with a timestamp header.

---

## File Naming Conventions

| File type | Convention | Example |
|---|---|---|
| Main do-file | `NN_descripcion.do` | `02_limpiar_matriculados.do` |
| Versioned do-file | `NN_descripcion_vK.do` | `02_limpiar_matriculados_v2.do` |
| Original data | `NOMBRE_ORIGINAL.ext` | `Matriculados_2023-2S.xlsx` |
| Processed data | `NOMBRE_descriptor.dta` | `BASE_FCE_ARMONIZADA_con_id.dta` |
| Session log | `session_YYYY-MM-DD.md` | `session_2026-04-13.md` |
| QC report | `QC_report_YYYY-MM-DD.md` | `QC_report_2026-04-13.md` |

---

## Directory Structure

```
C:\code\SemilleroAnalisisEconometrico\          ← GitHub repo
├── requirements-spec.md                         ← this file
├── README.md
├── .gitignore                                   ← excludes all data formats
├── code\
│   ├── 00_configuracion.do                     ← global path macros
│   ├── 01_inventario_datos.do
│   ├── 02_limpiar_matriculados.do
│   ├── 03_limpiar_cursadas.do
│   ├── 04_limpiar_cancelaciones.do
│   ├── 05_limpiar_egresados.do
│   ├── 06_limpiar_retirados.do
│   ├── 07_limpiar_rendimiento_mat.do
│   ├── 08_crear_llave_ids.do
│   ├── 09_armonizar_periodos.do
│   ├── 10_construir_panel.do
│   ├── 11_control_calidad.do
│   └── 12_crear_muestra.do
├── docs\
│   ├── DICCIONARIO.md
│   └── fuentes_datos.md
└── logs\
    └── .gitkeep

C:\Drive2023\UNAL_Docente\SemilleroAnalisisEconometrico\   ← Google Drive
├── DatosOriginales\                            ← NEVER MODIFIED
│   └── Registro_FCE_2025\
│       ├── Matriculado\
│       ├── Cursadas\
│       ├── Cancelaciones\
│       ├── Egresados\
│       └── Retirados_desde_2009.xlsx
├── DatosProcesados\
│   └── ProcesadosMarcos\                       ← inherited from prior project
└── DatosArmonizados\                           ← outputs of this project
    ├── keys\                                   ← confidential crosswalks
    ├── panel\                                  ← main harmonized panels
    ├── muestras\                               ← samples
    └── outputs\                               ← tables and figures
```

---

## Approval

[x] Research Director approved: 2026-04-13
