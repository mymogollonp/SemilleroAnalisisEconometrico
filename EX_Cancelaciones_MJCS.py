# =============================================================================
# EX_Cancelaciones_MJC.py
# Exploración inicial — Módulo: Cancelaciones
# RA: Maria Jose Cadena
# Proyecto: Armonización de Datos UNAL — Semillero de Análisis Econométrico
# Fecha: 2026-04-24
# =============================================================================
# INSTRUCCIONES:
#   Ajusta RUTA_ARCHIVO con la ruta real a tu carpeta DatosOriginales/Cancelaciones
#   Ajusta ARCHIVO_EJEMPLO con el nombre de uno de los archivos .xlsx del módulo
# =============================================================================

import sys
from pathlib import Path
import os
import glob
import pandas as pd

# -----------------------------------------------------------------------------
# 0. Configuración de rutas
# -----------------------------------------------------------------------------

# Sube un nivel desde 1_LimpiezaDatos/ hasta la raíz del proyecto
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import DIR_DATOS

ARCHIVO_EJEMPLO = "Cancelaciones_2009-2S.xlsx"  # <-- ajusta al nombre real

RUTA_DATOS = DIR_DATOS / "DatosOriginales" / "Cancelaciones"
RUTA_ARCHIVO = DIR_DATOS / "DatosOriginales" / "Cancelaciones" / ARCHIVO_EJEMPLO

# -----------------------------------------------------------------------------
# 1. Cargar el archivo de ejemplo
# -----------------------------------------------------------------------------

print("=" * 60)
print(f"Archivo: {ARCHIVO_EJEMPLO}")
print("=" * 60)

df = pd.read_excel(RUTA_ARCHIVO)

# -----------------------------------------------------------------------------
# 2. Dimensiones
# -----------------------------------------------------------------------------

print(f"\n>>> Dimensiones del archivo")
print(f"    Filas        : {df.shape[0]:,}")
print(f"    Columnas     : {df.shape[1]}")

# -----------------------------------------------------------------------------
# 3. Lista de variables (nombre, tipo, missings)
# -----------------------------------------------------------------------------

print(f"\n>>> Variables disponibles")
print(f"{'Variable':<35} {'Tipo':<15} {'Missings':>8}  {'%Missing':>8}")
print("-" * 70)
for col in df.columns:
    n_miss = df[col].isna().sum()
    pct_miss = n_miss / len(df) * 100
    print(f"{col:<35} {str(df[col].dtype):<15} {n_miss:>8,}  {pct_miss:>7.1f}%")

# -----------------------------------------------------------------------------
# 4. Primeras filas
# -----------------------------------------------------------------------------

print(f"\n>>> Primeras 5 filas")
with pd.option_context("display.max_columns", None, "display.width", 120):
    print(df.head())

# -----------------------------------------------------------------------------
# 5. Estadísticas descriptivas básicas (columnas numéricas)
# -----------------------------------------------------------------------------

cols_num = df.select_dtypes(include="number").columns.tolist()
if cols_num:
    print(f"\n>>> Estadísticas descriptivas (columnas numéricas)")
    print(df[cols_num].describe().round(2).to_string())

# -----------------------------------------------------------------------------
# 6. Inventario de todos los archivos del módulo
# -----------------------------------------------------------------------------

archivos = sorted(glob.glob(os.path.join(RUTA_DATOS, "*.xlsx")))

print(f"\n{'=' * 60}")
print(f"Inventario de archivos en el módulo Cancelaciones")
print(f"{'=' * 60}")
print(f"Total de archivos encontrados: {len(archivos)}\n")

resumen = []
for ruta in archivos:
    nombre = os.path.basename(ruta)
    try:
        tmp = pd.read_excel(ruta, nrows=0)     # solo encabezados para velocidad
        ncols = tmp.shape[1]
        tmp_full = pd.read_excel(ruta)
        nrows = tmp_full.shape[0]
        columnas = list(tmp_full.columns)
        resumen.append({
            "archivo": nombre,
            "n_obs": nrows,
            "n_vars": ncols,
            "variables": columnas,
        })
        print(f"  {nombre:<45}  obs={nrows:>6,}  vars={ncols:>3}")
    except Exception as e:
        print(f"  {nombre:<45}  ERROR: {e}")

# -----------------------------------------------------------------------------
# 7. Detección de inconsistencias de nombres entre archivos
# -----------------------------------------------------------------------------

print(f"\n{'=' * 60}")
print("Comparación de encabezados entre archivos")
print("=" * 60)

if resumen:
    # Conjunto de variables por archivo
    sets_vars = {r["archivo"]: set(r["variables"]) for r in resumen}
    todos = set().union(*sets_vars.values())
    referencia_nombre, referencia_set = list(sets_vars.items())[0]

    print(f"\nArchivo de referencia: {referencia_nombre}")
    print(f"Variables en referencia: {sorted(referencia_set)}\n")

    for archivo, vars_set in sets_vars.items():
        solo_en_referencia = referencia_set - vars_set
        solo_en_este      = vars_set - referencia_set
        if solo_en_referencia or solo_en_este:
            print(f"  Diferencias en '{archivo}':")
            if solo_en_referencia:
                print(f"    Faltan (están en referencia, no aquí): {sorted(solo_en_referencia)}")
            if solo_en_este:
                print(f"    Extras (no están en referencia):       {sorted(solo_en_este)}")

print(f"\n{'=' * 60}")
print("Exploración finalizada.")
print("=" * 60)
