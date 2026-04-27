# =============================================================================
# 02_masterpersonas_Matriculados_NC.R
# Master Dataset de Personas — Módulo Matriculados (con PII)
# RA: Nicolas Camacho
# Proyecto: Semillero Análisis Econométrico — UNAL FCE
# Fecha: 2026-04-19
# =============================================================================
# PROPÓSITO: Iterar sobre los 34 archivos de Matriculados y construir un
#            dataset con la historia completa de identificadores por persona.
# OUTPUT: DatosArmonizados/keys/MASTER_PERSONAS_MATRICULADOS_PII.csv
# REGLA: Este archivo es CONFIDENCIAL — nunca subir a GitHub
# =============================================================================

# Por si es necesario limpiar el entorno
rm(list=ls())

library(readxl)
library(dplyr)
library(stringr)

# --- 1. Rutas -----------------------------------------------------------------
ruta_matriculados <- "C:/Users/nicom/OneDrive/Documentos/Semillero_Microeconometria/datos_originales/Matriculado"

ruta_output <- "C:/Users/nicom/OneDrive/Documentos/Semillero_Microeconometria/DatosArmonizados/keys"

if (!dir.exists(ruta_output)) {
  dir.create(ruta_output, recursive = TRUE)
  cat("Carpeta creada:", ruta_output, "\n")
}

archivos <- list.files(ruta_matriculados, pattern = "\\.xlsx$", full.names = TRUE)
cat("Archivos encontrados:", length(archivos), "\n\n")

# --- 2. Mapa de renombres de columnas inconsistentes -------------------------
renombres <- c(
  "NOMBRES"   = "NOMBRES_LEGAL",
  "APELLIDO1" = "APELLIDO1_LEGAL",
  "APELLIDO2" = "APELLIDO2_LEGAL",
  "SEXO"      = "SEXO_LEGAL"
)

# --- 3. Iterar sobre archivos y extraer variables de identificación ----------
lista <- list()

for (i in seq_along(archivos)) {
  
  archivo <- archivos[i]
  nombre  <- basename(archivo)
  cat("[", i, "/", length(archivos), "]", nombre, "\n")
  
  df <- tryCatch(
    read_excel(archivo, sheet = 1, col_types = "text"),
    error = function(e) { cat("  ERROR:", conditionMessage(e), "\n"); return(NULL) }
  )
  
  if (is.null(df)) next
  
  # Armonizar nombres de columnas inconsistentes entre años
  cols_a_renombrar <- intersect(names(df), names(renombres))
  if (length(cols_a_renombrar) > 0) {
    df <- rename(df, !!!setNames(cols_a_renombrar, renombres[cols_a_renombrar]))
  }
  
  # Avisar si falta alguna columna esperada
  cols_necesarias <- c("CORREO", "T_DOCUMENTO", "DOCUMENTO",
                       "NOMBRES_LEGAL", "APELLIDO1_LEGAL", "APELLIDO2_LEGAL",
                       "SEXO_LEGAL", "PERIODO")
  cols_faltantes <- cols_necesarias[!cols_necesarias %in% names(df)]
  if (length(cols_faltantes) > 0) {
    cat("  AVISO — columnas faltantes:", paste(cols_faltantes, collapse = ", "), "\n")
  }
  
  # Construir subconjunto con nombres canónicos del proyecto
  df_sub <- df %>%
    transmute(
      correo           = if ("CORREO"          %in% names(df)) CORREO          else NA_character_,
      tipo_documento   = if ("T_DOCUMENTO"     %in% names(df)) T_DOCUMENTO     else NA_character_,
      numero_documento = if ("DOCUMENTO"       %in% names(df)) DOCUMENTO       else NA_character_,
      nombre_completo  = if (all(c("NOMBRES_LEGAL","APELLIDO1_LEGAL","APELLIDO2_LEGAL") %in% names(df)))
        paste(NOMBRES_LEGAL, APELLIDO1_LEGAL, APELLIDO2_LEGAL)
      else NA_character_,
      sexo             = if ("SEXO_LEGAL" %in% names(df)) {
        # Estandarizar a F / M sin importar cómo venga escrito
        case_when(
          str_to_upper(SEXO_LEGAL) %in% c("FEMENINO", "FEMENINA") ~ "F",
          str_to_upper(SEXO_LEGAL) == "MASCULINO"                 ~ "M",
          SEXO_LEGAL %in% c("F", "M")                             ~ SEXO_LEGAL,
          is.na(SEXO_LEGAL)                                        ~ NA_character_,
          TRUE ~ SEXO_LEGAL  # conservar cualquier otro valor desconocido
        )
      } else NA_character_,
      PERIODO          = if ("PERIODO"         %in% names(df)) PERIODO         else NA_character_,
      ARCHIVO_FUENTE   = nombre
    )
  
  lista[[i]] <- df_sub
}

# --- 4. Apilar ----------------------------------------------------------------
master_raw <- bind_rows(lista)

cat("\n============================================================\n")
cat("FILAS TOTALES APILADAS:", nrow(master_raw), "\n")
cat("============================================================\n\n")

# --- 5. Deduplicar y ordenar --------------------------------------------------
# Conservar todas las combinaciones DISTINTAS por persona a lo largo del tiempo.
# arrange(correo, PERIODO) → todos los semestres de un estudiante juntos y en orden.

master <- master_raw %>%
  distinct(correo, tipo_documento, numero_documento,
           nombre_completo, sexo, PERIODO,
           .keep_all = TRUE) %>%
  arrange(correo, PERIODO)

cat("Filas tras deduplicación:", nrow(master), "\n")
cat("Personas únicas (por correo):", n_distinct(master$correo, na.rm = TRUE), "\n\n")

# --- 6. Validaciones ----------------------------------------------------------
cat("============================================================\n")
cat("VALIDACIONES\n")
cat("============================================================\n")

# 6a. Distribución de tipos de documento
tipos_reconocidos <- c("C", "E", "P", "T", "O")
tipos_observados  <- master %>% count(tipo_documento, sort = TRUE)

cat("\nDistribución de tipos de documento:\n")
print(tipos_observados)

tipos_desconocidos <- tipos_observados %>%
  filter(!tipo_documento %in% tipos_reconocidos, !is.na(tipo_documento))
if (nrow(tipos_desconocidos) > 0) {
  cat("\nAVISO — tipos NO reconocidos (revisar con PI):\n")
  print(tipos_desconocidos)
} else {
  cat("\nOK — todos los tipos de documento son reconocidos.\n")
}

# 6b. Formato del número de documento por tipo
cat("\n--- Verificación de formato de número de documento ---\n")

master <- master %>%
  mutate(
    FORMATO_DOC_VALIDO = case_when(
      tipo_documento == "C" ~ str_detect(numero_documento, "^[0-9]{6,10}$"),   # CC:  6-10 dígitos
      tipo_documento == "T" ~ str_detect(numero_documento, "^[0-9]{10,11}$"),  # TI: 10-11 dígitos
      tipo_documento == "E" ~ !is.na(numero_documento),                         # CE:  alfanumérico
      tipo_documento == "P" ~ !is.na(numero_documento),                         # PA:  alfanumérico
      tipo_documento == "O" ~ !is.na(numero_documento),                         # Otro
      TRUE ~ NA
    )
  )

n_invalidos <- sum(master$FORMATO_DOC_VALIDO == FALSE, na.rm = TRUE)
cat("Registros con formato de documento inválido:", n_invalidos, "\n")

if (n_invalidos > 0) {
  cat("\nEjemplos (primeros 20):\n")
  master %>%
    filter(FORMATO_DOC_VALIDO == FALSE) %>%
    select(correo, tipo_documento, numero_documento, PERIODO) %>%
    head(20) %>%
    print()
}

# 6c. Verificar que sexo solo tiene F, M o NA
cat("\n--- Distribución de sexo tras estandarización ---\n")
master %>% count(sexo, sort = TRUE) %>% print()

valores_sexo_raros <- master %>%
  filter(!is.na(sexo), !sexo %in% c("F", "M")) %>%
  count(sexo)
if (nrow(valores_sexo_raros) > 0) {
  cat("AVISO — valores de sexo fuera de F/M (revisar con PI):\n")
  print(valores_sexo_raros)
}

# 6d. Personas con más de un valor de sexo
cat("\n--- Personas con más de un valor de sexo ---\n")

sexo_multiple <- master %>%
  filter(!is.na(correo), !is.na(sexo)) %>%
  group_by(correo) %>%
  summarise(n_valores_sexo = n_distinct(sexo), .groups = "drop") %>%
  filter(n_valores_sexo > 1)

cat("Personas con más de un valor de sexo:", nrow(sexo_multiple), "\n")

# 6e. Missings en variables clave
cat("\n--- Missings en variables clave ---\n")
for (col in c("correo", "tipo_documento", "numero_documento",
              "nombre_completo", "sexo", "PERIODO")) {
  n   <- sum(is.na(master[[col]]))
  pct <- round(n / nrow(master) * 100, 1)
  cat(" ", col, ":", n, "missings (", pct, "%)\n")
}

# --- 7. Personas con cambios en variables de identidad -----------------------

# Función auxiliar: detecta en qué periodo OCURRIÓ el cambio
detectar_cambios <- function(datos, variable) {
  datos %>%
    filter(!is.na(correo), !is.na(.data[[variable]])) %>%
    arrange(correo, PERIODO) %>%
    group_by(correo) %>%
    mutate(
      valor_anterior = lag(.data[[variable]]),
      hubo_cambio    = !is.na(valor_anterior) & .data[[variable]] != valor_anterior
    ) %>%
    summarise(
      n_valores          = n_distinct(.data[[variable]]),
      valores            = paste(sort(unique(.data[[variable]])), collapse = " | "),
      periodos_de_cambio = {
        periodos_c <- PERIODO[hubo_cambio]
        valores_c  <- .data[[variable]][hubo_cambio]
        prev_c     <- valor_anterior[hubo_cambio]
        if (length(periodos_c) == 0) NA_character_
        else paste(paste0(periodos_c, " (", prev_c, " → ", valores_c, ")"), collapse = " | ")
      },
      .groups = "drop"
    ) %>%
    filter(n_valores > 1) %>%
    arrange(correo)
}

# 7a. Cambios de SEXO
cambios_sexo <- detectar_cambios(master, "sexo")
cat("\n--- Personas con más de un valor de SEXO:", nrow(cambios_sexo), "---\n")
if (nrow(cambios_sexo) > 0) print(cambios_sexo, n = 10)

# 7b. Cambios de NOMBRE_COMPLETO
cambios_nombre <- detectar_cambios(master, "nombre_completo")
cat("\n--- Personas con más de un NOMBRE_COMPLETO:", nrow(cambios_nombre), "---\n")
if (nrow(cambios_nombre) > 0) print(cambios_nombre, n = 10)

# 7c. Cambios de TIPO_DOCUMENTO
cambios_tipo_doc <- detectar_cambios(master, "tipo_documento")
cat("\n--- Personas con más de un TIPO_DOCUMENTO:", nrow(cambios_tipo_doc), "---\n")
if (nrow(cambios_tipo_doc) > 0) print(cambios_tipo_doc, n = 10)

# 7d. Cambios de NUMERO_DOCUMENTO (ahora incluye si también cambió tipo_documento)
cambios_num_doc <- master %>%
  filter(!is.na(correo), !is.na(numero_documento)) %>%
  arrange(correo, PERIODO) %>%
  group_by(correo) %>%
  mutate(
    num_anterior  = lag(numero_documento),
    tipo_anterior = lag(tipo_documento),
    hubo_cambio   = !is.na(num_anterior) & numero_documento != num_anterior
  ) %>%
  summarise(
    n_valores          = n_distinct(numero_documento),
    valores            = paste(sort(unique(numero_documento)), collapse = " | "),
    periodos_de_cambio = {
      periodos_c    <- PERIODO[hubo_cambio]
      num_prev      <- num_anterior[hubo_cambio]
      num_new       <- numero_documento[hubo_cambio]
      tipo_prev     <- tipo_anterior[hubo_cambio]
      tipo_new      <- tipo_documento[hubo_cambio]
      cambio_tipo   <- tipo_prev != tipo_new & !is.na(tipo_prev) & !is.na(tipo_new)
      if (length(periodos_c) == 0) NA_character_
      else paste(
        paste0(
          periodos_c,
          " (", num_prev, " → ", num_new, ")",
          ifelse(cambio_tipo,
                 paste0(" [tipo: ", tipo_prev, " → ", tipo_new, "]"),
                 "")
        ),
        collapse = " | "
      )
    },
    tambien_cambio_tipo = any(
      hubo_cambio & tipo_anterior != tipo_documento &
        !is.na(tipo_anterior) & !is.na(tipo_documento)
    ),
    .groups = "drop"
  ) %>%
  filter(n_valores > 1) %>%
  arrange(correo)

cat("\n--- Personas con más de un NUMERO_DOCUMENTO:", nrow(cambios_num_doc), "---\n")
if (nrow(cambios_num_doc) > 0) print(cambios_num_doc, n = Inf)


# 7e. Resumen de cambios
cat("\n--- Resumen de cambios ---\n")
cat("Personas con cambio de sexo:             ", nrow(cambios_sexo),     "\n")
cat("Personas con cambio de nombre:           ", nrow(cambios_nombre),   "\n")
cat("Personas con cambio de tipo documento:   ", nrow(cambios_tipo_doc), "\n")
cat("Personas con cambio de número documento: ", nrow(cambios_num_doc),  "\n")

# 7f. Guardar reporte de cambios en CSV (sin PII fuera de keys/)
ruta_cambios <- file.path(ruta_output, "CAMBIOS_IDENTIDAD_MATRICULADOS.csv")

cambios_todos <- bind_rows(
  cambios_sexo     %>% mutate(variable = "sexo",             tambien_cambio_tipo = NA),
  cambios_nombre   %>% mutate(variable = "nombre_completo",  tambien_cambio_tipo = NA),
  cambios_tipo_doc %>% mutate(variable = "tipo_documento",   tambien_cambio_tipo = NA),
  cambios_num_doc  %>% mutate(variable = "numero_documento")
) %>%
  select(variable, correo, n_valores, valores, periodos_de_cambio, tambien_cambio_tipo) %>%
  arrange(variable, correo)

write.csv(cambios_todos, file = ruta_cambios, row.names = FALSE)
cat("\nReporte de cambios guardado en:\n", ruta_cambios, "\n")

# --- 8. Guardar output --------------------------------------------------------

ruta_csv <- file.path(ruta_output, "MASTER_PERSONAS_MATRICULADOS_PII.csv")
write.csv(master, file = ruta_csv, row.names = FALSE)

cat("\n============================================================\n")
cat("ARCHIVO GUARDADO EN:\n", ruta_csv, "\n")
cat("============================================================\n")

# --- 8. Resumen para el reporte semanal ---------------------------------------
cat("\n============================================================\n")
cat("RESUMEN PARA EL REPORTE SEMANAL\n")
cat("============================================================\n")
cat("N personas únicas (por correo):          ", n_distinct(master$correo, na.rm = TRUE), "\n")
cat("N registros totales en el master:        ", nrow(master), "\n")
cat("N personas con >1 valor de sexo:         ", nrow(sexo_multiple), "\n")
cat("N documentos con formato inválido:       ", n_invalidos, "\n")
cat("Tipos de documento observados:           ", paste(sort(unique(master$tipo_documento)), collapse = ", "), "\n")



