#%% =============================================================================
# 0. SETUP
# =============================================================================

import pandas as pd
import re

from config import DIR_DATOS

DIR_INPUT  = DIR_DATOS / "DatosArmonizados" / "retirados_limpios"
DIR_OUTPUT        = DIR_DATOS / "DatosArmonizados" / "retirados_por_periodo"
DIR_LIMPIOS       = DIR_OUTPUT / "retirados_por_periodo_limpios"
DIR_INCONSISTENTES = DIR_OUTPUT / "inconsistentes"

CSV_RETIRADOS = next(DIR_INPUT.glob("*.csv"))

PERIODO_MIN = (2009, 1)
PERIODO_MAX = (2025, 1)


#%% =============================================================================
# 1. CARGAR
# =============================================================================

df = pd.read_csv(CSV_RETIRADOS, sep=";", dtype=str)

print(f"Archivo cargado: {CSV_RETIRADOS.name}")
print(f"Filas: {len(df)}  |  Columnas: {len(df.columns)}")


#%% =============================================================================
# 2. DIAGNÓSTICO DE PERIODO_BLOQUEO
# =============================================================================

_patron = re.compile(r"^(20\d{2})-([12])S$")

def parsear_periodo(valor: str):
    """Devuelve (anio: int, semestre: int) o None si el formato es inesperado."""
    if pd.isna(valor):
        return None
    m = _patron.match(str(valor).strip())
    if m:
        return int(m.group(1)), int(m.group(2))
    return None


periodos_unicos = sorted(df["PERIODO_BLOQUEO"].dropna().unique())
print(f"\nPeriodos únicos encontrados ({len(periodos_unicos)}):")
for p in periodos_unicos:
    print(f"  {p!r}")


#%% =============================================================================
# 3. IDENTIFICAR PERIODOS FUERA DEL RANGO ESPERADO
# =============================================================================

fuera_rango = []
formato_raro = []

for p in periodos_unicos:
    parsed = parsear_periodo(p)
    if parsed is None:
        formato_raro.append(p)
    elif parsed < PERIODO_MIN or parsed > PERIODO_MAX:
        fuera_rango.append(p)

print(f"\n{'=' * 60}")
print(f"Rango esperado: {PERIODO_MIN[0]}-{PERIODO_MIN[1]}S  →  "
      f"{PERIODO_MAX[0]}-{PERIODO_MAX[1]}S")
print(f"{'=' * 60}")

if fuera_rango:
    print(f"  WARN  Periodos fuera de rango ({len(fuera_rango)}): {fuera_rango}")
else:
    print("  OK  Todos los periodos están dentro del rango esperado")

if formato_raro:
    print(f"  WARN  Periodos con formato inesperado ({len(formato_raro)}): {formato_raro}")
else:
    print("  OK  Todos los periodos tienen formato YYYY-#S")

nulos_periodo = df["PERIODO_BLOQUEO"].isna().sum()
if nulos_periodo:
    print(f"  WARN  Filas con PERIODO_BLOQUEO nulo: {nulos_periodo}")


#%% =============================================================================
# 4. PARTIR Y GUARDAR UN CSV POR PERIODO
# =============================================================================

DIR_LIMPIOS.mkdir(parents=True, exist_ok=True)
DIR_INCONSISTENTES.mkdir(parents=True, exist_ok=True)

for periodo, grupo in df.groupby("PERIODO_BLOQUEO", dropna=False):
    parsed = parsear_periodo(periodo) if pd.notna(periodo) else None
    es_inconsistente = (
        pd.isna(periodo)
        or parsed is None
        or parsed < PERIODO_MIN
        or parsed > PERIODO_MAX
    )

    if pd.isna(periodo):
        nombre_archivo = "retirados_sin_periodo.csv"
    else:
        nombre_archivo = f"retirados_{str(periodo).strip()}.csv"

    carpeta = DIR_INCONSISTENTES if es_inconsistente else DIR_LIMPIOS
    grupo.to_csv(carpeta / nombre_archivo, index=False, sep=";", encoding="utf-8-sig")

print(f"Archivos generados en: {DIR_OUTPUT}")


#%% =============================================================================
# 5. RESUMEN POR PERIODO 
# =============================================================================

conteo = {}
for periodo, grupo in df.groupby("PERIODO_BLOQUEO", dropna=False):
    parsed = parsear_periodo(periodo) if pd.notna(periodo) else None
    es_inconsistente = (
        pd.isna(periodo)
        or parsed is None
        or parsed < PERIODO_MIN
        or parsed > PERIODO_MAX
    )
    conteo[periodo] = (len(grupo), es_inconsistente)

print(f"Total periodos: {len(conteo)}")
print(f"\nFilas por periodo:")
for p, (n, inconsistente) in sorted(conteo.items(), key=lambda x: (x[0] is None, x[0])):
    parsed = parsear_periodo(p) if pd.notna(p) else None
    if pd.isna(p) or parsed is None:
        marca = "  ← formato raro o nulo  [inconsistentes]"
    elif parsed < PERIODO_MIN or parsed > PERIODO_MAX:
        marca = "  ← FUERA DE RANGO  [inconsistentes]"
    else:
        marca = "  [limpios]"
    print(f"  {str(p):<15} {n:>6} filas{marca}")




# %%
