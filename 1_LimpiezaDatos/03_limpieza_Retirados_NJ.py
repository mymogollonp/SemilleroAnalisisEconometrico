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


#%% =============================================================================
# 4. LIMPIEZA BASE
# =============================================================================

# Estandarizar periodo
if "PERIODO_BLOQUEO" in df.columns:
    df["PERIODO_BLOQUEO"] = df["PERIODO_BLOQUEO"].apply(estandarizar_periodo)


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
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print("Archivo guardado en:", output_file)

# %%
