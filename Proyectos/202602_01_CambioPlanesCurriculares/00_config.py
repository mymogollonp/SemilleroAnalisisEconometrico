# 00_config.py
import getpass
from pathlib import Path
if getpass.getuser() == "jerso":
    DIR_PROYECTOS = Path("G:\\.shortcut-targets-by-id\\1f3W8JcZ308fkcpQU03NJuKypF-xkvwt1\\SemilleroMicroeconometriaProyectos")
DIR_FINAL    = DIR_PROYECTOS / "FinalWorkingDataSets"
DIR_PROYECTO = DIR_PROYECTOS / "202602_01_CambioPlanesCurriculares"
