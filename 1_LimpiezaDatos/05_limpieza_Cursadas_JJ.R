# =========================================================
# Tarea 4 — Diagnóstico y limpieza: Módulo Cursadas
# Proyecto: Armonización de datos académicos UNAL
# Autor: JJ
# =========================================================
#
# Este script hace tres cosas en orden:
#   PARTE 1 — Diagnóstico de variables categóricas/binarias
#   PARTE 2 — Diagnóstico de variables de texto libre
#   PARTE 3 — Limpieza y producción de CSVs limpios
#
# Input:  DatosOriginales/Cursadas/Cursadas_[YYYY-NS].xlsx
#         LLAVE_ID_UNAL_FCE.csv (correo → id_unal)
# Output: DatosArmonizados/2_DatosLimpios/Cursadas/Cursadas_[YYYY-NS]_limpio.csv
#
# Excepciones de estructura:
#   Tres archivos tienen los encabezados en fila 2 (skip = 1):
#     - Cursadas_2021-2S.xlsx
#     - Cursadas_2023-1S.xlsx
#     - Cursadas_2025-1S.xlsx
# =========================================================

library(readxl)
library(dplyr)
library(stringr)
library(readr)

# ── Rutas (compartidas por las tres partes) ─────────────────────
ruta_input  <- "Cursadas-20260419T235746Z-3-001/Cursadas"
ruta_output <- "Semana a semana/Semana 5/CSVs limpios"
ruta_llave  <- "Semana a semana/Semana 5/LLAVE_ID_UNAL_FCE.csv"

# ── Constantes compartidas ──────────────────────────────────────
archivos_excepcion <- c(
  "Cursadas_2021-2S.xlsx",
  "Cursadas_2023-1S.xlsx",
  "Cursadas_2025-1S.xlsx"
)

archivos <- sort(list.files(
  path       = ruta_input,
  pattern    = "^Cursadas_.*\\.xlsx$",
  full.names = TRUE
))

cat(sprintf("Archivos encontrados: %d\n\n", length(archivos)))

# =========================================================
# PARTE 1 — Diagnóstico: variables categóricas y binarias
# =========================================================
#
# Lee solo las 14 variables categóricas/binarias de los 33
# archivos, las apila y calcula frecuencias consolidadas.
# Output: solo consola.
# =========================================================

cat(rep("▓", 60), "\n", sep = "")
cat("PARTE 1 — DIAGNÓSTICO: VARIABLES CATEGÓRICAS Y BINARIAS\n")
cat(rep("▓", 60), "\n\n", sep = "")

vars_categoricas <- c(
  "CALIFICACION_ALFABETICA",
  "TIPO",
  "TIPOLOGIA",
  "ANULADA",
  "BLOQUEADA",
  "CERRADA",
  "CON VALIDEZ ACADEMICA",
  "ACT_PRINCIPAL",
  "TIPO_NIVEL",
  "ACCESO",
  "SUBACCESO",
  "NODO_INICIO",
  "IND",
  "CARMNL"
)

lista_cat <- vector("list", length(archivos))

for (i in seq_along(archivos)) {
  nombre_archivo <- basename(archivos[i])
  skip_filas     <- if (nombre_archivo %in% archivos_excepcion) 1L else 0L
  
  cat(sprintf("[%02d/%02d] Leyendo: %s (skip = %d)\n",
              i, length(archivos), nombre_archivo, skip_filas))
  
  df_raw <- read_excel(
    path      = archivos[i],
    sheet     = 2,
    skip      = skip_filas,
    col_types = "text"
  )
  
  cols_presentes <- intersect(vars_categoricas, colnames(df_raw))
  cols_faltantes <- setdiff(vars_categoricas, colnames(df_raw))
  
  if (length(cols_faltantes) > 0) {
    warning(sprintf("  [!] Columnas ausentes en %s: %s",
                    nombre_archivo, paste(cols_faltantes, collapse = ", ")))
  }
  
  lista_cat[[i]] <- select(df_raw, all_of(cols_presentes))
}

df_cat <- bind_rows(lista_cat)
cat(sprintf("\nFilas totales apiladas: %s\n\n", format(nrow(df_cat), big.mark = ",")))

imprimir_frecuencias <- function(df, variable) {
  cat(rep("═", 60), "\n", sep = "")
  cat(sprintf("VARIABLE: %s\n", variable))
  cat(rep("═", 60), "\n", sep = "")
  
  if (!variable %in% colnames(df)) {
    cat("  [!] Variable no encontrada en el dataset consolidado.\n\n")
    return(invisible(NULL))
  }
  
  col         <- df[[variable]]
  n_total     <- length(col)
  n_na        <- sum(is.na(col))
  n_vacio     <- sum(!is.na(col) & str_trim(col) == "")
  n_na_string <- sum(!is.na(col) & str_trim(col) == "NA")
  
  valores_validos <- col[!is.na(col) & str_trim(col) != ""]
  
  if (length(valores_validos) == 0) {
    cat("  (sin valores no vacíos)\n")
  } else {
    tbl <- sort(table(valores_validos), decreasing = TRUE)
    tabla <- data.frame(
      Valor      = names(tbl),
      Frecuencia = as.integer(tbl),
      stringsAsFactors = FALSE
    )
    tabla$Porcentaje <- sprintf("%.2f%%", 100 * tabla$Frecuencia / n_total)
    print(tabla, row.names = FALSE)
  }
  
  cat(sprintf("\n  NA reales   : %s (%.2f%%)\n",
              format(n_na, big.mark = ","), 100 * n_na / n_total))
  cat(sprintf("  \"NA\" string : %s (%.2f%%)\n",
              format(n_na_string, big.mark = ","), 100 * n_na_string / n_total))
  cat(sprintf("  Vacíos      : %s (%.2f%%)\n",
              format(n_vacio, big.mark = ","), 100 * n_vacio / n_total))
  cat(sprintf("  Total       : %s\n\n", format(n_total, big.mark = ",")))
}

for (v in vars_categoricas) {
  imprimir_frecuencias(df_cat, v)
}

# NODO_INICIO — lista completa de valores únicos
cat(rep("═", 60), "\n", sep = "")
cat("NODO_INICIO — lista completa de valores únicos\n")
cat(rep("═", 60), "\n", sep = "")

nodo        <- df_cat[["NODO_INICIO"]]
nodo_validos <- nodo[!is.na(nodo) & str_trim(nodo) != ""]
tbl_nodo    <- sort(table(nodo_validos), decreasing = TRUE)
df_nodo     <- data.frame(
  Valor      = names(tbl_nodo),
  Frecuencia = as.integer(tbl_nodo),
  stringsAsFactors = FALSE
)
df_nodo$Porcentaje <- sprintf("%.4f%%", 100 * df_nodo$Frecuencia / length(nodo))
print(df_nodo, row.names = FALSE)
cat(sprintf("\nValores únicos en NODO_INICIO: %d\n\n", nrow(df_nodo)))

# Liberar memoria
rm(lista_cat, df_cat, df_nodo)

# =========================================================
# PARTE 2 — Diagnóstico: variables de texto libre
# =========================================================
#
# Analiza FACULTAD, PROGRAMA_CURRICULAR, PLAN, ASIGNATURA
# buscando typos, strings cortos, y caracteres no ASCII.
# Output: solo consola.
# =========================================================

cat(rep("▓", 60), "\n", sep = "")
cat("PARTE 2 — DIAGNÓSTICO: VARIABLES DE TEXTO LIBRE\n")
cat(rep("▓", 60), "\n\n", sep = "")

vars_texto <- c(
  "FACULTAD",
  "PROGRAMA_CURRICULAR",
  "PLAN",
  "ASIGNATURA"
)

lista_txt <- vector("list", length(archivos))

for (i in seq_along(archivos)) {
  nombre_archivo <- basename(archivos[i])
  skip_filas     <- if (nombre_archivo %in% archivos_excepcion) 1L else 0L
  
  cat(sprintf("[%02d/%02d] Leyendo: %s (skip = %d)\n",
              i, length(archivos), nombre_archivo, skip_filas))
  
  df_raw <- read_excel(
    path      = archivos[i],
    sheet     = 2,
    skip      = skip_filas,
    col_types = "text"
  )
  
  cols_presentes <- intersect(vars_texto, colnames(df_raw))
  lista_txt[[i]] <- select(df_raw, all_of(cols_presentes))
}

df_txt <- bind_rows(lista_txt)
cat(sprintf("\nFilas totales apiladas: %s\n\n", format(nrow(df_txt), big.mark = ",")))

diagnostico_texto <- function(df, variable) {
  cat(rep("═", 60), "\n", sep = "")
  cat(sprintf("VARIABLE: %s\n", variable))
  cat(rep("═", 60), "\n", sep = "")
  
  if (!variable %in% colnames(df)) {
    cat("  [!] Variable no encontrada.\n\n")
    return(invisible(NULL))
  }
  
  col          <- df[[variable]]
  col_validos  <- col[!is.na(col) & str_trim(col) != ""]
  n_total      <- length(col)
  n_na         <- sum(is.na(col))
  n_unicos     <- length(unique(col_validos))
  
  cat(sprintf("  Total filas    : %s\n", format(n_total,  big.mark = ",")))
  cat(sprintf("  NA reales      : %s (%.2f%%)\n", format(n_na, big.mark = ","), 100 * n_na / n_total))
  cat(sprintf("  Valores únicos : %s\n\n", format(n_unicos, big.mark = ",")))
  
  tbl <- sort(table(col_validos), decreasing = TRUE)
  df_tbl <- data.frame(
    Valor      = names(tbl),
    Frecuencia = as.integer(tbl),
    stringsAsFactors = FALSE
  )
  
  cat("  --- TOP 30 más frecuentes ---\n")
  print(head(df_tbl, 30), row.names = FALSE)
  
  cat("\n  --- BOTTOM 30 menos frecuentes ---\n")
  print(tail(df_tbl, 30), row.names = FALSE)
  
  cortos <- col_validos[nchar(str_trim(col_validos)) <= 3]
  if (length(cortos) > 0) {
    cat(sprintf("\n  --- Strings de longitud <= 3 (%d casos) ---\n", length(cortos)))
    print(as.data.frame(sort(table(cortos), decreasing = TRUE)), row.names = FALSE)
  } else {
    cat("\n  Sin strings de longitud <= 3.\n")
  }
  
  no_ascii <- col_validos[str_detect(col_validos, "[^\x20-\x7E]")]
  if (length(no_ascii) > 0) {
    cat(sprintf("\n  --- Strings con caracteres no ASCII (%d casos) ---\n", length(no_ascii)))
    print(head(as.data.frame(sort(table(no_ascii), decreasing = TRUE)), 30), row.names = FALSE)
  } else {
    cat("\n  Sin caracteres no ASCII detectados.\n")
  }
  
  cat("\n")
}

for (v in vars_texto) {
  diagnostico_texto(df_txt, v)
}

# Liberar memoria
rm(lista_txt, df_txt)

# =========================================================
# PARTE 3 — Limpieza y producción de CSVs limpios
# =========================================================
#
# Lee cada archivo original, anonimiza con la llave,
# elimina PII, aplica limpieza global y específica,
# y guarda un CSV limpio por semestre.
# =========================================================

cat(rep("▓", 60), "\n", sep = "")
cat("PARTE 3 — LIMPIEZA Y PRODUCCIÓN DE CSVs\n")
cat(rep("▓", 60), "\n\n", sep = "")

dir.create(ruta_output, recursive = TRUE, showWarnings = FALSE)

# Cargar llave de anonimización
llave <- read_csv(ruta_llave, col_types = cols(.default = "c"))
cat(sprintf("Llave cargada: %s registros\n\n", format(nrow(llave), big.mark = ",")))

cols_pii <- c(
  "DOCUMENTO",
  "NOMBRES",
  "APELLIDOS",
  "CORREO",
  "CODIGO",
  "HIST_ACADEMICA"
)

# ── Función: limpiar texto (global) ─────────────────────────────
# 1. str_squish: strip + colapsa espacios internos múltiples
# 2. Mayúsculas
# 3. Tildes y caracteres especiales → ASCII
# 4. Eliminar cualquier carácter no ASCII restante
limpiar_texto <- function(x) {
  x <- str_squish(x)
  x <- str_to_upper(x)
  x <- str_replace_all(x, "Á", "A")
  x <- str_replace_all(x, "É", "E")
  x <- str_replace_all(x, "Í", "I")
  x <- str_replace_all(x, "Ó", "O")
  x <- str_replace_all(x, "Ú", "U")
  x <- str_replace_all(x, "Ü", "U")
  x <- str_replace_all(x, "Ñ", "N")
  x <- str_replace_all(x, "á", "A")
  x <- str_replace_all(x, "é", "E")
  x <- str_replace_all(x, "í", "I")
  x <- str_replace_all(x, "ó", "O")
  x <- str_replace_all(x, "ú", "U")
  x <- str_replace_all(x, "ü", "U")
  x <- str_replace_all(x, "ñ", "N")
  x <- str_replace_all(x, "[^\x20-\x7E]", "")
  x
}

# ── Diccionario de correcciones para NODO_INICIO ────────────────
# Se aplica DESPUÉS de limpiar_texto()
corregir_nodo_inicio <- function(x) {
  x <- str_replace_all(x, "\\bINICO\\b",        "INICIO")
  x <- str_replace_all(x, "\\bAPARTIR\\b",      "A PARTIR")
  x <- str_replace_all(x, "LECTO-ESCRITUA\\b",  "LECTO-ESCRITURA")
  x <- str_replace_all(x, "\\bATICIPADA\\b",    "ANTICIPADA")
  x
}

limpiar_semestre <- function(ruta_archivo, llave) {
  nombre_archivo <- basename(ruta_archivo)
  periodo        <- str_extract(nombre_archivo, "\\d{4}-\\dS")
  skip_filas     <- if (nombre_archivo %in% archivos_excepcion) 1L else 0L
  
  cat(sprintf("  Procesando: %s (skip = %d)\n", nombre_archivo, skip_filas))
  
  # 1. Leer
  df <- read_excel(
    path      = ruta_archivo,
    sheet     = 2,
    skip      = skip_filas,
    col_types = "text"
  )
  
  # 2. Join con la llave: CORREO → id_unal
  if ("CORREO" %in% colnames(df)) {
    df <- df %>%
      mutate(CORREO = str_to_lower(str_trim(CORREO))) %>%
      left_join(llave, by = c("CORREO" = "correo"))
    
    n_sin_id <- sum(is.na(df$id_unal))
    if (n_sin_id > 0) {
      cat(sprintf("  [!] %s filas sin id_unal (correo no encontrado en llave)\n",
                  format(n_sin_id, big.mark = ",")))
    }
    
    df <- df %>% relocate(id_unal, .before = CORREO)
    
  } else {
    warning(sprintf("  [!] Columna CORREO no encontrada en %s", nombre_archivo))
    df$id_unal <- NA_character_
  }
  
  # 3. Eliminar PII
  cols_a_eliminar <- intersect(cols_pii, colnames(df))
  df <- select(df, -all_of(cols_a_eliminar))
  
  # 4. Limpieza global de texto
  df <- df %>%
    mutate(across(where(is.character), limpiar_texto))
  
  # 5. Limpiezas específicas
  
  # CALIFICACION_ALFABETICA: "NA" string → NA real
  if ("CALIFICACION_ALFABETICA" %in% colnames(df)) {
    df <- df %>%
      mutate(CALIFICACION_ALFABETICA = if_else(
        CALIFICACION_ALFABETICA == "NA",
        NA_character_,
        CALIFICACION_ALFABETICA
      ))
  }
  
  # NODO_INICIO: diccionario de correcciones de typos
  if ("NODO_INICIO" %in% colnames(df)) {
    df <- df %>%
      mutate(NODO_INICIO = corregir_nodo_inicio(NODO_INICIO))
  }
  
  # 6. Guardar CSV
  nombre_salida <- sprintf("Cursadas_%s_limpio.csv", periodo)
  ruta_salida   <- file.path(ruta_output, nombre_salida)
  
  write_excel_csv(df, ruta_salida, na = "")
  
  cat(sprintf("  Guardado: %s (%s filas, %s columnas)\n\n",
              nombre_salida,
              format(nrow(df), big.mark = ","),
              ncol(df)))
  
  invisible(NULL)
}

for (f in archivos) {
  limpiar_semestre(f, llave)
}

cat("Limpieza completada.\n")
cat(sprintf("CSVs guardados en: %s\n", ruta_output))