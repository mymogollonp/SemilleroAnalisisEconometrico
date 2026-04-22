# ==============================================================================
# Example_Inventario.R
# Semillero de Análisis Econométrico — UNAL
# REFERENCE SCRIPT — adapt to your module; name your script 01_Inventario_[module]_[initials].R
#
# Purpose: Inventory and profiling of all data files in one module.
#   1. Load ALL files in the module folder
#   2. General structure and duplicate detection
#   3. Variable name consistency across semesters
#   4. Identify the unique key at observation level
#
# Output: printed console report — copy relevant findings to semanaNN_[initials].md
# ==============================================================================

# ── 0. Packages ───────────────────────────────────────────────────────────────
# install.packages(c("readxl", "dplyr", "purrr", "stringr", "janitor"))
library(readxl)
library(dplyr)
library(purrr)
library(stringr)
library(janitor)

# ── 1. Configuration ──────────────────────────────────────────────────────────
# Source your config file — each RA adds their path block in 00_config.R
# source("00_config.R")

MODULE <- "Matriculados"   # change: "Cursadas", "Cancelaciones", "Egresados", "Retirados"

dir_module <- file.path(
  "C:/Drive2023/UNAL_Docente/SemilleroAnalisisEconometrico/DatosOriginales/Registro_FCE_2025",
  MODULE
)

# ── 2. Load all files ─────────────────────────────────────────────────────────
files_xlsx <- list.files(dir_module, pattern = "\\.xlsx$", full.names = TRUE, ignore.case = TRUE)
files_csv  <- list.files(dir_module, pattern = "\\.csv$",  full.names = TRUE, ignore.case = TRUE)

cat("Files found:\n")
cat("  xlsx:", length(files_xlsx), "\n")
cat("  csv :", length(files_csv),  "\n\n")

read_safe <- function(path) {
  tryCatch(
    read_xlsx(path, col_types = "text"),  # read all as text to avoid type conflicts
    error = function(e) {
      cat("ERROR reading:", basename(path), "\n", conditionMessage(e), "\n")
      NULL
    }
  )
}

data_list <- map(files_xlsx, read_safe)
names(data_list) <- basename(files_xlsx)
data_list <- compact(data_list)

cat("Files loaded successfully:", length(data_list), "\n")

# ── 3. General structure ──────────────────────────────────────────────────────
cat("\n============================================================\n")
cat("SECTION 1 — GENERAL STRUCTURE\n")
cat("============================================================\n")

walk2(data_list, names(data_list), function(df, name) {
  cat("\n---", name, "---\n")
  cat("  Rows:", nrow(df), " | Cols:", ncol(df), "\n")
  miss <- df |> summarise(across(everything(), ~sum(is.na(.x)))) |> unlist()
  miss <- miss[miss > 0]
  if (length(miss) > 0) {
    cat("  Variables with missing values:\n")
    print(sort(miss, decreasing = TRUE))
  } else {
    cat("  Missing values: none\n")
  }
})

# ── 4. Duplicates ─────────────────────────────────────────────────────────────
cat("\n============================================================\n")
cat("SECTION 2 — DUPLICATES (full-row)\n")
cat("============================================================\n")

walk2(data_list, names(data_list), function(df, name) {
  n_dup <- sum(duplicated(df))
  pct   <- round(100 * n_dup / nrow(df), 2)
  cat(name, "— duplicate rows:", n_dup, "/", nrow(df), paste0("(", pct, "%)\n"))
})

# ── 5. Variable name consistency across files ─────────────────────────────────
cat("\n============================================================\n")
cat("SECTION 3 — VARIABLE CONSISTENCY ACROSS SEMESTERS\n")
cat("============================================================\n")

all_vars <- map(data_list, names)

common_vars    <- Reduce(intersect, all_vars)
all_union_vars <- Reduce(union,     all_vars)
not_in_all     <- setdiff(all_union_vars, common_vars)

cat("\nVariables present in ALL files (", length(common_vars), "):\n", sep = "")
cat(paste0("  ", common_vars, collapse = "\n"), "\n")

if (length(not_in_all) > 0) {
  cat("\nVariables NOT present in all files — possible renames across semesters:\n")
  for (v in not_in_all) {
    present_in <- names(all_vars)[map_lgl(all_vars, ~v %in% .x)]
    cat("  ", v, "— in:", paste(basename(present_in), collapse = ", "), "\n")
  }
} else {
  cat("\nAll files share exactly the same variable names.\n")
}

# ── 6. Identify uniqueness key ────────────────────────────────────────────────
cat("\n============================================================\n")
cat("SECTION 4 — UNIQUENESS KEY CANDIDATES\n")
cat("============================================================\n")

walk2(data_list, names(data_list), function(df, name) {
  cat("\n---", name, "---\n")

  single_keys <- names(df)[map_lgl(df, ~n_distinct(.x, na.rm = FALSE) == nrow(df))]

  if (length(single_keys) > 0) {
    cat("  Single-variable unique key(s):", paste(single_keys, collapse = ", "), "\n")
  } else {
    cat("  No single-variable unique key.\n")
    cat("  Variable cardinalities (top 10):\n")
    card <- df |>
      summarise(across(everything(), ~n_distinct(.x))) |>
      unlist() |>
      sort(decreasing = TRUE) |>
      head(10)
    print(card)
    cat("  -> Test composite keys manually, e.g. correo + cod_plan + periodo\n")
  }
})

cat("\n============================================================\n")
cat("DONE. Copy findings to your semanaNN_[initials].md report.\n")
cat("============================================================\n")
