/*==============================================================================
  PROYECTO: Armonización de Datos UNAL — Semillero de Análisis Econométrico
  ARCHIVO:  1_LimpiezaDatos/02_inventario_cursadas.do
  PROPÓSITO: Explorar sistemáticamente todos los archivos de Cursadas.
             Reporta: variables, tipos, missings, consistencia entre años,
             rango de calificaciones (verificar escala 0–5),
             y la(s) variable(s) que identifican de forma única cada observación.
  RESPONSABLE: Jeronimo Jimenez
  FECHA:    2026-04-14

  INSTRUCCIONES:
  1. Asegúrate de haber completado tu bloque de rutas en 00_configuracion.do
  2. Ejecuta desde el directorio raíz del repositorio:
       do "1_LimpiezaDatos/02_inventario_cursadas.do"
  3. Revisa el log en logs/inventario_cursadas_FECHA.log
  4. Documenta hallazgos en RAtaskreport/semana01_JeronimoJ.md:
     - Nombre del campo de ID personal
     - Variables disponibles y si cambian entre años
     - Si la escala de calificaciones es 0–5 en todos los archivos
     - La(s) variable(s) que identifican de forma única cada observación

  SALIDAS:
    logs/inventario_cursadas_YYYY-MM-DD.log
==============================================================================*/


/*------------------------------------------------------------------------------
  SECCIÓN 1. CONFIGURACIÓN
------------------------------------------------------------------------------*/

clear all
set more off
version 16

do "00_configuracion.do"

local fecha = subinstr("$S_DATE", " ", "-", .)
log using "${dir_logs}/inventario_cursadas_`fecha'.log", replace text

di "================================================================"
di "INVENTARIO: CURSADAS"
di "Fecha: $S_DATE $S_TIME"
di "Usuario: `c(username)'"
di "Ruta de datos: ${dir_cur_orig}"
di "================================================================"


/*------------------------------------------------------------------------------
  SECCIÓN 2. CONTEO DE ARCHIVOS
------------------------------------------------------------------------------*/

local files : dir "${dir_cur_orig}" files "Cursadas_*.xlsx"
local nfiles = 0
foreach f of local files { local ++nfiles }

di _n "Total archivos encontrados: `nfiles'"
di "Se esperaban 33 archivos (2009-1S a 2025-1S)."
if `nfiles' != 33 {
    di as error "⚠ Número de archivos inesperado. Verificar carpeta."
}


/*------------------------------------------------------------------------------
  SECCIÓN 3. LOOP: PERFIL DE CADA ARCHIVO
------------------------------------------------------------------------------*/

local baseline_vars  ""
local archivo_base   ""
local inconsistentes ""
local i = 0

foreach f of local files {
    local ++i

    import excel using "${dir_cur_orig}/`f'", firstrow clear

    local periodo = subinstr("`f'", "Cursadas_", "", .)
    local periodo = subinstr("`periodo'", ".xlsx",    "", .)

    ds
    local vars_actuales = r(varlist)
    local nvars = wordcount("`vars_actuales'")

    di _n "────────────────────────────────────────────────────────"
    di "Archivo [`i'/`nfiles']: `f'"
    di "Período: `periodo'   |   Obs: " _N "   |   Variables: `nvars'"
    di "Variables: `vars_actuales'"

    di _n "  Nombre Stata          Tipo        Etiqueta (header Excel)"
    di    "  ─────────────────────────────────────────────────────────"
    foreach v of varlist _all {
        local tipo  : type `v'
        local label : variable label `v'
        di "  %-22s %-12s %s" "`v'" "`tipo'" "`label'"
    }

    di _n "  Missings por variable:"
    quietly misstable summarize, all
    if r(N_gt_zero) == 0 di "    (Sin missings)"

    * ── Chequeo de rango de calificaciones (escala esperada: 0–5) ────────────
    di _n "  Rango de variables numéricas (verificar escala calificaciones 0–5):"
    foreach v of varlist _all {
        local tipo : type `v'
        if substr("`tipo'", 1, 3) != "str" {
            quietly summarize `v'
            if r(N) > 0 {
                di "    `v': min=" r(min) "  max=" r(max) "  mean=" %5.2f r(mean)
                if r(max) > 5 | r(min) < 0 {
                    di as error "    ⚠ `v' FUERA de rango 0–5"
                }
            }
        }
    }

    * ── Unicidad de observaciones ───────────────────────────────────────────
    di _n "  Unicidad — variable(s) que identifican de forma única cada observación:"
    local encontro_clave 0
    foreach v of varlist _all {
        capture isid `v'
        if _rc == 0 {
            di "    ✓ `v' es clave única (" _N " valores distintos = " _N " obs)"
            local encontro_clave 1
        }
    }
    if `encontro_clave' == 0 {
        di "    (ninguna variable individual es clave única — la clave es compuesta)"
        di "    Anotar en el reporte qué combinación de variables identifica la obs"
    }

    local vars_sorted : list sort vars_actuales
    if `i' == 1 {
        local baseline_vars = "`vars_sorted'"
        local archivo_base  = "`f'"
    }
    else {
        if "`vars_sorted'" != "`baseline_vars'" {
            di as error "  ⚠ VARIABLES DISTINTAS al archivo base (`archivo_base')"
            local diff_add : list vars_sorted - baseline_vars
            local diff_del : list baseline_vars - vars_sorted
            if "`diff_add'" != "" di as error "    Variables nuevas    : `diff_add'"
            if "`diff_del'" != "" di as error "    Variables faltantes : `diff_del'"
            local inconsistentes "`inconsistentes' `f'"
        }
    }

    clear
}


/*------------------------------------------------------------------------------
  SECCIÓN 4. RESUMEN FINAL
------------------------------------------------------------------------------*/

di _n "================================================================"
di "RESUMEN INVENTARIO CURSADAS"
di "Total archivos procesados : `nfiles'"
di "Variables en archivo base : `baseline_vars'"

if "`inconsistentes'" == "" {
    di "Consistencia entre archivos: OK"
}
else {
    di as error "⚠ Archivos con variables inconsistentes:"
    foreach f of local inconsistentes {
        di as error "  - `f'"
    }
}

di _n "PRÓXIMOS PASOS:"
di "  1. Identificar el campo de ID personal; confirmar coincide con Matriculados"
di "  2. Verificar si alguna variable de calificaciones reportó ⚠ fuera de rango"
di "  3. Identificar la(s) variable(s) que forman la clave única de observación"
di "  4. Documentar hallazgos en RAtaskreport/semana01_JeronimoJ.md"
di "================================================================"
di "Fin: $S_DATE $S_TIME"

log close

/*==============================================================================
  FIN DEL DO-FILE
==============================================================================*/
