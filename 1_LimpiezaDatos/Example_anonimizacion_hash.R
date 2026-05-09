# =========================================================
# Ejemplo: Crear llave de anonimización basada en hash
# Script: 1_LimpiezaDatos/Example_anonimizacion_hash.R
#
# Propósito:
#   Muestra cómo generar id_unal a partir del archivo
#   MASTER_PERSONAS_PII consolidado, usando SHA-256 con sal.
#
# Prerequisito:
#   El MASTER_PERSONAS_PII.csv ya debe existir en keys/.
#   Ejecutar primero 02_Masterpersonas_Cursadas_JJ.R y los
#   demás scripts de master de personas de cada módulo,
#   y consolidarlos en un único archivo antes de correr esto.
#
# Salida:
#   DatosArmonizados/keys/LLAVE_ID_UNAL_FCE.csv
#   Columnas: correo | id_unal
#   Una fila por persona única. Confidencial — nunca a GitHub.
#
# Semilla documentada: 20260223
# Sal documentada:     "semillero_unal_fce_20260223"
#
# Reproducibilidad:
#   SHA-256 es determinista — misma sal + mismo correo = mismo hash siempre.
#   set.seed() cubre cualquier operación aleatoria futura en este script.
#   Nunca cambiar SEMILLA ni SAL una vez generada la llave: hacerlo produce
#   IDs distintos y rompe el cruce con datos ya anonimizados.
# =========================================================

library(dplyr)
library(readr)
library(stringr)
library(purrr)
library(digest)   # install.packages("digest") si no está instalado


# Semilla global ----------------------------------------------------------------
# Debe coincidir con la semilla del proyecto definida en el WORKPLAN.
SEMILLA <- 20260223
set.seed(SEMILLA)


# 1. Rutas ----------------------------------------------------------------------
# Ajustar según tu bloque en 00_configuracion.R

usuario <- Sys.info()[["user"]]

if (usuario == "JeronimoJ") {
  dir_datos <- "C:/TuRuta/SemilleroAnalisisEconometrico"
  dir_code  <- "C:/TuRuta/code/SemilleroAnalisisEconometrico"
} else {
  stop("Usuario no configurado. Agrega tu bloque de rutas.")
}

ruta_master_pii <- file.path(dir_datos, "DatosArmonizados/keys/MASTER_PERSONAS_PII.csv")
ruta_llave      <- file.path(dir_datos, "DatosArmonizados/keys/LLAVE_ID_UNAL_FCE.csv")


# 2. Parámetros de anonimización ------------------------------------------------

# La sal se combina con el identificador antes de hashear.
# Incorpora la semilla numérica del proyecto para que quede
# vinculada al mismo número documentado en el WORKPLAN.
SAL <- paste0("semillero_unal_fce_", SEMILLA)


# 3. Leer master PII ------------------------------------------------------------

master_pii <- readr::read_csv(
  ruta_master_pii,
  col_types = readr::cols(.default = "c"),
  na = c("", "NA")
)

message("Personas en master PII: ", nrow(master_pii))

# Verificar que el campo clave existe
stopifnot(
  "La columna 'correo' no existe en MASTER_PERSONAS_PII.csv" =
    "correo" %in% names(master_pii)
)


# 4. Normalizar el identificador ------------------------------------------------
# Siempre normalizar antes de hashear para que variaciones de
# mayúsculas/espacios no generen IDs distintos para la misma persona.

master_pii <- master_pii %>%
  dplyr::mutate(
    correo_norm = stringr::str_to_lower(stringr::str_trim(correo))
  )

# Verificar que no haya correos vacíos tras normalización
n_vacios <- sum(is.na(master_pii$correo_norm) | master_pii$correo_norm == "")
if (n_vacios > 0) {
  warning(n_vacios, " personas sin correo válido — quedarán sin id_unal.")
}


# 5. Generar hash SHA-256 -------------------------------------------------------
# digest() con algo = "sha256" y serialize = FALSE aplica SHA-256 directamente
# al string. Al combinar SAL + correo el hash es único para este proyecto
# aunque el mismo correo aparezca en otros datasets.

master_pii <- master_pii %>%
  dplyr::mutate(
    hash_raw = dplyr::if_else(
      is.na(correo_norm) | correo_norm == "",
      NA_character_,
      purrr::map_chr(
        correo_norm,
        ~ digest::digest(paste0(SAL, .x), algo = "sha256", serialize = FALSE)
      )
    )
  )


# 6. Verificar colisiones de hash -----------------------------------------------
# Con SHA-256 las colisiones son astronómicamente improbables, pero verificar
# siempre para garantizar que la llave es 1 a 1.

n_hashes_unicos  <- dplyr::n_distinct(master_pii$hash_raw, na.rm = TRUE)
n_correos_unicos <- dplyr::n_distinct(master_pii$correo_norm, na.rm = TRUE)

if (n_hashes_unicos != n_correos_unicos) {
  stop(
    "Colisión detectada: ", n_correos_unicos, " correos únicos pero ",
    n_hashes_unicos, " hashes únicos. Revisar los datos."
  )
}

message("Sin colisiones: ", n_hashes_unicos, " hashes únicos para ",
        n_correos_unicos, " correos únicos.")


# 7. Asignar id_unal en formato UNAL000001 --------------------------------------
# Ordenar por hash_raw garantiza que el mapeo correo → id_unal es
# determinista y reproducible con la misma sal, sin importar el orden
# de los datos de entrada.

llave <- master_pii %>%
  dplyr::filter(!is.na(hash_raw)) %>%
  dplyr::arrange(hash_raw) %>%
  dplyr::mutate(
    id_unal = paste0("UNAL", stringr::str_pad(dplyr::row_number(), width = 6, pad = "0"))
  ) %>%
  dplyr::select(correo = correo_norm, id_unal)


# 8. Validaciones finales -------------------------------------------------------

stopifnot(
  "id_unal no es único en la llave" =
    dplyr::n_distinct(llave$id_unal) == nrow(llave),
  "correo no es único en la llave" =
    dplyr::n_distinct(llave$correo) == nrow(llave)
)

message("Llave generada: ", nrow(llave), " personas.")
message("Rango de IDs: ", llave$id_unal[1], " — ", llave$id_unal[nrow(llave)])


# 9. Exportar llave -------------------------------------------------------------

readr::write_csv(llave, ruta_llave, na = "")

message("Llave guardada en: ", ruta_llave)
message("Notificar al equipo que LLAVE_ID_UNAL_FCE.csv está disponible.")
