# INVENTARIO DE CURSADAS ---------------------------------------------------

# 0. Paquetes --------------------------------------------------------------

library(readxl)
library(dplyr)
library(purrr)
library(stringr)
library(tidyr)
library(tibble)

# 1. Configuración general -------------------------------------------------

ruta_cursadas <- "Cursadas-20260419T235746Z-3-001/Cursadas"
sheet_datos   <- 2

# En estos archivos usamos la fila 2 porque la fila 1 no contiene los encabezados reales.
archivos_fila2 <- c(
  "Cursadas_2021-2S.xlsx",
  "Cursadas_2023-1S.xlsx",
  "Cursadas_2025-1S.xlsx"
)

archivos <- list.files(
  path = ruta_cursadas,
  pattern = "\\.xls[x]?$",
  full.names = TRUE,
  recursive = FALSE,
  ignore.case = TRUE
)

if (length(archivos) == 0) {
  stop("No se encontraron archivos Excel en la ruta indicada.")
}

total_archivos <- length(archivos)

cat("Número de archivos encontrados:", total_archivos, "\n")

# 2. Utilidades generales --------------------------------------------------

obtener_nombre_archivo <- function(path) {
  basename(path)
}

obtener_periodo_archivo <- function(path) {
  str_extract(obtener_nombre_archivo(path), "\\d{4}-[12]S")
}

obtener_skip <- function(path) {
  archivo_actual <- obtener_nombre_archivo(path)
  if (archivo_actual %in% archivos_fila2) 1 else 0
}

anunciar_inicio <- function(etiqueta, i, total, path) {
  cat(etiqueta, i, "de", total, ":", obtener_nombre_archivo(path),
      "| skip =", obtener_skip(path), "\n")
  flush.console()
}

anunciar_fin <- function(etiqueta, i, total, path, extra = NULL) {
  cat("  ->", etiqueta, i, "de", total, ":", obtener_nombre_archivo(path))
  if (!is.null(extra) && nzchar(extra)) {
    cat(extra)
  }
  cat("\n")
  flush.console()
}

leer_excel_base <- function(path, n_max = NULL, col_types = NULL) {
  args <- list(
    path = path,
    sheet = sheet_datos,
    skip = obtener_skip(path),
    .name_repair = "minimal"
  )
  
  if (!is.null(n_max)) {
    args$n_max <- n_max
  }
  
  if (!is.null(col_types)) {
    args$col_types <- col_types
  }
  
  df <- do.call(read_excel, args)
  names(df) <- str_squish(names(df))
  df
}

leer_excel_texto <- function(path) {
  leer_excel_base(path, col_types = "text")
}

leer_nombres_variables <- function(path) {
  names(leer_excel_base(path, n_max = 0))
}

validar_columnas <- function(df, columnas_requeridas, path) {
  faltantes <- setdiff(columnas_requeridas, names(df))
  
  if (length(faltantes) > 0) {
    stop(
      paste(
        "En", obtener_nombre_archivo(path),
        "faltan estas columnas:",
        paste(faltantes, collapse = ", ")
      )
    )
  }
}

limpiar_texto <- function(x) {
  x <- as.character(x)
  x <- str_replace_all(x, "\u00A0", " ")
  x <- str_squish(x)
  x[x %in% c("", "NA", "N/A", "NULL", ".", "-", "--")] <- NA_character_
  x
}

leer_variables <- function(path, vars) {
  df <- leer_excel_texto(path)
  validar_columnas(df, vars, path)
  
  df %>%
    select(all_of(vars)) %>%
    mutate(across(everything(), limpiar_texto))
}

medir_duplicados <- function(df) {
  if (nrow(df) == 0) {
    return(tibble(
      grupos_duplicados = 0L,
      exceso_filas = 0L
    ))
  }
  
  conteo <- df %>%
    count(across(everything()), name = "n")
  
  tibble(
    grupos_duplicados = sum(conteo$n > 1),
    exceso_filas = sum(conteo$n - 1L)
  )
}

# 3. Inventario estructural del módulo ------------------------------------

leer_encabezados <- function(path) {
  archivo_actual <- obtener_nombre_archivo(path)
  df0 <- leer_excel_base(path, n_max = 0)
  
  tibble(
    archivo = archivo_actual,
    periodo = obtener_periodo_archivo(path),
    variable = names(df0)
  )
}

variables_por_periodo <- map_dfr(archivos, function(path) {
  cat("Leyendo:", obtener_nombre_archivo(path), "\n")
  leer_encabezados(path)
})

resumen_variables <- variables_por_periodo %>%
  count(periodo, archivo, name = "n_variables") %>%
  arrange(periodo)

print(resumen_variables, n = 40)

presencia_resumen <- variables_por_periodo %>%
  distinct(periodo, variable) %>%
  count(variable, name = "n_periodos") %>%
  arrange(n_periodos, variable)

variables_que_cambian <- presencia_resumen %>%
  filter(n_periodos < n_distinct(variables_por_periodo$periodo))

print(variables_que_cambian, n = 100)

# No hay variables que aparezcan o desaparezcan a lo largo de los años.
# Siempre se tiene el mismo grupo de variables.

# 4. Número de observaciones ----------------------------------------------

contar_obs_archivo <- function(path, i, total) {
  anunciar_inicio("Contando", i, total, path)
  
  df <- leer_excel_texto(path)
  
  tibble(
    archivo = obtener_nombre_archivo(path),
    n_obs = nrow(df)
  )
}

obs_por_archivo <- map2_dfr(
  archivos,
  seq_along(archivos),
  ~ contar_obs_archivo(.x, .y, total_archivos)
)

obs_por_archivo

total_obs <- sum(obs_por_archivo$n_obs)

total_obs

obs_por_archivo_con_total <- bind_rows(
  obs_por_archivo,
  tibble(archivo = "TOTAL_33_ARCHIVOS", n_obs = total_obs)
)

obs_por_archivo_con_total

# 5. Verificar si las notas siempre están en la escala 0-5 -----------------

diagnostico_calificacion_numerica <- function(path, i, total) {
  anunciar_inicio("Leyendo", i, total, path)
  
  df <- leer_excel_texto(path)
  archivo_actual <- obtener_nombre_archivo(path)
  
  if (!"CALIFICACION_NUMERICA" %in% names(df)) {
    cat("  -> No se encontró CALIFICACION_NUMERICA en", archivo_actual, "\n")
    flush.console()
    
    return(
      tibble(
        archivo = archivo_actual,
        n_obs = nrow(df),
        error = "No existe la columna CALIFICACION_NUMERICA",
        n_missing = NA_integer_,
        n_no_parsea = NA_integer_,
        n_fuera_rango = NA_integer_,
        min_nota = NA_real_,
        max_nota = NA_real_,
        ejemplos_no_parsea = NA_character_,
        ejemplos_fuera_rango = NA_character_
      )
    )
  }
  
  nota_txt <- limpiar_texto(df$CALIFICACION_NUMERICA)
  nota_txt <- ifelse(is.na(nota_txt), NA_character_, str_replace_all(nota_txt, ",", "."))
  nota_num <- suppressWarnings(as.numeric(nota_txt))
  
  anunciar_fin("Terminado", i, total, path)
  
  tibble(
    archivo = archivo_actual,
    n_obs = nrow(df),
    error = NA_character_,
    n_missing = sum(is.na(nota_txt)),
    n_no_parsea = sum(!is.na(nota_txt) & is.na(nota_num)),
    n_fuera_rango = sum(!is.na(nota_num) & (nota_num < 0 | nota_num > 5)),
    min_nota = if (all(is.na(nota_num))) NA_real_ else min(nota_num, na.rm = TRUE),
    max_nota = if (all(is.na(nota_num))) NA_real_ else max(nota_num, na.rm = TRUE),
    ejemplos_no_parsea = paste(
      head(unique(nota_txt[!is.na(nota_txt) & is.na(nota_num)]), 5),
      collapse = " | "
    ),
    ejemplos_fuera_rango = paste(
      head(unique(nota_txt[!is.na(nota_num) & (nota_num < 0 | nota_num > 5)]), 5),
      collapse = " | "
    )
  )
}

resumen_notas <- map2_dfr(
  archivos,
  seq_along(archivos),
  ~ diagnostico_calificacion_numerica(.x, .y, total_archivos)
)

resumen_notas

# Hay muchos faltantes; tal vez son cancelados o casos que no registran nota numérica.

resumen_general_notas <- resumen_notas %>%
  summarise(
    archivos_revisados = n(),
    archivos_con_error = sum(!is.na(error)),
    total_fuera_rango = sum(n_fuera_rango, na.rm = TRUE),
    total_no_parsea = sum(n_no_parsea, na.rm = TRUE),
    min_global = min(min_nota, na.rm = TRUE),
    max_global = max(max_nota, na.rm = TRUE)
  )

resumen_general_notas

# Todas las notas observadas están dentro de la escala 0-5.

# 6. Búsqueda de variables como identificador único de una observación -----

vars_llave <- c(
  "PERIODO",
  "CORREO",
  "CODIGO",
  "HIST_ACADEMICA",
  "DOCUMENTO",
  "COD_ASIGNATURA",
  "ASIGNATURA",
  "GRUPO_ASIGNATURA",
  "GRUPO_ACT",
  "ACTIVIDAD",
  "VECES_VISTA"
)

llaves_candidatas <- list(
  k1 = c("CORREO", "COD_ASIGNATURA"),
  k2 = c("CORREO", "COD_ASIGNATURA", "GRUPO_ASIGNATURA"),
  k3 = c("CORREO", "COD_ASIGNATURA", "GRUPO_ASIGNATURA", "ACTIVIDAD"),
  k4 = c("CORREO", "COD_ASIGNATURA", "GRUPO_ASIGNATURA", "GRUPO_ACT", "ACTIVIDAD"),
  k5 = c("CODIGO", "COD_ASIGNATURA", "GRUPO_ASIGNATURA", "GRUPO_ACT", "ACTIVIDAD"),
  k6 = c("CORREO", "COD_ASIGNATURA", "GRUPO_ASIGNATURA", "GRUPO_ACT", "ACTIVIDAD", "VECES_VISTA")
)

leer_vars_llave <- function(path) {
  leer_variables(path, vars_llave)
}

evaluar_llave <- function(df, vars, nombre_llave) {
  base_llave <- df %>%
    select(all_of(vars))
  
  filas_con_missing <- sum(!complete.cases(base_llave))
  
  metricas_todas <- medir_duplicados(base_llave)
  metricas_completas <- medir_duplicados(base_llave %>% filter(complete.cases(.)))
  
  tibble(
    llave = nombre_llave,
    columnas = paste(vars, collapse = " + "),
    filas_con_missing_en_llave = filas_con_missing,
    grupos_duplicados_todas = metricas_todas$grupos_duplicados,
    exceso_filas_todas = metricas_todas$exceso_filas,
    grupos_duplicados_completas = metricas_completas$grupos_duplicados,
    exceso_filas_completas = metricas_completas$exceso_filas
  )
}

probar_llaves_archivo <- function(path, i, total) {
  anunciar_inicio("Probando llaves", i, total, path)
  
  df <- leer_vars_llave(path)
  
  out <- imap_dfr(
    llaves_candidatas,
    ~ evaluar_llave(df, .x, .y)
  ) %>%
    mutate(archivo = obtener_nombre_archivo(path), .before = 1)
  
  anunciar_fin("Terminado", i, total, path)
  
  out
}

resultado_llaves <- map2_dfr(
  archivos,
  seq_along(archivos),
  ~ probar_llaves_archivo(.x, .y, total_archivos)
)

resumen_llaves <- resultado_llaves %>%
  group_by(llave, columnas) %>%
  summarise(
    archivos_con_duplicados_todas = sum(exceso_filas_todas > 0),
    total_exceso_filas_todas = sum(exceso_filas_todas),
    archivos_con_duplicados_completas = sum(exceso_filas_completas > 0),
    total_exceso_filas_completas = sum(exceso_filas_completas),
    archivos_con_missing = sum(filas_con_missing_en_llave > 0),
    .groups = "drop"
  ) %>%
  arrange(
    archivos_con_duplicados_completas,
    total_exceso_filas_completas,
    archivos_con_duplicados_todas,
    total_exceso_filas_todas,
    archivos_con_missing
  )

resumen_llaves

# Ninguna de las llaves candidatas identificó de forma única las observaciones en los 33 archivos.
# La combinación basada en CODIGO (k5) solo mejora al restringir a casos completos, pero en el total
# de filas presenta el peor desempeño, por lo que no es una buena candidata práctica.
# Entre las llaves basadas en CORREO, la que mejor desempeño tuvo fue:
# CORREO + COD_ASIGNATURA + GRUPO_ASIGNATURA + GRUPO_ACT + ACTIVIDAD + VECES_VISTA.
# Aun así, esta combinación sigue dejando duplicados en todos los archivos, así que no puede
# considerarse una llave única definitiva; solo es la mejor aproximación entre las probadas.

# 7. Buscar cómo mejorar la llave con mejor desempeño ----------------------

llave_mejor <- c(
  "CORREO",
  "COD_ASIGNATURA",
  "GRUPO_ASIGNATURA",
  "GRUPO_ACT",
  "ACTIVIDAD",
  "VECES_VISTA"
)

vars_contexto <- c(
  "PERIODO",
  "CORREO",
  "CODIGO",
  "HIST_ACADEMICA",
  "DOCUMENTO",
  "COD_ASIGNATURA",
  "ASIGNATURA",
  "GRUPO_ASIGNATURA",
  "GRUPO_ACT",
  "ACTIVIDAD",
  "VECES_VISTA",
  "ACT_PRINCIPAL",
  "COD_TIPOLOGIA",
  "TIPOLOGIA",
  "TIPO",
  "IND",
  "APERTURA",
  "COD_UAB_ASIGNATURA",
  "UAB_ASIGNATURA",
  "CALIFICACION_NUMERICA",
  "CALIFICACION_ALFABETICA",
  "ANULADA",
  "BLOQUEADA",
  "CERRADA",
  "CON VALIDEZ ACADEMICA"
)

vars_a_comparar <- setdiff(vars_contexto, llave_mejor)

leer_contexto_duplicados <- function(path) {
  leer_variables(path, vars_contexto)
}

comparar_duplicados_archivo <- function(path, i, total) {
  anunciar_inicio("Comparando duplicados", i, total, path)
  
  df <- leer_contexto_duplicados(path) %>%
    mutate(fila_archivo = row_number())
  
  dup <- df %>%
    group_by(across(all_of(llave_mejor))) %>%
    mutate(
      n_en_grupo = n(),
      grupo_id = cur_group_id()
    ) %>%
    ungroup() %>%
    filter(n_en_grupo > 1)
  
  resumen_grupos <- dup %>%
    group_by(grupo_id, across(all_of(llave_mejor))) %>%
    summarise(
      archivo = obtener_nombre_archivo(path),
      n_filas_grupo = n(),
      across(
        all_of(vars_a_comparar),
        ~ n_distinct(.x, na.rm = FALSE),
        .names = "nd_{.col}"
      ),
      .groups = "drop"
    )
  
  anunciar_fin(
    "Terminado",
    i,
    total,
    path,
    extra = paste(
      "| grupos duplicados =", nrow(resumen_grupos),
      "| filas duplicadas =", nrow(dup)
    )
  )
  
  list(
    detalle = dup %>% mutate(archivo = obtener_nombre_archivo(path), .before = 1),
    resumen = resumen_grupos
  )
}

salida_duplicados <- map2(
  archivos,
  seq_along(archivos),
  ~ comparar_duplicados_archivo(.x, .y, total_archivos)
)

detalle_duplicados <- bind_rows(map(salida_duplicados, "detalle"))
resumen_grupos_duplicados <- bind_rows(map(salida_duplicados, "resumen"))

ranking_variables_que_varian <- resumen_grupos_duplicados %>%
  summarise(
    across(
      starts_with("nd_"),
      ~ sum(.x > 1, na.rm = TRUE)
    )
  ) %>%
  pivot_longer(
    everything(),
    names_to = "variable",
    values_to = "grupos_donde_varia"
  ) %>%
  mutate(variable = str_remove(variable, "^nd_")) %>%
  arrange(desc(grupos_donde_varia))

ranking_variables_que_varian

resumen_duplicados_exactos <- detalle_duplicados %>%
  select(archivo, all_of(vars_contexto)) %>%
  count(across(everything()), name = "n") %>%
  summarise(
    grupos_exactamente_iguales = sum(n > 1),
    filas_en_duplicados_exactos = sum(n[n > 1])
  )

resumen_duplicados_exactos

# Los resultados sugieren que el problema de unicidad no se debe solo a una llave incompleta.
# Se identificó un número alto de duplicados exactos, lo que indica que el extracto contiene
# filas repetidas que no pueden distinguirse con las variables observadas. Además, entre los
# duplicados no exactos, las variables que más frecuentemente toman valores distintos dentro
# del grupo son ASIGNATURA, HIST_ACADEMICA, APERTURA, COD_UAB_ASIGNATURA y UAB_ASIGNATURA.
# También presentan variación varios estados administrativos y variables de clasificación,
# como BLOQUEADA, CERRADA, ANULADA, CON VALIDEZ ACADEMICA, TIPO, TIPOLOGIA y COD_TIPOLOGIA.
# Esto sugiere que la base podría estar registrando tanto duplicados reales como múltiples
# estados o versiones administrativas de una misma cursada.

duplicados_exactos <- detalle_duplicados %>%
  group_by(archivo, across(all_of(vars_contexto))) %>%
  mutate(
    n_exacto = n(),
    grupo_exacto = cur_group_id()
  ) %>%
  ungroup() %>%
  filter(n_exacto > 1)

resumen_grupos_exactos <- duplicados_exactos %>%
  distinct(archivo, grupo_exacto, n_exacto) %>%
  arrange(desc(n_exacto), archivo, grupo_exacto)

resumen_grupos_exactos

# Esta tabla muestra que dentro del subconjunto de filas que ya duplicaban con la mejor llave,
# encontramos 28 123 grupos de duplicados exactos usando las variables de vars_contexto.

# 8. Mirar si hay duplicados exactos con las variables completas -----------

vars_48 <- leer_nombres_variables(archivos[1])

length(vars_48)   # debería dar 48
vars_48

leer_48_vars <- function(path, vars_48) {
  leer_variables(path, vars_48)
}

buscar_duplicados_exactos_48_archivo <- function(path, i, total, vars_48) {
  anunciar_inicio("Buscando duplicados exactos (48 vars)", i, total, path)
  
  df <- leer_48_vars(path, vars_48) %>%
    mutate(fila_archivo = row_number())
  
  dup <- df %>%
    group_by(across(all_of(vars_48))) %>%
    mutate(
      n_exacto = n(),
      grupo_exacto = cur_group_id()
    ) %>%
    ungroup() %>%
    filter(n_exacto > 1) %>%
    mutate(archivo = obtener_nombre_archivo(path), .before = 1)
  
  resumen <- tibble(
    archivo = obtener_nombre_archivo(path),
    n_obs = nrow(df),
    grupos_exactos_48 = if (nrow(dup) == 0) 0L else n_distinct(dup$grupo_exacto),
    filas_en_duplicados_exactos_48 = nrow(dup),
    max_repeticiones_48 = if (nrow(dup) == 0) 0L else max(dup$n_exacto)
  )
  
  anunciar_fin(
    "Terminado",
    i,
    total,
    path,
    extra = paste(
      "| grupos exactos =", resumen$grupos_exactos_48,
      "| filas duplicadas =", resumen$filas_en_duplicados_exactos_48
    )
  )
  
  list(
    resumen = resumen,
    detalle = dup
  )
}

salida_dup_48 <- map2(
  archivos,
  seq_along(archivos),
  ~ buscar_duplicados_exactos_48_archivo(.x, .y, total_archivos, vars_48)
)

resumen_dup_48 <- bind_rows(map(salida_dup_48, "resumen"))
detalle_dup_48 <- bind_rows(map(salida_dup_48, "detalle"))

resumen_dup_48

resumen_grupos_exactos_48 <- detalle_dup_48 %>%
  distinct(archivo, grupo_exacto, n_exacto) %>%
  arrange(desc(n_exacto), archivo, grupo_exacto)

resumen_grupos_exactos_48

grupos_a_mostrar_48 <- resumen_grupos_exactos_48 %>%
  slice_head(n = 10)

ejemplos_dup_exactos_48 <- detalle_dup_48 %>%
  semi_join(
    grupos_a_mostrar_48,
    by = c("archivo", "grupo_exacto", "n_exacto")
  ) %>%
  arrange(desc(n_exacto), archivo, grupo_exacto, fila_archivo)

ejemplos_dup_exactos_48

resumen_dup_48_total <- resumen_dup_48 %>%
  summarise(
    total_grupos_exactos_48 = sum(grupos_exactos_48, na.rm = TRUE),
    total_filas_en_duplicados_exactos_48 = sum(filas_en_duplicados_exactos_48, na.rm = TRUE),
    max_repeticion_global_48 = max(max_repeticiones_48, na.rm = TRUE)
  )

resumen_dup_48_total

# 9. Comentarios finales ---------------------------------------------------

# El campo exacto de ID personal es DOCUMENTO. También existen CODIGO e HIST_ACADEMICA,
# pero DOCUMENTO es el identificador personal directo del estudiante.

# Los nombres de las variables NO cambian a lo largo de los años.

# Todas las notas observadas están dentro de la escala 0-5.
# Los faltantes en CALIFICACION_NUMERICA requieren revisión sustantiva posterior.

# No hay variables que por el momento puedan funcionar como identificador único,
# al menos hasta solucionar o entender mejor el problema de los duplicados.

# Lista completa de variables
print(vars_48)

