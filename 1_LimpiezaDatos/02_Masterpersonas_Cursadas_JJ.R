# =========================================================
# Semana 2 - Master de personas desde Cursadas
# Script: 1_LimpiezaDatos/02_masterpersonas_Cursadas_JJ.R
#
# Nota importante:
# En Cursadas NO existen variables de tipo_documento ni sexo.
# Por tanto, en este módulo:
#   - tipo_documento = NA
#   - sexo = NA
# Estos campos podrán completarse luego al unir con otras fuentes.

library(readxl)
library(dplyr)
library(stringr)
library(purrr)
library(tidyr)
library(readr)


# 1. Rutas----------------------------------------------------------------------

ruta_cursadas <- "Cursadas-20260419T235746Z-3-001/Cursadas"
ruta_salida   <- "Semana a semana/Semana 2"

output_master <- file.path(ruta_salida, "MASTER_PERSONAS_CURSADAS_PII.csv")

# 2. Archivos a procesar--------------------------------------------------------

archivos_excel <- list.files(
  path = ruta_cursadas,
  pattern = "\\.xlsx$",
  full.names = TRUE
)

# En estos archivos usamos la fila 2 porque la fila 1
# no contiene los encabezados reales.
archivos_skip_1 <- c(
  "Cursadas_2021-2S.xlsx",
  "Cursadas_2023-1S.xlsx",
  "Cursadas_2025-1S.xlsx"
)

# 3. Funciones auxiliares de limpieza-------------------------------------------

limpiar_texto <- function(x) {
  x <- as.character(x)
  x <- str_trim(x)
  x <- str_squish(x)
  x[x %in% c("", "NA", "N/A", "NULL", "null", "na")] <- NA_character_
  x
}

extraer_periodo_desde_archivo <- function(nombre_archivo) {
  str_extract(nombre_archivo, "\\d{4}-\\dS")
}

colapsar_unicos <- function(x, sep = " | ") {
  x <- unique(na.omit(x))
  x <- x[x != ""]
  if (length(x) == 0) return(NA_character_)
  paste(x, collapse = sep)
}

moda_simple <- function(x) {
  x <- x[!is.na(x) & x != ""]
  if (length(x) == 0) return(NA_character_)
  tab <- sort(table(x), decreasing = TRUE)
  names(tab)[1]
}

# 4. Función para leer y armonizar un archivo de Cursadas-----------------------

leer_y_armonizar_cursadas <- function(ruta_archivo, sheet_datos = 2) {
  
  nombre_archivo  <- basename(ruta_archivo)
  periodo_archivo <- extraer_periodo_desde_archivo(nombre_archivo)
  
  # En estos archivos usamos la fila 2 porque la fila 1
  # no contiene los encabezados reales.
  skip_usar <- ifelse(nombre_archivo %in% archivos_skip_1, 1, 0)
  
  message("Leyendo: ", nombre_archivo, " | skip = ", skip_usar)
  
  df_raw <- read_excel(
    path = ruta_archivo,
    sheet = sheet_datos,
    skip = skip_usar,
    col_types = "text"
  )
  
  names(df_raw) <- names(df_raw) |>
    stringr::str_trim() |>
    stringr::str_squish()
  
  columnas_necesarias <- c("DOCUMENTO", "CORREO", "NOMBRES", "APELLIDOS")
  
  faltantes <- setdiff(columnas_necesarias, names(df_raw))
  
  if (length(faltantes) > 0) {
    stop(
      paste0(
        "En el archivo ", nombre_archivo,
        " faltan estas columnas requeridas: ",
        paste(faltantes, collapse = ", ")
      )
    )
  }
  
  df_canonica <- df_raw %>%
    transmute(
      archivo_origen   = nombre_archivo,
      periodo          = periodo_archivo,
      correo           = stringr::str_to_lower(limpiar_texto(CORREO)),
      tipo_documento   = NA_character_,
      numero_documento = limpiar_texto(DOCUMENTO),
      nombre_completo  = stringr::str_squish(
        paste(
          limpiar_texto(NOMBRES),
          limpiar_texto(APELLIDOS)
        )
      ),
      sexo             = NA_character_,
      fuente           = "Cursadas"
    ) %>%
    mutate(
      nombre_completo = dplyr::na_if(nombre_completo, "")
    )
  
  return(df_canonica)
}

# 5. Apilar todos los archivos de Cursadas--------------------------------------

cursadas_apilada <- purrr::map_dfr(
  .x = archivos_excel,
  .f = leer_y_armonizar_cursadas
)

# Quitar filas completamente vacías en los campos centrales
cursadas_apilada <- cursadas_apilada %>%
  dplyr::filter(
    !(
      is.na(periodo) &
        is.na(correo) &
        is.na(numero_documento) &
        is.na(nombre_completo)
    )
  )

# 6. Chequeos básicos de la base apilada----------------------------------------

# Estructura general
names(cursadas_apilada)
dim(cursadas_apilada)

# Cantidad de archivos y periodos observados
dplyr::n_distinct(cursadas_apilada$archivo_origen)
dplyr::n_distinct(cursadas_apilada$periodo)

# Completitud de variables centrales
cursadas_apilada %>%
  dplyr::summarise(
    filas_totales       = dplyr::n(),
    docs_no_missing     = sum(!is.na(numero_documento)),
    docs_missing        = sum(is.na(numero_documento)),
    correos_no_missing  = sum(!is.na(correo)),
    correos_missing     = sum(is.na(correo)),
    nombres_no_missing  = sum(!is.na(nombre_completo)),
    nombres_missing     = sum(is.na(nombre_completo))
  )

# Muestra rápida para inspección visual
cursadas_apilada %>%
  dplyr::select(
    archivo_origen,
    periodo,
    correo,
    numero_documento,
    nombre_completo
  ) %>%
  head(15)

# 7. Validaciones de consistencia por numero_documento--------------------------

# Base auxiliar: una fila por numero_documento
resumen_documento <- cursadas_apilada %>%
  dplyr::filter(!is.na(numero_documento), numero_documento != "") %>%
  dplyr::group_by(numero_documento) %>%
  dplyr::summarise(
    n_filas   = dplyr::n(),
    n_periodos = dplyr::n_distinct(periodo, na.rm = TRUE),
    n_correos = dplyr::n_distinct(correo, na.rm = TRUE),
    n_nombres = dplyr::n_distinct(nombre_completo, na.rm = TRUE),
    correos_observados = colapsar_unicos(correo),
    nombres_observados = colapsar_unicos(nombre_completo),
    periodos_observados = colapsar_unicos(periodo),
    .groups = "drop"
  )

# Resumen general
resumen_documento %>%
  dplyr::summarise(
    personas_con_documento = dplyr::n(),
    docs_con_mas_de_un_correo = sum(n_correos > 1),
    docs_con_mas_de_un_nombre = sum(n_nombres > 1),
    max_correos_por_doc = max(n_correos, na.rm = TRUE),
    max_nombres_por_doc = max(n_nombres, na.rm = TRUE)
  )

# Ver casos con más de un correo
resumen_documento %>%
  dplyr::filter(n_correos > 1) %>%
  dplyr::arrange(desc(n_correos), desc(n_filas)) %>%
  dplyr::select(
    numero_documento,
    n_filas,
    n_periodos,
    n_correos,
    correos_observados,
    nombres_observados
  ) %>%
  head(20)

# Ver casos con más de un nombre
resumen_documento %>%
  dplyr::filter(n_nombres > 1) %>%
  dplyr::arrange(desc(n_nombres), desc(n_filas)) %>%
  dplyr::select(
    numero_documento,
    n_filas,
    n_periodos,
    n_nombres,
    nombres_observados,
    correos_observados
  ) %>%
  head(20)

# Resultado esperado de esta validación:
# numero_documento funciona como identificador principal de persona.
# Solo se observa un caso con más de un nombre asociado al mismo documento,
# pero corresponde visualmente a la misma persona con una variación menor del nombre.
# Por tanto, se puede consolidar a nivel de numero_documento.

# 8. Construir master de personas-----------------------------------------------

master_personas <- cursadas_apilada %>%
  dplyr::filter(!is.na(numero_documento), numero_documento != "") %>%
  dplyr::group_by(numero_documento) %>%
  dplyr::summarise(
    tipo_documento = NA_character_,
    nombre_completo = moda_simple(nombre_completo),
    correo = moda_simple(correo),
    sexo = NA_character_,
    fuente = "Cursadas",
    periodos_observados = colapsar_unicos(periodo),
    archivos_observados = colapsar_unicos(archivo_origen),
    n_filas_cursadas = dplyr::n(),
    n_periodos = dplyr::n_distinct(periodo, na.rm = TRUE),
    n_correos_observados = dplyr::n_distinct(correo, na.rm = TRUE),
    n_nombres_observados = dplyr::n_distinct(nombre_completo, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  dplyr::select(
    fuente,
    tipo_documento,
    numero_documento,
    nombre_completo,
    correo,
    sexo,
    periodos_observados,
    archivos_observados,
    n_filas_cursadas,
    n_periodos,
    n_correos_observados,
    n_nombres_observados
  )

# Chequeos del master
dim(master_personas)

master_personas %>%
  dplyr::summarise(
    personas = dplyr::n(),
    docs_unicos = dplyr::n_distinct(numero_documento),
    nombres_missing = sum(is.na(nombre_completo)),
    correos_missing = sum(is.na(correo)),
    docs_con_mas_de_un_correo = sum(n_correos_observados > 1),
    docs_con_mas_de_un_nombre = sum(n_nombres_observados > 1)
  )

head(master_personas, 20)

# 9. Exportar master de personas------------------------------------------------

# Verificar que hay una sola fila por numero_documento
master_personas %>%
  dplyr::count(numero_documento) %>%
  dplyr::filter(n > 1)

# Exportar archivo final
readr::write_csv(
  master_personas,
  output_master,
  na = ""
)

# 10. Mini reporte de validación

# Resumen general del proceso:
# - Se procesaron 4,665,718 registros de cursadas.
# - Se construyó un master final con 142,636 personas únicas (una fila por numero_documento).

# Calidad de la llave:
# - numero_documento identifica de forma única a cada persona (sin duplicados en el master).
# - No se detectaron documentos con múltiples correos ni múltiples nombres en el 
#master (Solo un documento que aparece con dos nombres, aparentemente la misma 
#persona; un registro con el primer apellido, y otro registro con los dos apellidos.

# Completitud de variables:
# - nombre_completo: 0 valores faltantes.
# - correo: 114 valores faltantes (~0.08% del total).
# - numero_documento: completo en el master.

# Conclusión:
# - El master de personas es consistente, sin duplicados y con muy bajo nivel de faltantes.
# - numero_documento funciona adecuadamente como identificador principal.
# - El dataset está listo para ser utilizado en etapas posteriores de integración con otras fuentes.

# Output generado:
# - DatosArmonizados/keys/MASTER_PERSONAS_CURSADAS_PII.csv


