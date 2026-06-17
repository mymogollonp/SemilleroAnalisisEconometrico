# =============================================================================
# Tarea 13 — Armonizar IDs (cobertura y cruce de id_unal)
#
# Qué hace:
#   Parte 1: Verifica qué porcentaje de filas tiene id_unal en los 33 CSVs
#            limpios de Cursadas. Lee en modo binario con reintentos para
#            evitar errores de encoding.
#   Parte 2: Extrae los id_unal únicos de Cursadas y Matriculados y reporta
#            cuántos están en uno pero no en el otro.
#
# Input:
#   - 33 CSVs limpios de Cursadas  →  CURSADAS_GLOB
#   - CSVs limpios de Matriculados →  MATRICULADOS_GLOB
#
# Output:
#   - Solo consola: cobertura por archivo, consolidado y cruce de IDs.
#     No escribe archivos.
#
# Por qué:
#   Antes de armonizar periodos hay que confirmar que la llave id_unal está
#   presente en (casi) todos los registros y entender qué personas aparecen
#   en Cursadas sin haber sido Matriculados.
# =============================================================================

import os
import glob
import csv
import io
import time
from pathlib import Path

# ── Rutas ────────────────────────────────────────────────────────────────────
BASE_DIR          = r"c:\Users\Jero\Documents\Semillero Econometría"
CURSADAS_GLOB     = "Semana a Semana/Semana 5/Cursados/Cursadas_*_limpio.csv"
MATRICULADOS_GLOB = "Semana a Semana/Semana 7/Datos Anonimizados/Matriculados_*_limpio.csv"

os.chdir(BASE_DIR)

cursadas_files     = sorted(glob.glob(CURSADAS_GLOB,     recursive=True))
matriculados_files = sorted(glob.glob(MATRICULADOS_GLOB, recursive=True))

print(f"Cursadas encontradas:     {len(cursadas_files)}")
print(f"Matriculados encontradas: {len(matriculados_files)}")

# ── Parte 1: Cobertura de id_unal en Cursadas ─────────────────────────────
def count_id_unal_in_file(path, column='id_unal', retries=3):
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            with open(path, 'rb') as bf:
                txt = io.TextIOWrapper(bf, encoding='utf-8', errors='replace', newline='')
                reader = csv.reader(txt)
                header = next(reader)
                try:
                    idx = header.index(column)
                except ValueError:
                    return {'file': path, 'total': 0, 'present': 0, 'missing': 0, 'error': 'no_column'}
                total = 0
                present = 0
                for row in reader:
                    total += 1
                    val = row[idx].strip() if idx < len(row) else ''
                    if val != '' and val.lower() not in ('na', 'nan'):
                        present += 1
                return {'file': path, 'total': total, 'present': present,
                        'missing': total - present, 'error': None}
        except Exception as e:
            last_err = e
            time.sleep(0.3)
    return {'file': path, 'total': 0, 'present': 0, 'missing': 0, 'error': str(last_err)}


print("\n--- Parte 1: Cobertura id_unal en Cursadas ---")
results = []
for f in cursadas_files:
    res = count_id_unal_in_file(f)
    results.append(res)
    if res['error'] is None:
        pct = (res['missing'] / res['total'] * 100) if res['total'] > 0 else 0.0
        print(f"{Path(f).name}: filas={res['total']}, con_id_unal={res['present']}, "
              f"sin_id_unal={res['missing']}, pct_sin={pct:.2f}%")
    else:
        print(f"{Path(f).name}: ERROR: {res['error']}")

total_rows    = sum(r['total']   for r in results)
total_present = sum(r['present'] for r in results)
total_missing = sum(r['missing'] for r in results)
pct_missing   = (total_missing / total_rows * 100) if total_rows > 0 else 0.0
print("\n--- Consolidado Cursadas ---")
print(f"total_filas={total_rows}, con_id_unal={total_present}, "
      f"sin_id_unal={total_missing}, pct_sin={pct_missing:.2f}%")

# ── Parte 2: Cruce Cursadas vs Matriculados ───────────────────────────────
def iter_id_unal_from_file(path, column='id_unal', retries=3):
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            with open(path, 'rb') as bf:
                txt = io.TextIOWrapper(bf, encoding='utf-8', errors='replace', newline='')
                reader = csv.reader(txt)
                header = next(reader)
                try:
                    idx = header.index(column)
                except ValueError:
                    return
                for row in reader:
                    if idx < len(row):
                        v = row[idx].strip()
                        if v != '' and v.lower() not in ('na', 'nan'):
                            yield v
            return
        except Exception as e:
            last_err = e
            time.sleep(0.3)


def unique_ids_from_files(file_list):
    s = set()
    for f in file_list:
        for v in iter_id_unal_from_file(f):
            s.add(v)
    return s


print("\n--- Parte 2: Cruce id_unal Cursadas vs Matriculados ---")
ids_curs = unique_ids_from_files(cursadas_files)
ids_mat  = unique_ids_from_files(matriculados_files)

print(f"id_unal únicos en Cursadas:                          {len(ids_curs):,}")
print(f"id_unal únicos en Matriculados:                      {len(ids_mat):,}")
print(f"id_unal en Cursadas que SÍ están en Matriculados:    {len(ids_curs & ids_mat):,}")
n_solo_curs = len(ids_curs - ids_mat)
pct_solo    = (n_solo_curs / len(ids_curs) * 100) if ids_curs else 0.0
print(f"id_unal en Cursadas que NO están en Matriculados:    {n_solo_curs:,}  ({pct_solo:.2f}%)")
print(f"id_unal en Matriculados que NO están en Cursadas:    {len(ids_mat - ids_curs):,}")
