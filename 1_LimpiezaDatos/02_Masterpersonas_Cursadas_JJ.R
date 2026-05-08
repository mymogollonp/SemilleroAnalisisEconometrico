# =========================================================
# Semana 2 - Master de personas desde Cursadas
# Script: 1_LimpiezaDatos/02_masterpersonas_Cursadas_JJ.R
#
# Nota importante:
# En Cursadas NO existen variables de tipo_documento ni sexo.
# Por tanto, en este módulo:
#   - tipo_documento = NA
#   - sexo = NA
#   - genero = NA
#   - fecha_nacimiento = NA
# Estos campos podrán completarse luego al unir con otras fuentes.

library(readxl)
library(dplyr)
library(stringr)
library(stringi)
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

limpiar_nombre_completo <- function(x) {
  x <- limpiar_texto(x)
  x <- stringi::stri_trans_general(x, "Latin-ASCII")
  x <- stringr::str_to_upper(x)
  x <- stringr::str_replace_all(x, "[^A-Z0-9 ]", " ")
  x <- stringr::str_squish(x)
  x <- dplyr::na_if(x, "")
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
  
  # APERTURA se conserva cuando existe en el archivo.
  # Si algún archivo no la trae, se crea vacía para que el script no se rompa.
  if (!"APERTURA" %in% names(df_raw)) {
    df_raw$APERTURA <- NA_character_
  }
  
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
      apertura         = limpiar_texto(APERTURA),
      correo           = stringr::str_to_lower(limpiar_texto(CORREO)),
      tipo_documento   = NA_character_,
      numero_documento = limpiar_texto(DOCUMENTO),
      nombre_completo  = limpiar_nombre_completo(
        paste(
          limpiar_texto(NOMBRES),
          limpiar_texto(APELLIDOS)
        )
      ),
      sexo             = NA_character_,
      fuente           = "Cursadas"
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
        is.na(apertura) &
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
    apertura_no_missing = sum(!is.na(apertura)),
    apertura_missing    = sum(is.na(apertura)),
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
    apertura,
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
    n_aperturas = dplyr::n_distinct(apertura, na.rm = TRUE),
    correos_observados = colapsar_unicos(correo),
    nombres_observados = colapsar_unicos(nombre_completo),
    aperturas_observadas = colapsar_unicos(apertura),
    periodos_observados = colapsar_unicos(periodo),
    .groups = "drop"
  )

# Resumen general
resumen_documento %>%
  dplyr::summarise(
    personas_con_documento = dplyr::n(),
    docs_con_mas_de_un_correo = sum(n_correos > 1),
    docs_con_mas_de_un_nombre = sum(n_nombres > 1),
    docs_con_mas_de_una_apertura = sum(n_aperturas >1),
    max_correos_por_doc = max(n_correos, na.rm = TRUE),
    max_nombres_por_doc = max(n_nombres, na.rm = TRUE),
    max_aperturas_por_doc = max(n_aperturas, na.rm = TRUE)
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
    n_aperturas,
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
    n_aperturas,
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
# Llave: correo (no numero_documento)
# Variables con columnas dinámicas: numero_documento, nombre_completo, apertura
# Variables fijas como NA: tipo_documento, sexo, genero, fecha_nacimiento
# Solo entran registros con correo no vacío

# Función auxiliar: pivotea los valores únicos de una variable en columnas numeradas
pivotar_valores_unicos <- function(df, variable, prefijo) {
  df %>%
    dplyr::group_by(correo) %>%
    dplyr::summarise(
      valores = list(unique(na.omit(.data[[variable]][.data[[variable]] != ""]))),
      .groups = "drop"
    ) %>%
    dplyr::mutate(
      n_vals = purrr::map_int(valores, length)
    ) %>%
    {
      max_n <- max(.$n_vals, na.rm = TRUE)
      if (max_n == 0) {
        dplyr::select(., correo) %>%
          dplyr::mutate(!!paste0(prefijo, "1") := NA_character_)
      } else {
        purrr::reduce(
          seq_len(max_n),
          function(acc, i) {
            col_name <- paste0(prefijo, i)
            acc %>%
              dplyr::mutate(
                !!col_name := purrr::map_chr(valores, ~ if (length(.x) >= i) .x[[i]] else NA_character_)
              )
          },
          .init = .
        ) %>%
          dplyr::select(-valores, -n_vals)
      }
    }
}

# Base de entrada: solo registros con correo válido
base_con_correo <- cursadas_apilada %>%
  dplyr::filter(!is.na(correo), correo != "")

# Registros sin correo (para reporte)
base_sin_correo <- cursadas_apilada %>%
  dplyr::filter(is.na(correo) | correo == "")

message("Registros con correo: ", nrow(base_con_correo))
message("Registros sin correo (excluidos del master): ", nrow(base_sin_correo))

# Columnas dinámicas por variable
cols_numero_documento <- pivotar_valores_unicos(base_con_correo, "numero_documento", "numero_documento")
cols_nombre_completo  <- pivotar_valores_unicos(base_con_correo, "nombre_completo",  "nombre_completo")
cols_apertura         <- pivotar_valores_unicos(base_con_correo, "apertura",         "apertura")

# Columna archivo_origen colapsada
col_archivo_origen <- base_con_correo %>%
  dplyr::group_by(correo) %>%
  dplyr::summarise(
    archivo_origen = colapsar_unicos(archivo_origen),
    .groups = "drop"
  )

# Unir todo por correo
master_personas <- col_archivo_origen %>%
  dplyr::left_join(cols_numero_documento, by = "correo") %>%
  dplyr::left_join(cols_nombre_completo,  by = "correo") %>%
  dplyr::left_join(cols_apertura,         by = "correo") %>%
  dplyr::mutate(
    tipo_documento   = NA_character_,
    sexo             = NA_character_,
    genero           = NA_character_,
    fecha_nacimiento = NA_character_
  )

# Ordenar columnas: fijas primero, luego dinámicas
cols_fijas    <- c("correo", "tipo_documento", "sexo", "genero", "fecha_nacimiento")
cols_nombre   <- sort(grep("^nombre_completo", names(master_personas), value = TRUE))
cols_doc      <- sort(grep("^numero_documento", names(master_personas), value = TRUE))
cols_apertura_final <- sort(grep("^apertura", names(master_personas), value = TRUE))

master_personas <- master_personas %>%
  dplyr::select(
    dplyr::all_of(cols_fijas),
    dplyr::all_of(cols_nombre),
    dplyr::all_of(cols_doc),
    dplyr::all_of(cols_apertura_final),
    archivo_origen
  )

# Chequeos del master
dim(master_personas)
names(master_personas)

master_personas %>%
  dplyr::summarise(
    personas          = dplyr::n(),
    correos_unicos    = dplyr::n_distinct(correo),
    nombre1_missing   = sum(is.na(nombre_completo1)),
    doc1_missing      = sum(is.na(numero_documento1)),
    apertura1_missing = sum(is.na(apertura1))
  )

head(master_personas, 20)

# 9. Exportar master de personas------------------------------------------------

# Verificar unicidad por correo
master_personas %>%
  dplyr::count(correo) %>%
  dplyr::filter(n > 1)

# Exportar archivo final
readr::write_csv(
  master_personas,
  output_master,
  na = ""
)

# 10. Mini reporte de validación

## 10. Mini reporte de validación

# Resumen general del proceso:
# - Se procesaron 4,665,718 registros de cursadas.
# - 324 registros fueron excluidos del master por no tener correo.
# - El master final tiene 142,519 personas únicas (una fila por correo) y 17 columnas.

# Calidad de la llave:
# - correo identifica de forma única a cada persona (sin duplicados en el master).
# - El conteo de duplicados por correo devolvió 0 filas.

# Columnas dinámicas generadas:
# - nombre_completo1, nombre_completo2 (algunos correos tienen hasta 2 nombres distintos)
# - numero_documento1, numero_documento2 (algunos correos tienen hasta 2 documentos distintos)
# - apertura1 a apertura7 (algunos correos tienen hasta 7 aperturas distintas)

# Completitud de variables (sobre el master final):
# - nombre_completo1: 0 valores faltantes.
# - numero_documento1: 0 valores faltantes.
# - apertura1: 0 valores faltantes.

# Conclusión:
# - El master es consistente, sin duplicados y sin faltantes en las variables principales.
# - correo funciona adecuadamente como identificador principal.
# - El dataset está listo para integrarse con otras fuentes.