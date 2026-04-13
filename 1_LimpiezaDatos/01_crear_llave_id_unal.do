/*==============================================================================
  PROYECTO: Armonización de Datos UNAL — Semillero de Análisis Econométrico
  ARCHIVO:  01_crear_llave_id_unal.do
  PROPÓSITO: Construir el ID único anónimo (id_unal) a partir de Matriculados,
             que es el archivo de partida y define el universo completo de
             estudiantes del proyecto.
  AUTOR:    Semillero de Análisis Econométrico — Universidad Nacional de Colombia
  FECHA:    2026-04-13

  INSUMOS (DatosOriginales/Registro_FCE_2025/Matriculado/):
    - Matriculados_2009-1S.csv   (o .xlsx)
    - Matriculados_2023-2S.csv   (o .xlsx)

    ⚠ NOTA: verificar en Fase 2 (inventario) cuál es el campo de ID personal
    disponible en Matriculados (correo UNAL, cédula, o código estudiantil).
    Actualizar el nombre de la variable de identificación en la Sección 2.

  SALIDAS (DatosArmonizados/keys/ — CONFIDENCIAL, nunca a GitHub):
    - LLAVE_ID_UNAL.dta    crosswalk: ID real ↔ id_unal
    - LLAVE_ID_UNAL.csv    misma llave en CSV

  DESCRIPCIÓN DE LA LLAVE (id_unal):
    El ID único anónimo se construye mediante permutación aleatoria con semilla
    fija, sin usar ningún dato personal en el identificador resultante:
      1. Consolidar todos los IDs reales únicos de ambos archivos de Matriculados
      2. Ordenar por un número aleatorio generado con semilla fija (set seed)
      3. El rango en ese orden (1, 2, 3, ...) es el número anónimo del estudiante
      4. Formato: prefijo "UNAL" + 6 dígitos con ceros ("UNAL000001", "UNAL004832")

    Propiedades garantizadas:
      (1) Unicidad         — los rangos son estrictamente únicos por construcción
      (2) Anonimato        — el ID no contiene ni correo, ni nombre, ni ningún PII
      (3) Reproducibilidad — la misma semilla siempre produce los mismos IDs
      (4) Irreversibilidad — el rango no permite recuperar el ID real original
      (5) Compatibilidad   — funciona en cualquier versión de Stata

  SEMILLA:
    set seed 20260223 — heredada del proyecto anterior (BASE_DATOS_REGISTRO_UNAL_BOGOTA).
    Esta semilla debe mantenerse fija para que los IDs sean reproducibles y
    compatibles con cualquier trabajo anterior. NO cambiar sin documentarlo en
    el log de sesión y notificar al Director del Semillero.

  ESTRUCTURA DEL DO-FILE:
    Sección 1. Configuración global
    Sección 2. Cargar Matriculados y extraer universo de estudiantes
    Sección 3. Generar id_unal mediante permutación aleatoria
    Sección 4. Verificar unicidad
    Sección 5. Guardar llave
==============================================================================*/


/*------------------------------------------------------------------------------
  SECCIÓN 1. CONFIGURACIÓN GLOBAL
------------------------------------------------------------------------------*/

clear all
set more off
version 17

* ── Rutas del proyecto ─────────────────────────────────────────────────────
global dir_originales "C:/Drive2023/UNAL_Docente/SemilleroAnalisisEconometrico/DatosOriginales/Registro_FCE_2025/Matriculado"
global dir_keys       "C:/Drive2023/UNAL_Docente/SemilleroAnalisisEconometrico/DatosArmonizados/keys"
global dir_logs       "C:/Drive2023/UNAL_Docente/SemilleroAnalisisEconometrico/DatosProcesados/ProcesadosMarcos/logs"

* ── Marca de tiempo ────────────────────────────────────────────────────────
local fecha_hoy = c(current_date)
di "Inicio del do-file: `fecha_hoy' " c(current_time)


/*------------------------------------------------------------------------------
  SECCIÓN 2. CARGAR MATRICULADOS Y EXTRAER UNIVERSO DE ESTUDIANTES

  ⚠ PENDIENTE FASE 2 (inventario): confirmar el nombre exacto de la variable
  de identificación personal en los archivos de Matriculados.
  Reemplazar VAR_ID_PERSONAL por el nombre real (ej: correo, cedula, cod_estudiante).
  Una vez confirmado, eliminar esta advertencia.
------------------------------------------------------------------------------*/

* --- Archivo 1: Matriculados 2009-1S ----------------------------------------
import delimited using "${dir_originales}/Matriculados_2009-1S.csv", ///
    varnames(1)    ///
    encoding("UTF-8") ///
    clear

* Conservar solo el campo de identificación personal
* ⚠ Reemplazar VAR_ID_PERSONAL por el nombre real de la variable
keep VAR_ID_PERSONAL
rename VAR_ID_PERSONAL id_real

* Marcar origen para diagnóstico
gen fuente = "2009-1S"
tempfile mat_2009
save `mat_2009'

* --- Archivo 2: Matriculados 2023-2S ----------------------------------------
import delimited using "${dir_originales}/Matriculados_2023-2S.csv", ///
    varnames(1)    ///
    encoding("UTF-8") ///
    clear

keep VAR_ID_PERSONAL
rename VAR_ID_PERSONAL id_real

gen fuente = "2023-2S"
tempfile mat_2023
save `mat_2023'

* --- Consolidar universo único de estudiantes --------------------------------
use `mat_2009', clear
append using `mat_2023'

* Eliminar duplicados: un estudiante que aparece en ambos períodos
* solo necesita un registro en la llave
duplicates drop id_real, force

di _n "=== UNIVERSO DE ESTUDIANTES ==="
di "  Total estudiantes únicos: " _N

* Validar que id_real no tiene vacíos
assert !missing(id_real)


/*------------------------------------------------------------------------------
  SECCIÓN 3. GENERAR id_unal MEDIANTE PERMUTACIÓN ALEATORIA CON SEMILLA FIJA
------------------------------------------------------------------------------*/

* Orden de partida determinístico
sort id_real

* Semilla heredada del proyecto anterior — NO cambiar
* Documentar en log si alguna vez se necesita extender con nueva semilla
set seed 20260223

gen double rand_perm = runiform()   // número aleatorio por estudiante
sort rand_perm                      // orden scrambled sin relación con id_real
gen long rank_anon = _n             // rango en el orden scrambled

sort id_real                        // restaurar orden original

* Generar id_unal: prefijo UNAL + 6 dígitos con ceros
gen id_unal = "UNAL" + string(rank_anon, "%06.0f")

* Eliminar variables auxiliares
drop rand_perm rank_anon fuente

* Etiquetar variables
label variable id_real  "Identificador personal del estudiante (confidencial — no compartir)"
label variable id_unal  "ID anónimo: permutación aleatoria, semilla 20260223, formato UNALxxxxxx"

* Vista previa (solo id_unal — no imprimir id_real en logs)
di _n "=== PRIMERAS 10 OBSERVACIONES (id_unal únicamente) ==="
list id_unal in 1/10, sep(0)


/*------------------------------------------------------------------------------
  SECCIÓN 4. VERIFICAR UNICIDAD
------------------------------------------------------------------------------*/

duplicates report id_unal
local n_unal = r(unique_value)
local n_obs  = _N

di _n "── Diagnóstico de unicidad ──────────────────────────────────"
di "  Estudiantes totales : `n_obs'"
di "  id_unal únicos      : `n_unal'"

if `n_obs' == `n_unal' {
    di "  RESULTADO: id_unal es ÚNICO para cada estudiante. ✓"
}
else {
    di as error "  ADVERTENCIA: id_unal tiene DUPLICADOS. Revisar semilla o id_real."
    duplicates list id_unal
}

assert id_unal != ""
di _n "=== VERIFICACIÓN DE UNICIDAD COMPLETADA ==="


/*------------------------------------------------------------------------------
  SECCIÓN 5. GUARDAR LLAVE
  Destino: DatosArmonizados/keys/ — CONFIDENCIAL, nunca a GitHub
------------------------------------------------------------------------------*/

compress

save "${dir_keys}/LLAVE_ID_UNAL.dta", replace

export delimited using "${dir_keys}/LLAVE_ID_UNAL.csv", replace

di _n "============================================================"
di "Llave guardada en DatosArmonizados/keys/:"
di "  LLAVE_ID_UNAL.dta"
di "  LLAVE_ID_UNAL.csv"
di _n "Estudiantes en la llave : " _N
di "Fin del do-file: " c(current_date) " " c(current_time)
di "============================================================"

/*==============================================================================
  FIN DEL DO-FILE
==============================================================================*/
