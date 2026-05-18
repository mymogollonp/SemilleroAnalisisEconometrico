#%% =============================================================================
# 1. IMPORTS Y CONFIG
# =============================================================================

from pathlib import Path
import unicodedata
import pandas as pd

from config import DIR_DATOS

ARCHIVO_RETIRADOS = (
    DIR_DATOS
    / "DatosOriginales"
    / "Retirados"
    / "Retirados_desde_2009.xlsx"
)

OUTPUT_DIR = DIR_DATOS / "DatosArmonizados" / "retirados_limpios"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

LLAVE_PATH = Path(__file__).parent / "LLAVE_ID_UNAL_FCE.csv"


#%% =============================================================================
# 2. CARGA
# =============================================================================

df = pd.read_excel(ARCHIVO_RETIRADOS, dtype=str)
df.columns = [str(col).strip() for col in df.columns]

print("Filas cargadas:", len(df))
print("Columnas:", len(df.columns))


#%% =============================================================================
# 3. FUNCIONES BASE
# =============================================================================

def quitar_tildes(texto: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFKD", texto)
        if not unicodedata.combining(c)
    )


def estandarizar_periodo(valor: str) -> str:
    if pd.isna(valor):
        return pd.NA

    valor = str(valor)

    # ejemplos: 2024-1, 2024-1S, 20241
    if "-" in valor:
        año, sem = valor.split("-")
    else:
        año, sem = valor[:4], valor[4:]

    sem = sem.replace("S", "")

    return f"{año}-{sem}S"


MAPEO_NIVEL_TITULO = {
    "PREGRADO": "PREGRADO",
    "ESPECIALIZACION": "ESPECIALIZACION",
    "ESPECIALIDAD": "ESPECIALIZACION",
    "MAESTRIA": "MAESTRIA",
    "DOCTORADO": "DOCTORADO",
}

def armonizar_nivel(serie: pd.Series) -> pd.Series:
    norm = serie.astype(str).str.strip().map(quitar_tildes).str.upper()
    norm = norm.where(norm != "NAN", other=pd.NA)
    resultado = norm.map(lambda x: MAPEO_NIVEL_TITULO.get(x, x) if pd.notna(x) else pd.NA)
    no_mapeados = set(norm.dropna()) - set(MAPEO_NIVEL_TITULO)
    if no_mapeados:
        print(f"  [nivel] valores sin mapeo: {sorted(no_mapeados)}")
    return resultado


_llave = pd.read_csv(LLAVE_PATH, dtype=str)
_llave["correo"] = _llave["correo"].str.lower().str.strip()
MAPA_CORREO_ID = _llave.set_index("correo")["id_unal"].to_dict()


def anonimizar_correo(df: pd.DataFrame) -> pd.DataFrame:
    if "CORREO" not in df.columns:
        return df
    df = df.copy()
    df["CORREO"] = df["CORREO"].str.lower().str.strip()
    sin_match = df["CORREO"].dropna()
    sin_match = sin_match[~sin_match.isin(MAPA_CORREO_ID)]
    if not sin_match.empty:
        print(f"  [anonimizar] {len(sin_match)} correos sin llave: {sorted(sin_match.unique())[:5]}")
    df["ID_UNAL"] = df["CORREO"].map(MAPA_CORREO_ID)
    return df.drop(columns=["CORREO"])


COLUMNAS_PII = ["DOCUMENTO", "NOMBRES_LEGAL", "APELLIDO1_LEGAL", "APELLIDO2_LEGAL"]

def eliminar_pii(df: pd.DataFrame) -> pd.DataFrame:
    cols_a_eliminar = [c for c in COLUMNAS_PII if c in df.columns]
    return df.drop(columns=cols_a_eliminar)


def convertir_decimal_a_coma(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    patron = r"^(\d+)\.(\d+)$"
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].str.replace(patron, r"\1,\2", regex=True)
    return df


#%% =============================================================================
# 4. LIMPIEZA BASE
# =============================================================================

# Estandarizar periodo
if "PERIODO_BLOQUEO" in df.columns:
    df["PERIODO_BLOQUEO"] = df["PERIODO_BLOQUEO"].apply(estandarizar_periodo)

# Armonizar nivel
if "NIVEL" in df.columns:
    df["NIVEL"] = armonizar_nivel(df["NIVEL"])


#%% =============================================================================
# 5. VALIDACIÓN COD_BLOQUEO vs BLOQUEO
# =============================================================================

validacion = (
    df
    .dropna(subset=["COD_BLOQUEO", "BLOQUEO"])
    .groupby("COD_BLOQUEO")["BLOQUEO"]
    .nunique()
    .reset_index(name="n_descripciones")
)

inconsistentes = validacion[validacion["n_descripciones"] > 1]

print("Códigos inconsistentes:", len(inconsistentes))

if not inconsistentes.empty:
    print("\nDetalle inconsistencias:")
    print(
        df[df["COD_BLOQUEO"].isin(inconsistentes["COD_BLOQUEO"])]
        [["COD_BLOQUEO", "BLOQUEO"]]
        .drop_duplicates()
        .sort_values(["COD_BLOQUEO"])
        .to_string(index=False)
    )

#%% =============================================================================
# 6. ELIMINAR DUPLICADOS EXACTOS
# =============================================================================

antes = len(df)
df = df.drop_duplicates()
despues = len(df)

print("Duplicados eliminados:", antes - despues)


#%% =============================================================================
# 7. OUTPUT
# =============================================================================

output_file = OUTPUT_DIR / "retirados_limpio.csv"
(
    df
    .pipe(eliminar_pii)
    .pipe(anonimizar_correo)
    .pipe(convertir_decimal_a_coma)
    .to_csv(output_file, index=False, encoding="utf-8-sig", sep=";")
)

print("Archivo guardado en:", output_file)

#%% =============================================================================
# 8. VERIFICACIÓN 1-a-1: COD_PROGRAMA ↔ PROGRAMA  +  Complementar diccionario
# =============================================================================

_cols_requeridas = {"COD_PROGRAMA", "PROGRAMA"}

if not (_cols_requeridas <= set(df.columns)):
    print("\n[PROGRAMAS] El archivo no contiene COD_PROGRAMA y/o PROGRAMA — sección omitida.")
else:
    _df_prog = (
        df[["COD_PROGRAMA", "PROGRAMA"]]
        .dropna(subset=["COD_PROGRAMA", "PROGRAMA"])
        .assign(
            COD_PROGRAMA=lambda d: d["COD_PROGRAMA"].str.strip().str.upper(),
            PROGRAMA=lambda d: d["PROGRAMA"].str.strip().str.upper(),
        )
        .drop_duplicates()
    )

    # Verificación 1-a-1
    _por_codigo = (
        _df_prog.groupby("COD_PROGRAMA")["PROGRAMA"]
        .nunique()
        .reset_index()
        .rename(columns={"PROGRAMA": "N_PROGRAMAS"})
    )
    _conflictos = _por_codigo[_por_codigo["N_PROGRAMAS"] > 1]

    print("\n" + "=" * 70)
    print("VERIFICACIÓN 1-a-1: COD_PROGRAMA → PROGRAMA (Retirados)")
    print("=" * 70)
    if _conflictos.empty:
        print("  OK — cada código apunta a un único nombre de programa.")
    else:
        print(f"  CONFLICTOS: {len(_conflictos)} código(s) con más de un nombre:")
        for _, _row in _conflictos.iterrows():
            _nombres = sorted(
                _df_prog.loc[
                    _df_prog["COD_PROGRAMA"] == _row["COD_PROGRAMA"], "PROGRAMA"
                ].unique()
            )
            print(f"    {_row['COD_PROGRAMA']!r}  →  {_nombres}")

    # Complementar diccionario generado por el script de Egresados
    _dict_path = (
        DIR_DATOS
        / "DatosArmonizados"
        / "archivos_limpios_egresados"
        / "diccionario_programas.xlsx"
    )

    if _dict_path.exists():
        _dict_existente = pd.read_excel(_dict_path, dtype=str)
        _codigos_existentes = set(_dict_existente["COD_PROGRAMA"].str.strip().str.upper())
    else:
        _dict_existente = pd.DataFrame(columns=["COD_PROGRAMA", "PROGRAMA(S)"])
        _codigos_existentes = set()

    _nuevos = _df_prog[~_df_prog["COD_PROGRAMA"].isin(_codigos_existentes)]
    _nuevos_dict = (
        _nuevos.groupby("COD_PROGRAMA")["PROGRAMA"]
        .agg(lambda x: " | ".join(sorted(x.unique())))
        .reset_index()
        .rename(columns={"PROGRAMA": "PROGRAMA(S)"})
    )

    print("\n" + "-" * 70)
    if _nuevos_dict.empty:
        print("  Sin programas nuevos — el diccionario de Egresados ya los cubre todos.")
    else:
        print(f"  {len(_nuevos_dict)} programa(s) nuevos encontrados en Retirados:")
        for _, _row in _nuevos_dict.iterrows():
            print(f"    {_row['COD_PROGRAMA']!r}  →  {_row['PROGRAMA(S)']!r}")

        _dict_actualizado = (
            pd.concat([_dict_existente, _nuevos_dict], ignore_index=True)
            .sort_values("COD_PROGRAMA")
            .reset_index(drop=True)
        )
        _dict_actualizado.to_excel(_dict_path, index=False, sheet_name="Programas")
        print(f"\n  Diccionario actualizado en: {_dict_path}")
        print(f"  Total programas en el diccionario: {len(_dict_actualizado)}")

# %%
