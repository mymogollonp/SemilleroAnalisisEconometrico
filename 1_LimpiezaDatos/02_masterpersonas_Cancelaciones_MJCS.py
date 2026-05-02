#%%
"""
Armonización de Cancelaciones — UNAL FCE
=======================================
RA: Maria Jose Cadena
Script: 02_masterpersonas_Cancelaciones_MJCS.py
Proyecto: Semillero de Análisis Econométrico

Nota de diseño:
  - La fuente no contiene columnas de tipo_documento ni sexo/género.
  - Ambas columnas se incluyen en el output como NaN para mantener
    el esquema canónico. NO se infiere ni imputa ningún valor.
"""
import sys
import unicodedata
import pandas as pd
import numpy as np
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import DIR_DATOS

# -----------------------------------------------------------------------------
# 0. RUTAS
# -----------------------------------------------------------------------------

RUTA_DATOS     = DIR_DATOS / "DatosOriginales" / "Cancelaciones"
RUTA_OUTPUT    = DIR_DATOS / "DatosArmonizados" / "keys"
ARCHIVO_SALIDA = RUTA_OUTPUT / "MASTER_PERSONAS_CANCELACIONES_PII.csv"

assert RUTA_DATOS.exists(),  f"Ruta de datos no encontrada: {RUTA_DATOS}"
assert RUTA_OUTPUT.exists(), f"Ruta de output no encontrada: {RUTA_OUTPUT}"

# -----------------------------------------------------------------------------
# 1. FUNCIONES
# -----------------------------------------------------------------------------

def inferir_periodo(nombre_archivo: str) -> str | None:
    """Extrae el período académico del nombre del archivo (ej. '2012-2S')."""
    match = re.search(r"\d{4}-[12]S", nombre_archivo)
    if match:
        return match.group()
    match = re.search(r"\d{5}", nombre_archivo)
    if match:
        return f"{match.group()[:4]}-{match.group()[4]}S"
    return None


def quitar_tildes(texto) -> str:
    """Elimina tildes, diéresis y convierte ñ → N. Deja el resto intacto."""
    if pd.isna(texto):
        return texto
    nfkd = unicodedata.normalize("NFD", str(texto))
    return "".join(c for c in nfkd if not unicodedata.combining(c))



# -----------------------------------------------------------------------------
# 2. LECTURA ITERATIVA — todos los archivos del módulo
# -----------------------------------------------------------------------------

archivos = sorted(RUTA_DATOS.glob("*.xlsx"))
assert len(archivos) > 0, f"No se encontraron archivos .xlsx en {RUTA_DATOS}"

print(f"Archivos encontrados: {len(archivos)}")

registros = []
log       = []

# Archivos cuya hoja de datos no es la primera (sheet_name=0).
# Clave: nombre del archivo SIN extensión. Valor: nombre o índice de la hoja.
HOJAS_ESPECIALES: dict[str, str | int] = {
    "Cancelaciones_2024-2S": "Sheet2",
}

COLS_CLAVE = {"correo_institucional", "documento", "nombres_apellidos"}

for i, archivo in enumerate(archivos, 1):
    print(f"[{i}/{len(archivos)}] {archivo.name}")

    periodo = inferir_periodo(archivo.name)
    hoja    = HOJAS_ESPECIALES.get(archivo.stem, 0)   # 0 = primera hoja por defecto

    try:
        df = pd.read_excel(archivo, sheet_name=hoja, dtype=str)
        df.columns = df.columns.str.lower().str.strip()

        # Fallback: si la hoja elegida no tiene columnas clave, avisar (no reintentar
        # a ciegas para evitar leer datos incorrectos silenciosamente).
        if COLS_CLAVE.isdisjoint(df.columns):
            print(f"  AVISO: hoja '{hoja}' de {archivo.name} no tiene columnas clave.")
            print(f"  Columnas encontradas: {list(df.columns)}")
            print(f"  → Agregar a HOJAS_ESPECIALES si la hoja correcta es otra.")

    except Exception as e:
        print(f"  ERROR leyendo archivo: {e}")
        continue

    if df.empty:
        print("  Archivo vacío, se omite.")
        continue

    # Devuelve la columna si existe; si no, una Serie de NaN con el mismo índice.
    # Pasar None a pd.DataFrame() causa ValueError porque pandas no sabe el tamaño.
    def get(col):
        return df[col] if col in df.columns else pd.Series(np.nan, index=df.index)

    correo     = get("correo_institucional")
    numero_doc = get("documento")
    nombre     = get("nombres_apellidos")

    log.append({
        "archivo"      : archivo.name,
        "periodo"      : periodo,
        "n_obs"        : len(df),
        "tiene_correo" : "correo_institucional" in df.columns,
        "tiene_num_doc": "documento"            in df.columns,
        "tiene_nombre" : "nombres_apellidos"    in df.columns,
    })

    df_clean = pd.DataFrame({
        "fuente"          : "Cancelaciones",   # módulo de origen
        "correo"          : correo.values,
        "tipo_documento"  : np.nan,            # no disponible en esta fuente
        "numero_documento": numero_doc.values,
        "nombre_completo" : nombre.values,
        "sexo"            : np.nan,            # no disponible en esta fuente
        "fecha_nacimiento": np.nan,            # no disponible en esta fuente
        "periodo"         : periodo,
        "archivo_fuente"  : archivo.name,
    })

    registros.append(df_clean)

df_all = pd.concat(registros, ignore_index=True)
print(f"\nTotal registros apilados: {len(df_all)}")

# -----------------------------------------------------------------------------
# 3. LIMPIEZA
# -----------------------------------------------------------------------------

df_all["correo"]           = df_all["correo"].str.strip().str.lower()
df_all["numero_documento"] = df_all["numero_documento"].str.strip()
df_all["nombre_completo"]  = (
    df_all["nombre_completo"]
    .str.strip()
    .str.upper()
    .apply(quitar_tildes)        # sin tildes ni ñ
)

# Eliminar filas sin correo (sin correo no se puede identificar la persona)
df_all = df_all[df_all["correo"].notna() & (df_all["correo"] != "")]
print(f"Registros con correo válido: {len(df_all)}")

# -----------------------------------------------------------------------------
# 4. HISTORIAS — conservar TODOS los valores observados por persona
# -----------------------------------------------------------------------------

# Documentos: todos los números y tipos distintos por persona
df_docs = (
    df_all.dropna(subset=["numero_documento"])
    .drop_duplicates(["correo", "tipo_documento", "numero_documento"])
)

# Nombres: todas las variantes observadas
df_nombres = (
    df_all.dropna(subset=["nombre_completo"])
    .drop_duplicates(["correo", "nombre_completo"])
)

# Períodos observados por persona: todos los períodos concatenados con " | "
periodos_obs = (
    df_all.dropna(subset=["periodo"])
    .drop_duplicates(["correo", "periodo"])
    .sort_values(["correo", "periodo"])
    .groupby("correo")["periodo"]
    .apply(lambda x: " | ".join(x))
    .reset_index(name="periodos_observados")
)

# Master: una fila por persona (correo único) con el nombre más reciente
df_master = (
    df_all.sort_values("periodo")
    .drop_duplicates(["correo", "numero_documento", "nombre_completo"])
    .drop_duplicates("correo", keep="last")   # un registro por persona
    .copy()
)

df_master = df_master.merge(periodos_obs, on="correo", how="left")

# Esquema canónico final
df_master = df_master[[
    "fuente", "correo", "tipo_documento", "numero_documento",
    "nombre_completo", "sexo", "fecha_nacimiento", "periodos_observados"
]]

# -----------------------------------------------------------------------------
# 5. VALIDACIONES
# -----------------------------------------------------------------------------

# Formato básico del número de documento (sin asumir tipo)
def validar_formato_doc(numero) -> str:
    if pd.isna(numero) or str(numero).strip() == "":
        return np.nan
    numero = str(numero).strip()
    if re.match(r"^\d{6,11}$", numero):
        return "numerico_valido"
    elif re.match(r"^[a-zA-Z0-9]+$", numero):
        return "alfanumerico"
    return "invalido"

df_master["validez_doc"] = df_master["numero_documento"].apply(validar_formato_doc)
invalidos = df_master[df_master["validez_doc"] == "invalido"]

# -----------------------------------------------------------------------------
# 6. OUTPUT
# -----------------------------------------------------------------------------

df_master.to_csv(ARCHIVO_SALIDA, index=False, encoding="utf-8-sig")
print(f"\nGuardado en: {ARCHIVO_SALIDA}")

# -----------------------------------------------------------------------------
# 7. REPORTE DE CALIDAD
# -----------------------------------------------------------------------------

sep = "=" * 60
print(f"\n{sep}")
print("  REPORTE DE CALIDAD — MASTER PERSONAS CANCELACIONES")
print(sep)

print(f"\nArchivos procesados             : {len(archivos)}")
print(f"Registros apilados (total)      : {len(df_all)}")
print(f"Personas únicas (correos)       : {df_master['correo'].nunique()}")

print("\n--- tipo_documento, sexo y fecha_nacimiento ---")
print("  Las tres columnas son NaN en esta fuente (no disponibles).")

print(f"\n--- Formato de número de documento ---")
print(f"  Registros con formato inválido: {len(invalidos)}")
if len(invalidos) > 0:
    print(invalidos[["correo", "numero_documento"]].head(10).to_string(index=False))

print("\n--- Log de archivos ---")
print(pd.DataFrame(log).to_string(index=False))

print(f"\n{sep}")
print("  Fin del reporte")
print(sep)

# %%