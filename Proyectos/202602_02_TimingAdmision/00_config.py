# 00_config.py

import getpass
from pathlib import Path

usuario = getpass.getuser()

# --- Un bloque por persona ---
if usuario == "dilantovarroa":  # Dilan Tovar (Mac)
    DIR_PROYECTOS = Path("/Users/dilantovarroa/Library/CloudStorage/GoogleDrive-ditovarr@unal.edu.co/Mi unidad/SemilleroMicroeconometriaProyectos")
else:
    raise RuntimeError(f"Usuario '{usuario}' no configurado: agrega tu bloque en 00_config.py")

# Carpetas del proyecto
DIR_FINAL      = DIR_PROYECTOS / "FinalWorkingDataSets"   
DIR_PROYECTO   = DIR_PROYECTOS / "202602_02_TimingAdmision"
DIR_DATA       = DIR_PROYECTO / "data"
DIR_OUTPUT     = DIR_PROYECTO / "output"
DIR_NORMATIVA  = DIR_PROYECTO / "Revision_normativa"
DIR_LITERATURA = DIR_PROYECTO / "Literatura"
