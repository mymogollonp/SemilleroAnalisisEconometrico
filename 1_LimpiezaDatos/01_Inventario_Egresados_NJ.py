
#%%
from pathlib import Path

import pandas as pd

from config import DIR_DATOS


HOJA_EGRESADOS = "Sheet2"
DIR_EGRESADOS = DIR_DATOS / "DatosOriginales" / "Egresados"
LLAVE_TENTATIVA_COLS = ["EMAIL", "COD_PLAN"]


#%% =============================================================================
# 1. CONFIGURACIÓN Y LISTADO DE ARCHIVOS
# =============================================================================

def listar_archivos_excel(directorio: Path) -> list[Path]:
    return sorted(
        archivo
        for archivo in directorio.glob("*.xlsx")
        if not archivo.name.startswith("~$")
    )


archivos = listar_archivos_excel(DIR_EGRESADOS)

print("Carpeta analizada:", DIR_EGRESADOS)
print("Archivos encontrados:", len(archivos))
print("Primeros archivos:")
print(archivos[:5])


#%% =============================================================================
# 2. ESTRUCTURA GENERAL POR ARCHIVO
# =============================================================================

def cargar_archivo_excel(
    archivo: Path,
    hoja: str = HOJA_EGRESADOS,
) -> pd.DataFrame:
    df = pd.read_excel(archivo, sheet_name=hoja)
    df.columns = [str(columna).strip() for columna in df.columns]
    return df


def resumir_estructura_general_por_archivo(
    archivos: list[Path],
    hoja: str = HOJA_EGRESADOS,
) -> pd.DataFrame:
    filas = []

    for archivo in archivos:
        df = cargar_archivo_excel(archivo, hoja=hoja)

        filas.append(
            {
                "archivo": archivo.name,
                "n_filas": len(df),
                "n_columnas": len(df.columns),
                "missings_totales": int(df.isna().sum().sum()),
                "duplicados_exactos": int(df.duplicated().sum()),
            }
        )

    return pd.DataFrame(filas)


estructura_general_df = resumir_estructura_general_por_archivo(archivos)

print("Estructura general por archivo:")
print(estructura_general_df.to_string(index=False))


#%% =============================================================================
# 3. COMPARACIÓN DE ESTRUCTURAS DE COLUMNAS
# =============================================================================

def obtener_columnas(
    archivo: Path,
    hoja: str = HOJA_EGRESADOS,
) -> list[str]:
    df = cargar_archivo_excel(archivo, hoja=hoja)
    return [str(columna).strip() for columna in df.columns]


def construir_firma_columnas(columnas: list[str]) -> str:
    return " | ".join(columnas)


def construir_diccionario_estructuras(
    archivos: list[Path],
) -> tuple[pd.DataFrame, dict[str, dict[str, list[str]]]]:
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


def resumir_estructuras_unicas(df_archivos: pd.DataFrame) -> pd.DataFrame:
    return (
        df_archivos
        .groupby("firma_columnas", as_index=False)
        .agg(
            n_archivos=("archivo", "count"),
            archivos=("archivo", lambda x: " ; ".join(sorted(x))),
            n_columnas=("n_columnas", "first"),
        )
        .sort_values(["n_archivos", "n_columnas"], ascending=[False, False])
        .reset_index(drop=True)
    )


def etiquetar_estructuras(
    firmas_columnas: dict[str, dict[str, list[str]]],
) -> pd.DataFrame:
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
    estructuras_ordenadas = []

    for _, fila in estructuras_df.iterrows():
        archivo_ejemplo = fila["archivo_ejemplo"]
        firma = df_archivos.loc[
            df_archivos["archivo"] == archivo_ejemplo,
            "firma_columnas",
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


df_archivos, firmas_columnas = construir_diccionario_estructuras(archivos)
estructuras_unicas_df = resumir_estructuras_unicas(df_archivos)
estructuras_df = etiquetar_estructuras(firmas_columnas)
comparaciones_df = comparar_estructuras(
    df_archivos=df_archivos,
    estructuras_df=estructuras_df,
    firmas_columnas=firmas_columnas,
)

print("Estructuras únicas encontradas:", len(estructuras_unicas_df))
print("\nResumen de estructuras:")
print(estructuras_df.to_string(index=False))

print("\nComparaciones entre estructuras:")
print(comparaciones_df.to_string(index=False))


#%% =============================================================================
# 4. FORMATO DE FECHA_GRADUADO POR ARCHIVO
# =============================================================================

def diagnosticar_fecha_graduado_por_archivo(
    archivos: list[Path],
    hoja: str = HOJA_EGRESADOS,
) -> pd.DataFrame:
    filas = []

    for archivo in archivos:
        df = cargar_archivo_excel(archivo, hoja=hoja)

        if "FECHA_GRADUADO" not in df.columns:
            filas.append(
                {
                    "archivo": archivo.name,
                    "existe_columna": False,
                    "n_filas": len(df),
                    "n_no_nulos": 0,
                    "tipos_python": pd.NA,
                    "ejemplos": pd.NA,
                }
            )
            continue

        fecha = df["FECHA_GRADUADO"]
        no_nulos = fecha.dropna()

        tipos = (
            no_nulos
            .map(lambda x: type(x).__name__)
            .value_counts()
            .to_dict()
        )

        ejemplos = (
            no_nulos
            .drop_duplicates()
            .head(5)
            .astype(str)
            .tolist()
        )

        filas.append(
            {
                "archivo": archivo.name,
                "existe_columna": True,
                "n_filas": len(df),
                "n_no_nulos": len(no_nulos),
                "tipos_python": tipos,
                "ejemplos": " | ".join(ejemplos),
            }
        )

    return pd.DataFrame(filas)


fecha_por_archivo_df = diagnosticar_fecha_graduado_por_archivo(archivos)

print("Formato de FECHA_GRADUADO por archivo:")
print(fecha_por_archivo_df.to_string(index=False))


#%% =============================================================================
# 5. CONSOLIDACIÓN DE BASE DE EGRESADOS
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


def cargar_egresados(
    archivos: list[Path],
    hoja: str = HOJA_EGRESADOS,
) -> pd.DataFrame:
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


egresados = cargar_egresados(archivos)

print("Filas consolidadas:", len(egresados))
print("Columnas consolidadas:", len(egresados.columns))


#%% =============================================================================
# 6. MISSINGS POR VARIABLE
# =============================================================================

def resumir_missings_por_variable(egresados: pd.DataFrame) -> pd.DataFrame:
    resumen = pd.DataFrame(
        {
            "variable": egresados.columns,
            "n_missing": egresados.isna().sum().values,
            "pct_missing": (egresados.isna().mean().values * 100).round(4),
        }
    )

    return resumen.sort_values(
        ["pct_missing", "variable"],
        ascending=[False, True],
    ).reset_index(drop=True)


missings_df = resumir_missings_por_variable(egresados)

print("Missings por variable:")
print(missings_df.head(30).to_string(index=False))


#%% =============================================================================
# 7. DIAGNÓSTICO DE EMAIL COMO LLAVE
# =============================================================================

def diagnosticar_llave_simple_email(
    egresados: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if "EMAIL" not in egresados.columns:
        raise ValueError("No existe la columna EMAIL en la base consolidada.")

    repetidos = (
        egresados
        .dropna(subset=["EMAIL"])
        .groupby("EMAIL", as_index=False)
        .size()
        .rename(columns={"size": "n_filas"})
        .query("n_filas > 1")
        .sort_values("n_filas", ascending=False)
    )

    resumen = pd.DataFrame(
        [
            {
                "total_filas": len(egresados),
                "email_nulos": egresados["EMAIL"].isna().sum(),
                "email_no_nulos": egresados["EMAIL"].notna().sum(),
                "email_unicos_sin_nulos": egresados["EMAIL"].nunique(dropna=True),
                "email_repetidos": len(repetidos),
            }
        ]
    )

    return resumen, repetidos


resumen_email, repetidos_email = diagnosticar_llave_simple_email(egresados)

print("Diagnóstico EMAIL:")
print(resumen_email.to_string(index=False))

print("\nTop 20 correos repetidos:")
print(repetidos_email.head(20).to_string(index=False))


#%% =============================================================================
# 8. DIAGNÓSTICO DE EMAIL + COD_PLAN
# =============================================================================

def construir_base_llave_tentativa(
    egresados: pd.DataFrame,
    llave_cols: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    for columna in llave_cols:
        if columna not in egresados.columns:
            raise ValueError(f"Falta la columna {columna}")

    base = egresados.dropna(subset=llave_cols).copy()
    base["LLAVE"] = base[llave_cols].astype(str).agg(" || ".join, axis=1)

    rep_keys = (
        base
        .groupby("LLAVE", as_index=False)
        .size()
        .rename(columns={"size": "n_filas"})
        .query("n_filas > 1")
        .sort_values("n_filas", ascending=False)
    )

    return base, rep_keys


def diagnosticar_llave_email_cod_plan(
    egresados: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    base, rep_keys = construir_base_llave_tentativa(
        egresados,
        LLAVE_TENTATIVA_COLS,
    )

    n_filas_validas = len(base)
    n_llaves_unicas = base["LLAVE"].nunique()
    pct_unicidad = (
        n_llaves_unicas / n_filas_validas * 100
        if n_filas_validas
        else 0
    )

    resumen = pd.DataFrame(
        [
            {
                "total_filas": len(egresados),
                "email_nulos": egresados["EMAIL"].isna().sum(),
                "cod_plan_nulos": egresados["COD_PLAN"].isna().sum(),
                "filas_con_email_o_cod_plan_nulo": egresados[
                    LLAVE_TENTATIVA_COLS
                ].isna().any(axis=1).sum(),
                "filas_validas_para_llave": n_filas_validas,
                "combinaciones_unicas": n_llaves_unicas,
                "combinaciones_repetidas": len(rep_keys),
                "pct_unicidad": round(pct_unicidad, 4),
            }
        ]
    )

    return resumen, base, rep_keys


resumen_llave, base_llave, rep_keys = diagnosticar_llave_email_cod_plan(
    egresados
)

print("Diagnóstico EMAIL + COD_PLAN:")
print(resumen_llave.to_string(index=False))

print("\nTop 20 combinaciones repetidas:")
print(rep_keys.head(20).to_string(index=False))


#%% =============================================================================
# 9. VARIABLES QUE EXPLICAN REPETIDOS
# =============================================================================

def analizar_variacion_en_llaves_repetidas(
    base: pd.DataFrame,
    rep_keys: pd.DataFrame,
    llave_cols: list[str],
) -> pd.DataFrame:
    detalle = base[base["LLAVE"].isin(rep_keys["LLAVE"])].copy()
    variacion_cols = []

    for columna in base.columns:
        if columna in llave_cols or columna == "LLAVE":
            continue

        tmp = detalle.groupby("LLAVE")[columna].nunique(dropna=False)
        n_llaves_que_varian = int((tmp > 1).sum())

        variacion_cols.append(
            {
                "columna": columna,
                "llaves_repetidas_donde_varia": n_llaves_que_varian,
            }
        )

    return (
        pd.DataFrame(variacion_cols)
        .sort_values("llaves_repetidas_donde_varia", ascending=False)
        .reset_index(drop=True)
    )


variacion_df = analizar_variacion_en_llaves_repetidas(
    base=base_llave,
    rep_keys=rep_keys,
    llave_cols=LLAVE_TENTATIVA_COLS,
)

print("Columnas que más diferencian repetidos:")
print(variacion_df.head(30).to_string(index=False))


#%% =============================================================================
# 10. MAIN PARA EJECUCIÓN COMPLETA
# =============================================================================

def main() -> None:
    archivos_main = listar_archivos_excel(DIR_EGRESADOS)

    if not archivos_main:
        raise FileNotFoundError(
            f"No se encontraron archivos .xlsx en {DIR_EGRESADOS}"
        )

    estructura_general_main = resumir_estructura_general_por_archivo(archivos_main)

    df_archivos_main, firmas_columnas_main = construir_diccionario_estructuras(
        archivos_main
    )
    estructuras_unicas_main = resumir_estructuras_unicas(df_archivos_main)
    estructuras_main = etiquetar_estructuras(firmas_columnas_main)
    comparaciones_main = comparar_estructuras(
        df_archivos=df_archivos_main,
        estructuras_df=estructuras_main,
        firmas_columnas=firmas_columnas_main,
    )

    fecha_por_archivo_main = diagnosticar_fecha_graduado_por_archivo(archivos_main)
    egresados_main = cargar_egresados(archivos_main)
    missings_main = resumir_missings_por_variable(egresados_main)
    resumen_email_main, repetidos_email_main = diagnosticar_llave_simple_email(
        egresados_main
    )
    resumen_llave_main, base_llave_main, rep_keys_main = diagnosticar_llave_email_cod_plan(
        egresados_main
    )
    variacion_main = analizar_variacion_en_llaves_repetidas(
        base=base_llave_main,
        rep_keys=rep_keys_main,
        llave_cols=LLAVE_TENTATIVA_COLS,
    )

    print("=" * 60)
    print("INVENTARIO DE EGRESADOS")
    print("=" * 60)
    print(f"Carpeta analizada: {DIR_EGRESADOS}")
    print(f"Archivos encontrados: {len(archivos_main)}")

    print("\n" + "=" * 60)
    print("ESTRUCTURA GENERAL POR ARCHIVO")
    print("=" * 60)
    print(estructura_general_main.to_string(index=False))

    print("\n" + "=" * 60)
    print("COMPARACIÓN DE ESTRUCTURA DE EGRESADOS")
    print("=" * 60)
    print(f"Archivos analizados: {len(df_archivos_main)}")
    print(f"Estructuras únicas encontradas: {len(estructuras_unicas_main)}")
    print("\nResumen de estructuras:")
    print(estructuras_main.to_string(index=False))
    print("\nComparaciones:")
    print(comparaciones_main.to_string(index=False))

    print("\n" + "=" * 60)
    print("FORMATO DE FECHA_GRADUADO POR ARCHIVO")
    print("=" * 60)
    print(fecha_por_archivo_main.to_string(index=False))

    print("\n" + "=" * 60)
    print("BASE CONSOLIDADA")
    print("=" * 60)
    print(f"Filas consolidadas: {len(egresados_main)}")
    print(f"Columnas consolidadas: {len(egresados_main.columns)}")

    print("\n" + "=" * 60)
    print("MISSINGS POR VARIABLE EN BASE CONSOLIDADA")
    print("=" * 60)
    print(missings_main.head(30).to_string(index=False))

    print("\n" + "=" * 60)
    print("DIAGNÓSTICO DE EMAIL COMO LLAVE TENTATIVA")
    print("=" * 60)
    print(resumen_email_main.to_string(index=False))
    if not repetidos_email_main.empty:
        print("\nTop 20 correos repetidos:")
        print(repetidos_email_main.head(20).to_string(index=False))

    print("\n" + "=" * 60)
    print("DIAGNÓSTICO DE EMAIL + COD_PLAN COMO LLAVE TENTATIVA")
    print("=" * 60)
    print(resumen_llave_main.to_string(index=False))
    if not rep_keys_main.empty:
        print("\nTop 20 combinaciones repetidas:")
        print(rep_keys_main.head(20).to_string(index=False))

    print("\n" + "=" * 75)
    print("COLUMNAS QUE MÁS DIFERENCIAN REPETIDOS EN EGRESADOS")
    print("=" * 75)
    print(f"Llaves repetidas analizadas: {len(rep_keys_main)}")
    print(variacion_main.head(30).to_string(index=False))


#%%
if __name__ == "__main__":
    main()