#%% =============================================================================
# 0. SETUP
# =============================================================================

import pandas as pd
from config import DIR_DATOS

DIR_ARMONIZADOS = DIR_DATOS / "DatosArmonizados" / "retirados_limpios"
ARCHIVO = DIR_ARMONIZADOS / "retirados_limpio.csv"


#%% =============================================================================
# 1. CARGAR ARCHIVO ARMONIZADO
# =============================================================================

df = pd.read_csv(ARCHIVO, sep=";", dtype=str)

print(f"Filas: {len(df)}")
print(f"Variables ({len(df.columns)}): {df.columns.tolist()}")

#%% =============================================================================
# 2. VALORES POR VARIABLE
# =============================================================================
# Para cada variable responde:
#   - ¿Qué valores toma? (valores únicos observados tras armonización)


def _vals_no_nulos(serie: pd.Series) -> pd.Series:
    vals = serie.dropna()
    if vals.dtype == object:
        vals = vals[vals.str.strip() != ""]
    return vals


print("\n" + "=" * 70)
print("DICCIONARIO DE VARIABLES — BASE ARMONIZADA DE RETIRADOS")
print("=" * 70)

for columna in df.columns:
    vals = _vals_no_nulos(df[columna])
    vals_sorted = sorted(str(v) for v in vals.unique()) if not vals.empty else []
    n_vals = len(vals_sorted)

    print(f"\nVARIABLE : {columna}")

    if n_vals == 0:
        print("  Valores únicos: (ninguno)")
    elif n_vals <= 50:
        print(f"  Valores únicos ({n_vals}): {vals_sorted}")
    else:
        print(f"  Valores únicos ({n_vals}): {vals_sorted[:50]} ... [y {n_vals - 50} más]")

    print("-" * 70)

# %%
