#%%
from pathlib import Path
import unicodedata

import pandas as pd

from config import DIR_DATOS


HOJA_EGRESADOS = "Sheet2"
DIR_EGRESADOS = DIR_DATOS / "DatosOriginales" / "Egresados"
DIR_KEYS = DIR_DATOS / "DatosArmonizados" / "keys"
OUTPUT_FILE = DIR_KEYS / "MASTER_PERSONAS_EGRESADOS_PII.csv"


#%% =============================================================================
# 1. CARGA DE ARCHIVOS
# =============================================================================

def listar_archivos_excel(directorio: Path) -> list[Path]:
    return sorted(
        archivo
        for archivo in directorio.glob("*.xlsx")
        if not archivo.name.startswith("~$")
    )


def cargar_archivo_excel(
    archivo: Path,
    hoja: str = HOJA_EGRESADOS,
) -> pd.DataFrame:
    df = pd.read_excel(archivo, sheet_name=hoja, dtype=str)
    df.columns = [str(col).strip() for col in df.columns]
    return df


archivos = listar_archivos_excel(DIR_EGRESADOS)

print("Archivos encontrados:", len(archivos))
print("Primeros archivos:")
print(archivos[:5])


#%% =============================================================================
# 2. LIMPIEZA Y ARMONIZACIÓN DE CAMPOS PII
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


def armonizar_tipo_documento(tipo_documento: pd.Series) -> pd.Series:
    tipo_norm = normalizar_texto(tipo_documento, upper=True)

    mapa = {
        "CEDULA": "CC",
        "CEDULA DE CIUDADANIA": "CC",
        "TARJETA DE IDENTIDAD": "TI",
        "CEDULA DE EXTRANJERIA": "CE",
        "PASAPORTE": "PA",
        "PERMISO DE RESIDENCIA Y TRABAJO": "OTRO",
        "PERMISO ESPECIAL DE PERMANENCIA": "PEP",
        "OTROS": "OTRO",
    }

    return tipo_norm.map(mapa).fillna(tipo_norm)


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


def combinar_nombre_completo(df: pd.DataFrame) -> pd.Series:
    nombres = obtener_serie(df, "NOMBRES_LEGAL").fillna(
        obtener_serie(df, "NOMBRES")
    )
    ap1 = obtener_serie(df, "APELLIDO1_LEGAL").fillna(
        obtener_serie(df, "PRIMER_APELLIDO")
    )
    ap2 = obtener_serie(df, "APELLIDO2_LEGAL").fillna(
        obtener_serie(df, "SEGUNDO_APELLIDO")
    )

    nombre = (
        nombres.fillna("")
        + " "
        + ap1.fillna("")
        + " "
        + ap2.fillna("")
    )
    nombre = nombre.str.replace(r"\s+", " ", regex=True).str.strip()

    return nombre.str.upper().replace({"": pd.NA})


def armonizar_periodo(df: pd.DataFrame) -> pd.Series:
    p1 = obtener_serie(df, "PERIODO_TERMINACION")
    p2 = obtener_serie(df, "PER_NODO_GRADUACION")
    p3 = obtener_serie(df, "FECHA_GRADUADO")

    return p1.fillna(p2).fillna(p3)


def armonizar_pii_egresados(
    df: pd.DataFrame,
    archivo_origen: str,
) -> pd.DataFrame:
    correo = obtener_serie(df, "EMAIL", lower=True)

    tipo_documento_raw = obtener_serie(df, "T_DOCUMENTO")
    tipo_documento = armonizar_tipo_documento(tipo_documento_raw)

    numero_documento = obtener_serie(df, "DOCUMENTO")
    nombre_completo = combinar_nombre_completo(df)
    periodo = armonizar_periodo(df)

    sexo_raw = obtener_serie(df, "SEXO_LEGAL").fillna(
        obtener_serie(df, "SEXO")
    )
    genero_raw = obtener_serie(df, "GENERO")
    sexo = armonizar_sexo(sexo_raw, genero_raw)

    fecha_nacimiento = obtener_serie(df, "FECHA_NACIMIENTO")
    fecha_nacimiento = pd.to_datetime(fecha_nacimiento, errors="coerce")

    return pd.DataFrame(
        {
            "correo": correo,
            "tipo_documento": tipo_documento,
            "tipo_documento_raw": tipo_documento_raw,
            "numero_documento": numero_documento,
            "nombre_completo": nombre_completo,
            "sexo": sexo,
            "sexo_raw": sexo_raw,
            "genero_raw": genero_raw,
            "periodo": periodo,
            "fecha_nacimiento": fecha_nacimiento,
            "archivo_origen": archivo_origen,
        }
    )


def cargar_y_armonizar_todos_los_egresados(
    archivos: list[Path],
) -> pd.DataFrame:
    dfs = []

    for archivo in archivos:
        df = cargar_archivo_excel(archivo)
        pii = armonizar_pii_egresados(df, archivo.name)
        dfs.append(pii)

    return pd.concat(dfs, ignore_index=True)


all_pii = cargar_y_armonizar_todos_los_egresados(archivos)

print("Filas PII armonizadas:", len(all_pii))
print("Personas únicas por correo:", all_pii["correo"].nunique(dropna=True))
print("Personas únicas por documento:", all_pii["numero_documento"].nunique(dropna=True))


#%% =============================================================================
# 3. MASTER DIAGNÓSTICO
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
        "fecha_nacimiento",
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
print("\nCausas de repetición en master diagnóstico:")
print(causas_repeticion.to_string())


#%% =============================================================================
# 4. COMPLETAR TIPO_DOCUMENTO FALTANTE
# =============================================================================

def completar_tipo_documento_por_persona(all_pii: pd.DataFrame) -> pd.DataFrame:
    df = all_pii.copy()

    df["id_doc_persona"] = (
        df["correo"].fillna("SIN_CORREO")
        + " || "
        + df["numero_documento"].fillna("SIN_DOCUMENTO")
    )

    tipo_por_persona = (
        df.dropna(subset=["tipo_documento"])
        .groupby("id_doc_persona")["tipo_documento"]
        .agg(lambda x: x.mode().iloc[0])
    )

    df["tipo_documento"] = df["tipo_documento"].fillna(
        df["id_doc_persona"].map(tipo_por_persona)
    )

    return df.drop(columns=["id_doc_persona"])


def tabla_frecuencias(serie: pd.Series, nombre: str) -> pd.DataFrame:
    return (
        serie
        .fillna("NA")
        .value_counts(dropna=False)
        .rename_axis(nombre)
        .reset_index(name="n")
    )


all_pii_completo = completar_tipo_documento_por_persona(all_pii)

print("Tipo documento antes de completar:")
print(tabla_frecuencias(all_pii["tipo_documento"], "tipo_documento"))

print("\nTipo documento después de completar:")
print(tabla_frecuencias(all_pii_completo["tipo_documento"], "tipo_documento"))


#%% =============================================================================
# 5. MASTER FINAL
# =============================================================================

def construir_master_personas(all_pii: pd.DataFrame) -> pd.DataFrame:
    all_pii_completo = completar_tipo_documento_por_persona(all_pii)

    all_pii_ordenado = (
        all_pii_completo
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
                "tipo_documento",
            ],
            keep="last",
        )
        .reset_index(drop=True)
    )



# -------------------------
# Detectar conflictos tipo_documento
# -------------------------

def consolidar_tipos_documento(master: pd.DataFrame) -> pd.DataFrame:
    df = master.copy()

    df["id_persona"] = (
        df["correo"].fillna("SIN_CORREO")
        + "||"
        + df["numero_documento"].fillna("SIN_DOCUMENTO")
    )

    tipos_por_persona = (
        df.dropna(subset=["tipo_documento"])
        .groupby("id_persona")["tipo_documento"]
        .agg(lambda x: sorted(set(x)))
    )

    tipos_df = tipos_por_persona.apply(
        lambda x: pd.Series(x[:2])
    ).rename(columns={0: "tipo_documento1", 1: "tipo_documento2"})

    df = df.merge(tipos_df, left_on="id_persona", right_index=True, how="left")

    return df.drop(columns=["id_persona"])

master = construir_master_personas(all_pii)
master = consolidar_tipos_documento(master)

master = (
    master
    .sort_values(["correo", "numero_documento", "periodo"], na_position="last")
    .drop_duplicates(
        subset=["correo", "numero_documento"],
        keep="last"
    )
    .reset_index(drop=True)
)

master = master.rename(columns={
    "genero_raw": "genero"
})

master = master[
    [
        "correo",
        "tipo_documento",
        "tipo_documento2",
        "sexo",
        "numero_documento",
        "nombre_completo",
        "fecha_nacimiento",
        "genero",
        "archivo_origen",
    ]
]

print("Filas en master final:", len(master))
print("Personas únicas por correo en master:", master["correo"].nunique(dropna=True))
print("Personas únicas por documento en master:", master["numero_documento"].nunique(dropna=True))


#%% =============================================================================
# 6. DIAGNÓSTICO DE REPETICIONES EN MASTER FINAL
# =============================================================================

id_persona_final = master["correo"].fillna(master["numero_documento"])

master_final_repetidos = (
    master
    .assign(id_persona=id_persona_final)
    .loc[lambda df: df.duplicated("id_persona", keep=False)]
    .sort_values(["id_persona", "periodo"], na_position="last")
)

columnas_diagnostico_final = [
    "tipo_documento",
    "numero_documento",
    "nombre_completo",
    "sexo",
    "sexo_raw",
    "genero_raw",
    "periodo",
    "fecha_nacimiento",
]

if not master_final_repetidos.empty:
    diagnostico_master_final = (
        master_final_repetidos
        .groupby("id_persona")
        .agg(
            n_filas=("id_persona", "size"),
            **{
                f"n_{col}": (col, lambda x: x.fillna("NA").nunique())
                for col in columnas_diagnostico_final
            }
        )
        .reset_index()
        .sort_values("n_filas", ascending=False)
    )

    causas_master_final = pd.Series({
        col: (diagnostico_master_final[f"n_{col}"] > 1).sum()
        for col in columnas_diagnostico_final
    }).sort_values(ascending=False)
else:
    diagnostico_master_final = pd.DataFrame()
    causas_master_final = pd.Series(dtype="int64")


print("Personas repetidas en master final:", master_final_repetidos["id_persona"].nunique())

if not causas_master_final.empty:
    print("\nCausas de repetición en master final:")
    print(causas_master_final.to_string())

    print("\nDetalle de personas repetidas en master final:")
    print(master_final_repetidos.to_string(index=False))
else:
    print("No hay personas repetidas en master final.")

#%%
# Personas con más de un valor de sexo/género en master final

master_temp = master.assign(
    id_persona=master["correo"].fillna(master["numero_documento"])
)

variacion_sexo_genero_final = (
    master_temp
    .groupby("id_persona")[["sexo", "genero"]]
    .nunique(dropna=False)
)

print("Personas con más de un sexo armonizado:")
print((variacion_sexo_genero_final["sexo"] > 1).sum())


print("Personas con más de un genero:")
print((variacion_sexo_genero_final["genero"] > 1).sum())



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
    df = master.copy()

    mascara_cc = (
        df["tipo_documento"].eq("CC")
        & ~df["numero_documento"].str.match(r"^\d{6,10}$", na=False)
    )

    mascara_ti = (
        df["tipo_documento"].eq("TI")
        & ~df["numero_documento"].str.match(r"^\d{10,11}$", na=False)
    )

    return df[mascara_cc | mascara_ti].copy()


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
    if not DIR_EGRESADOS.exists():
        raise FileNotFoundError(f"No existe la carpeta: {DIR_EGRESADOS}")

    archivos_main = listar_archivos_excel(DIR_EGRESADOS)

    if not archivos_main:
        raise FileNotFoundError(
            f"No se encontraron archivos .xlsx en: {DIR_EGRESADOS}"
        )

    all_pii_main = cargar_y_armonizar_todos_los_egresados(archivos_main)

    master_diag_main = construir_master_diagnostico(all_pii_main)
    diagnostico_repetidos_main, causas_repeticion_main = diagnosticar_repeticiones_master(
        master_diag_main
    )

    all_pii_completo_main = completar_tipo_documento_por_persona(all_pii_main)
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
    print("MASTER PERSONAS - EGRESADOS")
    print("=" * 70)
    print(f"Archivos procesados: {len(archivos_main)}")
    print(f"Total filas cargadas: {len(all_pii_main)}")
    print(f"Filas en master diagnóstico: {len(master_diag_main)}")
    print(f"Filas en master final: {len(master_main)}")

    print("\nTipo documento antes de completar:")
    print(
        tabla_frecuencias(all_pii_main["tipo_documento"], "tipo_documento")
        .to_string(index=False)
    )

    print("\nTipo documento después de completar:")
    print(
        tabla_frecuencias(all_pii_completo_main["tipo_documento"], "tipo_documento")
        .to_string(index=False)
    )

    print("\nCausas de repetición en master diagnóstico:")
    print(causas_repeticion_main.to_string())

    print(
        "\nPersonas repetidas en master final: "
        f"{master_final_repetidos_main['id_persona'].nunique() if not master_final_repetidos_main.empty else 0}"
    )

    print(
        "\nRegistros con formato documental inesperado en master final: "
        f"{len(invalid_format_main)}"
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
        print("\nTodos los tipos de documento observados están reconocidos.")

    if not invalid_format_main.empty:
        print("\nMuestra de registros con formato documental inesperado:")
        print(invalid_format_main.head(10).to_string(index=False))

    guardar_master(master_main)
    print(f"\nGuardado en: {OUTPUT_FILE}")


#%%
if __name__ == "__main__":
    main()