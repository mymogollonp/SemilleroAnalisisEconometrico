# 00_config.R — Proyecto 202602_03_ModalidadTrabajoGrado

usuario <- Sys.info()[["user"]]

if (usuario == "mcc") {
  dir_proyectos <- "/Users/mcc/Library/CloudStorage/GoogleDrive-mcarrilloca@unal.edu.co/Mi unidad/SemilleroMicroeconometriaProyectos"
} else {
  stop("Usuario no configurado. Agrega tu ruta en 00_config.R")
}

dir_final    <- file.path(dir_proyectos, "FinalWorkingDataSets")
dir_proyecto <- file.path(dir_proyectos, "202602_03_ModalidadTrabajoGrado")
dir_data     <- file.path(dir_proyecto, "data")
dir_output   <- file.path(dir_proyecto, "output")
dir_norma    <- file.path(dir_proyecto, "Revision_normativa")
