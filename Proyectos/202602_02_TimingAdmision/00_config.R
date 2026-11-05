# 00_config.R — rutas de cada usuario (único archivo con rutas absolutas)
usuario <- Sys.getenv("USERNAME")
if (usuario == "USUARIO") {   # Julian Bermudez
  dir_proyectos <- "G:/Mi unidad/SemilleroMicroeconometriaProyectos"
}
dir_final    <- file.path(dir_proyectos, "FinalWorkingDataSets")
dir_proyecto <- file.path(dir_proyectos, "202602_02_TimingAdmision")
dir_data     <- file.path(dir_proyecto, "data")
dir_output   <- file.path(dir_proyecto, "output")