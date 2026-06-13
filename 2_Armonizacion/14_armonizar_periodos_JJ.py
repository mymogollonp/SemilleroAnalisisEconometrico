# =============================================================================
# Tarea 14 — Armonizar periodos (verificar formato y generar periodo_num)
#
# Qué hace:
#   1. Verifica que todos los valores de PERIODO en los 33 CSVs limpios de
#      Cursadas cumplan el formato YYYY-N[SAI] (ej. 2009-1S, 2011-2A, 2010-1I).
#      Reporta en consola los valores fuera de formato sin eliminarlos.
#   2. Agrega la columna `periodo_num` (entero ordinal: YYYY*10 + N) a cada
#      CSV y sobreescribe el archivo en disco.
#
# Formatos aceptados y mapeo:
#   YYYY-1S → periodo_num = YYYY1  (semestre regular)
#   YYYY-2S → periodo_num = YYYY2
#   YYYY-1A → periodo_num = YYYY1  (anual, se trata como semestre 1)
#   YYYY-2A → periodo_num = YYYY2
#   YYYY-1I → periodo_num = YYYY1  (intersemestral, se trata como semestre 1)
#   YYYY-2I → periodo_num = YYYY2
#
# Input:
#   - 33 CSVs limpios de Cursadas  →  CURSADAS_GLOB
#
# Output:
#   - Los mismos 33 CSVs sobreescritos con la columna `periodo_num` añadida.
#   - Consola: reporte de validación y resumen de archivos procesados.
#
# Por qué:
#   Los CSVs originales solo tienen PERIODO en texto. periodo_num permite
#   ordenar cronológicamente y hacer cruces numéricos entre módulos.
# =============================================================================

import os
import glob
import re
from pathlib import Path
import pandas as pd

# ── Rutas ────────────────────────────────────────────────────────────────────
BASE_DIR      = r"c:\Users\Jero\Documents\Semillero Econometría"
CURSADAS_GLOB = "Semana a Semana/Semana 5/Cursados/Cursadas_*_limpio.csv"

os.chdir(BASE_DIR)

cursadas_files = sorted(glob.glob(CURSADAS_GLOB, recursive=True))
print(f"Cursadas encontradas: {len(cursadas_files)}")

# ── Funciones ─────────────────────────────────────────────────────────────────
def periodo_to_num(p):
    if p is None:
        return None
    p = str(p).strip()
    m = re.search(r'(\d{4}).*?(1|2)', p)
    if not m:
        return None
    year = int(m.group(1))
    term = int(m.group(2))
    return year * 10 + term


def apply_periodo_num_to_files(file_list, dry_run=True):
    summary = []
    for f in file_list:
        try:
            df = pd.read_csv(f, dtype=str)
        except Exception as e:
            summary.append((f, 'read_error', str(e)))
            continue
        if 'PERIODO' not in df.columns:
            summary.append((f, 'no_periodo', None))
            continue
        df['periodo_num'] = df['PERIODO'].apply(periodo_to_num)
        if not dry_run:
            try:
                df.to_csv(f, index=False)
                summary.append((f, 'written', df['periodo_num'].notna().sum()))
            except Exception as e:
                summary.append((f, 'write_error', str(e)))
        else:
            summary.append((f, 'dry_run', df['periodo_num'].notna().sum()))
    return summary


# ── Verificación de formato PERIODO ──────────────────────────────────────────
PERIODO_RE = re.compile(r'^\d{4}-[12][SAI]$')
print("\nVerificando formato PERIODO en los 33 archivos de Cursadas...")
invalidos_total = 0
for f in cursadas_files:
    try:
        df = pd.read_csv(f, usecols=['PERIODO'], dtype=str)
    except Exception as e:
        print(f"  ERROR leyendo {Path(f).name}: {e}")
        continue
    mask_inv = ~df['PERIODO'].str.match(PERIODO_RE, na=False)
    vals_inv = df.loc[mask_inv, 'PERIODO'].value_counts()
    if not vals_inv.empty:
        print(f"  {Path(f).name}: valores fuera de formato canónico "
              f"(se mapean al semestre más cercano):")
        for val, cnt in vals_inv.items():
            print(f"    '{val}' — {cnt:,} filas")
        invalidos_total += int(mask_inv.sum())
if invalidos_total == 0:
    print("OK — todos los valores de PERIODO cumplen el formato YYYY-N[SAI].")
else:
    print(f"\nTotal filas con PERIODO fuera de formato canónico: {invalidos_total:,}")

# ── Aplicar periodo_num y sobreescribir archivos ──────────────────────────────
print("\nAplicando periodo_num a los 33 CSVs de Cursadas...")
summary = apply_periodo_num_to_files(cursadas_files, dry_run=False)
for s in summary:
    print(s)
print(f"\nTotal archivos procesados: {len(summary)}")
