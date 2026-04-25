#%%
from pathlib import Path
import pandas as pd
from config import DIR_DATOS


HOJA_RETIRADOS = "Sheet2"
ARCHIVO_RETIRADOS = (
    DIR_DATOS
    / "DatosOriginales"
    / "Retirados"
    / "Retirados_desde_2009.xlsx"
)

LLAVE_FINAL_COLS = ["CORREO", "COD_PLAN", "PERIODO_BLOQUEO", "COD_BLOQUEO"]


#%% =============================================================================
# 1. CARGA Y LIMPIEZA BASE
# =============================================================================

def normalizar_texto(serie: pd.Series, lower: bool = False) -> pd.Series:
    serie = serie.astype(str).str.strip()

    if lower:
        serie = serie.str.lower()

    serie = serie.replace(
        {
            "": pd.NA,
            "nan": pd.NA,
            "none": pd.NA,
            "None": pd.NA,
            "NaT": pd.NA,
            "nat": pd.NA,
        }
    )

    return serie


def cargar_retirados(
    archivo: Path = ARCHIVO_RETIRADOS,
    hoja: str = HOJA_RETIRADOS,
) -> pd.DataFrame:
    df = pd.read_excel(archivo, sheet_name=hoja)
    df.columns = [str(c).strip() for c in df.columns]

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = normalizar_texto(df[col])

    if "CORREO" in df.columns:
        df["CORREO"] = normalizar_texto(df["CORREO"], lower=True)

    return df


# OUTPUT BLOQUE
print("Archivo existe:", ARCHIVO_RETIRADOS.exists())

df = cargar_retirados()

print("Dimensiones:", df.shape)
print("Columnas:", len(df.columns))


#%% =============================================================================
# 2. ESTRUCTURA GENERAL
# =============================================================================

def resumir_estructura_general(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [{
            "n_filas": len(df),
            "n_columnas": len(df.columns),
            "missings_totales": int(df.isna().sum().sum()),
            "duplicados_exactos": int(df.duplicated().sum()),
        }]
    )


estructura_df = resumir_estructura_general(df)

print("Estructura general:")
print(estructura_df.to_string(index=False))


#%% =============================================================================
# 3. MISSINGS
# =============================================================================

def resumir_missings(df: pd.DataFrame) -> pd.DataFrame:
    return (
        pd.DataFrame({
            "variable": df.columns,
            "n_missing": df.isna().sum().values,
            "pct_missing": (df.isna().mean().values * 100).round(4),
        })
        .sort_values(["pct_missing", "variable"], ascending=[False, True])
        .reset_index(drop=True)
    )


missings_df = resumir_missings(df)

print("Missings principales:")
print(missings_df.head(30).to_string(index=False))


#%% =============================================================================
# 4. PRUEBA DE LLAVES
# =============================================================================

def evaluar_llaves_tentativas(df: pd.DataFrame) -> pd.DataFrame:
    combinaciones = {
        "CORREO": ["CORREO"],
        "CORREO+COD_PLAN": ["CORREO", "COD_PLAN"],
        "CORREO+PERIODO_BLOQUEO": ["CORREO", "PERIODO_BLOQUEO"],
        "CORREO+COD_PLAN+PERIODO_BLOQUEO": [
            "CORREO", "COD_PLAN", "PERIODO_BLOQUEO"
        ],
    }

    resultados = []

    for nombre, cols in combinaciones.items():
        base = df.dropna(subset=cols).copy()
        llave = base[cols].astype(str).agg(" || ".join, axis=1)

        n = len(base)
        n_unicas = llave.nunique()

        resultados.append({
            "llave": nombre,
            "filas_validas": n,
            "pct_unicidad": round((n_unicas / n * 100), 4) if n else None,
        })

    return pd.DataFrame(resultados)


llaves_df = evaluar_llaves_tentativas(df)

print("Evaluación de llaves:")
print(llaves_df.to_string(index=False))


#%% =============================================================================
# 5. DUPLICADOS EXACTOS
# =============================================================================

def analizar_duplicados_exactos(df: pd.DataFrame):
    mask = df.duplicated(keep=False)
    duplicados = df[mask]

    return len(df), len(duplicados)


n_total, n_dup = analizar_duplicados_exactos(df)

print("Duplicados exactos:")
print(f"Total filas: {n_total}")
print(f"Filas duplicadas: {n_dup}")


#%% =============================================================================
# 6. ANÁLISIS DE REPETIDOS SIN COD_BLOQUEO
# =============================================================================

def construir_base_llave(df, cols):
    base = df.dropna(subset=cols).copy()
    base["LLAVE"] = base[cols].astype(str).agg(" || ".join, axis=1)
    return base


def analizar_variacion(df, cols):
    base = construir_base_llave(df, cols)
    rep = base[base["LLAVE"].duplicated(keep=False)]

    resultados = []

    for col in df.columns:
        if col in cols:
            continue

        n = (rep.groupby("LLAVE")[col].nunique(dropna=False) > 1).sum()

        resultados.append({
            "columna": col,
            "llaves_donde_varia": int(n)
        })

    return pd.DataFrame(resultados).sort_values(
        "llaves_donde_varia",
        ascending=False
    )


variacion_df = analizar_variacion(
    df,
    ["CORREO", "COD_PLAN", "PERIODO_BLOQUEO"]
)

print("Columnas que explican repetidos:")
print(variacion_df.head(20).to_string(index=False))


#%% =============================================================================
# 7. VALIDACIÓN DE LLAVE FINAL
# =============================================================================

def evaluar_llave_final(df, cols):
    base = construir_base_llave(df, cols)
    n_total = len(base)
    n_unicas = base["LLAVE"].nunique()

    return n_total, n_unicas


n_total_final, n_unicas_final = evaluar_llave_final(df, LLAVE_FINAL_COLS)

pct = n_unicas_final / n_total_final * 100

print("Llave final:")
print(f"Filas válidas: {n_total_final}")
print(f"Únicas: {n_unicas_final}")
print(f"Unicidad: {pct:.4f}%")