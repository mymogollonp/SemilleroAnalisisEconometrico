# =============================================================================
# 02_base_cursadas.py
#
# Qué hace:
#   Construye la base de trabajo de Cursadas: un CSV por período académico con
#   una fila por (id_unal, COD_PLAN), consolidando créditos, promedios y
#   acumulados a partir de los registros individuales de asignatura.
#
# Input:
#   Cursadas_[YYYY-NS]_limpio.csv  (33 archivos, uno por período)
#   Ruta: Semana 5/Cursados/
#
# Output:
#   BASE_CURSADAS_[YYYY-NS].csv  (un archivo por período)
#   Ruta: Semana 8/
#
# Por qué:
#   Los CSVs limpios tienen una fila por asignatura cursada. La base de trabajo
#   colapsa al nivel alumno-plan-período para que sea el insumo directo de los
#   modelos de rendimiento académico.
# =============================================================================

import glob
import os

import pandas as pd

# ---------------------------------------------------------------------------
# RUTAS
# ---------------------------------------------------------------------------
INPUT_GLOB = (
    r"c:\Users\Jero\Documents\Semillero Econometría"
    r"\Semana a Semana\Semana 5\Cursados\Cursadas_*_limpio.csv"
)
OUTPUT_DIR = (
    r"c:\Users\Jero\Documents\Semillero Econometría"
    r"\Semana a Semana\Semana 8\Bases de trabajo" 
    
)

# ---------------------------------------------------------------------------
# MAPEO TIPOLOGÍA → nombre de columna
# ---------------------------------------------------------------------------
TIPOLOGIA_MAP = {
    "DISCIPLINAR OBLIGATORIA":     "creditos_cursados_periodo_disciplinar_obligatoria",
    "FUNDAMENTACION OBLIGATORIA":  "creditos_cursados_periodo_fundamentacion_obligatoria",
    "LIBRE ELECCION":              "creditos_cursados_periodo_libre_eleccion",
    "DISCIPLINAR OPTATIVA":        "creditos_cursados_periodo_disciplinar_optativa",
    "NIVELACION":                  "creditos_cursados_periodo_nivelacion",
    "FUNDAMENTACION OPTATIVA":     "creditos_cursados_periodo_fundamentacion_optativa",
    "TRABAJO DE GRADO":            "creditos_cursados_periodo_trabajo_de_grado",
    "ACTIVIDADES ACADEMICAS":      "creditos_cursados_periodo_actividades_academicas",
    "ELEGIBLES":                   "creditos_cursados_periodo_elegibles",
    "TESIS":                       "creditos_cursados_periodo_tesis",
    "OBLIGATORIA":                 "creditos_cursados_periodo_obligatoria",
}

TIPOLOGIA_COLS = list(TIPOLOGIA_MAP.values())

OUTPUT_COLS = [
    "id_unal", "periodo", "periodo_num", "academic_año", "academic_semestre", "cod_plan",
    "creditos_cursados_periodo",
    "creditos_aprobados_periodo",
    "creditos_reprobados_periodo",
    *TIPOLOGIA_COLS,
    "creditos_cursados_acumulados",
    "promedio_simple_periodo",
    "promedio_simple_acumulado",
    "papa_periodo",
]

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. LECTURA Y APILADO
# ---------------------------------------------------------------------------
files = sorted(glob.glob(INPUT_GLOB))
print(f"Leyendo {len(files)} archivos...")

df = pd.concat(
    [pd.read_csv(f, low_memory=False) for f in files],
    ignore_index=True,
)

df["CALIFICACION_NUMERICA"] = pd.to_numeric(df["CALIFICACION_NUMERICA"], errors="coerce")
df["CREDITOS_ASIGNATURA"] = pd.to_numeric(df["CREDITOS_ASIGNATURA"], errors="coerce").fillna(0)

print(f"Total filas apiladas: {len(df):,}")

# ---------------------------------------------------------------------------
# 2. MÉTRICAS DEL PERÍODO (nivel id_unal + COD_PLAN + período)
# ---------------------------------------------------------------------------
KEYS = ["id_unal", "COD_PLAN", "periodo_num"]

# -- 2a. Créditos totales cursados (todas las filas) --
cred_cursados = (
    df.groupby(KEYS, sort=False)["CREDITOS_ASIGNATURA"]
    .sum()
    .rename("creditos_cursados_periodo")
)

# -- 2b. Créditos aprobados / reprobados (solo filas con nota) --
# Rows with NaN grade produce 0 via .where(), so they're excluded naturally.
df["_cred_aprobados"] = df["CREDITOS_ASIGNATURA"].where(
    df["CALIFICACION_NUMERICA"] >= 3.0, other=0
)
df["_cred_reprobados"] = df["CREDITOS_ASIGNATURA"].where(
    df["CALIFICACION_NUMERICA"] < 3.0, other=0
)

cred_aprobados = (
    df.groupby(KEYS, sort=False)["_cred_aprobados"]
    .sum()
    .rename("creditos_aprobados_periodo")
)
cred_reprobados = (
    df.groupby(KEYS, sort=False)["_cred_reprobados"]
    .sum()
    .rename("creditos_reprobados_periodo")
)

# -- 2c. Promedio simple del período (media aritmética de notas, skipna) --
prom_simple = (
    df.groupby(KEYS, sort=False)["CALIFICACION_NUMERICA"]
    .mean()
    .rename("promedio_simple_periodo")
)

# -- 2d. PAPA del período (promedio ponderado por créditos, solo filas con nota) --
df["_nota_x_cred"] = (df["CALIFICACION_NUMERICA"] * df["CREDITOS_ASIGNATURA"]).fillna(0)
df["_cred_con_nota"] = df["CREDITOS_ASIGNATURA"].where(
    df["CALIFICACION_NUMERICA"].notna(), other=0
)

grp = df.groupby(KEYS, sort=False)
papa = (grp["_nota_x_cred"].sum() / grp["_cred_con_nota"].sum()).rename("papa_periodo")

# -- 2e. Créditos por tipología (todas las filas, pivot) --
tipologia_pivot = df.pivot_table(
    index=KEYS,
    columns="TIPOLOGIA",
    values="CREDITOS_ASIGNATURA",
    aggfunc="sum",
    fill_value=0,
)
tipologia_pivot.columns.name = None
tipologia_pivot = tipologia_pivot.rename(columns=TIPOLOGIA_MAP)

# Garantizar que existan todas las columnas de tipología aunque no aparezcan en el período
for col in TIPOLOGIA_COLS:
    if col not in tipologia_pivot.columns:
        tipologia_pivot[col] = 0

tipologia_pivot = tipologia_pivot[TIPOLOGIA_COLS]

# ---------------------------------------------------------------------------
# 3. ENSAMBLAR BASE DE PERÍODOS
# ---------------------------------------------------------------------------
base = (
    cred_cursados.to_frame()
    .join(cred_aprobados)
    .join(cred_reprobados)
    .join(prom_simple)
    .join(papa)
    .join(tipologia_pivot)
    .reset_index()
)

# ---------------------------------------------------------------------------
# 4. ACUMULADOS (expanding window, ordenado por periodo_num dentro del panel)
# ---------------------------------------------------------------------------
base = base.sort_values(["id_unal", "COD_PLAN", "periodo_num"]).reset_index(drop=True)

panel = base.groupby(["id_unal", "COD_PLAN"], sort=False)

base["creditos_cursados_acumulados"] = panel["creditos_cursados_periodo"].transform(
    lambda s: s.expanding().sum()
)

# promedio_simple_acumulado: media de los promedios simples de período hasta ese punto
# (NaN en períodos sin notas se omiten, como hace expanding().mean())
base["promedio_simple_acumulado"] = panel["promedio_simple_periodo"].transform(
    lambda s: s.expanding().mean()
)

# ---------------------------------------------------------------------------
# 5. COLUMNAS DE IDENTIFICACIÓN
# ---------------------------------------------------------------------------
# Derivar desde periodo_num para que sea consistente con el agrupamiento canónico
base["academic_año"] = (base["periodo_num"] // 10).astype(int)
base["academic_semestre"] = (base["periodo_num"] % 10).astype(int)
base["periodo"] = base["academic_año"].astype(str) + "-" + base["academic_semestre"].astype(str) + "S"
base["cod_plan"] = base["COD_PLAN"]

# ---------------------------------------------------------------------------
# 6. SPLIT POR periodo_num Y EXPORTACIÓN
# ---------------------------------------------------------------------------
base_out = base[OUTPUT_COLS].copy()

# Redondear columnas numéricas a enteros para evitar problemas de punto decimal en Excel
cols_enteras = [
    "creditos_cursados_periodo", "creditos_aprobados_periodo", "creditos_reprobados_periodo",
    "creditos_cursados_acumulados",
    *TIPOLOGIA_COLS,
]
for col in cols_enteras:
    base_out[col] = base_out[col].round(0).astype("Int64")

for periodo_num, grupo in base_out.groupby("periodo_num"):
    anio = str(int(periodo_num) // 10)
    semestre = str(int(periodo_num) % 10)
    periodo_canonico = f"{anio}-{semestre}S"
    out_path = os.path.join(OUTPUT_DIR, f"BASE_CURSADAS_{periodo_canonico}.csv")
    grupo.to_csv(out_path, index=False, encoding="utf-8-sig", sep=";")
    print(f"  {out_path}  ({len(grupo):,} filas)")

print(f"\nListo. {base_out['periodo_num'].nunique()} archivos guardados en {OUTPUT_DIR}")
