# =============================================================================
# reporte_inconsistencias.R
# Genera logs/reporte_inconsistencias_master_YYYY-MM-DD.md
# Input : MASTER_PERSONAS_PII.csv  (mismo directorio o ajustar ruta)
# Output: logs/reporte_inconsistencias_master_<fecha>.md
# El script NO modifica ni exporta ningún CSV.
# =============================================================================

library(dplyr)
library(tidyr)
library(stringr)

# ── Rutas ────────────────────────────────────────────────────────────────────
input_path          <- "Semana a semana/Semana 4/MASTER_PERSONAS_PII.csv"
sin_correo_path     <- "Semana a semana/Semana 4/REGISTROS_SIN_CORREO.csv"

dir.create("logs", showWarnings = FALSE)
fecha_hoy   <- Sys.Date()
output_path <- file.path("logs",
                         paste0("reporte_inconsistencias_master_", fecha_hoy, ".md"))

# ── Lectura ───────────────────────────────────────────────────────────────────
master <- read.csv(input_path, stringsAsFactors = FALSE, encoding = "UTF-8")

# ── Helpers ───────────────────────────────────────────────────────────────────

# Tabla markdown desde data.frame
md_table <- function(df) {
  header <- paste0("| ", paste(names(df), collapse = " | "), " |")
  sep    <- paste0("| ", paste(rep("---", ncol(df)), collapse = " | "), " |")
  rows   <- apply(df, 1, function(r) paste0("| ", paste(r, collapse = " | "), " |"))
  paste(c(header, sep, rows), collapse = "\n")
}

# ── Secciones del reporte ─────────────────────────────────────────────────────

## 1. Cobertura por módulo
cobertura_modulos <- function(df) {
  todos_modulos <- df$modulos_observados %>%
    str_split(",\\s*") %>%
    unlist() %>%
    trimws() %>%
    .[. != ""] %>%
    table() %>%
    as.data.frame(stringsAsFactors = FALSE)
  names(todos_modulos) <- c("Módulo", "N_personas_únicas")
  todos_modulos <- todos_modulos[order(-todos_modulos$N_personas_únicas), ]
  md_table(todos_modulos)
}

## 2. Distribución por número de módulos
dist_modulos <- function(df) {
  dist <- df %>%
    count(n_modulos_observados, name = "N_correos") %>%
    rename(`N módulos` = n_modulos_observados)
  md_table(as.data.frame(dist))
}

## 3. Inconsistencias tipo_documento
incons_tipo_doc <- function(df) {
  n_multi <- sum(df$n_valores_tipo_documento > 1, na.rm = TRUE)
  
  pares <- df %>%
    filter(n_valores_tipo_documento > 1,
           !is.na(tipo_documento_1), !is.na(tipo_documento_2)) %>%
    mutate(par = paste(tipo_documento_1, "→", tipo_documento_2)) %>%
    count(par, name = "Frecuencia") %>%
    arrange(desc(Frecuencia)) %>%
    head(10)
  
  list(n_multi = n_multi, tabla_pares = md_table(as.data.frame(pares)))
}

## 4. Inconsistencias numero_documento
incons_num_doc <- function(df) {
  sum(df$n_valores_numero_documento > 1, na.rm = TRUE)
}

## 5. Inconsistencias nombre_completo
incons_nombre <- function(df) {
  n_multi  <- sum(df$n_valores_nombre_completo > 1, na.rm = TRUE)
  max_vars <- max(df$n_valores_nombre_completo, na.rm = TRUE)
  list(n_multi = n_multi, max_vars = max_vars)
}

## 6. Inconsistencias fecha_nacimiento
incons_fecha <- function(df) {
  n_multi <- sum(df$n_valores_fecha_nacimiento > 1, na.rm = TRUE)
  
  fechas_validas <- df$fecha_nacimiento_1[
    !is.na(df$fecha_nacimiento_1) & df$fecha_nacimiento_1 != ""]
  
  rango <- if (length(fechas_validas) > 0) {
    fechas_parsed <- as.Date(fechas_validas, optional = TRUE)
    fechas_ok     <- fechas_parsed[!is.na(fechas_parsed)]
    if (length(fechas_ok) > 0)
      paste(min(fechas_ok), "a", max(fechas_ok))
    else
      "no parseable"
  } else {
    "sin datos"
  }
  
  list(n_multi = n_multi, rango = rango)
}

## 7. Inconsistencias sexo
incons_sexo <- function(df) {
  n_multi <- sum(df$n_valores_sexo > 1, na.rm = TRUE)
  
  dist_sexo <- df %>%
    filter(!is.na(sexo_1), sexo_1 != "") %>%
    count(sexo_1, name = "N") %>%
    arrange(desc(N)) %>%
    rename(`Valor canónico (sexo_1)` = sexo_1)
  
  list(n_multi = n_multi, tabla = md_table(as.data.frame(dist_sexo)))
}

## 8. Inconsistencias apertura
incons_apertura <- function(df) {
  n_multi  <- sum(df$n_valores_apertura > 1, na.rm = TRUE)
  max_aper <- max(df$n_valores_apertura, na.rm = TRUE)
  list(n_multi = n_multi, max_aper = max_aper)
}

## 9. Personas sin correo
personas_sin_correo <- function(path) {
  if (!file.exists(path)) return("no disponible")
  sc <- read.csv(path, stringsAsFactors = FALSE)
  nrow(sc)
}

## 10. Correos NO presentes en módulo matriculados
incons_no_matriculados <- function(df) {
  no_mat <- df[!grepl("matriculados", df$modulos_observados, fixed = TRUE), ]
  n_total_no_mat <- nrow(no_mat)
  
  dist <- no_mat %>%
    count(modulos_observados, name = "N_correos") %>%
    arrange(desc(N_correos)) %>%
    rename(`Módulos observados` = modulos_observados)
  
  list(n = n_total_no_mat, tabla = md_table(as.data.frame(dist)))
}

# ── Cálculo de todos los indicadores ─────────────────────────────────────────
n_total        <- nrow(master)
cob_tab        <- cobertura_modulos(master)
dist_mod_tab   <- dist_modulos(master)
tipo_doc       <- incons_tipo_doc(master)
n_num_doc      <- incons_num_doc(master)
nombre_res     <- incons_nombre(master)
fecha_res      <- incons_fecha(master)
sexo_res       <- incons_sexo(master)
apertura_res   <- incons_apertura(master)
n_sin_correo   <- personas_sin_correo(sin_correo_path)
no_mat_res     <- incons_no_matriculados(master)

# ── Construcción del reporte ──────────────────────────────────────────────────
lineas <- c(
  paste0("# Reporte de Inconsistencias — Master Personas"),
  paste0("**Generado:** ", fecha_hoy, "  "),
  paste0("**Total correos únicos en master:** ", format(n_total, big.mark = ",")),
  "",
  "---",
  "",
  
  # 1
  "## 1. Cobertura por módulo",
  "",
  cob_tab,
  "",
  
  # 2
  "## 2. Distribución de personas por número de módulos",
  "",
  dist_mod_tab,
  "",
  
  # 3
  "## 3. Inconsistencias de `tipo_documento`",
  "",
  paste0("- **Correos con más de un tipo de documento:** ",
         format(tipo_doc$n_multi, big.mark = ",")),
  "",
  "### Pares más frecuentes (`tipo_documento_1` → `tipo_documento_2`)",
  "",
  tipo_doc$tabla_pares,
  "",
  
  # 4
  "## 4. Inconsistencias de `numero_documento`",
  "",
  paste0("- **Correos con más de un número de documento:** ",
         format(n_num_doc, big.mark = ",")),
  "",
  
  # 5
  "## 5. Inconsistencias de `nombre_completo`",
  "",
  paste0("- **Correos con más de un nombre:** ",
         format(nombre_res$n_multi, big.mark = ",")),
  paste0("- **Máximo de variantes observado:** ", nombre_res$max_vars),
  "",
  
  # 6
  "## 6. Inconsistencias de `fecha_nacimiento`",
  "",
  paste0("- **Correos con más de una fecha de nacimiento:** ",
         format(fecha_res$n_multi, big.mark = ",")),
  paste0("- **Rango de `fecha_nacimiento_1`:** ", fecha_res$rango),
  "",
  
  # 7
  "## 7. Inconsistencias de `sexo`",
  "",
  paste0("- **Correos con más de un valor de sexo:** ",
         format(sexo_res$n_multi, big.mark = ",")),
  "",
  "### Distribución de valores canónicos (`sexo_1`)",
  "",
  sexo_res$tabla,
  "",
  
  # 8
  "## 8. Inconsistencias de `apertura`",
  "",
  paste0("- **Correos con más de una apertura:** ",
         format(apertura_res$n_multi, big.mark = ",")),
  paste0("- **Máximo de aperturas distintas observado:** ", apertura_res$max_aper),
  "",
  
  # 10
  "## 10. Correos NO presentes en módulo `matriculados`",
  "",
  paste0("> Se esperaría que toda persona del master aparezca en `matriculados`. ",
         "Los siguientes correos no cumplen esa condición."),
  "",
  paste0("- **Total correos sin `matriculados`:** ",
         format(no_mat_res$n, big.mark = ","),
         " de ", format(n_total, big.mark = ","),
         " (", round(no_mat_res$n / n_total * 100, 1), "%)"),
  "",
  "### Distribución por combinación de módulos",
  "",
  no_mat_res$tabla,
  "",
  "## 9. Personas sin correo",
  "",
  if (is.numeric(n_sin_correo)) {
    paste0("- **N registros sin correo (`REGISTROS_SIN_CORREO.csv`):** ",
           format(n_sin_correo, big.mark = ","))
  } else {
    paste0("- **N registros sin correo:** ", n_sin_correo,
           "  *(archivo `REGISTROS_SIN_CORREO.csv` no encontrado en el directorio de trabajo)*")
  },
  "",
  "---",
  "*Reporte generado automáticamente. No contiene datos PII.*"
)

# ── Escritura ─────────────────────────────────────────────────────────────────
writeLines(lineas, con = output_path, useBytes = FALSE)
message("Reporte guardado en: ", output_path)

