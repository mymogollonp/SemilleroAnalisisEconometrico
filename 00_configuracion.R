# ============================================================
#  00_configuracion.do — Rutas raíz por usuario
# Editar la sección correspondiente a tu máquina
# ============================================================
  
  local usuario = c(username)
  
  if "`usuario'" == "NicolasC" {
    global dir_datos  "C:/TuRuta/SemilleroAnalisisEconometrico"
    global dir_code   "C:/TuRuta/code/SemilleroAnalisisEconometrico"
  }
  else if "`usuario'" == "JeronimoJ" {
    global dir_datos  "C:/TuRuta/SemilleroAnalisisEconometrico"
    global dir_code   "C:/TuRuta/code/SemilleroAnalisisEconometrico"
  }
  