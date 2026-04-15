/*==============================================================================
  PROYECTO: Armonización de Datos UNAL — Semillero de Análisis Econométrico
  ARCHIVO:  1_LimpiezaDatos/01_crear_llave_idunal.do
  PROPÓSITO: Construir el crosswalk id_unal ↔ ID real a partir del universo
             completo de estudiantes en Matriculados (todos los semestres).
  RESPONSABLE: Nicolas Camacho
  FECHA:    2026-04-14

  PREREQUISITO: ejecutar 02_inventario_matriculados.do primero para confirmar
  el nombre exacto de la variable de ID personal en los archivos.

  ⚠ ACCIÓN REQUERIDA ANTES DE EJECUTAR:
    En la Sección 2, reemplazar VAR_ID_PERSONAL con el nombre real de la
    variable de identificación encontrado en el inventario.
    Ejemplos típicos: correo, correo_unal, cod_estudiante, cedula

  INSUMOS:
    DatosOriginales/Matriculado/Matriculados_YYYY-NS.xlsx (34 archivos)

  SALIDAS (DatosArmonizados/keys/ — CONFIDENCIAL, nunca a GitHub):
    LLAVE_ID_UNAL_FCE.csv   crosswalk: ID real ↔ id_unal

  SEMILLA: 20260223 — mantener fija. Documentar en el log de sesión si cambia.

  SECCIONES:
    1. Configuración
    2. Loop: extraer IDs únicos de todos los archivos Matriculados
    3. Generar id_unal (permutación aleatoria con semilla fija)
    4. Verificar unicidad
    5. Guardar llave
==============================================================================*/


/*------------------------------------------------------------------------------
  SECCIÓN 1. CONFIGURACIÓN
------------------------------------------------------------------------------*/

clear all
set more off
version 16

do "00_configuracion.do"

local fecha = subinstr("$S_DATE", " ", "-", .)
log using "${dir_logs}/06_crear_llave_idunal_`fecha'.log", replace text

di "Inicio: $S_DATE $S_TIME"
di "Usuario: `c(username)'"


/*------------------------------------------------------------------------------
  SECCIÓN 2. LOOP: EXTRAER IDs ÚNICOS DE TODOS LOS ARCHIVOS MATRICULADOS

  ⚠ REEMPLAZAR VAR_ID_PERSONAL con el nombre real de la variable de ID.
    Ejecutar 01_inventario_matriculados.do primero para confirmarlo.
    Si el nombre cambia entre años, agregar un rename dentro del loop.
------------------------------------------------------------------------------*/

local var_id "VAR_ID_PERSONAL"

local files : dir "${dir_mat_orig}" files "Matriculados_*.xlsx"
local nfiles = 0
foreach f of local files { local ++nfiles }

di _n "Archivos Matriculados encontrados: `nfiles'"

if `nfiles' == 0 {
    di as error "No se encontraron archivos en ${dir_mat_orig}"
    error 1
}

local i = 0
foreach f of local files {
    local ++i

    import excel using "${dir_mat_orig}/`f'", firstrow clear

    capture confirm variable `var_id'
    if _rc != 0 {
        di as error "Archivo: `f'"
        di as error "Variable `var_id' NO encontrada. Revisar con 01_inventario_matriculados.do"
        error 111
    }

    keep `var_id'
    rename `var_id' id_real
    drop if missing(id_real)

    tempfile mat_`i'
    save `mat_`i''

    di "  `i'/`nfiles' — `f' — obs: " _N
}

use `mat_1', clear
forvalues j = 2/`nfiles' {
    append using `mat_`j''
}

duplicates drop id_real, force
sort id_real

di _n "=== UNIVERSO ÚNICO DE ESTUDIANTES ==="
di "Total IDs únicos: " _N

assert !missing(id_real)


/*------------------------------------------------------------------------------
  SECCIÓN 3. GENERAR id_unal (PERMUTACIÓN ALEATORIA CON SEMILLA FIJA)
------------------------------------------------------------------------------*/

sort id_real

* Semilla fija del proyecto — NO CAMBIAR sin documentar en el log de sesión
set seed 20260223

gen double rand_perm = runiform()
sort rand_perm
gen long rank_anon = _n

gen id_unal = "UNAL" + string(rank_anon, "%06.0f")

drop rand_perm rank_anon

label variable id_real "ID personal del estudiante (CONFIDENCIAL)"
label variable id_unal "ID anónimo — semilla 20260223 — formato UNALxxxxxx"

di _n "Primeros 5 id_unal generados (no se imprime id_real):"
list id_unal in 1/5, noobs


/*------------------------------------------------------------------------------
  SECCIÓN 4. VERIFICAR UNICIDAD
------------------------------------------------------------------------------*/

quietly duplicates report id_unal
local n_unal = r(unique_value)
local n_obs  = _N

di _n "── Diagnóstico de unicidad ──────────────────────────────"
di "  Estudiantes totales : `n_obs'"
di "  id_unal únicos      : `n_unal'"

if `n_obs' == `n_unal' {
    di "  RESULTADO: id_unal es ÚNICO para cada estudiante. OK"
}
else {
    di as error "  id_unal tiene DUPLICADOS. Revisar."
    error 1
}

assert id_unal != ""
assert !missing(id_unal)


/*------------------------------------------------------------------------------
  SECCIÓN 5. GUARDAR LLAVE
  Destino: DatosArmonizados/keys/ — CONFIDENCIAL, nunca a GitHub
------------------------------------------------------------------------------*/

export delimited using "${dir_keys}/LLAVE_ID_UNAL_FCE.csv", replace

di _n "============================================================"
di "Llave guardada: ${dir_keys}/LLAVE_ID_UNAL_FCE.csv"
di "Estudiantes en la llave: " _N
di "Fin: $S_DATE $S_TIME"
di "============================================================"

log close

/*==============================================================================
  FIN DEL DO-FILE
==============================================================================*/
