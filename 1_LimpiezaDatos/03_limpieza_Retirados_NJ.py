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
    .pipe(convertir_decimal_a_coma)
    .to_csv(output_file, index=False, encoding="utf-8-sig", sep=";")
)

print("Archivo guardado en:", output_file)

# %%
