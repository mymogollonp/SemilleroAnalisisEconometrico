#%%
"""
Inventario de Cancelaciones — UNAL FCE
=======================================
RA: Maria Jose Cadena
Script: 01_Inventario_Cancelaciones_MJC.py
Proyecto: Semillero de Análisis Econométrico

Qué hace este script
--------------------
1.  Lista y carga todos los archivos de DatosOriginales/Cancelaciones/.
2.  Reporta estructura general (filas, columnas, missings, duplicados) por archivo.
3.  Compara encabezados entre semestres (detecta renombrados de variables).
4.  Reporta missings por variable × semestre en tabla larga y tabla cruzada.
5.  Muestra duplicados exactos por archivo y sobre el panel apilado.
6.  Evalúa candidatos a llave única: CORREO_INSTITUCIONAL, DOCUMENTO y combinaciones.
7.  Diagnostica repetidos dentro de la llave elegida y qué columnas los diferencian.
8.  Muestra ejemplos de valores de la variable de período/fecha de cancelación.
9.  Confirma si el primer archivo disponible es Cancelaciones_2009-2S.

Reglas del proyecto aplicadas
------------------------------
R5: todas las rutas vienen de config.py (DIR_DATOS). Sin paths hardcodeados.
R6: solo lectura sobre DatosOriginales/.
R3: no genera archivos CSV ni XLSX (solo imprime en consola).
"""

import sys
from pathlib import Path
import pandas as pd

# Sube un nivel desde 1_LimpiezaDatos/ hasta la raíz del proyecto
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import DIR_DATOS

# ---------------------------------------------------------------------------
# Constantes — ajustar si cambian los nombres reales de columnas
# ---------------------------------------------------------------------------
CARPETA_CANCELACIONES = DIR_DATOS / "DatosOriginales" / "Cancelaciones"

# Columnas de identificación personal observadas en el dataset
COL_CORREO    = "CORREO_INSTITUCIONAL"
COL_DOCUMENTO = "DOCUMENTO"
COL_PERIODO   = "PERIODO"
COL_PLAN      = "COD_PLAN"

# Archivos cuya primera hoja no contiene los datos reales.
# Cancelaciones_2024-2S: Sheet1 tiene solo 6 cols; datos reales en Sheet2.
HOJAS_ESPECIALES: dict[str, str] = {
    "Cancelaciones_2024-2S": "Sheet2",
}

# Candidatos a llave única que se evaluarán.
# Se comparan variantes con CORREO vs. DOCUMENTO para decidir cuál usar.
LLAVES_CANDIDATAS: dict[str, list[str]] = {
    COL_CORREO:                                      [COL_CORREO],
    COL_DOCUMENTO:                                   [COL_DOCUMENTO],
    f"{COL_CORREO}+{COL_PERIODO}":                   [COL_CORREO,    COL_PERIODO],
    f"{COL_DOCUMENTO}+{COL_PERIODO}":                [COL_DOCUMENTO, COL_PERIODO],
    f"{COL_CORREO}+{COL_PLAN}+{COL_PERIODO}":        [COL_CORREO,    COL_PLAN, COL_PERIODO],
    f"{COL_DOCUMENTO}+{COL_PLAN}+{COL_PERIODO}":     [COL_DOCUMENTO, COL_PLAN, COL_PERIODO],
    f"{COL_CORREO}+{COL_PLAN}+{COL_PERIODO}+COD_ASIGNATURA": [
        COL_CORREO, COL_PLAN, COL_PERIODO, "COD_ASIGNATURA"
    ],
}

# Llave final tentativa (actualizar con el resultado del inventario)
LLAVE_FINAL_COLS = [COL_CORREO, COL_PERIODO, COL_PLAN]

# Llave para el diagnóstico de repetidos (un nivel menos que la final)
LLAVE_DIAG = [COL_CORREO, COL_PERIODO]


# ---------------------------------------------------------------------------
# Utilidades generales
# ---------------------------------------------------------------------------
def normalizar_texto(serie: pd.Series, lower: bool = False) -> pd.Series:
    """Limpia espacios y reemplaza valores vacíos/nulos por pd.NA."""
    serie = serie.astype(str).str.strip()
    if lower:
        serie = serie.str.lower()
    return serie.replace(
        {"": pd.NA, "nan": pd.NA, "none": pd.NA,
         "None": pd.NA, "NaT": pd.NA, "nat": pd.NA}
    )


# ---------------------------------------------------------------------------
# Carga de archivos
# ---------------------------------------------------------------------------
def listar_archivos(carpeta: Path) -> list[Path]:
    """Lista todos los .xlsx de la carpeta, ordenados por nombre."""
    archivos = sorted(carpeta.glob("*.xlsx"))
    if not archivos:
        raise FileNotFoundError(f"No se encontraron archivos .xlsx en: {carpeta}")
    return archivos


def cargar_archivo(archivo: Path) -> pd.DataFrame:
    """
    Carga un Excel. Usa hoja especial si está en HOJAS_ESPECIALES,
    de lo contrario la primera hoja. Normaliza columnas y texto.
    """
    hoja = HOJAS_ESPECIALES.get(archivo.stem, 0)
    df = pd.read_excel(archivo, sheet_name=hoja)
    df.columns = [str(c).strip().upper() for c in df.columns]

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = normalizar_texto(df[col])

    if COL_CORREO in df.columns:
        df[COL_CORREO] = normalizar_texto(df[COL_CORREO], lower=True)

    df["_ARCHIVO"] = archivo.stem
    return df


def cargar_todos(carpeta: Path) -> dict[str, pd.DataFrame]:
    """Carga todos los archivos; avisa cuando usa hoja especial."""
    archivos = listar_archivos(carpeta)
    resultado = {}
    for archivo in archivos:
        if archivo.stem in HOJAS_ESPECIALES:
            hoja = HOJAS_ESPECIALES[archivo.stem]
            print(f"  [HOJA ESPECIAL] {archivo.stem}: leyendo hoja '{hoja}'")
        resultado[archivo.stem] = cargar_archivo(archivo)
    return resultado


# ---------------------------------------------------------------------------
# 1. Estructura general por archivo
# ---------------------------------------------------------------------------
def resumir_estructura_por_archivo(dfs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Una fila por archivo: filas, columnas, missings totales, duplicados exactos."""
    filas = []
    for nombre, df in dfs.items():
        cols = [c for c in df.columns if not c.startswith("_")]
        filas.append(
            {
                "archivo": nombre,
                "n_filas": len(df),
                "n_columnas": len(cols),
                "missings_totales": int(df[cols].isna().sum().sum()),
                "duplicados_exactos": int(df[cols].duplicated().sum()),
            }
        )
    return pd.DataFrame(filas)


# ---------------------------------------------------------------------------
# 2. Tipos de dato por variable y archivo
# ---------------------------------------------------------------------------
def resumir_tipos_por_archivo(dfs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Para cada (archivo, variable) reporta el dtype de pandas."""
    filas = []
    for nombre, df in dfs.items():
        for col in df.columns:
            if not col.startswith("_"):
                filas.append(
                    {"archivo": nombre, "variable": col, "dtype": str(df[col].dtype)}
                )
    return pd.DataFrame(filas)


# ---------------------------------------------------------------------------
# 3. Consistencia de columnas entre semestres
# ---------------------------------------------------------------------------
def resumir_consistencia_columnas(dfs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Por cada variable indica en cuántos archivos aparece y en cuáles no.
    Ordena primero las más inconsistentes.
    """
    nombres = sorted(
        {c for df in dfs.values() for c in df.columns if not c.startswith("_")}
    )
    archivos = list(dfs.keys())
    filas = []
    for col in nombres:
        ausente_en = [a for a in archivos if col not in dfs[a].columns]
        filas.append(
            {
                "variable": col,
                "n_archivos_presente": len(archivos) - len(ausente_en),
                "n_archivos_ausente": len(ausente_en),
                "ausente_en": "; ".join(ausente_en) if ausente_en else "",
            }
        )
    return (
        pd.DataFrame(filas)
        .sort_values(["n_archivos_ausente", "variable"], ascending=[False, True])
        .reset_index(drop=True)
    )


# ---------------------------------------------------------------------------
# 4. Missings por variable × semestre
# ---------------------------------------------------------------------------
def resumir_missings_por_archivo(dfs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    DataFrame largo (archivo, variable, n_missing, pct_missing).
    Incluye todas las combinaciones, incluso las sin missings.
    """
    filas = []
    for nombre, df in dfs.items():
        cols = [c for c in df.columns if not c.startswith("_")]
        for col in cols:
            filas.append(
                {
                    "archivo": nombre,
                    "variable": col,
                    "n_missing": int(df[col].isna().sum()),
                    "pct_missing": round(df[col].isna().mean() * 100, 4),
                }
            )
    return pd.DataFrame(filas)


def pivotear_missings(missings_df: pd.DataFrame) -> pd.DataFrame:
    """Tabla cruzada variable × semestre con pct_missing como valores."""
    return missings_df.pivot_table(
        index="variable",
        columns="archivo",
        values="pct_missing",
        fill_value=0.0,
    )


# ---------------------------------------------------------------------------
# 5. Duplicados exactos
# ---------------------------------------------------------------------------
def analizar_duplicados_exactos(
    df: pd.DataFrame,
) -> tuple[int, int, pd.DataFrame]:
    """Duplicados de fila completa ignorando la columna _ARCHIVO."""
    cols = [c for c in df.columns if not c.startswith("_")]
    mask = df[cols].duplicated(keep=False)
    df_dup = df[mask].copy()
    n_total = len(df)
    n_dup = len(df_dup)

    if not df_dup.empty:
        grupos = (
            df_dup[cols]
            .groupby(cols, dropna=False)
            .size()
            .reset_index(name="n_repeticiones")
            .sort_values("n_repeticiones", ascending=False)
        )
    else:
        grupos = pd.DataFrame()

    return n_total, n_dup, grupos


def duplicados_por_archivo(dfs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Tabla resumen de duplicados exactos por archivo."""
    filas = []
    for nombre, df in dfs.items():
        n_total, n_dup, _ = analizar_duplicados_exactos(df)
        filas.append(
            {
                "archivo": nombre,
                "n_filas": n_total,
                "n_filas_duplicadas": n_dup,
                "pct_duplicadas": round(n_dup / n_total * 100, 4) if n_total else 0,
            }
        )
    return pd.DataFrame(filas)


# ---------------------------------------------------------------------------
# 6. Análisis de llaves
# ---------------------------------------------------------------------------
def construir_base_llave(
    df: pd.DataFrame,
    llave_cols: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Filtra filas con llave completa y construye columna LLAVE."""
    faltantes = [c for c in llave_cols if c not in df.columns]
    if faltantes:
        raise ValueError(f"Columnas ausentes en el DataFrame: {faltantes}")

    base = df.dropna(subset=llave_cols).copy()
    base["LLAVE"] = base[llave_cols].astype(str).agg(" || ".join, axis=1)

    rep_keys = (
        base.groupby("LLAVE").size().reset_index(name="n_filas")
    )
    rep_keys = rep_keys[rep_keys["n_filas"] > 1].copy()
    return base, rep_keys


def evaluar_llaves_candidatas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Evalúa todas las combinaciones de LLAVES_CANDIDATAS.
    Compara CORREO_INSTITUCIONAL vs. DOCUMENTO para decidir cuál usar.
    """
    resultados = []
    for nombre, columnas in LLAVES_CANDIDATAS.items():
        ausentes = [c for c in columnas if c not in df.columns]
        if ausentes:
            resultados.append(
                {
                    "llave_probada": nombre,
                    "filas_validas": None,
                    "combinaciones_unicas": None,
                    "combinaciones_repetidas": None,
                    "pct_unicidad": None,
                    "nota": f"Columna ausente: {ausentes}",
                }
            )
            continue

        base = df.dropna(subset=columnas).copy()
        llave = base[columnas].astype(str).agg(" || ".join, axis=1)
        n_filas = len(base)
        n_unicas = llave.nunique()
        n_repetidas = int((llave.value_counts() > 1).sum())
        pct = round(n_unicas / n_filas * 100, 4) if n_filas else None

        resultados.append(
            {
                "llave_probada": nombre,
                "filas_validas": n_filas,
                "combinaciones_unicas": n_unicas,
                "combinaciones_repetidas": n_repetidas,
                "pct_unicidad": pct,
                "nota": "",
            }
        )
    return pd.DataFrame(resultados)


def analizar_repetidos_dentro_de_llave(
    df: pd.DataFrame,
    llave_cols: list[str],
) -> pd.DataFrame:
    """
    Para cada llave repetida indica si las filas son idénticas
    (duplicado exacto) o distintas (conflicto real de datos).
    """
    base, rep_keys = construir_base_llave(df, llave_cols)
    detalle = base[base["LLAVE"].isin(rep_keys["LLAVE"])].copy()
    cols_sin_llave = [
        c for c in df.columns if c not in llave_cols and not c.startswith("_")
    ]
    resultados = []
    for llave, grupo in detalle.groupby("LLAVE"):
        n_filas = len(grupo)
        n_distintas = grupo[cols_sin_llave].drop_duplicates().shape[0]
        resultados.append(
            {
                "LLAVE": llave,
                "n_filas": n_filas,
                "n_filas_distintas": n_distintas,
                "es_duplicado_exacto": n_distintas == 1,
            }
        )
    return pd.DataFrame(resultados)


def analizar_variacion_en_llaves_repetidas(
    df: pd.DataFrame,
    llave_cols: list[str],
) -> pd.DataFrame:
    """Indica en qué columnas varían los registros con llave repetida."""
    base, rep_keys = construir_base_llave(df, llave_cols)
    detalle = base[base["LLAVE"].isin(rep_keys["LLAVE"])].copy()
    variacion = []
    for col in df.columns:
        if col in llave_cols or col.startswith("_"):
            continue
        tmp = detalle.groupby("LLAVE")[col].nunique(dropna=False)
        variacion.append(
            {"columna": col, "llaves_repetidas_donde_varia": int((tmp > 1).sum())}
        )
    return (
        pd.DataFrame(variacion)
        .sort_values("llaves_repetidas_donde_varia", ascending=False)
        .reset_index(drop=True)
    )


def evaluar_llave_final(
    df: pd.DataFrame,
    llave_cols: list[str],
) -> tuple[int, int, pd.DataFrame]:
    """Evalúa la llave final definida en LLAVE_FINAL_COLS."""
    base, rep_keys = construir_base_llave(df, llave_cols)
    return len(base), base["LLAVE"].nunique(), rep_keys


# ---------------------------------------------------------------------------
# 7. Ejemplos de valores del período de cancelación
# ---------------------------------------------------------------------------
def mostrar_ejemplos_periodo(
    dfs: dict[str, pd.DataFrame],
    col_periodo: str = COL_PERIODO,
    n: int = 5,
) -> None:
    """
    Por cada archivo imprime ejemplos reales de la variable de período.
    Permite ver si el formato cambia entre semestres.
    """
    print(f"  {'ARCHIVO':<40} EJEMPLOS DE VALORES")
    print("  " + "-" * 70)
    for nombre, df in dfs.items():
        if col_periodo not in df.columns:
            print(f"  {nombre:<40} [columna ausente]")
            continue
        ejemplos = df[col_periodo].dropna().astype(str).unique()[:n].tolist()
        print(f"  {nombre:<40} {ejemplos}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    """Ejecuta el inventario completo de Cancelaciones."""
    if not CARPETA_CANCELACIONES.exists():
        raise FileNotFoundError(
            f"No existe la carpeta de Cancelaciones: {CARPETA_CANCELACIONES}"
        )

    print("=" * 75)
    print("INVENTARIO DE CANCELACIONES — UNAL FCE")
    print("=" * 75)
    print(f"Carpeta: {CARPETA_CANCELACIONES}")
    print()

    # Carga ----------------------------------------------------------------
    dfs = cargar_todos(CARPETA_CANCELACIONES)
    archivos = list(dfs.keys())

    print(f"\nTotal archivos cargados: {len(archivos)}")
    for a in archivos:
        print(f"  · {a}")

    primer   = archivos[0] if archivos else "(ninguno)"
    esperado = "Cancelaciones_2009-2S"
    flag     = "OK" if primer == esperado else "REVISAR — se esperaba " + esperado
    print(f"\nPrimer archivo disponible: {primer}  [{flag}]")
    print()

    # -----------------------------------------------------------------------
    # 1. Estructura por archivo
    # -----------------------------------------------------------------------
    print("=" * 75)
    print("1. ESTRUCTURA POR ARCHIVO")
    print("=" * 75)
    estructura_df = resumir_estructura_por_archivo(dfs)
    print(estructura_df.to_string(index=False))
    print()

    # -----------------------------------------------------------------------
    # 2. Tipos de dato
    # -----------------------------------------------------------------------
    print("=" * 75)
    print("2. TIPOS DE DATO POR VARIABLE Y ARCHIVO (tabla cruzada)")
    print("=" * 75)
    tipos_df    = resumir_tipos_por_archivo(dfs)
    tipos_pivot = tipos_df.pivot_table(
        index="variable", columns="archivo", values="dtype", aggfunc="first"
    )
    print(tipos_pivot.to_string())
    print()

    # -----------------------------------------------------------------------
    # 3. Consistencia de columnas entre semestres
    # -----------------------------------------------------------------------
    print("=" * 75)
    print("3. CONSISTENCIA DE NOMBRES DE VARIABLES ENTRE SEMESTRES")
    print("=" * 75)
    consistencia_df   = resumir_consistencia_columnas(dfs)
    siempre_presentes = consistencia_df[consistencia_df["n_archivos_ausente"] == 0]
    a_veces_ausentes  = consistencia_df[consistencia_df["n_archivos_ausente"] >  0]

    print(f"Variables presentes en TODOS los archivos ({len(siempre_presentes)}):")
    print(
        siempre_presentes[["variable", "n_archivos_presente"]]
        .to_string(index=False)
    )
    print()
    if not a_veces_ausentes.empty:
        print(f"Variables ausentes en al menos un archivo ({len(a_veces_ausentes)}):")
        print(a_veces_ausentes.to_string(index=False))
    else:
        print("Todas las variables son consistentes entre semestres.")
    print()

    # -----------------------------------------------------------------------
    # 4. Missings por variable × semestre
    # -----------------------------------------------------------------------
    print("=" * 75)
    print("4. MISSINGS POR VARIABLE × SEMESTRE")
    print("=" * 75)
    missings_df = resumir_missings_por_archivo(dfs)

    print("4a. Detalle largo — solo variables con al menos un missing:")
    missings_con_problema = (
        missings_df[missings_df["n_missing"] > 0]
        .sort_values(["variable", "archivo"])
        .reset_index(drop=True)
    )
    if missings_con_problema.empty:
        print("  Sin missings en ningún archivo.")
    else:
        print(missings_con_problema.to_string(index=False))
    print()

    print("4b. Tabla cruzada pct_missing  (variable × semestre):")
    pivot_missings      = pivotear_missings(missings_df)
    pivot_con_problema  = pivot_missings[(pivot_missings > 0).any(axis=1)]
    if pivot_con_problema.empty:
        print("  Sin missings en ningún archivo.")
    else:
        print(pivot_con_problema.to_string())
    print()

    # -----------------------------------------------------------------------
    # 5. Duplicados exactos
    # -----------------------------------------------------------------------
    print("=" * 75)
    print("5. DUPLICADOS EXACTOS")
    print("=" * 75)

    print("5a. Por archivo:")
    print(duplicados_por_archivo(dfs).to_string(index=False))
    print()

    df_panel = pd.concat(dfs.values(), ignore_index=True)

    print("5b. Panel apilado completo:")
    n_total, n_dup, grupos_dup = analizar_duplicados_exactos(df_panel)
    print(f"  Total filas:                  {n_total}")
    print(f"  Filas en duplicados exactos:  {n_dup}")
    print(f"  Grupos únicos duplicados:     {len(grupos_dup)}")
    if not grupos_dup.empty:
        print("\n  Top 20 grupos duplicados exactos:")
        print(grupos_dup[["n_repeticiones"]].head(20).to_string(index=False))
    print()

    # -----------------------------------------------------------------------
    # 6. Ejemplos de valores del período de cancelación
    # -----------------------------------------------------------------------
    print("=" * 75)
    print(f"6. EJEMPLOS DE VALORES EN '{COL_PERIODO}' (formato de período/fecha)")
    print("=" * 75)
    mostrar_ejemplos_periodo(dfs, col_periodo=COL_PERIODO)
    print()

    # -----------------------------------------------------------------------
    # 7. Candidatos a llave única — CORREO vs. DOCUMENTO
    # -----------------------------------------------------------------------
    print("=" * 75)
    print("7. EVALUACIÓN DE CANDIDATOS A LLAVE ÚNICA")
    print("   Compara CORREO_INSTITUCIONAL vs. DOCUMENTO como identificador")
    print("=" * 75)
    llaves_df = evaluar_llaves_candidatas(df_panel)
    print(llaves_df.to_string(index=False))
    print()
    print("  Si DOCUMENTO tiene mayor % de unicidad que CORREO_INSTITUCIONAL,")
    print("  plantear al PI usarlo como identificador principal.")
    print()

    # -----------------------------------------------------------------------
    # 8. Diagnóstico de repetidos dentro de LLAVE_DIAG
    # -----------------------------------------------------------------------
    llave_diag_ok = all(c in df_panel.columns for c in LLAVE_DIAG)

    if llave_diag_ok:
        print("=" * 75)
        print(f"8. DIAGNÓSTICO DE REPETIDOS EN {' + '.join(LLAVE_DIAG)}")
        print("=" * 75)
        repetidos_df = analizar_repetidos_dentro_de_llave(df_panel, LLAVE_DIAG)

        if repetidos_df.empty:
            print("  No hay llaves repetidas con esta combinación.")
        else:
            n_dup_exacto = int(repetidos_df["es_duplicado_exacto"].sum())
            n_con_dif    = int((~repetidos_df["es_duplicado_exacto"]).sum())
            print(f"  Llaves repetidas totales:                {len(repetidos_df)}")
            print(f"  → Son duplicados exactos (misma fila):   {n_dup_exacto}")
            print(f"  → Tienen diferencias reales entre filas: {n_con_dif}")
            print()
            print("  Top 20 llaves repetidas:")
            print(repetidos_df.head(20).to_string(index=False))
        print()

        print("8b. Columnas que diferencian los repetidos:")
        variacion_df = analizar_variacion_en_llaves_repetidas(df_panel, LLAVE_DIAG)
        print(variacion_df.head(20).to_string(index=False))
        print()
    else:
        faltantes = [c for c in LLAVE_DIAG if c not in df_panel.columns]
        print(f"  AVISO: columnas ausentes para diagnóstico: {faltantes}")
        print()

    # -----------------------------------------------------------------------
    # 9. Prueba final de llave tentativa
    # -----------------------------------------------------------------------
    print("=" * 75)
    print("9. PRUEBA FINAL DE LLAVE TENTATIVA")
    print("=" * 75)
    llave_final_ok = all(c in df_panel.columns for c in LLAVE_FINAL_COLS)

    if llave_final_ok:
        n_total_f, n_unicas_f, rep_final = evaluar_llave_final(
            df_panel, LLAVE_FINAL_COLS
        )
        pct = n_unicas_f / n_total_f * 100 if n_total_f else 0

        print(f"  Llave evaluada:          {' + '.join(LLAVE_FINAL_COLS)}")
        print(f"  Filas válidas:           {n_total_f}")
        print(f"  Combinaciones únicas:    {n_unicas_f}")
        print(f"  Combinaciones repetidas: {len(rep_final)}")
        print(f"  Porcentaje de unicidad:  {pct:.4f}%")

        if not rep_final.empty:
            print("\n  Top 20 llaves repetidas:")
            print(rep_final.head(20).to_string(index=False))
        else:
            print("\n  Sin repetidos. Esta combinación identifica de forma única cada observación.")
    else:
        faltantes = [c for c in LLAVE_FINAL_COLS if c not in df_panel.columns]
        print(f"  AVISO: columnas ausentes: {faltantes}. Actualizar LLAVE_FINAL_COLS.")

    print()
    print("=" * 75)
    print("FIN DEL INVENTARIO")
    print("=" * 75)


#%%
if __name__ == "__main__":
    main()
# %%
