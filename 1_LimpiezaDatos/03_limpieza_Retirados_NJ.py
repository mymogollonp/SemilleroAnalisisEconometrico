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

# Estandarizar periodos
for _col_periodo in ("PERIODO_BLOQUEO", "CONVOCATORIA", "APERTURA"):
    if _col_periodo in df.columns:
        df[_col_periodo] = df[_col_periodo].apply(estandarizar_periodo)

# Armonizar nivel
if "NIVEL" in df.columns:
    df["NIVEL"] = armonizar_nivel(df["NIVEL"])


#%% =============================================================================
# 5. VALIDACIÓN DE PARES CÓDIGO ↔ DESCRIPCIÓN
# =============================================================================

PARES_COD_DESC = [
    ("COD_FACULTAD",              "FACULTAD"),
    ("COD_UAB",                   "UAB"),
    ("COD_PROGRAMA",              "PROGRAMA"),
    ("COD_PLAN",                  "PLAN"),
    ("COD_ACCESO",                "NOMBRE_ACCESO"),
    ("COD_SUBACCESO",             "NOMBRE_SUBACCESO"),
    ("COD_NODO_INICIO",           "NODO_INICIO"),
    ("COD_PAIS_NACIMIENTO",       "PAIS_NACIMIENTO"),
    ("COD_DEPTO_NACIMIENTO",      "DEPTO_NACIMIENTO"),
    ("COD_MUN_NACIMIENTO",        "MUN_NACIMIENTO"),
    ("COD_COLEGIO",               "COLEGIO"),
    ("COD_DEPARTAMENTO_COLEGIO",  "DEPARTAMENTO_COLEGIO"),
    ("COD_MUNICIPIO_COLEGIO",     "MUNICIPIO_COLEGIO"),
]


def validar_par_cod_desc(df, col_cod, col_desc):
    if not {col_cod, col_desc} <= set(df.columns):
        print(f"\n[OMITIDO] {col_cod} y/o {col_desc} no están en el archivo")
        return

    df_par = (
        df[[col_cod, col_desc]]
        .assign(**{
            col_cod:  lambda d: d[col_cod].str.strip().str.upper(),
            col_desc: lambda d: d[col_desc].str.strip().str.upper(),
        })
        .drop_duplicates()
    )

    cod_sin_desc  = df_par[df_par[col_cod].notna()  & df_par[col_desc].isna()]
    desc_sin_cod  = df_par[df_par[col_cod].isna()   & df_par[col_desc].notna()]
    df_completo   = df_par.dropna(subset=[col_cod, col_desc])

    cod_multi_desc = (
        df_completo.groupby(col_cod)[col_desc].nunique()
        .reset_index(name="N").query("N > 1")
    )
    desc_multi_cod = (
        df_completo.groupby(col_desc)[col_cod].nunique()
        .reset_index(name="N").query("N > 1")
    )

    print(f"\n{'=' * 70}")
    print(f"{col_cod} <-> {col_desc}  (pares únicos: {len(df_par)})")
    print(f"{'=' * 70}")

    if cod_sin_desc.empty:
        print("  OK  códigos sin descripción: ninguno")
    else:
        print(f"  WARN  códigos sin descripción ({len(cod_sin_desc)}): "
              f"{sorted(cod_sin_desc[col_cod].unique())[:10]}")

    if desc_sin_cod.empty:
        print("  OK  descripciones sin código: ninguna")
    else:
        print(f"  WARN  descripciones sin código ({len(desc_sin_cod)}): "
              f"{sorted(desc_sin_cod[col_desc].unique())[:10]}")

    if cod_multi_desc.empty:
        print("  OK  cada código apunta a una única descripción")
    else:
        print(f"  WARN  códigos con múltiples descripciones ({len(cod_multi_desc)}):")
        for _, row in cod_multi_desc.iterrows():
            vals = sorted(df_completo.loc[df_completo[col_cod] == row[col_cod], col_desc].unique())
            print(f"      {row[col_cod]!r} -> {vals}")

    if desc_multi_cod.empty:
        print("  OK  cada descripción apunta a un único código")
    else:
        print(f"  WARN  descripciones con múltiples códigos ({len(desc_multi_cod)}):")
        for _, row in desc_multi_cod.iterrows():
            vals = sorted(df_completo.loc[df_completo[col_desc] == row[col_desc], col_cod].unique())
            print(f"      {row[col_desc]!r} <- {vals}")


print("VALIDACIÓN DE PARES CÓDIGO <-> DESCRIPCIÓN")
for _col_cod, _col_desc in PARES_COD_DESC:
    validar_par_cod_desc(df, _col_cod, _col_desc)

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
# 8. COMPLEMENTAR DICCIONARIO DE PROGRAMAS
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

#%% =============================================================================
# 9. VALIDACIÓN DE NOTAS (PROMEDIOS)
# =============================================================================

COLS_NOTAS = ["PAPA", "PROM_ACADEMICO"]
RANGO_NOTAS = (0.0, 5.0)

print("\nVALIDACIÓN DE NOTAS")

for _col in COLS_NOTAS:
    if _col not in df.columns:
        print(f"\n  [OMITIDO] {_col} no está en el archivo")
        continue

    _serie_num = pd.to_numeric(df[_col], errors="coerce")
    _n_nulos       = df[_col].isna().sum()
    _n_no_numeric  = int(_serie_num.isna().sum() - _n_nulos)
    _n_validos     = int(_serie_num.notna().sum())
    _fuera_rango   = _serie_num[(_serie_num < RANGO_NOTAS[0]) | (_serie_num > RANGO_NOTAS[1])]

    print(f"\n{'=' * 70}")
    print(f"{_col}  (filas totales: {len(df)})")
    print(f"{'=' * 70}")
    print(f"  Nulos           : {_n_nulos}")
    print(f"  No numéricos    : {_n_no_numeric}")
    print(f"  Válidos         : {_n_validos}")

    if _n_validos > 0:
        print(f"  Min / Max       : {_serie_num.min():.4f} / {_serie_num.max():.4f}")
        if _fuera_rango.empty:
            print(f"  OK  todos los valores están en [{RANGO_NOTAS[0]}, {RANGO_NOTAS[1]}]")
        else:
            print(f"  WARN  {len(_fuera_rango)} valores fuera de [{RANGO_NOTAS[0]}, {RANGO_NOTAS[1]}]: "
                  f"{sorted(_fuera_rango.unique())[:10]}")
# %%
