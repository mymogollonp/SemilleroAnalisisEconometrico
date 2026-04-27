/*==============================================================================
  PROYECTO: Armonización de Datos UNAL — Semillero de Análisis Econométrico
  ARCHIVO:  00_configuracion.do
  PROPÓSITO: Definir todos los globales de rutas del proyecto.
             Este do-file se llama al inicio de CADA do-file del proyecto.
  FECHA:    2026-04-14

  INSTRUCCIONES PARA CADA RA:
  1. Busca el bloque con tu nombre de usuario de Windows (ver c(username))
  2. Reemplaza "C:/COMPLETAR/..." con las rutas reales en tu máquina
  3. Guarda el archivo, haz commit y push al repositorio
  4. Para saber tu nombre de usuario de Windows, ejecuta en Stata: di c(username)
==============================================================================*/

clear all
set more off

* ── Detectar usuario de Windows ────────────────────────────────────────────
local usuario = c(username)
di "Usuario detectado: `usuario'"

* ── Rutas raíz según máquina (cada RA completa su bloque) ──────────────────

if "`usuario'" == "NicolasC" {
    * ⚠ Reemplazar con tus rutas reales
    global dir_datos  "C:/COMPLETAR/SemilleroAnalisisEconometrico"
    global dir_code   "C:/COMPLETAR/code/SemilleroAnalisisEconometrico"
}
else if "`usuario'" == "JeronimoJ" {
    * ⚠ Reemplazar con tus rutas reales
    global dir_datos  "C:/COMPLETAR/SemilleroAnalisisEconometrico"
    global dir_code   "C:/COMPLETAR/code/SemilleroAnalisisEconometrico"
}
else if "`usuario'" == "majoc" {
    * ⚠ Reemplazar con tus rutas reales
    global dir_datos  "G:/.shortcut-targets-by-id/10I6zKIZovl02Q4Q7DklodKBGjHWu6boA/SemilleroAnalisisEconometrico/DatosOriginales"
    global dir_code   "C:/SemilleroAnalisisEconometrico"
}
else if "`usuario'" == "NicolasJ" {
    * ⚠ Reemplazar con tus rutas reales
    global dir_datos  "C:/COMPLETAR/SemilleroAnalisisEconometrico"
    global dir_code   "C:/COMPLETAR/code/SemilleroAnalisisEconometrico"
}
else if "`usuario'" == "karollg" | "`usuario'" == "monikean" {
    * PI / CoPI — rutas en Drive
    global dir_datos  "C:/Drive2023/UNAL_Docente/SemilleroAnalisisEconometrico"
    global dir_code   "C:/code/SemilleroAnalisisEconometrico"
}
else {
    di as error "================================================================"
    di as error "USUARIO NO RECONOCIDO: `usuario'"
    di as error "Agregar tu bloque en 00_configuracion.do, hacer commit y push."
    di as error "================================================================"
    error 1
}

* ── Rutas derivadas (iguales para todos una vez definidas las raíces) ────────

* Datos
global dir_originales   "${dir_datos}/DatosOriginales"
global dir_armonizados  "${dir_datos}/DatosArmonizados"
global dir_keys         "${dir_datos}/DatosArmonizados/keys"
global dir_anonimizados "${dir_datos}/DatosArmonizados/1_DatosAnonimizados"
global dir_limpios      "${dir_datos}/DatosArmonizados/2_DatosLimpios"
global dir_panel        "${dir_datos}/DatosArmonizados/panel"
global dir_muestras     "${dir_datos}/DatosArmonizados/muestras"
global dir_outputs      "${dir_datos}/DatosArmonizados/outputs"
global dir_heredado     "${dir_datos}/HeredadoMarcos/ProcesadosMarcos"

* Datos originales por módulo
global dir_mat_orig     "${dir_originales}/Matriculado"
global dir_cur_orig     "${dir_originales}/Cursadas"
global dir_can_orig     "${dir_originales}/Cancelaciones"
global dir_egr_orig     "${dir_originales}/Egresados"
global dir_ret_orig     "${dir_originales}/Retirados"

* Datos anonimizados por módulo
global dir_mat_anon     "${dir_anonimizados}/Matriculado"
global dir_cur_anon     "${dir_anonimizados}/Cursadas"
global dir_can_anon     "${dir_anonimizados}/Cancelaciones"
global dir_egr_anon     "${dir_anonimizados}/Egresados"
global dir_ret_anon     "${dir_anonimizados}/Retirados"

* Código y logs
global dir_logs         "${dir_code}/logs"

* ── Verificar que las carpetas raíz existen ─────────────────────────────────
foreach ruta in "${dir_datos}" "${dir_originales}" "${dir_armonizados}" {
    capture confirm file "`ruta'/."
    if _rc != 0 {
        di as error "CARPETA NO ENCONTRADA: `ruta'"
        di as error "Verificar rutas en 00_configuracion.do"
        error 601
    }
}

* ── Confirmación ─────────────────────────────────────────────────────────────
di _n "================================================================"
di "Configuración cargada — usuario: `usuario'"
di "  dir_datos : ${dir_datos}"
di "  dir_code  : ${dir_code}"
di "================================================================"

/*==============================================================================
  FIN DEL DO-FILE
==============================================================================*/
