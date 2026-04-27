#%%
from pathlib import Path
import unicodedata

import pandas as pd

from config import DIR_DATOS


HOJA_RETIRADOS = "Sheet2"
ARCHIVO_RETIRADOS = (
    DIR_DATOS
    / "DatosOriginales"
    / "Retirados"
    / "Retirados_desde_2009.xlsx"
)

DIR_KEYS = DIR_DATOS / "DatosArmonizados" / "keys"
OUTPUT_FILE = DIR_KEYS / "MASTER_PERSONAS_RETIRADOS_PII.csv"


#%% =============================================================================
# 1. CARGA DE ARCHIVO
# =============================================================================

def cargar_retirados(
    archivo: Path = ARCHIVO_RETIRADOS,
    hoja: str = HOJA_RETIRADOS,
) -> pd.DataFrame:
    df = pd.read_excel(archivo, sheet_name=hoja, dtype=str)
    df.columns = [str(col).strip() for col in df.columns]
    return df


df = cargar_retirados()

print("Archivo existe:", ARCHIVO_RETIRADOS.exists())
print("Ruta:", ARCHIVO_RETIRADOS)
print("Dimensiones:", df.shape)
print("Columnas:", len(df.columns))


#%% =============================================================================
# 2. LIMPIEZA Y ARMONIZACIÓN DE PII
# =============================================================================

def quitar_tildes(texto: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFKD", texto)
        if not unicodedata.combining(c)
    )


def normalizar_texto(
    serie: pd.Series,
    lower: bool = False,
    upper: bool = False,
) -> pd.Series:
    serie = serie.astype(str).str.strip()

    serie = serie.replace(
        {
            "": pd.NA,
            "nan": pd.NA,
            "none": pd.NA,
            "None": pd.NA,
            "NaT": pd.NA,
            "nat": pd.NA,
            "<NA>": pd.NA,
        }
    )

    serie = serie.map(lambda x: quitar_tildes(x) if pd.notna(x) else pd.NA)

    if lower:
        serie = serie.str.lower()

    if upper:
        serie = serie.str.upper()

    return serie


def obtener_serie(
    df: pd.DataFrame,
    nombre_columna: str,
    lower: bool = False,
    upper: bool = False,
) -> pd.Series:
    if nombre_columna not in df.columns:
        return pd.Series([pd.NA] * len(df), index=df.index, dtype="object")

    return normalizar_texto(df[nombre_columna], lower=lower, upper=upper)


def armonizar_sexo(sexo_raw: pd.Series, genero_raw: pd.Series) -> pd.Series:
    sexo_norm = normalizar_texto(sexo_raw, upper=True)
    genero_norm = normalizar_texto(genero_raw, upper=True)

    base = sexo_norm.fillna(genero_norm)

    mapa = {
        "H": "M",
        "MASCULINO": "M",
        "D": "F",
        "FEMENINO": "F",
        "MUJER": "F",
        "X": "X",
        "NO BINARIO": "X",
        "NO DISPONIBLE": pd.NA,
    }

    return base.map(mapa).fillna(base)


def normalizar_nombre_propio(nombre: pd.Series) -> pd.Series:
    return (
        nombre
        .str.lower()
        .str.title()
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
        .replace({"": pd.NA})
    )


def combinar_nombre_completo(df: pd.DataFrame) -> pd.Series:
    nombres = obtener_serie(df, "NOMBRES_LEGAL")
    ap1 = obtener_serie(df, "APELLIDO1_LEGAL")
    ap2 = obtener_serie(df, "APELLIDO2_LEGAL")

    nombre = (
        nombres.fillna("")
        + " "
        + ap1.fillna("")
        + " "
        + ap2.fillna("")
    )

    nombre = nombre.str.replace(r"\s+", " ", regex=True).str.strip()

    return nombre.replace({"": pd.NA})


def armonizar_pii_retirados(df: pd.DataFrame) -> pd.DataFrame:
    correo = obtener_serie(df, "CORREO", lower=True)

    tipo_documento = pd.Series([pd.NA] * len(df), index=df.index, dtype="object")
    tipo_documento_raw = pd.Series([pd.NA] * len(df), index=df.index, dtype="object")

    numero_documento = obtener_serie(df, "DOCUMENTO")

    nombre_completo_raw = combinar_nombre_completo(df)
    nombre_completo = normalizar_nombre_propio(nombre_completo_raw)

    sexo_raw = obtener_serie(df, "SEXO_LEGAL")
    genero_raw = obtener_serie(df, "GENERO")
    sexo = armonizar_sexo(sexo_raw, genero_raw)

    periodo = obtener_serie(df, "PERIODO_BLOQUEO")

    return pd.DataFrame(
        {
            "correo": correo,
            "tipo_documento": tipo_documento,
            "tipo_documento_raw": tipo_documento_raw,
            "numero_documento": numero_documento,
            "nombre_completo": nombre_completo,
            "nombre_completo_raw": nombre_completo_raw,
            "sexo": sexo,
            "sexo_raw": sexo_raw,
            "genero_raw": genero_raw,
            "periodo": periodo,
            "archivo_origen": ARCHIVO_RETIRADOS.name,
        }
    )


all_pii = armonizar_pii_retirados(df)

print("Filas PII:", len(all_pii))
print("Personas únicas por correo:", all_pii["correo"].nunique(dropna=True))
print("Personas únicas por documento:", all_pii["numero_documento"].nunique(dropna=True))


#%% =============================================================================
# 3. CONSISTENCIA CORREO-DOCUMENTO
# =============================================================================

def diagnosticar_consistencia_correo_documento(
    all_pii: pd.DataFrame,
) -> dict[str, object]:
    docs_por_correo = (
        all_pii
        .dropna(subset=["correo"])
        .groupby("correo")["numero_documento"]
        .nunique(dropna=True)
        .reset_index(name="n_documentos")
        .query("n_documentos > 1")
        .sort_values("n_documentos", ascending=False)
    )

    detalle_docs_por_correo = (
        all_pii
        .loc[all_pii["correo"].isin(docs_por_correo["correo"])]
        .sort_values(["correo", "numero_documento", "periodo"])
    )

    correos_por_doc = (
        all_pii
        .dropna(subset=["numero_documento"])
        .groupby("numero_documento")["correo"]
        .nunique(dropna=True)
        .reset_index(name="n_correos")
        .query("n_correos > 1")
        .sort_values("n_correos", ascending=False)
    )

    return {
        "filas_sin_correo": int(all_pii["correo"].isna().sum()),
        "documentos_unicos_sin_correo": int(
            all_pii.loc[
                all_pii["correo"].isna(),
                "numero_documento",
            ].nunique(dropna=True)
        ),
        "filas_sin_documento": int(all_pii["numero_documento"].isna().sum()),
        "correos_unicos_sin_documento": int(
            all_pii.loc[
                all_pii["numero_documento"].isna(),
                "correo",
            ].nunique(dropna=True)
        ),
        "docs_por_correo": docs_por_correo,
        "detalle_docs_por_correo": detalle_docs_por_correo,
        "correos_por_doc": correos_por_doc,
    }


diag_correo_doc = diagnosticar_consistencia_correo_documento(all_pii)

print("Diagnóstico correo-documento:")
print("Filas sin correo:", diag_correo_doc["filas_sin_correo"])
print("Documentos únicos sin correo:", diag_correo_doc["documentos_unicos_sin_correo"])
print("Filas sin documento:", diag_correo_doc["filas_sin_documento"])
print("Correos únicos sin documento:", diag_correo_doc["correos_unicos_sin_documento"])
print("Correos con más de un documento:", len(diag_correo_doc["docs_por_correo"]))
print("Documentos con más de un correo:", len(diag_correo_doc["correos_por_doc"]))

if not diag_correo_doc["docs_por_correo"].empty:
    print("\nDetalle de correos con más de un documento:")
    print(
        diag_correo_doc["detalle_docs_por_correo"][
            [
                "correo",
                "numero_documento",
                "nombre_completo",
                "sexo",
                "periodo",
                "archivo_origen",
            ]
        ].to_string(index=False)
    )


#%% =============================================================================
# 4. MASTER DIAGNÓSTICO
# =============================================================================

def construir_master_diagnostico(all_pii: pd.DataFrame) -> pd.DataFrame:
    return (
        all_pii
        .drop_duplicates(
            subset=[
                "correo",
                "tipo_documento",
                "numero_documento",
                "nombre_completo",
                "sexo",
                "sexo_raw",
                "genero_raw",
                "periodo",
            ]
        )
        .sort_values(
            ["correo", "numero_documento", "periodo"],
            na_position="last",
        )
        .reset_index(drop=True)
    )


def diagnosticar_repeticiones_master(
    master_diag: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series]:
    id_persona = master_diag["correo"].fillna(master_diag["numero_documento"])

    master_repetidos = (
        master_diag
        .assign(id_persona=id_persona)
        .loc[lambda df: df.duplicated("id_persona", keep=False)]
        .sort_values(["id_persona", "periodo"], na_position="last")
    )

    columnas_diagnostico = [
        "tipo_documento",
        "numero_documento",
        "nombre_completo",
        "sexo",
        "sexo_raw",
        "genero_raw",
        "periodo",
    ]

    diagnostico = (
        master_repetidos
        .groupby("id_persona")
        .agg(
            n_filas=("id_persona", "size"),
            **{
                f"n_{col}": (col, lambda x: x.fillna("NA").nunique())
                for col in columnas_diagnostico
            }
        )
        .reset_index()
        .sort_values("n_filas", ascending=False)
    )

    causas = pd.Series(
        {
            col: (diagnostico[f"n_{col}"] > 1).sum()
            for col in columnas_diagnostico
        }
    ).sort_values(ascending=False)

    return diagnostico, causas


master_diag = construir_master_diagnostico(all_pii)
diagnostico_repetidos, causas_repeticion = diagnosticar_repeticiones_master(
    master_diag
)

print("Filas en master diagnóstico:", len(master_diag))
print("Personas repetidas en master diagnóstico:", len(diagnostico_repetidos))
print("\nCausas de repetición en master diagnóstico:")
print(causas_repeticion.to_string())


#%% =============================================================================
# 5. MASTER FINAL
# =============================================================================

def construir_master_personas(all_pii: pd.DataFrame) -> pd.DataFrame:
    all_pii_ordenado = (
        all_pii
        .sort_values(
            ["correo", "numero_documento", "periodo"],
            na_position="last",
        )
    )

    return (
        all_pii_ordenado
        .drop_duplicates(
            subset=[
                "correo",
                "numero_documento",
                "sexo",
            ],
            keep="first",
        )
        .reset_index(drop=True)
    )


master = construir_master_personas(all_pii)

print("Filas en master final:", len(master))
print("Personas únicas por correo en master:", master["correo"].nunique(dropna=True))
print("Personas únicas por documento en master:", master["numero_documento"].nunique(dropna=True))


#%% =============================================================================
# 6. REPETICIONES EN MASTER FINAL
# =============================================================================

id_persona_final = master["correo"].fillna(master["numero_documento"])

master_final_repetidos = (
    master
    .assign(id_persona=id_persona_final)
    .loc[lambda df: df.duplicated("id_persona", keep=False)]
    .sort_values(["id_persona", "periodo"], na_position="last")
)

print("Personas repetidas en master final:", master_final_repetidos["id_persona"].nunique())

if not master_final_repetidos.empty:
    print("\nDetalle de personas repetidas en master final:")
    print(
        master_final_repetidos[
            [
                "correo",
                "numero_documento",
                "nombre_completo",
                "sexo",
                "periodo",
                "archivo_origen",
            ]
        ].to_string(index=False)
    )
else:
    print("No hay personas repetidas en master final.")


#%% =============================================================================
# 7. VALIDACIONES FINALES
# =============================================================================

def validar_tipos_documento(master: pd.DataFrame) -> pd.DataFrame:
    valid_types = {"CC", "CE", "PA", "TI", "NUIP", "PEP", "OTRO"}

    return (
        master
        .dropna(subset=["tipo_documento"])
        .loc[lambda df: ~df["tipo_documento"].isin(valid_types)]
        .groupby("tipo_documento", as_index=False)
        .size()
        .sort_values("size", ascending=False)
    )


def validar_formato_documento(master: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(columns=master.columns)


def tabla_frecuencias(serie: pd.Series, nombre: str) -> pd.DataFrame:
    return (
        serie
        .fillna("NA")
        .value_counts(dropna=False)
        .rename_axis(nombre)
        .reset_index(name="n")
    )


unknown_types = validar_tipos_documento(master)
invalid_format = validar_formato_documento(master)

print("Distribución tipo_documento:")
print(tabla_frecuencias(master["tipo_documento"], "tipo_documento"))

print("\nDistribución sexo:")
print(tabla_frecuencias(master["sexo"], "sexo"))

print("\nTipos no reconocidos:")
print(unknown_types)

print("\nRegistros con formato documental inesperado:", len(invalid_format))


#%% =============================================================================
# 8. GUARDAR OUTPUT
# =============================================================================

def guardar_master(master: pd.DataFrame) -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    master.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")


guardar_master(master)

print("Guardado en:", OUTPUT_FILE)


#%% =============================================================================
# 9. MAIN PARA EJECUCIÓN COMPLETA
# =============================================================================

def main() -> None:
    if not ARCHIVO_RETIRADOS.exists():
        raise FileNotFoundError(
            f"No existe el archivo de Retirados: {ARCHIVO_RETIRADOS}"
        )

    df_main = cargar_retirados()
    all_pii_main = armonizar_pii_retirados(df_main)

    diag_correo_doc_main = diagnosticar_consistencia_correo_documento(all_pii_main)

    master_diag_main = construir_master_diagnostico(all_pii_main)
    diagnostico_repetidos_main, causas_repeticion_main = diagnosticar_repeticiones_master(
        master_diag_main
    )

    master_main = construir_master_personas(all_pii_main)

    id_persona_final_main = master_main["correo"].fillna(
        master_main["numero_documento"]
    )
    master_final_repetidos_main = (
        master_main
        .assign(id_persona=id_persona_final_main)
        .loc[lambda df: df.duplicated("id_persona", keep=False)]
    )

    unknown_types_main = validar_tipos_documento(master_main)
    invalid_format_main = validar_formato_documento(master_main)

    print("=" * 70)
    print("MASTER PERSONAS - RETIRADOS")
    print("=" * 70)
    print(f"Archivo procesado: {ARCHIVO_RETIRADOS.name}")
    print(f"Total filas cargadas: {len(df_main)}")
    print(f"Filas PII armonizadas: {len(all_pii_main)}")
    print(f"Filas en master diagnóstico: {len(master_diag_main)}")
    print(f"Filas en master final: {len(master_main)}")

    print("\nDiagnóstico correo-documento:")
    print(f"Filas sin correo: {diag_correo_doc_main['filas_sin_correo']}")
    print(
        "Documentos únicos sin correo: "
        f"{diag_correo_doc_main['documentos_unicos_sin_correo']}"
    )
    print(f"Filas sin documento: {diag_correo_doc_main['filas_sin_documento']}")
    print(
        "Correos únicos sin documento: "
        f"{diag_correo_doc_main['correos_unicos_sin_documento']}"
    )
    print(
        "Correos asociados a más de un documento: "
        f"{len(diag_correo_doc_main['docs_por_correo'])}"
    )
    print(
        "Documentos asociados a más de un correo: "
        f"{len(diag_correo_doc_main['correos_por_doc'])}"
    )

    if not diag_correo_doc_main["docs_por_correo"].empty:
        print("\nDetalle de correos asociados a más de un documento:")
        print(
            diag_correo_doc_main["detalle_docs_por_correo"][
                [
                    "correo",
                    "numero_documento",
                    "nombre_completo",
                    "sexo",
                    "periodo",
                    "archivo_origen",
                ]
            ].to_string(index=False)
        )

    print("\nCausas de repetición en master diagnóstico:")
    print(causas_repeticion_main.to_string())

    print(
        "\nPersonas repetidas en master final: "
        f"{master_final_repetidos_main['id_persona'].nunique() if not master_final_repetidos_main.empty else 0}"
    )

    if not master_final_repetidos_main.empty:
        print("\nDetalle de personas repetidas en master final:")
        print(
            master_final_repetidos_main[
                [
                    "correo",
                    "numero_documento",
                    "nombre_completo",
                    "sexo",
                    "periodo",
                    "archivo_origen",
                ]
            ].to_string(index=False)
        )

    print("\nDistribución de tipo_documento en master final:")
    print(
        tabla_frecuencias(master_main["tipo_documento"], "tipo_documento")
        .to_string(index=False)
    )

    print("\nDistribución de sexo en master final:")
    print(
        tabla_frecuencias(master_main["sexo"], "sexo")
        .to_string(index=False)
    )

    if not unknown_types_main.empty:
        print("\nTipos de documento no reconocidos:")
        print(unknown_types_main.to_string(index=False))
    else:
        print("\nNo hay tipos de documento no reconocidos.")

    print(
        "\nRegistros con formato documental inesperado en master final: "
        f"{len(invalid_format_main)}"
    )

    guardar_master(master_main)
    print(f"\nGuardado en: {OUTPUT_FILE}")


#%%
if __name__ == "__main__":
    main()