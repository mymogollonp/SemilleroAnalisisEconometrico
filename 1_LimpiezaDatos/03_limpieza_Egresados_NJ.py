#%% =============================================================================
# 0. SETUP
# =============================================================================

from pathlib import Path
import pandas as pd
import unicodedata
import re

from config import DIR_DATOS

DIR_INPUT = DIR_DATOS / "DatosOriginales" / "Egresados"
DIR_OUTPUT = DIR_DATOS / "DatosArmonizados" / "archivos_limpios_egresados"
HOJA = "Sheet2"

DIR_OUTPUT.mkdir(parents=True, exist_ok=True)


#%% =============================================================================
# 1. UTILIDADES
# =============================================================================

def quitar_tildes(texto: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFKD", texto)
        if not unicodedata.combining(c)
    )


def limpiar_nombre_columna(col: str) -> str:
    col = col.strip().upper()
    col = quitar_tildes(col)
    col = re.sub(r"\s+", "_", col)
    return col


def estandarizar_periodo(valor: str) -> str:
    if pd.isna(valor):
        return pd.NA

    valor = str(valor).strip().upper()

    # Ej: 2024-1S, 2024 1, 20241
    match = re.search(r"(20\d{2}).*?([12])", valor)
    if match:
        return f"{match.group(1)}-{match.group(2)}S"

    return valor


def estandarizar_fecha(valor: str):
    return pd.to_datetime(valor, errors="coerce")


#%% =============================================================================
# 2. MAPEO DE COLUMNAS 
# =============================================================================

MAPEO_COLUMNAS = {
    # nombres
    "NOMBRES": "NOMBRES",
    "NOMBRES_LEGAL": "NOMBRES",
    "PRIMER_APELLIDO": "APELLIDO1",
    "APELLIDO1_LEGAL": "APELLIDO1",
    "SEGUNDO_APELLIDO": "APELLIDO2",
    "APELLIDO2_LEGAL": "APELLIDO2",

    # sexo/genero
    "SEXO": "SEXO",
    "SEXO_LEGAL": "SEXO",
    "GENERO": "GENERO",

    # documento
    "DOCUMENTO": "NUMERO_DOCUMENTO",
    "T_DOCUMENTO": "TIPO_DOCUMENTO",

    # fechas
    "FECHA_GRADUADO": "FECHA_GRADO",
    "FECHA_NACIMIENTO": "FECHA_NACIMIENTO",

   

    # correo
    "EMAIL": "CORREO",
}


#%% =============================================================================
# 3. LISTAR Y CARGAR ARCHIVOS
# =============================================================================

def listar_archivos():
    return sorted(
        f for f in DIR_INPUT.glob("*.xlsx")
        if not f.name.startswith("~$")
    )

archivos = listar_archivos()

print("Archivos encontrados:", len(archivos))
print("Primeros:", archivos[:3])


def cargar_archivo(path):
    df = pd.read_excel(path, sheet_name=HOJA, dtype=str)
    df.columns = [limpiar_nombre_columna(c) for c in df.columns]
    return df

#%% =============================================================================
# 4. HOMOLOGAR COLUMNAS
# =============================================================================

def homologar_columnas(df):
    df = df.copy()

    nuevas = {
        col: MAPEO_COLUMNAS.get(col, col)
        for col in df.columns
    }

    return df.rename(columns=nuevas)

#%% =============================================================================
# 5. LIMPIEZA POR ARCHIVO
# =============================================================================
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



def limpiar_archivo(df, nombre_archivo):

    df = homologar_columnas(df)

    if "PERIODO" in df.columns:
        df["PERIODO"] = df["PERIODO"].apply(estandarizar_periodo)

    if "FECHA_GRADO" in df.columns:
        df["FECHA_GRADO"] = estandarizar_fecha(df["FECHA_GRADO"])

    if "FECHA_NACIMIENTO" in df.columns:
        df["FECHA_NACIMIENTO"] = estandarizar_fecha(df["FECHA_NACIMIENTO"])

    if "CORREO" in df.columns:
        df["CORREO"] = df["CORREO"].str.lower().str.strip()


    if "SEXO" in df.columns or "GENERO" in df.columns:
            df["SEXO"] = armonizar_sexo(
                obtener_serie(df, "SEXO"),
                obtener_serie(df, "GENERO")
            )

    antes = len(df)
    df = df.drop_duplicates()
    despues = len(df)

    print(f"{nombre_archivo}: {antes - despues} duplicados eliminados")

    

    return df

#%% =============================================================================
# 6. LIMPIAR TODOS LOS ARCHIVOS
# =============================================================================

dfs_limpios = []

for archivo in archivos:
    df = cargar_archivo(archivo)
    df_clean = limpiar_archivo(df, archivo.name)
    dfs_limpios.append(df_clean)

print("Archivos procesados:", len(dfs_limpios))

# Construir lista global de columnas (orden consistente)
columnas_globales = list(dfs_limpios[0].columns)

for df in dfs_limpios[1:]:
    for col in df.columns:
        if col not in columnas_globales:
            columnas_globales.append(col)

#%% =============================================================================
# 7. ESQUEMA GLOBAL (UNIÓN DE COLUMNAS)
# =============================================================================

print("Total columnas finales:", len(columnas_globales))

#%% =============================================================================
# 8. ALINEAR COLUMNAS
# =============================================================================

def alinear_columnas(df, columnas_objetivo):
    df = df.copy()

    for col in columnas_objetivo:
        if col not in df.columns:
            df[col] = pd.NA

    return df[columnas_objetivo]

dfs_finales = [
    alinear_columnas(df, columnas_globales)
    for df in dfs_limpios
]


#%% =============================================================================
# 9. GUARDAR CSV LIMPIOS
# =============================================================================

for df, archivo in zip(dfs_finales, archivos):

    output_path = DIR_OUTPUT / f"{archivo.stem}_limpio.csv"

    df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(" Archivos guardados correctamente")
#%% ==============================================================================
# 10. VALIDACIÓN: Revisar columnas en los CSV generados
# ================================================================================
columnas_totales = set()

for archivo in DIR_OUTPUT.glob("*.csv"):
    df = pd.read_csv(archivo, nrows=0)
    columnas_totales.update(df.columns)

print("\n Columnas globales:")
print(sorted(columnas_totales))
# %%
for archivo in DIR_OUTPUT.glob("*.csv"):
    df = pd.read_csv(archivo, nrows=0)  # solo carga columnas
    print(f"\n {archivo.name}")
    print(df.columns.tolist())
# %%
listas = []

for archivo in DIR_OUTPUT.glob("*.csv"):
    df = pd.read_csv(archivo, nrows=0)
    listas.append(set(df.columns))

base = listas[0]

for i, cols in enumerate(listas):
    if cols != base:
        print(f"⚠️ Archivo {i} tiene diferencias")
# %%
