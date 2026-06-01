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

LLAVE_PATH = Path(__file__).parent / "LLAVE_ID_UNAL_FCE.csv" 


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


def extraer_anio_semestre(stem: str):
    match = re.search(r"(20\d{2}).*?([12])", stem)
    if match:
        return match.group(1), match.group(2)
    return pd.NA, pd.NA


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

    # nivel titulo (columna fuente: NIVEL)
    "NIVEL": "NIVEL_TITULO",

    # modalidad (columna fuente: MODALIDAD_TG)
    "MODALIDAD_TG": "MODALIDAD",

    # cod plan
    "COD_PLAN": "COD_PLAN",
    "CODIGO_PLAN": "COD_PLAN",
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
    duplicadas = [c for c in df.columns if re.search(r"\.\d+$", c)]
    if duplicadas:
        print(f"  [cargar] columnas duplicadas descartadas en {path.name}: {duplicadas}")
    df = df.drop(columns=duplicadas)
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
# 5. DIAGNÓSTICO: Valores únicos de campos a armonizar (revisar antes de mapear)
# =============================================================================

_campos_unicos = {"NIVEL_TITULO": {}, "MODALIDAD": {}, "COD_PLAN": {}}

for _archivo in listar_archivos():
    _df = homologar_columnas(cargar_archivo(_archivo))
    _sem = _archivo.stem 
    for _campo in _campos_unicos: 
        if _campo in _df.columns:
            _uniq = sorted(_df[_campo].dropna().str.strip().str.upper().unique())
            _campos_unicos[_campo][_sem] = _uniq

print("\n" + "=" * 70)
print("NIVEL_TITULO — valores únicos globales")
print("=" * 70)
for v in sorted({v for vals in _campos_unicos["NIVEL_TITULO"].values() for v in vals}): 
    print(f"  {v!r}")

print("\n" + "=" * 70)
print("MODALIDAD — valores únicos por semestre")
print("=" * 70)
for _sem, vals in _campos_unicos["MODALIDAD"].items():
    print(f"\n  {_sem}")
    for v in vals:
        print(f"    {v!r}")

print("\n" + "-" * 70)
print("MODALIDAD — valores únicos globales")
print("-" * 70)
for v in sorted({v for vals in _campos_unicos["MODALIDAD"].values() for v in vals}):
    print(f"  {v!r}")

print("\n" + "=" * 70)
print("COD_PLAN — resumen")
print("=" * 70)
_cod_global = sorted({v for vals in _campos_unicos["COD_PLAN"].values() for v in vals})
print(f"  Total códigos únicos: {len(_cod_global)}")
print(f"  Primeros 20: {_cod_global[:20]}")

#%% =============================================================================
# 6. LIMPIEZA POR ARCHIVO
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


MAPEO_NIVEL_TITULO = {
    "PREGRADO": "PREGRADO",
    "ESPECIALIZACION": "ESPECIALIZACION",
    "ESPECIALIDAD": "ESPECIALIZACION",   
    "MAESTRIA": "MAESTRIA",
    "DOCTORADO": "DOCTORADO",
}

def armonizar_nivel_titulo(serie: pd.Series) -> pd.Series:
    norm = normalizar_texto(serie, upper=True)
    resultado = norm.map(lambda x: MAPEO_NIVEL_TITULO.get(x, x) if pd.notna(x) else pd.NA)
    no_mapeados = set(norm.dropna()) - set(MAPEO_NIVEL_TITULO)
    if no_mapeados:
        print(f"  [nivel_titulo] valores sin mapeo: {sorted(no_mapeados)}")
    return resultado


MAPEO_MODALIDAD = {
    # 1. Trabajos investigativos (Art. 10 Par., Acuerdo CSU 033/2007)
    #    Subtipos legales: Trabajo monográfico, Participación en proyectos de investigación, Proyecto final
    #    Se incluyen tesis y trabajos de grado genéricos por su naturaleza investigativa
    "TESIS": "TRABAJO_INVESTIGATIVO",
    "TESIS DE DOCTORADO": "TRABAJO_INVESTIGATIVO",
    "TESIS DE MAESTRIA": "TRABAJO_INVESTIGATIVO",
    "TRABAJO DE GRADO": "TRABAJO_INVESTIGATIVO",
    "TRABAJO ESCRITO": "TRABAJO_INVESTIGATIVO",
    "TRABAJO FINAL": "TRABAJO_INVESTIGATIVO",
    "TRABAJO FINAL DE MAESTRIA": "TRABAJO_INVESTIGATIVO",
    "TRABAJOS INVESTIGATIVOS": "TRABAJO_INVESTIGATIVO",
    "TRABAJOS INVESTIGATIVOS / TRABAJO MONOGRAFICO": "TRABAJO_INVESTIGATIVO",
    "TRABAJOS INVESTIGATIVOS /TRABAJO MONOGRAFICO": "TRABAJO_INVESTIGATIVO",
    "TRABAJOS INVESTIGATIVOS / PARTICIPACION EN PROYECTOS DE INVESTIGACION": "TRABAJO_INVESTIGATIVO",
    "TRABAJOS INVESTIGATIVOS / PROYECTO FINAL": "TRABAJO_INVESTIGATIVO",
    # Subtipos de TI registrados erróneamente bajo Prácticas de extensión en la fuente
    "PRACTICAS DE EXTENSION / TRABAJO MONOGRAFICO": "TRABAJO_INVESTIGATIVO",
    "PRACTICAS DE EXTENSION / PARTICIPACION EN PROYECTOS DE INVESTIGACION": "TRABAJO_INVESTIGATIVO",
    "PRACTICAS DE EXTENSION / PROYECTO FINAL": "TRABAJO_INVESTIGATIVO",
    # 2. Prácticas de extensión (Art. 10 Par., Acuerdo CSU 033/2007)
    #    Subtipos legales: Participación en programas docente-asistenciales, Internados médicos,
    #                      Pasantías, Emprendimiento empresarial, Proyecto Social
    "PRACTICAS DE EXTENSION / PARTICIPACION EN PROGRAMAS DOCENTE-ASISTENCIALES": "PRACTICA_EXTENSION",
    "PRACTICAS DE EXTENSION / INTERNADOS MEDICOS": "PRACTICA_EXTENSION",
    "PRACTICAS DE EXTENSION / PASANTIAS": "PRACTICA_EXTENSION",
    "PRACTICAS DE EXTENSION / EMPRENDIMIENTO EMPRESARIAL": "PRACTICA_EXTENSION",
    "PRACTICAS DE EXTENSION / PROYECTO SOCIAL": "PRACTICA_EXTENSION",
    # Pasantías registradas como categoría independiente o bajo Trabajos investigativos en la fuente
    "PASANTIA": "PRACTICA_EXTENSION",
    "PASANTIA COLECTIVO ORLANDO FALS BORDA": "PRACTICA_EXTENSION",
    "TRABAJOS INVESTIGATIVOS / PASANTIAS": "PRACTICA_EXTENSION",
    # 3. Actividades especiales (Art. 10 Par., Acuerdo CSU 033/2007)
    #    Subtipos legales: Exámenes preparatorios
    "ACTIVIDADES ESPECIALES / EXAMENES PREPARATORIOS": "ACTIVIDADES_ESPECIALES",
    "EXAMEN DE HABILIDADES INSTRUMENTALES": "ACTIVIDADES_ESPECIALES",
    # 4. Opción de grado (Art. 10 Par., Acuerdo CSU 033/2007)
    #    Subtipos legales: Asignaturas de posgrado
    "OPCION DE GRADO": "OPCION_GRADO",
    "OPCION DE GRADO / ASIGNATURAS DE POSGRADO": "OPCION_GRADO",
    "OPCION DE GRADO / PROYECTO FINAL": "OPCION_GRADO",
    # Asignaturas de posgrado registradas bajo otras categorías en la fuente
    "TRABAJOS INVESTIGATIVOS / ASIGNATURAS DE POSGRADO": "OPCION_GRADO",
    "PRACTICAS DE EXTENSION / ASIGNATURAS DE POSGRADO": "OPCION_GRADO",
    # Producción artística (no contemplada en Art. 10 Par. — se conserva tal como está en los datos)
    "OBRAS DE CREACION ARTISTICA O PROYECTOS DE DISENO": "PRODUCCION_ARTISTICA",
    "PRODUCCION AUDIOVISUAL": "PRODUCCION_ARTISTICA",
}

_CATEGORIAS_MODALIDAD = set(MAPEO_MODALIDAD.values())

def armonizar_modalidad(serie: pd.Series) -> pd.Series:
    norm = normalizar_texto(serie, upper=True)
    mapeada = norm.map(lambda x: MAPEO_MODALIDAD.get(x, x) if pd.notna(x) else pd.NA)
    # Valores no reconocidos (ruido, errores de captura) → NA con aviso
    no_canonicos = {x for x in mapeada.dropna() if x not in _CATEGORIAS_MODALIDAD}
    if no_canonicos:
        print(f"  [modalidad] valores fuera del canónico → NA: {sorted(no_canonicos)}")
    return mapeada.map(lambda x: x if pd.notna(x) and x in _CATEGORIAS_MODALIDAD else pd.NA)


def estandarizar_cod_plan(serie: pd.Series) -> pd.Series:
    return (
        serie.astype(str)
        .str.strip()
        .replace({"nan": pd.NA, "None": pd.NA, "": pd.NA, "<NA>": pd.NA})
    )


#%% =============================================================================
# 6b. ANONIMIZACIÓN DE CORREO
# =============================================================================

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


COLUMNAS_PII = [
    "NOMBRES", "APELLIDO1", "APELLIDO2",
    "NUMERO_DOCUMENTO", "TIPO_DOCUMENTO",
    "FECHA_NACIMIENTO",
    "NOMBRE_DIRECTOR", "TITULO_TESIS",
    "NOMBRE_TRABAJO_GR",
    "DOC_DIRECTOR", "DIRECTOR",
    "DOC_CODIRECTOR", "CODIRECTOR",
    "DIRECCION_PROCEDENCIA", "TEL_PROCEDENCIA",
    "CARNET_UN",
]

def eliminar_pii(df: pd.DataFrame) -> pd.DataFrame:
    cols_a_eliminar = [c for c in COLUMNAS_PII if c in df.columns]
    return df.drop(columns=cols_a_eliminar)


def convertir_decimal_a_coma(df: pd.DataFrame) -> pd.DataFrame:
    """Reemplaza el punto decimal por coma en columnas numéricas string.

    Necesario porque Excel con locale colombiano interpreta el punto como
    separador de miles y convierte '3.96' en 396.
    Solo afecta strings con formato puro dígitos.punto.dígitos (ej. '3.96').
    """
    df = df.copy()
    patron = r"^(\d+)\.(\d+)$"
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].str.replace(patron, r"\1,\2", regex=True)
    return df


def limpiar_archivo(df, nombre_archivo):

    df = homologar_columnas(df)

    _anio, _semestre = extraer_anio_semestre(Path(nombre_archivo).stem)
    df.insert(0, "academic_semester", _semestre)
    df.insert(0, "academic_anio", _anio)

    for _col_periodo in ("CONVOCATORIA", "APERTURA", "PERIODO_TERMINACION", "PER_NODO_GRADUACION"):
        if _col_periodo in df.columns:
            df[_col_periodo] = df[_col_periodo].apply(estandarizar_periodo)

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

    if "NIVEL_TITULO" in df.columns:
        df["NIVEL_TITULO"] = armonizar_nivel_titulo(df["NIVEL_TITULO"])

    if "MODALIDAD" in df.columns:
        df["MODALIDAD"] = armonizar_modalidad(df["MODALIDAD"])

    if "COD_PLAN" in df.columns:
        df["COD_PLAN"] = estandarizar_cod_plan(df["COD_PLAN"])

    for _col_texto in (
        "DESC_PLAN", "ACCESO", "SUBACCESO", "FACULTAD", "PROGRAMA",
        "SEDE", "TIPO_NIVEL", "NODO_INI", "NODO_FIN",
        "NOMBRE_DEPTO_PROCEDENCIA", "NOMBRE_MUNICIPIO_PROCEDENCIA",
    ):
        if _col_texto in df.columns:
            df[_col_texto] = normalizar_texto(df[_col_texto], upper=True)

    antes = len(df)
    df = df.drop_duplicates()
    despues = len(df)

    print(f"{nombre_archivo}: {antes - despues} duplicados eliminados")

    

    return df

#%% =============================================================================
# 7. LIMPIAR TODOS LOS ARCHIVOS
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
# 8. ESQUEMA GLOBAL (UNIÓN DE COLUMNAS)
# =============================================================================

print("Total columnas finales:", len(columnas_globales))

#%% =============================================================================
# 9. ALINEAR COLUMNAS
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
# 10. GUARDAR CSV LIMPIOS
# =============================================================================

for df, archivo in zip(dfs_finales, archivos):

    output_path = DIR_OUTPUT / f"{archivo.stem}_limpio.csv"

    (
        df
        .pipe(eliminar_pii)
        .pipe(anonimizar_correo)
        .pipe(convertir_decimal_a_coma)
        .to_csv(output_path, index=False, encoding="utf-8-sig", sep=";")
    )

print(" Archivos guardados correctamente")

#%% =============================================================================
# 10b. VALIDACIÓN DE PARES CÓDIGO ↔ DESCRIPCIÓN
# =============================================================================

PARES_COD_DESC = [
    ("COD_PLAN",      "DESC_PLAN"),
    ("COD_ACCESO",    "ACCESO"),
    ("COD_SUBACCESO", "SUBACCESO"),
    ("COD_FACULTAD",  "FACULTAD"),
    ("COD_PROGRAMA",  "PROGRAMA"),
    ("COD_NIVEL",     "TIPO_NIVEL"),
    ("COD_NOD_INI",   "NODO_INI"),
    ("COD_NODO_FIN",  "NODO_FIN"),
]


def validar_par_cod_desc(dfs_lista, col_cod, col_desc):
    fragmentos = [
        df[[col_cod, col_desc]]
        for df in dfs_lista
        if {col_cod, col_desc} <= set(df.columns)
    ]
    if not fragmentos:
        print(f"\n[OMITIDO] ningún archivo contiene {col_cod} y {col_desc}")
        return

    df_par = (
        pd.concat(fragmentos, ignore_index=True)
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
        .reset_index(name="N")
        .query("N > 1")
    )
    desc_multi_cod = (
        df_completo.groupby(col_desc)[col_cod].nunique()
        .reset_index(name="N")
        .query("N > 1")
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
    validar_par_cod_desc(dfs_finales, _col_cod, _col_desc)

#%% Diccionario de programas (Excel) — solo para COD_PROGRAMA <-> PROGRAMA
_dfs_prog = [
    df[["COD_PROGRAMA", "PROGRAMA"]]
    for df in dfs_finales
    if {"COD_PROGRAMA", "PROGRAMA"} <= set(df.columns)
]

if _dfs_prog:
    _diccionario = (
        pd.concat(_dfs_prog, ignore_index=True)
        .dropna(subset=["COD_PROGRAMA", "PROGRAMA"])
        .assign(
            COD_PROGRAMA=lambda d: d["COD_PROGRAMA"].str.strip().str.upper(),
            PROGRAMA=lambda d: d["PROGRAMA"].str.strip().str.upper(),
        )
        .drop_duplicates()
        .groupby("COD_PROGRAMA")["PROGRAMA"]
        .agg(lambda x: " | ".join(sorted(x.unique())))
        .reset_index()
        .rename(columns={"PROGRAMA": "PROGRAMA(S)"})
        .sort_values("COD_PROGRAMA")
        .reset_index(drop=True)
    )
    _dict_path = DIR_OUTPUT / "diccionario_programas.xlsx"
    _diccionario.to_excel(_dict_path, index=False, sheet_name="Programas")
    print(f"\n  Diccionario de programas guardado en: {_dict_path}")
    print(f"  Total programas únicos: {len(_diccionario)}")

#%% =============================================================================
# 10c. VALIDACIÓN DE NOTAS (PROMEDIOS)
# =============================================================================

COLS_NOTAS = [
    "PAPA_SIN_REDONDEO",
    "PAPA",
    "PROM_ACAD_SIN_REDONDEO",
    "PROM_ACADEMICO",
    "PROM_GRADUADO_SIN_REDONDEO",
    "PROM_GRADUADO_SIN_REDONDEDO",   # nombre con typo en algunos archivos fuente
    "PROM_GRADUADO",
]

RANGO_NOTAS = (0.0, 5.0)


def validar_notas(dfs_lista, columnas, rango=RANGO_NOTAS):
    print("\nVALIDACIÓN DE NOTAS")

    for col in columnas:
        fragmentos = [df[col] for df in dfs_lista if col in df.columns]
        if not fragmentos:
            continue

        serie = pd.concat(fragmentos, ignore_index=True)
        serie_num = pd.to_numeric(serie, errors="coerce")

        n_total       = len(serie)
        n_nulos_orig  = serie.isna().sum()
        n_no_numeric  = int(serie_num.isna().sum() - n_nulos_orig)
        n_validos     = int(serie_num.notna().sum())
        fuera_rango   = serie_num[(serie_num < rango[0]) | (serie_num > rango[1])]

        print(f"\n{'=' * 70}")
        print(f"{col}  (filas totales: {n_total})")
        print(f"{'=' * 70}")
        print(f"  Nulos           : {n_nulos_orig}")
        print(f"  No numéricos    : {n_no_numeric}")
        print(f"  Válidos         : {n_validos}")

        if n_validos > 0:
            print(f"  Min / Max       : {serie_num.min():.4f} / {serie_num.max():.4f}")

            if fuera_rango.empty:
                print(f"  OK  todos los valores están en [{rango[0]}, {rango[1]}]")
            else:
                print(f"  WARN  {len(fuera_rango)} valores fuera de [{rango[0]}, {rango[1]}]: "
                      f"{sorted(fuera_rango.unique())[:10]}")


validar_notas(dfs_finales, COLS_NOTAS)

#%% ==============================================================================
# 11. VALIDACIÓN: Revisar columnas en los CSV generados
# ================================================================================
columnas_totales = set()

for archivo in DIR_OUTPUT.glob("*.csv"):
    df = pd.read_csv(archivo, nrows=0, sep=";")
    columnas_totales.update(df.columns)

print("\n Columnas globales:")
print(sorted(columnas_totales))
# %%
for archivo in DIR_OUTPUT.glob("*.csv"):
    df = pd.read_csv(archivo, nrows=0, sep=";")  # solo carga columnas
    print(f"\n {archivo.name}")
    print(df.columns.tolist())
# %%
listas = []

for archivo in DIR_OUTPUT.glob("*.csv"):
    df = pd.read_csv(archivo, nrows=0, sep=";")
    listas.append(set(df.columns))

base = listas[0]

for i, cols in enumerate(listas):
    if cols != base:
        print(f"⚠️ Archivo {i} tiene diferencias")
# %%
