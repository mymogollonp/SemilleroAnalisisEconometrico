# CONSOLIDACIÓN MASTER PERSONAS PII

library(progressr)
library(readr)
library(dplyr)
library(stringr)
library(stringi)
library(purrr)
library(tidyr)
library(rlang)

# 1. ARCHIVOS DE ENTRADA--------------------------------------------------------

archivos <- tibble::tribble(
  ~modulo_origen,   ~archivo,
  "matriculados",  "MASTER_PERSONAS_MATRICULADOS_PII.csv",
  "cursadas",      "MASTER_PERSONAS_CURSADAS_PII.csv",
  "cancelaciones", "MASTER_PERSONAS_CANCELACIONES_PII.csv",
  "egresados",     "MASTER_PERSONAS_EGRESADOS_PII.csv",
  "retirados",     "MASTER_PERSONAS_RETIRADOS_PII.csv"
)

# 2. FUNCIONES AUXILIARES-------------------------------------------------------

normalizar_nombre_columna <- function(x) {
  x %>%
    stringi::stri_trans_general("Latin-ASCII") %>%
    str_to_lower() %>%
    str_trim() %>%
    str_replace_all("\\s+", "_") %>%
    str_replace_all("[^a-z0-9_]", "_") %>%
    str_replace_all("_+", "_") %>%
    str_replace_all("^_|_$", "")
}

limpiar_texto <- function(x) {
  x %>%
    as.character() %>%
    str_trim() %>%
    na_if("")
}

limpiar_correo <- function(x) {
  x %>%
    as.character() %>%
    str_to_lower() %>%
    str_trim() %>%
    na_if("")
}

# Esta función toma el nombre de una columna y dice cuál debería ser
# su nombre canónico.
#
# Ejemplos:
# nombre_completo   -> nombre_completo_1
# nombre_completo1  -> nombre_completo_1
# nombre_completo_1 -> nombre_completo_1
# nombre_completo2  -> nombre_completo_2
# sexo              -> sexo_1
# numero_documento2 -> numero_documento_2

mapear_columna_canonica <- function(nombre_columna) {
  
  col <- normalizar_nombre_columna(nombre_columna)
  
  
  # correo
  
  if (col %in% c("correo", "email", "e_mail", "mail")) {
    return("correo")
  }
  
  
  # nombre_completo
  
  m_nombre <- str_match(col, "^nombre_completo_?([0-9]*)$")
  
  if (!is.na(m_nombre[1, 1])) {
    variante <- m_nombre[1, 2]
    
    if (variante == "") {
      variante <- "1"
    }
    
    return(paste0("nombre_completo_", variante))
  }
  
  
  # numero_documento
  
  m_numdoc <- str_match(col, "^numero_documento_?([0-9]*)$")
  
  if (!is.na(m_numdoc[1, 1])) {
    variante <- m_numdoc[1, 2]
    
    if (variante == "") {
      variante <- "1"
    }
    
    return(paste0("numero_documento_", variante))
  }
  
  
  # tipo_documento
  
  m_tipodoc <- str_match(col, "^tipo_documento_?([0-9]*)$")
  
  if (!is.na(m_tipodoc[1, 1])) {
    variante <- m_tipodoc[1, 2]
    
    if (variante == "") {
      variante <- "1"
    }
    
    return(paste0("tipo_documento_", variante))
  }
  
  
  # sexo
  
  m_sexo <- str_match(col, "^sexo_?([0-9]*)$")
  
  if (!is.na(m_sexo[1, 1])) {
    variante <- m_sexo[1, 2]
    
    if (variante == "") {
      variante <- "1"
    }
    
    return(paste0("sexo_", variante))
  }
  
  # apertura
  m_apertura <- str_match(col, "^apertura_?([0-9]*)$")
  if (!is.na(m_apertura[1, 1])) {
    variante <- m_apertura[1, 2]
    if (variante == "") variante <- "1"
    return(paste0("apertura_", variante))
  }
  
  # fecha_nacimiento
  m_fecha <- str_match(col, "^fecha_nacimiento_?([0-9]*)$")
  if (!is.na(m_fecha[1, 1])) {
    variante <- m_fecha[1, 2]
    if (variante == "") variante <- "1"
    return(paste0("fecha_nacimiento_", variante))
  }
  
  # Si no es una columna que nos interesa para el master final,
  # la dejamos sin mapear.
  return(NA_character_)
}

# Esta función combina columnas que terminaron mapeadas al mismo nombre canónico.
# Por ejemplo, si en una base existen al mismo tiempo:
# nombre_completo y nombre_completo_1,
# las combina en una sola columna nombre_completo_1.

coalesce_columnas <- function(df, columnas) {
  
  columnas_existentes <- columnas[columnas %in% names(df)]
  
  if (length(columnas_existentes) == 0) {
    return(rep(NA_character_, nrow(df)))
  }
  
  temp <- df %>%
    select(all_of(columnas_existentes)) %>%
    mutate(across(everything(), limpiar_texto))
  
  rlang::exec(dplyr::coalesce, !!!temp)
}

# 3. PASO B — ARMONIZAR CADA MÓDULO Y APILAR MÓDULOS----------------------------

armonizar_modulo <- function(modulo_actual, archivo_actual) {
  
  cat("\nProcesando módulo:", modulo_actual, "\n")
  
  df <- read_csv(
    archivo_actual,
    col_types = cols(.default = col_character()),
    show_col_types = FALSE
  )
  
  columnas_originales <- names(df)
  
  mapa <- tibble(
    columna_original = columnas_originales,
    columna_canonica = map_chr(columnas_originales, mapear_columna_canonica)
  ) %>%
    filter(!is.na(columna_canonica))
  
  
  salida <- tibble(
    modulo_origen = rep(modulo_actual, nrow(df))
  )
  
  columnas_canonicas <- sort(unique(mapa$columna_canonica))
  
  for (col_can in columnas_canonicas) {
    
    columnas_a_combinar <- mapa %>%
      filter(columna_canonica == col_can) %>%
      pull(columna_original)
    
    salida[[col_can]] <- coalesce_columnas(df, columnas_a_combinar)
  }
  
  if (!"correo" %in% names(salida)) {
    salida$correo <- NA_character_
  }
  
  salida <- salida %>%
    mutate(
      correo = limpiar_correo(correo)
    )
  
  return(salida)
}

base_larga_armonizada <- pmap_dfr(
  list(
    modulo_actual = archivos$modulo_origen,
    archivo_actual = archivos$archivo
  ),
  armonizar_modulo
)

# Reordenar columnas principales

columnas_principales <- c(
  "modulo_origen",
  "correo",
  "tipo_documento_1",
  "tipo_documento_2",
  "tipo_documento_3",
  "numero_documento_1",
  "numero_documento_2",
  "numero_documento_3",
  "nombre_completo_1",
  "nombre_completo_2",
  "nombre_completo_3",
  "sexo_1",
  "sexo_2",
  "sexo_3",
  "apertura_1",
  "apertura_2",
  "apertura_3",
  "apertura_4",
  "apertura_5",
  "apertura_6",
  "apertura_7",
  "fecha_nacimiento_1",
  "fecha_nacimiento_2"
)

base_larga_armonizada <- base_larga_armonizada %>%
  select(any_of(columnas_principales), everything())

write_csv(
  base_larga_armonizada,
  "MASTER_PERSONAS_PII_LARGO_ARMONIZADO.csv"
)


print(
  base_larga_armonizada %>%
    count(modulo_origen, name = "n_filas")
)

# 4. PASO C — CONSOLIDAR POR CORREO---------------------------------------------

familias <- c(
  "tipo_documento",
  "numero_documento",
  "nombre_completo",
  "sexo",
  "apertura",
  "fecha_nacimiento"
)

extraer_valores_familia <- function(df_grupo, familia) {
  
  columnas_familia <- names(df_grupo) %>%
    keep(~ str_detect(.x, paste0("^", familia, "_[0-9]+$")))
  
  if (length(columnas_familia) == 0) {
    return(character(0))
  }
  
  valores <- df_grupo %>%
    select(all_of(columnas_familia)) %>%
    unlist(use.names = FALSE) %>%
    limpiar_texto()
  
  valores <- valores[!is.na(valores)]
  
  # Esto preserva el orden en el que aparecen los valores,
  # pero elimina repetidos.
  valores <- unique(valores)
  
  return(valores)
}

consolidar_correo <- function(df_grupo) {
  
  salida <- tibble(
    correo = unique(df_grupo$correo)[1],
    modulos_observados = paste(sort(unique(df_grupo$modulo_origen)), collapse = ", "),
    n_modulos_observados = n_distinct(df_grupo$modulo_origen),
    n_registros_origen = nrow(df_grupo)
  )
  
  for (fam in familias) {
    
    valores <- extraer_valores_familia(df_grupo, fam)
    
    salida[[paste0("n_valores_", fam)]] <- length(valores)
    
    if (length(valores) == 0) {
      salida[[paste0(fam, "_1")]] <- NA_character_
    } else {
      for (i in seq_along(valores)) {
        salida[[paste0(fam, "_", i)]] <- valores[i]
      }
    }
  }
  
  return(salida)
}

# Separar registros sin correo.
# Como la deduplicación principal es por correo, estos no se pueden consolidar bien.

registros_sin_correo <- base_larga_armonizada %>%
  filter(is.na(correo) | correo == "")

base_con_correo <- base_larga_armonizada %>%
  filter(!is.na(correo), correo != "")

write_csv(
  registros_sin_correo,
  "REGISTROS_SIN_CORREO.csv"
)

base_por_correo <- base_con_correo %>%
  group_by(correo) %>%
  group_split()

correos_unicos <- base_con_correo %>%
  group_by(correo) %>%
  group_keys() %>%
  pull(correo)

handlers("txtprogressbar")


with_progress({
  
  p <- progressor(along = base_por_correo)
  
  master_personas_final <- map_dfr(seq_along(base_por_correo), function(i) {
    
    p(message = paste("Procesando correo", i, "de", length(base_por_correo)))
    
    consolidar_correo(base_por_correo[[i]])
  })
  
})


master_personas_final <- master_personas_final %>%
  arrange(correo)


write_csv(
  master_personas_final,
  "MASTER_PERSONAS_PII.csv"
)

# Diagnóstico de conflictos

correos_con_conflictos <- master_personas_final %>%
  filter(
    if_any(
      starts_with("n_valores_"),
      ~ as.numeric(.x) > 1
    )
  )

write_csv(
  correos_con_conflictos,
  "CORREOS_CON_CONFLICTOS.csv"
)


#4. Resumen del resultados------------------------------------------------------

#La consolidación del master de personas integró 474.867 registros provenientes 
#de los cinco módulos — matriculados (139.590), cursadas (142.519), cancelaciones 
#(76.415), egresados (74.949) y retirados (41.394) — y los deduplicó a 148.565 
#correos únicos. Solo 6 registros quedaron fuera del master por no tener correo 
#institucional (1 de egresados y 5 de retirados), lo que representa una cobertura 
#prácticamente total. En cuanto a la presencia por módulos, la mayoría de los 
#correos aparece en 3 o 4 módulos (60.810 y 53.305 respectivamente), 17.849 en 
#2, 9.873 en solo 1, y 6.728 en los 5 módulos simultáneamente.
#Se identificaron 78.840 correos con al menos un conflicto entre módulos. Las 
#variables con mayor disonencia son nombre completo (51.122 correos con más de 
#un valor) y apertura (34.529), seguidas por tipo de documento (11.916) y sexo 
#(2.698); número de documento y fecha de nacimiento presentan los menores niveles 
#de conflicto con 116 y 16 casos respectivamente. En cuanto al máximo de variantes 
#observado por persona, apertura es la variable más volátil con hasta 7 valores 
#distintos para un mismo correo, seguida por nombre completo con 5, sexo y número 
#de documento con 3, mientras que tipo de documento y fecha de nacimiento llegan 
#a un máximo de 2 variantes.
