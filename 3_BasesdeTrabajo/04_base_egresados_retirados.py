#%% =============================================================================
# 0. SETUP
# =============================================================================

import pandas as pd

from config import DIR_DATOS

DIR_EGRESADOS  = DIR_DATOS / "DatosArmonizados" / "archivos_limpios_egresados"
DIR_RETIRADOS  = DIR_DATOS / "DatosArmonizados" / "retirados_por_periodo" / "retirados_por_periodo_limpios"
DIR_OUTPUT     = DIR_DATOS / "DatosArmonizados" / "base_egresados_retirados"

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

df_ret = _ret_raw[[
    "ID_UNAL", "periodo", "academic_anio", "academic_semester",
    "COD_PLAN", "BLOQUEO",
]].copy()

print(f"Retirados : {len(df_ret):>7} filas | {df_ret['periodo'].nunique()} periodos")


#%% =============================================================================
# 3. DIAGNÓSTICO: DUPLICADOS EN LA LLAVE [ID_UNAL, periodo, COD_PLAN]
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
# 4. DEDUPLICAR RETIRADOS: agregar BLOQUEO por llave
# =============================================================================

# Un estudiante puede tener múltiples causas de retiro en el mismo periodo/plan.
# Se concatenan en una sola celda separada por " | ".
df_ret_dedup = (
    df_ret
    .groupby(LLAVE + ["academic_anio", "academic_semester"], dropna=False)["BLOQUEO"]
    .agg(lambda x: " | ".join(x.dropna().astype(str).unique()))
    .reset_index()
)

print(f"\nRetirados tras agregar BLOQUEO: {len(df_ret)} → {len(df_ret_dedup)} filas")


#%% =============================================================================
# 5. MERGE Y COLUMNAS BINARIAS
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
print(f"  graduado=1          : {merged['graduado'].sum()}")
print(f"  retirado=1          : {merged['retirado'].sum()}")
print(f"  graduado=1 y retirado=1 : {(merged['graduado'].astype(bool) & merged['retirado'].astype(bool)).sum()}")


#%% =============================================================================
# 6. GUARDAR UN CSV POR PERIODO + RESUMEN
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
# 7. INSPECCIÓN: filas con graduado=1 y retirado=1
# =============================================================================

ambos = merged[merged["graduado"].astype(bool) & merged["retirado"].astype(bool)]

print(f"\n{'=' * 70}")
print(f"FILAS CON graduado=1 y retirado=1  ({len(ambos)} casos)")
print(f"{'=' * 70}")
print(ambos.to_string(index=False))


#%% =============================================================================
# 8. VALIDACIÓN: egresados sin PROM_GRADUADO
# =============================================================================

egr_sin_nota = merged[
    (merged["graduado"] == 1) & merged["PROM_GRADUADO"].isna()
]

total_egr = int(merged["graduado"].sum())
n_sin_nota = len(egr_sin_nota)

print(f"\n{'=' * 70}")
print("VALIDACIÓN: PROM_GRADUADO en egresados")
print(f"{'=' * 70}")
print(f"  Total egresados (graduado=1) : {total_egr}")
print(f"  Con PROM_GRADUADO vacío      : {n_sin_nota}  ({n_sin_nota / total_egr * 100:.1f}%)")

if n_sin_nota > 0:
    por_periodo = (
        egr_sin_nota.groupby("periodo")
        .size()
        .rename("sin_nota")
        .reset_index()
        .sort_values("periodo")
    )
    print(f"\n  Distribución por periodo:")
    for _, row in por_periodo.iterrows():
        print(f"    {row['periodo']}: {int(row['sin_nota'])} sin nota")
