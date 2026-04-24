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

#%%
def normalizar_texto(serie: pd.Series, lower: bool = False) -> pd.Series:
    """Limpia espacios y reemplaza valores vacíos por NA."""
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
    """Carga la base de Retirados y normaliza nombres de columnas."""
    df = pd.read_excel(archivo, sheet_name=hoja)
    df.columns = [str(columna).strip() for columna in df.columns]

    for columna in df.columns:
        if df[columna].dtype == "object":
            df[columna] = normalizar_texto(df[columna])

    if "CORREO" in df.columns:
        df["CORREO"] = normalizar_texto(df["CORREO"], lower=True)

    return df


def resumir_estructura_general(df: pd.DataFrame) -> pd.DataFrame:
    """Resume la estructura general de la base."""
    return pd.DataFrame(
        [
            {
                "n_filas": len(df),
                "n_columnas": len(df.columns),
                "missings_totales": int(df.isna().sum().sum()),
                "duplicados_exactos": int(df.duplicated().sum()),
            }
        ]
    )


def resumir_missings_por_variable(df: pd.DataFrame) -> pd.DataFrame:
    """Resume missings por variable."""
    resumen = pd.DataFrame(
        {
            "variable": df.columns,
            "n_missing": df.isna().sum().values,
            "pct_missing": (df.isna().mean().values * 100).round(4),
        }
    )

    return resumen.sort_values(
        ["pct_missing", "variable"],
        ascending=[False, True],
    ).reset_index(drop=True)


def evaluar_llaves_tentativas(df: pd.DataFrame) -> pd.DataFrame:
    """Evalúa varias combinaciones de llave tentativa en Retirados."""
    combinaciones = {
        "CORREO": ["CORREO"],
        "CORREO+COD_PLAN": ["CORREO", "COD_PLAN"],
        "CORREO+PERIODO_BLOQUEO": ["CORREO", "PERIODO_BLOQUEO"],
        "CORREO+COD_PLAN+PERIODO_BLOQUEO": [
            "CORREO",
            "COD_PLAN",
            "PERIODO_BLOQUEO",
        ],
    }

    resultados = []

    for nombre, columnas in combinaciones.items():
        for columna in columnas:
            if columna not in df.columns:
                raise ValueError(f"Falta la columna {columna}")

        base = df.dropna(subset=columnas).copy()
        llave = base[columnas].astype(str).agg(" || ".join, axis=1)

        n_filas = len(base)
        n_unicas = llave.nunique()
        n_repetidas = int((llave.value_counts() > 1).sum())
        pct_unicidad = (n_unicas / n_filas * 100) if n_filas > 0 else None

        resultados.append(
            {
                "llave_probada": nombre,
                "filas_validas": n_filas,
                "combinaciones_unicas": n_unicas,
                "combinaciones_repetidas": n_repetidas,
                "pct_unicidad": (
                    round(pct_unicidad, 4)
                    if pct_unicidad is not None
                    else None
                ),
            }
        )

    return pd.DataFrame(resultados)


def analizar_duplicados_exactos(df: pd.DataFrame) -> tuple[int, int, pd.DataFrame]:
    """Analiza duplicados exactos de fila completa."""
    duplicados_mask = df.duplicated(keep=False)
    df_duplicados = df[duplicados_mask].copy()

    n_total = len(df)
    n_filas_duplicadas = len(df_duplicados)

    if not df_duplicados.empty:
        grupos = (
            df_duplicados.groupby(list(df.columns), dropna=False)
            .size()
            .reset_index(name="n_repeticiones")
            .sort_values("n_repeticiones", ascending=False)
        )
    else:
        grupos = pd.DataFrame()

    return n_total, n_filas_duplicadas, grupos


def construir_base_llave(
    df: pd.DataFrame,
    llave_cols: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Construye base válida y llaves repetidas para una llave dada."""
    for columna in llave_cols:
        if columna not in df.columns:
            raise ValueError(f"Falta la columna {columna}")

    base = df.dropna(subset=llave_cols).copy()
    base["LLAVE"] = base[llave_cols].astype(str).agg(" || ".join, axis=1)

    rep_keys = (
        base.groupby("LLAVE")
        .size()
        .reset_index(name="n_filas")
    )
    rep_keys = rep_keys[rep_keys["n_filas"] > 1].copy()

    return base, rep_keys


def analizar_repetidos_dentro_de_llave(
    df: pd.DataFrame,
    llave_cols: list[str],
) -> pd.DataFrame:
    """
    Analiza si las llaves repetidas corresponden a duplicados exactos
    o a filas distintas.
    """
    base, rep_keys = construir_base_llave(df, llave_cols)
    detalle = base[base["LLAVE"].isin(rep_keys["LLAVE"])].copy()

    resultados = []

    for llave, grupo in detalle.groupby("LLAVE"):
        n_filas = len(grupo)
        n_filas_distintas = grupo.drop(columns=["LLAVE"]).drop_duplicates().shape[0]

        resultados.append(
            {
                "LLAVE": llave,
                "n_filas": n_filas,
                "n_filas_distintas": n_filas_distintas,
                "es_duplicado_exacto": n_filas_distintas == 1,
            }
        )

    return pd.DataFrame(resultados)


def analizar_variacion_en_llaves_repetidas(
    df: pd.DataFrame,
    llave_cols: list[str],
) -> pd.DataFrame:
    """
    Para las llaves repetidas, identifica en cuántas llaves varía cada columna.
    """
    base, rep_keys = construir_base_llave(df, llave_cols)
    detalle = base[base["LLAVE"].isin(rep_keys["LLAVE"])].copy()

    variacion_cols = []

    for columna in df.columns:
        if columna in llave_cols:
            continue

        tmp = detalle.groupby("LLAVE")[columna].nunique(dropna=False)
        n_llaves_que_varian = int((tmp > 1).sum())

        variacion_cols.append(
            {
                "columna": columna,
                "llaves_repetidas_donde_varia": n_llaves_que_varian,
            }
        )

    return pd.DataFrame(variacion_cols).sort_values(
        "llaves_repetidas_donde_varia",
        ascending=False,
    )


def evaluar_llave_final(
    df: pd.DataFrame,
    llave_cols: list[str],
) -> tuple[int, int, pd.DataFrame]:
    """Evalúa la llave final tentativa."""
    base, rep_keys = construir_base_llave(df, llave_cols)
    n_total = len(base)
    n_unicas = base["LLAVE"].nunique()

    return n_total, n_unicas, rep_keys


def main() -> None:
    """Ejecuta el inventario de Retirados."""
    if not ARCHIVO_RETIRADOS.exists():
        raise FileNotFoundError(
            f"No existe el archivo de Retirados: {ARCHIVO_RETIRADOS}"
        )

    df = cargar_retirados()

    print("=" * 70)
    print("INVENTARIO DE RETIRADOS")
    print("=" * 70)
    print(f"Archivo analizado: {ARCHIVO_RETIRADOS}")
    print()

    print("=" * 70)
    print("ESTRUCTURA GENERAL")
    print("=" * 70)
    estructura_df = resumir_estructura_general(df)
    print(estructura_df.to_string(index=False))
    print()

    print("=" * 70)
    print("MISSINGS POR VARIABLE")
    print("=" * 70)
    missings_df = resumir_missings_por_variable(df)
    print(missings_df.head(30).to_string(index=False))
    print()

    print("=" * 70)
    print("PRUEBA DE LLAVES TENTATIVAS - RETIRADOS")
    print("=" * 70)
    llaves_df = evaluar_llaves_tentativas(df)
    print(llaves_df.to_string(index=False))
    print()

    print("=" * 70)
    print("DUPLICADOS EXACTOS DE FILA COMPLETA - RETIRADOS")
    print("=" * 70)
    n_total, n_filas_duplicadas, grupos_duplicados = analizar_duplicados_exactos(df)
    print(f"Total filas: {n_total}")
    print(f"Filas involucradas en duplicados exactos: {n_filas_duplicadas}")
    print(f"Grupos únicos de filas idénticas: {len(grupos_duplicados)}")

    if not grupos_duplicados.empty:
        print("\nTop 20 grupos duplicados exactos:")
        print(
            grupos_duplicados[["n_repeticiones"]]
            .head(20)
            .to_string(index=False)
        )
    print()

    print("=" * 70)
    print("DIAGNÓSTICO DE REPETIDOS DENTRO DE CORREO+COD_PLAN+PERIODO_BLOQUEO")
    print("=" * 70)
    repetidos_df = analizar_repetidos_dentro_de_llave(
        df,
        ["CORREO", "COD_PLAN", "PERIODO_BLOQUEO"],
    )

    n_llaves_rep = len(repetidos_df)
    n_llaves_dup_exacto = int(repetidos_df["es_duplicado_exacto"].sum())
    n_llaves_con_diferencias = int((~repetidos_df["es_duplicado_exacto"]).sum())

    print(f"Llaves repetidas analizadas: {n_llaves_rep}")
    print(f"Llaves cuyos repetidos son filas exactas: {n_llaves_dup_exacto}")
    print(f"Llaves repetidas con diferencias entre filas: {n_llaves_con_diferencias}")

    if not repetidos_df.empty:
        print("\nTop 20 llaves repetidas:")
        print(repetidos_df.head(20).to_string(index=False))
    print()

    print("=" * 70)
    print("COLUMNAS QUE MÁS DIFERENCIAN REPETIDOS EN RETIRADOS")
    print("=" * 70)
    variacion_df = analizar_variacion_en_llaves_repetidas(
        df,
        ["CORREO", "COD_PLAN", "PERIODO_BLOQUEO"],
    )
    print(variacion_df.head(20).to_string(index=False))
    print()

    print("=" * 75)
    print("PRUEBA FINAL DE LLAVE TENTATIVA - RETIRADOS")
    print("=" * 75)
    n_total_final, n_unicas_final, rep_final = evaluar_llave_final(
        df,
        LLAVE_FINAL_COLS,
    )
    pct_unicidad = (
        n_unicas_final / n_total_final * 100 if n_total_final > 0 else 0
    )

    print(f"Filas válidas: {n_total_final}")
    print(f"Combinaciones únicas: {n_unicas_final}")
    print(f"Combinaciones repetidas: {len(rep_final)}")
    print(f"Porcentaje de unicidad: {pct_unicidad:.4f}%")

    if not rep_final.empty:
        print("\nTop 20 llaves repetidas:")
        print(rep_final.head(20).to_string(index=False))
    else:
        print("\nNo hay llaves repetidas. La combinación funciona como llave única.")

#%%
if __name__ == "__main__":
    main()
# %%
