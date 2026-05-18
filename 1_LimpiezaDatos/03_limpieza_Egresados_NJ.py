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

    if "NIVEL_TITULO" in df.columns:
        df["NIVEL_TITULO"] = armonizar_nivel_titulo(df["NIVEL_TITULO"])

    if "MODALIDAD" in df.columns:
        df["MODALIDAD"] = armonizar_modalidad(df["MODALIDAD"])

    if "COD_PLAN" in df.columns:
        df["COD_PLAN"] = estandarizar_cod_plan(df["COD_PLAN"])

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
