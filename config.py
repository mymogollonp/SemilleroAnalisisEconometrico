from pathlib import Path
import getpass

USER = getpass.getuser()

if USER == "nicoj":
    DIR_DATOS = Path(r"C:\Users\nicoj\Desktop\semillerop\datos")
    DIR_CODE = Path(
        r"C:\Users\nicoj\Desktop\semillerop\SemilleroAnalisisEconometrico"
    )
else:
    raise ValueError(
        "Usuario no configurado en config.py. "
        "Agrega tus rutas locales antes de ejecutar scripts."
    )