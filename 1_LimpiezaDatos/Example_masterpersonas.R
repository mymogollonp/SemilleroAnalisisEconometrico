# ==============================================================================
# Example_masterpersonas.R
# Semillero de Análisis Econométrico — UNAL
# REFERENCE SCRIPT — adapt to your module; name your script 02_masterpersonas_[module]_[initials].R
#
# Purpose: Build the Master Dataset de Personas por Módulo (con PII).
#   - Iterates over ALL files in the module folder
#   - Extracts and harmonizes PII variables to canonical names
#   - Records ALL observed values of sexo/género per person (full history)
#   - Validates document type codes and number formats
#   - Output: MASTER_PERSONAS_[MODULE]_PII.csv → DatosArmonizados/keys/
#
# !! This file is CONFIDENTIAL. It stays in Drive only — NEVER commit to GitHub.
# ==============================================================================

# ── 0. Packages ───────────────────────────────────────────────────────────────
# install.packages(c("readxl", "dplyr", "purrr", "stringr", "janitor"))
library(readxl)
library(dplyr)
library(purrr)
library(stringr)
library(janitor)

# ── 1. Configuration ──────────────────────────────────────────────────────────
# source("00_config.R")

MODULE   <- "Matriculados"   # change: "Cursadas", "Cancelaciones", "Egresados", "Retirados"
INITIALS <- "NC"             # change to your initials

dir_module <- file.path(
  "C:/Drive2023/UNAL_Docente/SemilleroAnalisisEconometrico/DatosOriginales/Registro_FCE_2025",
  MODULE
)
dir_keys <- "C:/Drive2023/UNAL_Docente/SemilleroAnalisisEconometrico/DatosArmonizados/keys"

# ── 2. Variable name mapping ──────────────────────────────────────────────────
# !! Replace the RIGHT-HAND side values with the ACTUAL column names found
# !! in your module after running Example_Inventario.R
# !! The canonical names (left side) must NOT change — they are the project standard.

VAR_MAP <- list(
  correo           = "CORREO_UNAL",   # actual column name in your files
  tipo_documento   = "TIPO_DOC",      # actual column name
  numero_documento = "NUMERO_DOC",    # actual column name
  nombre_completo  = "NOMBRE",        # actual column name
  sexo             = "SEXO"           # actual column name
)

VAR_PERIODO <- "PERIODO"  # actual column name for the academic period

# ── 3. Load and extract PII from all files ────────────────────────────────────
files_xlsx <- list.files(dir_module, pattern = "\\.xlsx$", full.names = TRUE, ignore.case = TRUE)
cat("Files to process:", length(files_xlsx), "\n")

extract_pii <- function(path) {
  df <- tryCatch(
    read_xlsx(path, col_types = "text"),
    error = function(e) {
      cat("ERROR reading:", basename(path), "\n")
      return(NULL)
    }
  )
  if (is.null(df)) return(NULL)

  df <- clean_names(df)  # standardize to snake_case for matching

  # Rename columns to canonical names using VAR_MAP (case-insensitive)
  for (canonical in names(VAR_MAP)) {
    actual_lower <- str_to_lower(VAR_MAP[[canonical]])
    match_col    <- names(df)[str_to_lower(names(df)) == actual_lower]
    if (length(match_col) == 1) {
      df <- rename(df, !!canonical := match_col)
    } else if (length(match_col) == 0) {
      cat("  WARNING:", basename(path), "— column not found for", canonical,
          "(expected '", VAR_MAP[[canonical]], "')\n")
    }
  }

  # Rename period column
  periodo_lower <- str_to_lower(VAR_PERIODO)
  match_per     <- names(df)[str_to_lower(names(df)) == periodo_lower]
  if (length(match_per) == 1) df <- rename(df, periodo = match_per)

  # Keep only canonical columns that exist in this file
  cols_keep <- intersect(c(names(VAR_MAP), "periodo"), names(df))
  df[, cols_keep, drop = FALSE]
}

all_pii <- map(files_xlsx, extract_pii) |> compact() |> bind_rows()
cat("\nTotal rows loaded across all files:", nrow(all_pii), "\n")
cat("Unique people (by correo):", n_distinct(all_pii$correo, na.rm = TRUE), "\n")

# ── 4. Build master — preserve full sexo/género history ──────────────────────
# Keep all distinct (correo, tipo_doc, num_doc, nombre, sexo, periodo) combinations.
# A person CAN have different sexo values across semesters — we keep them all.
master <- all_pii |>
  distinct(correo, tipo_documento, numero_documento, nombre_completo, sexo, periodo) |>
  arrange(correo, periodo)

# ── 5. Validate document type codes ──────────────────────────────────────────
valid_types <- c("CC", "CE", "PA", "TI", "NUIP", "PEP")

unknown_types <- master |>
  filter(!is.na(tipo_documento), !str_to_upper(tipo_documento) %in% valid_types) |>
  count(tipo_documento, sort = TRUE)

if (nrow(unknown_types) > 0) {
  cat("\nUnknown document types found (report in your weekly report):\n")
  print(unknown_types)
} else {
  cat("\nAll document types are recognized codes.\n")
}

# ── 6. Validate document number format ───────────────────────────────────────
invalid_format <- master |>
  mutate(
    invalid = case_when(
      str_to_upper(tipo_documento) == "CC" &
        !str_detect(numero_documento, "^\\d{6,10}$")  ~ TRUE,
      str_to_upper(tipo_documento) == "TI" &
        !str_detect(numero_documento, "^\\d{10,11}$") ~ TRUE,
      TRUE ~ FALSE
    )
  ) |>
  filter(invalid)

cat("Records with unexpected document number format:", nrow(invalid_format), "\n")
if (nrow(invalid_format) > 0) {
  cat("Sample of invalid records:\n")
  print(head(invalid_format, 10))
}

# ── 7. Report people with multiple sexo/género values ────────────────────────
multi_sexo <- master |>
  group_by(correo) |>
  summarise(n_sexo_values = n_distinct(sexo, na.rm = TRUE), .groups = "drop") |>
  filter(n_sexo_values > 1)

cat("\nPeople with more than one sexo/género value observed:", nrow(multi_sexo), "\n")

# ── 8. Summary report ────────────────────────────────────────────────────────
cat("\n============================================================\n")
cat("SUMMARY REPORT — paste into semanaNN_[initials].md\n")
cat("============================================================\n")
cat("Module                          :", MODULE, "\n")
cat("Files processed                 :", length(files_xlsx), "\n")
cat("Total rows (all files combined) :", nrow(all_pii), "\n")
cat("Unique people in output         :", n_distinct(master$correo, na.rm = TRUE), "\n")
cat("Rows in output (with history)   :", nrow(master), "\n")
cat("People with >1 sexo/género value:", nrow(multi_sexo), "\n")
cat("Records with invalid doc format :", nrow(invalid_format), "\n")
cat("\nDocument type distribution:\n")
print(count(master, tipo_documento, sort = TRUE))

# ── 9. Save output ────────────────────────────────────────────────────────────
out_file <- file.path(dir_keys, paste0("MASTER_PERSONAS_", str_to_upper(MODULE), "_PII.csv"))
write.csv(master, out_file, row.names = FALSE, fileEncoding = "UTF-8")
cat("\nSaved to:", out_file, "\n")
cat("!! Reminder: this file is confidential — never commit it to GitHub.\n")
