from pathlib import Path
import getpass

USER = getpass.getuser()

if USER == "nicoj":
    DIR_DATOS = Path(r"C:\Users\nicoj\Desktop\semillerop\datos")
    DIR_CODE = Path(r"C:\Users\nicoj\Desktop\semillerop\SemilleroAnalisisEconometrico")

elif USER == "majoc":
    DIR_DATOS = Path(r"G:\.shortcut-targets-by-id\10I6zKIZovl02Q4Q7DklodKBGjHWu6boA\SemilleroAnalisisEconometrico")
    DIR_CODE = Path(r"C:\SemilleroAnalisisEconometrico")

else:
    raise ValueError(
        "Usuario no configurado en config.py. "
        "Agrega tus rutas locales antes de ejecutar scripts."
    )