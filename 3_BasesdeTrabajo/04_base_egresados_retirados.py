#%% =============================================================================
# 0. SETUP
# =============================================================================

import pandas as pd

from config import DIR_DATOS

DIR_EGRESADOS    = DIR_DATOS / "DatosArmonizados" / "archivos_limpios_egresados"
DIR_RETIRADOS    = DIR_DATOS / "DatosArmonizados" / "retirados_por_periodo" / "retirados_por_periodo_limpios"
DIR_MATRICULADOS = DIR_DATOS / "DatosArmonizados" / "matriculados"
DIR_OUTPUT       = DIR_DATOS / "DatosArmonizados" / "base_egresados_retirados"

DIR_OUTPUT.mkdir(parents=True, exist_ok=True)

LLAVE = ["ID_UNAL", "periodo", "COD_PLAN"]


#%% =============================================================================
# 1. CARGAR Y PREPARAR EGRESADOS
# =============================================================================

_egr_raw = pd.concat(
    [pd.read_csv(f, sep=";", dtype=str) for f in sorted(DIR_EGRESADOS.glob("*.csv"))],
    ignore_index=True,
)
_egr_raw["periodo"] = _egr_raw["academic_anio"] + "-" + _egr_raw["academic_semester"] + "S"

# Consolidar nota: usa PROM_GRADUADO, rellena con PAPA y luego PROM_ACADEMICO
for _col in ["PROM_GRADUADO", "PAPA", "PROM_ACADEMICO"]:
    _egr_raw[_col] = _egr_raw[_col].replace({"": pd.NA, "nan": pd.NA})

_egr_raw["PROM_GRADUADO"] = (
    _egr_raw["PROM_GRADUADO"]
    .fillna(_egr_raw["PAPA"])
    .fillna(_egr_raw["PROM_ACADEMICO"])
)

_egr_raw["APERTURA"] = _egr_raw["APERTURA"].replace({"": pd.NA, "nan": pd.NA})

df_egr = _egr_raw[[
    "ID_UNAL", "periodo", "academic_anio", "academic_semester",
    "COD_PLAN", "CRED_CONSEGUIDOS", "PROM_GRADUADO", "APERTURA",
]].drop_duplicates().copy()

print(f"Egresados : {len(df_egr):>7} filas | {df_egr['periodo'].nunique()} periodos")


#%% =============================================================================
# 2. CARGAR Y PREPARAR RETIRADOS
# =============================================================================

_ret_raw = pd.concat(
    [pd.read_csv(f, sep=";", dtype=str) for f in sorted(DIR_RETIRADOS.glob("*.csv"))],
    ignore_index=True,
)
_ret_raw = _ret_raw.rename(columns={"PERIODO_BLOQUEO": "periodo"})

# Derivar academic_anio y academic_semester a partir del periodo
_ret_raw[["academic_anio", "academic_semester"]] = (
    _ret_raw["periodo"].str.extract(r"^(20\d{2})-([12])S$")
)

# Limpiar columnas numéricas antes de seleccionar
for _col in ["PAPA", "PROM_ACADEMICO", "PORCENTAJE_AVANCE"]:
    _ret_raw[_col] = _ret_raw[_col].replace({"": pd.NA, "nan": pd.NA})

df_ret = _ret_raw[[
    "ID_UNAL", "periodo", "academic_anio", "academic_semester",
    "COD_PLAN", "BLOQUEO", "PAPA", "PROM_ACADEMICO", "PORCENTAJE_AVANCE",
]].copy()

print(f"Retirados : {len(df_ret):>7} filas | {df_ret['periodo'].nunique()} periodos")


#%% =============================================================================
# 3. CARGAR APERTURA DESDE MATRICULADOS (para rellenar celdas vacías)
# =============================================================================

_mat_raw = pd.concat(
    [pd.read_csv(f, dtype=str, encoding="latin-1") for f in sorted(DIR_MATRICULADOS.glob("*.csv"))],
    ignore_index=True,
)

# Renombrar id_unal para que coincida con el resto del código
_mat_raw = _mat_raw.rename(columns={"id_unal": "ID_UNAL"})
_mat_raw["APERTURA"] = _mat_raw["APERTURA"].replace({"": pd.NA, "nan": pd.NA})


df_mat_apertura = (
    _mat_raw[["ID_UNAL", "COD_PLAN", "APERTURA"]]
    .dropna(subset=["APERTURA"])
    .drop_duplicates(subset=["ID_UNAL", "COD_PLAN"])
    .copy()
)

print(f"Matriculados apertura lookup : {len(df_mat_apertura)} pares únicos ID_UNAL-COD_PLAN")


#%% =============================================================================
# 4. DIAGNÓSTICO: DUPLICADOS EN LA LLAVE [ID_UNAL, periodo, COD_PLAN]
# =============================================================================

print(f"\n{'=' * 70}")
print("DIAGNÓSTICO DE DUPLICADOS EN LA LLAVE")
print(f"{'=' * 70}")


def diagnostico_duplicados(df, nombre, col_variacion=None):
    dup_mask = df.duplicated(subset=LLAVE, keep=False)
    n_filas  = dup_mask.sum()
    n_llaves = df[dup_mask].groupby(LLAVE).ngroups if n_filas else 0

    if n_filas == 0:
        print(f"  OK  {nombre}: llave única en todas las filas")
    else:
        print(f"  WARN  {nombre}: {n_llaves} llaves con duplicados ({n_filas} filas)")
        if col_variacion:
            n_varian = (
                df[dup_mask]
                .groupby(LLAVE)[col_variacion]
                .nunique()
                .gt(1)
                .sum()
            )
            n_iguales = n_llaves - n_varian
            print(f"    └─ llaves donde {col_variacion} varía entre duplicados : {n_varian}")
            print(f"    └─ llaves donde {col_variacion} es idéntico (duplicados exactos) : {n_iguales}")
    return dup_mask


dup_egr = diagnostico_duplicados(df_egr, "Egresados")
dup_ret = diagnostico_duplicados(df_ret, "Retirados", col_variacion="BLOQUEO")


#%% =============================================================================
# 5. DEDUPLICAR RETIRADOS: agregar BLOQUEO y consolidar columnas por llave
# =============================================================================

# Un estudiante puede tener múltiples causas de retiro en el mismo periodo/plan.
# BLOQUEO se concatena; el resto de columnas deben ser iguales para todos los
# duplicados, así que tomamos el primer valor no nulo.
df_ret_dedup = (
    df_ret
    .groupby(LLAVE + ["academic_anio", "academic_semester"], dropna=False)
    .agg(
        BLOQUEO           = ("BLOQUEO",           lambda x: " | ".join(x.dropna().astype(str).unique())),
        PAPA              = ("PAPA",              "first"),
        PROM_ACADEMICO    = ("PROM_ACADEMICO",    "first"),
        PORCENTAJE_AVANCE = ("PORCENTAJE_AVANCE", "first"),
    )
    .reset_index()
)

print(f"\nRetirados tras agregar BLOQUEO: {len(df_ret)} → {len(df_ret_dedup)} filas")


#%% =============================================================================
# 6. MERGE Y COLUMNAS BINARIAS
# =============================================================================

merged = pd.merge(
    df_egr,
    df_ret_dedup,
    on=LLAVE,
    how="outer",
    suffixes=("_egr", "_ret"),
    indicator=True,
)

merged["graduado"] = merged["_merge"].isin(["both", "left_only"]).astype(int)
merged["retirado"] = merged["_merge"].isin(["both", "right_only"]).astype(int)
merged = merged.drop(columns=["_merge"])

# El outer join duplica academic_anio y academic_semester; unificarlas en una sola
for _col in ["academic_anio", "academic_semester"]:
    _egr_col, _ret_col = _col + "_egr", _col + "_ret"
    if _egr_col in merged.columns:
        merged[_col] = merged[_egr_col].fillna(merged[_ret_col])
        merged = merged.drop(columns=[_egr_col, _ret_col])

print(f"\nMerge completo: {len(merged)} filas")
print(f"  graduado=1              : {merged['graduado'].sum()}")
print(f"  retirado=1              : {merged['retirado'].sum()}")
print(f"  graduado=1 y retirado=1 : {(merged['graduado'].astype(bool) & merged['retirado'].astype(bool)).sum()}")


#%% =============================================================================
# 7. ENRIQUECER APERTURA DESDE MATRICULADOS
# =============================================================================

n_vacias_antes = merged["APERTURA"].isna().sum()

merged = pd.merge(
    merged,
    df_mat_apertura.rename(columns={"APERTURA": "APERTURA_mat"}),
    on=["ID_UNAL", "COD_PLAN"],
    how="left",
)

merged["APERTURA"] = merged["APERTURA"].fillna(merged["APERTURA_mat"])
merged = merged.drop(columns=["APERTURA_mat"])

n_vacias_despues = merged["APERTURA"].isna().sum()
print(f"\nAPERTURA vacía antes de enriquecer : {n_vacias_antes}")
print(f"APERTURA vacía después de matriculados : {n_vacias_despues}")


#%% =============================================================================
# 8. CONSTRUIR PROM_GRADUADO_RETIRADO Y PORCENTAJE_AVANCE
# =============================================================================

# Para egresados: PROM_GRADUADO ya viene calculado (con sus propios fillna).
# Para retirados puros: se usa PAPA y, si está vacío, PROM_ACADEMICO.
# Para "ambos": PROM_GRADUADO no es nulo, así que prevalece el valor de egresados.
merged["PROM_GRADUADO_RETIRADO"] = (
    merged["PROM_GRADUADO"]
    .fillna(merged["PAPA"])
    .fillna(merged["PROM_ACADEMICO"])
)
merged = merged.drop(columns=["PROM_GRADUADO", "PAPA", "PROM_ACADEMICO"])

# Para egresados (incluye "ambos"): avance completo.
# Para retirados puros: porcentaje registrado en la base de retirados.
es_graduado  = merged["graduado"] == 1
es_solo_ret  = (merged["retirado"] == 1) & (merged["graduado"] == 0)

merged["porcentaje_avance"] = pd.NA
merged.loc[es_graduado, "porcentaje_avance"] = pd.NA
merged.loc[es_solo_ret, "porcentaje_avance"] = merged.loc[es_solo_ret, "PORCENTAJE_AVANCE"]
merged = merged.drop(columns=["PORCENTAJE_AVANCE"])


#%% =============================================================================
# 9. GUARDAR UN CSV POR PERIODO + RESUMEN
# =============================================================================

resumen = []

for periodo, grupo in merged.groupby("periodo", dropna=False):
    nombre = f"BASE_EGRESADOS_RETIRADOS_{periodo}.csv" if pd.notna(periodo) else "base_sin_periodo.csv"
    grupo.to_csv(DIR_OUTPUT / nombre, index=False, sep=";", encoding="utf-8-sig")
    resumen.append({
        "periodo":   periodo,
        "n_total":   len(grupo),
        "graduados": int(grupo["graduado"].sum()),
        "retirados": int(grupo["retirado"].sum()),
        "ambos":     int((grupo["graduado"].astype(bool) & grupo["retirado"].astype(bool)).sum()),
    })

df_res = pd.DataFrame(resumen)

ancho = 72
print(f"\n{'=' * ancho}")
print("RESUMEN POR PERIODO")
print(f"{'=' * ancho}")
print(f"  {'Periodo':<13} {'Total':>8} {'Graduados':>10} {'Retirados':>10} {'Ambos':>7}")
print(f"  {'─' * (ancho - 2)}")
for _, row in df_res.iterrows():
    print(f"  {str(row['periodo']):<13} {int(row['n_total']):>8} {int(row['graduados']):>10} "
          f"{int(row['retirados']):>10} {int(row['ambos']):>7}")
print(f"  {'─' * (ancho - 2)}")
tot = df_res[["n_total", "graduados", "retirados", "ambos"]].sum()
print(f"  {'TOTAL':<13} {int(tot['n_total']):>8} {int(tot['graduados']):>10} "
      f"{int(tot['retirados']):>10} {int(tot['ambos']):>7}")

print(f"\nArchivos guardados en: {DIR_OUTPUT}")


#%% =============================================================================
# 10. INSPECCIÓN: filas con graduado=1 y retirado=1
# =============================================================================

ambos = merged[merged["graduado"].astype(bool) & merged["retirado"].astype(bool)]

print(f"\n{'=' * 70}")
print(f"FILAS CON graduado=1 y retirado=1  ({len(ambos)} casos)")
print(f"{'=' * 70}")
print(ambos.to_string(index=False))


#%% =============================================================================
# 11. PORCENTAJE DE VACÍOS POR COLUMNA Y SEMESTRE
# =============================================================================

# Calcular conteo y % de nulos por columna para cada periodo
def resumen_nulos(g):
    n_total = len(g)
    n_nulos = g.isna().sum()
    pct     = (n_nulos / n_total * 100).round(1)
    return n_nulos.astype(str) + " (" + pct.astype(str) + "%)"

tabla_nulos = (
    merged
    .groupby("periodo", dropna=False)
    .apply(resumen_nulos)
    .drop(columns=["periodo"], errors="ignore")
)

# Fila de totales generales
n_nulos_total = merged.isna().sum()
pct_total     = (n_nulos_total / len(merged) * 100).round(1)
fila_total    = (n_nulos_total.astype(str) + " (" + pct_total.astype(str) + "%)")
fila_total.name = "TOTAL"

tabla_nulos = pd.concat([tabla_nulos, fila_total.to_frame().T])

# Mostrar solo las columnas que tienen al menos un valor vacío en algún periodo
columnas_con_nulos = merged.columns[merged.isna().any()].tolist()
tabla_nulos = tabla_nulos[columnas_con_nulos]

print(f"\n{'=' * 70}")
print("VALORES VACÍOS POR COLUMNA Y SEMESTRE  n (%)  — solo columnas con vacíos")
print(f"{'=' * 70}")
print(tabla_nulos.to_string())

# %%
