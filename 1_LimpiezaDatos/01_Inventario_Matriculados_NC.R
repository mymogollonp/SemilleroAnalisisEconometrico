# =============================================================================
# 01_Inventario_Matriculados_NC.R
# Script de inventario — Módulo Matriculados
# RA: Nicolas Camacho
# Proyecto: Semillero Análisis Econométrico — UNAL FCE
# Fecha: 2026-04-19
# =============================================================================
# PROPÓSITO: Cargar todos los archivos del módulo y reportar:
#   1. Estructura general (filas, columnas, tipos)
#   2. Duplicados por archivo
#   3. Consistencia de variables entre semestres
#   4. Clave única de observación
#   5. Missings en variables clave
# OUTPUT: Imprime reporte en consola + guarda resumen en CSV
# =============================================================================

# Por si es necesario limpiar el entorno
rm(list=ls())

library(readxl)
library(dplyr)
library(tidyr)

# --- 1. Rutas -----------------------------------------------------------------
ruta_matriculados <- "C:/Users/nicom/OneDrive/Documentos/Semillero_Microeconometria/datos_originales/Matriculado"
ruta_output       <- "C:/Users/nicom/OneDrive/Documentos/Semillero_Microeconometria/outputs"

if (!dir.exists(ruta_matriculados)) {
  stop("No se encontró la carpeta. Verifica la ruta:\n", ruta_matriculados)
}

# --- 2. Listar archivos -------------------------------------------------------
archivos <- list.files(ruta_matriculados, pattern = "\\.xlsx$", full.names = TRUE)

cat("============================================================\n")
cat("Total de archivos encontrados:", length(archivos), "\n")
cat("============================================================\n\n")

# --- 3. Variables clave a revisar ---------------------------------------------

vars_clave <- c(
  "PERIODO", "CORREO", "LOGIN",
  "T_DOCUMENTO", "DOCUMENTO",
  "NOMBRES_LEGAL", "APELLIDO1_LEGAL", "APELLIDO2_LEGAL",
  "SEXO_LEGAL", "GENERO"
)

# Mapa de renombres para normalizar antes de verificar clave única
renombres <- c(
  "NOMBRES"   = "NOMBRES_LEGAL",
  "APELLIDO1" = "APELLIDO1_LEGAL",
  "APELLIDO2" = "APELLIDO2_LEGAL",
  "SEXO"      = "SEXO_LEGAL"
)

# --- 4. Iterar sobre todos los archivos ---------------------------------------
resumen_lista <- list()

for (i in seq_along(archivos)) {
  
  archivo <- archivos[i]
  nombre  <- basename(archivo)
  
  cat("------------------------------------------------------------\n")
  cat("[", i, "/", length(archivos), "]", nombre, "\n")
  
  df <- tryCatch(
    read_excel(archivo, sheet = 1, col_types = "text"),
    error = function(e) {
      cat("  ERROR al leer el archivo:", conditionMessage(e), "\n")
      return(NULL)
    }
  )
  
  if (is.null(df)) next
  
  # Armonizar nombres antes de analizar
  cols_a_renombrar <- intersect(names(df), names(renombres))
  if (length(cols_a_renombrar) > 0) {
    df <- rename(df, !!!setNames(cols_a_renombrar, renombres[cols_a_renombrar]))
  }
  
  n_filas <- nrow(df)
  n_cols  <- ncol(df)
  
  # 4a. Estructura general
  cat("  Filas:", n_filas, "| Columnas:", n_cols, "\n")
  
  # 4b. Variables clave presentes / ausentes
  cols_archivo <- names(df)
  presentes    <- vars_clave[vars_clave %in% cols_archivo]
  ausentes     <- vars_clave[!vars_clave %in% cols_archivo]
  
  if (length(ausentes) > 0) {
    cat("  AVISO — variables clave AUSENTES:", paste(ausentes, collapse = ", "), "\n")
  }
  
  # 4c. Missings en variables clave presentes
  for (v in presentes) {
    n_miss <- sum(is.na(df[[v]]))
    pct    <- round(n_miss / n_filas * 100, 1)
    if (n_miss > 0) {
      cat("  Missing en", v, ":", n_miss, "(", pct, "%)\n")
    }
  }
  
  # 4d. DUPLICADOS — filas exactamente iguales
  n_dup_filas <- sum(duplicated(df))
  if (n_dup_filas > 0) {
    cat("  AVISO — filas completamente duplicadas:", n_dup_filas, "\n")
  } else {
    cat("  Duplicados exactos: ninguno\n")
  }
  
  # 4e. CLAVE ÚNICA — verificar si CORREO + PERIODO identifica cada fila
  clave_unica_ok <- NA
  if (all(c("CORREO", "PERIODO") %in% cols_archivo)) {
    n_combinaciones <- df %>% distinct(CORREO, PERIODO) %>% nrow()
    clave_unica_ok  <- (n_combinaciones == n_filas)
    if (clave_unica_ok) {
      cat("  Clave única CORREO + PERIODO: OK\n")
    } else {
      n_dup_clave <- n_filas - n_combinaciones
      cat("  AVISO — CORREO + PERIODO NO es clave única.",
          n_dup_clave, "combinaciones repetidas.\n")
      # Mostrar ejemplos de duplicados por clave
      df %>%
        group_by(CORREO, PERIODO) %>%
        filter(n() > 1) %>%
        ungroup() %>%
        select(CORREO, PERIODO) %>%
        distinct() %>%
        head(5) %>%
        { cat("  Ejemplos de CORREO+PERIODO duplicados:\n"); print(.) }
    }
  }
  
  # 4f. Tipos de documento presentes
  if ("T_DOCUMENTO" %in% cols_archivo) {
    tipos_doc <- sort(unique(df$T_DOCUMENTO))
    cat("  Tipos de documento:", paste(tipos_doc, collapse = ", "), "\n")
  }
  
  # 4g. Valores de SEXO_LEGAL y GENERO
  if ("SEXO_LEGAL" %in% cols_archivo) {
    cat("  SEXO_LEGAL valores:", paste(sort(unique(df$SEXO_LEGAL)), collapse = ", "), "\n")
  }
  if ("GENERO" %in% cols_archivo) {
    cat("  GENERO valores:", paste(sort(unique(df$GENERO)), collapse = ", "), "\n")
  }
  
  # 4h. Guardar fila de resumen
  resumen_lista[[i]] <- data.frame(
    archivo         = nombre,
    n_filas         = n_filas,
    n_columnas      = n_cols,
    dup_filas       = n_dup_filas,
    clave_unica_ok  = clave_unica_ok,
    vars_presentes  = paste(presentes, collapse = ", "),
    vars_ausentes   = paste(ausentes,  collapse = ", "),
    stringsAsFactors = FALSE
  )
}

# --- 5. Resumen consolidado ---------------------------------------------------
cat("\n============================================================\n")
cat("RESUMEN CONSOLIDADO\n")
cat("============================================================\n")

resumen_df <- bind_rows(resumen_lista)
print(resumen_df, row.names = FALSE)

# --- 6. Consistencia de columnas entre semestres ------------------------------
cat("\n============================================================\n")
cat("CONSISTENCIA DE NOMBRES DE COLUMNAS ENTRE SEMESTRES\n")
cat("============================================================\n")

encabezados  <- lapply(archivos, function(f) names(read_excel(f, n_max = 0)))
names(encabezados) <- basename(archivos)

cols_comunes    <- Reduce(intersect, encabezados)
todas_las_cols  <- unique(unlist(encabezados))
cols_inconsist  <- todas_las_cols[!todas_las_cols %in% cols_comunes]

cat("Columnas presentes en TODOS los archivos:", length(cols_comunes), "\n")
cat("Columnas inconsistentes entre archivos:  ", length(cols_inconsist), "\n")

if (length(cols_inconsist) > 0) {
  cat("\nDetalle de columnas inconsistentes:\n")
  for (col in cols_inconsist) {
    presentes_en <- names(encabezados)[sapply(encabezados, function(e) col %in% e)]
    cat(" -", col, "→ presente en", length(presentes_en), "archivo(s)\n")
  }
}

# --- 7. Guardar resumen en CSV ------------------------------------------------
if (!dir.exists(ruta_output)) {
  dir.create(ruta_output, recursive = TRUE)
  cat("\nCarpeta de outputs creada en:", ruta_output, "\n")
}

write.csv(
  resumen_df,
  file      = file.path(ruta_output, "01_INV_resumen_Matriculados_NC.csv"),
  row.names = FALSE
)

cat("\nResumen guardado en:", file.path(ruta_output, "01_INV_resumen_Matriculados_NC.csv"), "\n")
cat("\n============================================================\n")
cat("FIN DEL INVENTARIO\n")
cat("============================================================\n")
