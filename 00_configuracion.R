# ============================================================
#  00_configuracion.do — Rutas raíz por usuario
# Editar la sección correspondiente a tu máquina
# ============================================================
  
usuario <- Sys.info()[["user"]]

 if (usuario == "JeronimoJ") {
  dir_datos <- "C:/TuRuta/SemilleroAnalisisEconometrico"
  dir_code  <- "C:/TuRuta/code/SemilleroAnalisisEconometrico"
  

} else if (usuario == "nicoj") {
  dir_datos <- "C:/Users/nicoj/Desktop/semillerop/datos"
  dir_code  <- "C:/Users/nicoj/Desktop/semillerop/SemilleroAnalisisEconometrico"
  
} else {
  stop("Usuario no configurado. Agrega tu ruta en 00_configuracion.R")
}
