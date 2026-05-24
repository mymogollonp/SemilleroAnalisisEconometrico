#%% =============================================================================
# 0. SETUP
# =============================================================================

from pathlib import Path
import pandas as pd
from config import DIR_DATOS

DIR_ARMONIZADOS = DIR_DATOS / "DatosArmonizados" / "archivos_limpios_egresados"

#%% =============================================================================
# 1. CARGAR ARCHIVOS ARMONIZADOS
# =============================================================================

archivos = sorted(DIR_ARMONIZADOS.glob("*_limpio.csv"))
print(f"Archivos armonizados encontrados: {len(archivos)}")

dfs = {}
for archivo in archivos:
    semestre = archivo.stem.replace("_limpio", "")
    df = pd.read_csv(archivo, sep=";", dtype=str)
    dfs[semestre] = df

#%% =============================================================================
# 2. RECOPILAR TODAS LAS VARIABLES
# =============================================================================

todas_columnas = []
for df in dfs.values():
    for col in df.columns:
        if col not in todas_columnas:
            todas_columnas.append(col)

print(f"Total variables en las bases armonizadas: {len(todas_columnas)}")
print(f"Variables: {todas_columnas}")

#%% =============================================================================
# 3. VALORES Y PERIODOS POR VARIABLE
# =============================================================================
# Para cada variable responde:
#   - ¿Qué valores toma?        (valores únicos observados tras armonización)
#   - ¿En qué periodos se encuentra? (en qué archivos/semestres aparece con datos)

def _vals_no_nulos(serie: pd.Series) -> pd.Series:
    vals = serie.dropna()
    if vals.dtype == object:
        vals = vals[vals.str.strip() != ""]
    return vals


print("\n" + "=" * 70)
print("DICCIONARIO DE VARIABLES — BASES ARMONIZADAS DE EGRESADOS")
print("=" * 70)

for columna in todas_columnas:
    periodos_con_datos = []
    valores_unicos: set = set()

    for semestre, df in dfs.items():
        if columna not in df.columns:
            continue
        vals = _vals_no_nulos(df[columna])
        if not vals.empty:
            periodos_con_datos.append(semestre)
            valores_unicos.update(vals.unique())

    vals_sorted = sorted(str(v) for v in valores_unicos)
    n_vals = len(vals_sorted)
    n_periodos = len(periodos_con_datos)

    print(f"\nVARIABLE : {columna}")
    print(f"  Periodos con datos ({n_periodos}): {sorted(periodos_con_datos)}")

    if n_vals == 0:
        print("  Valores únicos: (ninguno)")
    elif n_vals <= 50:
        print(f"  Valores únicos ({n_vals}): {vals_sorted}")
    else:
        print(f"  Valores únicos ({n_vals}): {vals_sorted[:50]} ... [y {n_vals - 50} más]")

    print("-" * 70)

