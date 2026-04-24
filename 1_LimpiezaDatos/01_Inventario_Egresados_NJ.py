#%%
from pathlib import Path

import pandas as pd

from config import DIR_DATOS


HOJA_EGRESADOS = "Sheet2"
DIR_EGRESADOS = DIR_DATOS / "DatosOriginales" / "Egresados"
LLAVE_TENTATIVA_COLS = ["EMAIL", "COD_PLAN"]
#%%

def listar_archivos_excel(directorio: Path) -> list[Path]:
    """Retorna archivos Excel válidos, excluyendo archivos temporales."""
    return sorted(
        archivo
        for archivo in directorio.glob("*.xlsx")
        if not archivo.name.startswith("~$")
    )


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


def cargar_archivo_excel(archivo: Path, hoja: str = HOJA_EGRESADOS) -> pd.DataFrame:
    """Carga un archivo Excel y normaliza nombres de columnas."""
    df = pd.read_excel(archivo, sheet_name=hoja)
    df.columns = [str(columna).strip() for columna in df.columns]
    return df


def cargar_egresados(
    archivos: list[Path],
    hoja: str = HOJA_EGRESADOS,
) -> pd.DataFrame:
    """Carga y concatena todos los archivos de Egresados."""
    dataframes = []

    for archivo in archivos:
        df = cargar_archivo_excel(archivo, hoja=hoja)
        df["archivo_origen"] = archivo.name
        dataframes.append(df)

    egresados = pd.concat(dataframes, ignore_index=True)
    egresados.columns = [str(columna).strip() for columna in egresados.columns]

    for columna in egresados.columns:
        if egresados[columna].dtype == "object":
            egresados[columna] = normalizar_texto(egresados[columna])

    if "EMAIL" in egresados.columns:
        egresados["EMAIL"] = normalizar_texto(egresados["EMAIL"], lower=True)

    if "COD_PLAN" in egresados.columns:
        egresados["COD_PLAN"] = normalizar_texto(egresados["COD_PLAN"])

    if "FECHA_GRADUADO" in egresados.columns:
        egresados["FECHA_GRADUADO"] = normalizar_texto(
            egresados["FECHA_GRADUADO"]
        )

    if "TITULOOBT" in egresados.columns:
        egresados["TITULOOBT"] = normalizar_texto(egresados["TITULOOBT"])

    return egresados


def obtener_columnas(
    archivo: Path,
    hoja: str = HOJA_EGRESADOS,
) -> list[str]:
    """Lee los nombres de columnas de una hoja de Excel."""
    df = cargar_archivo_excel(archivo, hoja=hoja)
    return [str(columna).strip() for columna in df.columns]


def construir_firma_columnas(columnas: list[str]) -> str:
    """Construye una firma única a partir del orden y nombres de columnas."""
    return " | ".join(columnas)


def resumir_estructuras_archivos(archivos: list[Path]) -> pd.DataFrame:
    """Resume la estructura de columnas de cada archivo."""
    filas = []

    for archivo in archivos:
        columnas = obtener_columnas(archivo)
        firma = construir_firma_columnas(columnas)

        filas.append(
            {
                "archivo": archivo.name,
                "n_columnas": len(columnas),
                "firma_columnas": firma,
            }
        )

    return pd.DataFrame(filas)


def resumir_estructuras_unicas(df_archivos: pd.DataFrame) -> pd.DataFrame:
    """Agrupa archivos con la misma estructura de columnas."""
    return (
        df_archivos.groupby("firma_columnas", as_index=False)
        .agg(
            n_archivos=("archivo", "count"),
            archivos=("archivo", lambda x: " ; ".join(sorted(x))),
            n_columnas=("n_columnas", "first"),
        )
        .sort_values(["n_archivos", "n_columnas"], ascending=[False, False])
        .reset_index(drop=True)
    )


def construir_diccionario_estructuras(
    archivos: list[Path],
) -> tuple[pd.DataFrame, dict[str, dict[str, list[str]]]]:
    """Construye un resumen por archivo y un diccionario por firma estructural."""
    filas = []
    firmas_columnas: dict[str, dict[str, list[str]]] = {}

    for archivo in archivos:
        columnas = obtener_columnas(archivo)
        firma = construir_firma_columnas(columnas)

        filas.append(
            {
                "archivo": archivo.name,
                "n_columnas": len(columnas),
                "firma_columnas": firma,
            }
        )

        if firma not in firmas_columnas:
            firmas_columnas[firma] = {
                "columnas": columnas,
                "archivos": [],
            }

        firmas_columnas[firma]["archivos"].append(archivo.name)

    return pd.DataFrame(filas), firmas_columnas


def etiquetar_estructuras(
    firmas_columnas: dict[str, dict[str, list[str]]],
) -> pd.DataFrame:
    """Asigna etiquetas E1, E2, ... a cada estructura encontrada."""
    estructuras = []

    for indice, (_, info) in enumerate(firmas_columnas.items(), start=1):
        estructuras.append(
            {
                "estructura_id": f"E{indice}",
                "n_archivos": len(info["archivos"]),
                "n_columnas": len(info["columnas"]),
                "archivo_ejemplo": sorted(info["archivos"])[0],
                "archivos": " ; ".join(sorted(info["archivos"])),
            }
        )

    return (
        pd.DataFrame(estructuras)
        .sort_values(["n_archivos", "n_columnas"], ascending=[False, False])
        .reset_index(drop=True)
    )


def comparar_estructuras(
    df_archivos: pd.DataFrame,
    estructuras_df: pd.DataFrame,
    firmas_columnas: dict[str, dict[str, list[str]]],
) -> pd.DataFrame:
    """Compara estructuras y muestra qué columnas aparecen solo en cada una."""
    estructuras_ordenadas = []

    for _, fila in estructuras_df.iterrows():
        archivo_ejemplo = fila["archivo_ejemplo"]
        firma = df_archivos.loc[
            df_archivos["archivo"] == archivo_ejemplo, "firma_columnas"
        ].iloc[0]

        estructuras_ordenadas.append(
            (fila["estructura_id"], firmas_columnas[firma]["columnas"])
        )

    comparaciones = []

    for i in range(len(estructuras_ordenadas)):
        estructura_a, columnas_a = estructuras_ordenadas[i]
        set_a = set(columnas_a)

        for j in range(i + 1, len(estructuras_ordenadas)):
            estructura_b, columnas_b = estructuras_ordenadas[j]
            set_b = set(columnas_b)

            solo_en_a = sorted(set_a - set_b)
            solo_en_b = sorted(set_b - set_a)

            comparaciones.append(
                {
                    "estructura_a": estructura_a,
                    "estructura_b": estructura_b,
                    "solo_en_a": " | ".join(solo_en_a) if solo_en_a else "",
                    "solo_en_b": " | ".join(solo_en_b) if solo_en_b else "",
                    "n_solo_en_a": len(solo_en_a),
                    "n_solo_en_b": len(solo_en_b),
                }
            )

    return pd.DataFrame(comparaciones)


def resumir_estructura_general_por_archivo(
    archivos: list[Path],
    hoja: str = HOJA_EGRESADOS,
) -> pd.DataFrame:
    """Resume filas, columnas, missings y duplicados exactos por archivo."""
    filas = []

    for archivo in archivos:
        df = cargar_archivo_excel(archivo, hoja=hoja)
        n_filas = len(df)
        n_columnas = len(df.columns)
        n_duplicados_exactos = int(df.duplicated().sum())
        missings_totales = int(df.isna().sum().sum())

        filas.append(
            {
                "archivo": archivo.name,
                "n_filas": n_filas,
                "n_columnas": n_columnas,
                "missings_totales": missings_totales,
                "duplicados_exactos": n_duplicados_exactos,
            }
        )

    return pd.DataFrame(filas)


def resumir_missings_por_variable(egresados: pd.DataFrame) -> pd.DataFrame:
    """Resume missings por variable en la base consolidada."""
    resumen = pd.DataFrame(
        {
            "variable": egresados.columns,
            "n_missing": egresados.isna().sum().values,
            "pct_missing": (
                egresados.isna().mean().values * 100
            ).round(4),
        }
    )

    return resumen.sort_values(
        ["pct_missing", "variable"], ascending=[False, True]
    ).reset_index(drop=True)


def diagnosticar_llave_simple_email(egresados: pd.DataFrame) -> None:
    """Imprime diagnóstico de EMAIL como llave tentativa."""
    if "EMAIL" not in egresados.columns:
        raise ValueError("No existe la columna EMAIL en la base consolidada.")

    n_total = len(egresados)
    n_nulos = egresados["EMAIL"].isna().sum()
    n_no_nulos = n_total - n_nulos
    n_unicos = egresados["EMAIL"].nunique(dropna=True)

    repetidos = (
        egresados.dropna(subset=["EMAIL"])
        .groupby("EMAIL", as_index=False)
        .size()
        .rename(columns={"size": "n_filas"})
    )
    repetidos = repetidos[repetidos["n_filas"] > 1].sort_values(
        "n_filas", ascending=False
    )

    print("=" * 60)
    print("DIAGNÓSTICO DE EMAIL COMO LLAVE TENTATIVA")
    print("=" * 60)
    print(f"Total filas: {n_total}")
    print(f"EMAIL nulos: {n_nulos}")
    print(f"EMAIL no nulos: {n_no_nulos}")
    print(f"EMAIL únicos (sin nulos): {n_unicos}")
    print(f"EMAIL repetidos: {len(repetidos)}")

    if not repetidos.empty:
        print("\nTop 20 correos repetidos:")
        print(repetidos.head(20).to_string(index=False))


def construir_base_llave_tentativa(
    egresados: pd.DataFrame,
    llave_cols: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Construye base válida y llaves repetidas para una llave tentativa."""
    for columna in llave_cols:
        if columna not in egresados.columns:
            raise ValueError(f"Falta la columna {columna}")

    base = egresados.dropna(subset=llave_cols).copy()
    base["LLAVE"] = base[llave_cols].astype(str).agg(" || ".join, axis=1)

    rep_keys = (
        base.groupby("LLAVE", as_index=False)
        .size()
        .rename(columns={"size": "n_filas"})
    )
    rep_keys = rep_keys[rep_keys["n_filas"] > 1].sort_values(
        "n_filas", ascending=False
    )

    return base, rep_keys


def diagnosticar_llave_email_cod_plan(
    egresados: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Imprime diagnóstico de EMAIL + COD_PLAN como llave tentativa."""
    base, rep_keys = construir_base_llave_tentativa(
        egresados,
        LLAVE_TENTATIVA_COLS,
    )

    n_total = len(egresados)
    n_email_nulo = egresados["EMAIL"].isna().sum()
    n_codplan_nulo = egresados["COD_PLAN"].isna().sum()
    n_alguno_nulo = egresados[LLAVE_TENTATIVA_COLS].isna().any(axis=1).sum()
    n_filas_validas = len(base)
    n_llaves_unicas = base["LLAVE"].nunique()
    pct_unicidad = (
        n_llaves_unicas / n_filas_validas * 100
        if n_filas_validas
        else 0
    )

    print()
    print("=" * 60)
    print("DIAGNÓSTICO DE EMAIL + COD_PLAN COMO LLAVE TENTATIVA")
    print("=" * 60)
    print(f"Total filas: {n_total}")
    print(f"EMAIL nulos: {n_email_nulo}")
    print(f"COD_PLAN nulos: {n_codplan_nulo}")
    print(f"Filas con EMAIL o COD_PLAN nulo: {n_alguno_nulo}")
    print(f"Filas válidas para evaluar la llave: {n_filas_validas}")
    print(f"Combinaciones únicas EMAIL+COD_PLAN: {n_llaves_unicas}")
    print(f"Combinaciones repetidas EMAIL+COD_PLAN: {len(rep_keys)}")
    print(f"Porcentaje de unicidad sobre filas válidas: {pct_unicidad:.4f}%")

    if not rep_keys.empty:
        print("\nTop 20 combinaciones repetidas:")
        print(rep_keys.head(20).to_string(index=False))

    return base, rep_keys


def analizar_variacion_en_llaves_repetidas(
    base: pd.DataFrame,
    rep_keys: pd.DataFrame,
    llave_cols: list[str],
) -> pd.DataFrame:
    """
    Para las llaves repetidas, identifica en cuántas llaves varía cada columna.
    """
    detalle = base[base["LLAVE"].isin(rep_keys["LLAVE"])].copy()
    variacion_cols = []

    for columna in base.columns:
        if columna in llave_cols or columna == "LLAVE":
            continue

        tmp = detalle.groupby("LLAVE")[columna].nunique(dropna=False)
        n_llaves_que_varian = (tmp > 1).sum()

        variacion_cols.append(
            {
                "columna": columna,
                "llaves_repetidas_donde_varia": int(n_llaves_que_varian),
            }
        )

    variacion_df = pd.DataFrame(variacion_cols).sort_values(
        "llaves_repetidas_donde_varia",
        ascending=False,
    )

    print()
    print("=" * 75)
    print("COLUMNAS QUE MÁS DIFERENCIAN REPETIDOS EN EGRESADOS")
    print("=" * 75)
    print(f"Llaves repetidas analizadas: {len(rep_keys)}")
    print()
    print(variacion_df.head(30).to_string(index=False))

    return variacion_df


def main() -> None:
    """Ejecuta el inventario de Egresados."""
    archivos = listar_archivos_excel(DIR_EGRESADOS)

    if not archivos:
        raise FileNotFoundError(
            f"No se encontraron archivos .xlsx en {DIR_EGRESADOS}"
        )

    print("=" * 60)
    print("INVENTARIO DE EGRESADOS")
    print("=" * 60)
    print(f"Carpeta analizada: {DIR_EGRESADOS}")
    print(f"Archivos encontrados: {len(archivos)}")

    print()
    print("=" * 60)
    print("ESTRUCTURA GENERAL POR ARCHIVO")
    print("=" * 60)
    estructura_general_df = resumir_estructura_general_por_archivo(archivos)
    print(estructura_general_df.to_string(index=False))

    print()
    print("=" * 60)
    print("COMPARACIÓN DE ESTRUCTURA DE EGRESADOS")
    print("=" * 60)
    df_archivos = resumir_estructuras_archivos(archivos)
    estructuras_unicas_df = resumir_estructuras_unicas(df_archivos)

    print(f"Archivos analizados: {len(df_archivos)}")
    print(f"Estructuras únicas encontradas: {len(estructuras_unicas_df)}")
    print()
    print("Resumen de estructuras:")
    print(
        estructuras_unicas_df[["n_archivos", "n_columnas"]].to_string(index=False)
    )

    if len(estructuras_unicas_df) == 1:
        print("\nTodos los archivos tienen la misma estructura de columnas.")
    else:
        print("\nHay diferencias de estructura entre archivos.")

    print()
    print("=" * 60)
    print("DIFERENCIAS ENTRE ESTRUCTURAS DE EGRESADOS")
    print("=" * 60)
    df_firmas, firmas_columnas = construir_diccionario_estructuras(archivos)
    estructuras_df = etiquetar_estructuras(firmas_columnas)
    comparaciones_df = comparar_estructuras(
        df_archivos=df_firmas,
        estructuras_df=estructuras_df,
        firmas_columnas=firmas_columnas,
    )

    print()
    print("Resumen de estructuras:")
    print(estructuras_df.to_string(index=False))
    print()
    print("Comparaciones:")
    print(comparaciones_df.to_string(index=False))

    egresados = cargar_egresados(archivos)

    print()
    print("=" * 60)
    print("MISSINGS POR VARIABLE EN BASE CONSOLIDADA")
    print("=" * 60)
    missings_df = resumir_missings_por_variable(egresados)
    print(missings_df.head(30).to_string(index=False))

    print()
    diagnosticar_llave_simple_email(egresados)

    base_llave, rep_keys = diagnosticar_llave_email_cod_plan(egresados)

    analizar_variacion_en_llaves_repetidas(
        base=base_llave,
        rep_keys=rep_keys,
        llave_cols=LLAVE_TENTATIVA_COLS,
    )

#%%
if __name__ == "__main__":
    main()
# %%
