# =============================================================================
# Script   : 03_base_cancelaciones.py
# Equipo   : Semillero de Análisis Econométrico — UNAL FCE
# Propósito: Fase 8 — Construcción de Base de Trabajo: Cancelaciones
#            A partir del archivo anonimizado producido por 05b, construye
#            BASE_CANCELACIONES.csv con exactamente las variables especificadas.
# Input    : DatosArmonizados/Cancelaciones/2_DatosLimpios/*.csv
#            (output de 05_anonimizacion_Cancelaciones_MJC.py)
# Output   : DatosArmonizados/Cancelaciones/3_BasedeTrabajo/BASE_CANCELACIONES.csv
# Regla    : Los archivos en DatosOriginales/ NUNCA se modifican.
#            Esta base contiene exclusivamente las variables aprobadas por PI/CoPI.
# =============================================================================

import pandas as pd
import numpy as np
import sys
import logging
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import DIR_DATOS  # type: ignore
from config import DIR_CODE   # type: ignore

INPUT_PATH  = DIR_DATOS / "DatosArmonizados" / "Cancelaciones" / "1_DatosAnonimizados"
OUTPUT_DIR  = DIR_DATOS / "DatosArmonizados" / "Cancelaciones" / "3_BasedeTrabajo"
OUTPUT_PATH = OUTPUT_DIR / "BASE_CANCELACIONES.csv"
LOG_PATH    = DIR_CODE / "logs" / "03_base_cancelaciones.log"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
(DIR_CODE / "logs").mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Logger
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_PATH, mode="w", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constantes de dominio
# ---------------------------------------------------------------------------

# Clave de observación: un registro = una cancelación de asignatura por estudiante
# NOTA: LOGIN_USUARIO_ESTUDIANTE fue eliminado en la anonimización → usar ID_UNAL
CLAVE_OBS = ["ID_UNAL", "PERIODO", "COD_PLAN", "COD_ASIGNATURA"]

# Columnas esperadas según el dataset real (post-anonimización)
# COLUMNAS_PII eliminadas en paso anterior: LOGIN_USUARIO_ESTUDIANTE, HIST_ACAD,
#   NOMBRE_COMPLETO, NUMERO_DOCUMENTO, TIPO_DOCUMENTO, FECHA_NACIMIENTO, SEXO, CORREO
COLUMNAS_ESPERADAS = [
    # Identificador anonimizado
    "ID_UNAL",
    # Programa académico
    "SEDE",
    "COD_FACULTAD",
    "FACULTAD",
    "COD_PLAN",
    "PLAN",
    "COD_PROG_CURRICULAR",
    "DESC_PROG_CURRICULAR",
    "CONVENIO_PLAN",
    "TIPO_NIVEL",
    # Admisión
    "ADMISION",
    "CONVOCATORIA",
    "APERTURA",
    "COD_ACCESO",
    "ACCESO",
    "COD_SUBACCESO",
    "SUBACCESO",
    "COD_NODO_INICIO",
    "NODO_INICIO",
    # Asignatura cancelada
    "COD_ASIGNATURA",
    "ASIGNATURA",
    "NOTA_ALFABETICA",
    "NOTA_NUMERICA",
    "CREDITOS",
    "GRUP_ACTI",
    "DES_GR_ACTIV",
    "GRUP_ACTA",
    # Período y sede de la asignatura
    "PERIODO",
    "COD_SEDE_ASIGNATURA",
    "COD_FACULTAD_ASIGNATURA",
    "FACULTAD_ASIGNATURA",
    "COD_UAB_ASIGNATURA",
    "UAB_ASIGNATURA",
    # Tipo y causa
    "TIPO_CANCELACION",
    "FECHA",
    "CORRECCION_CRED_PERDIDA",   # nombre normalizado (sin tilde ni encoding roto)
    "CAUSA_ANULA",
    "USUARIO_CANCELACION",
    "TIPO_USUARIO",
    # Socioeconómico
    "PBM",
    "PUNTAJE_ADMISION",
    # Trazabilidad
    "ARCHIVO_FUENTE",
]

# Patrones de columnas PII que NO deben sobrevivir bajo ningún alias
PII_PATTERNS = [
    "correo", "nombre", "apellido", "documento", "nacimiento",
    "email", "celular", "telefono", "direccion", "login", "hist_acad",
]

# ---------------------------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------------------------

def cargar_datos(path: Path) -> pd.DataFrame:
    """Lee todos los CSV en INPUT_PATH y los concatena."""
    log.info(f"[CARGA] Buscando CSV en: {path}")
    archivos = sorted(path.glob("*.csv"))

    if not archivos:
        log.error(f"[CARGA][ERROR] No se encontraron archivos CSV en: {path}")
        sys.exit(1)

    dfs = []
    for archivo in archivos:
        try:
            df_tmp = pd.read_csv(archivo, dtype=str, encoding="utf-8")
            df_tmp["ARCHIVO_FUENTE"] = archivo.name
            dfs.append(df_tmp)
            log.info(
                f"[CARGA][OK] {archivo.name}: "
                f"{len(df_tmp):,} filas | {df_tmp.shape[1]} columnas"
            )
        except Exception as e:
            log.error(f"[CARGA][ERROR] No se pudo leer {archivo.name}: {e}")
            raise

    df = pd.concat(dfs, ignore_index=True)
    log.info(
        f"[CARGA] Total consolidado: "
        f"{len(df):,} filas | {df.shape[1]} columnas | {len(archivos)} archivos"
    )
    return df


def normalizar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Estandariza nombres de columnas:
      - Strip de espacios y mayúsculas
      - Normaliza la columna con encoding roto 'CORRECIÃ"N DE CRED. PERDIDA'
      - Reemplaza espacios internos por guión bajo
    """
    log.info("[NORM] Normalizando nombres de columnas")

    df.columns = df.columns.str.strip().str.upper()

    rename_map = {}
    for col in df.columns:
        # Columna con encoding roto: 'CORRECIÃ"N DE CRED. PERDIDA' → 'CORRECCION_CRED_PERDIDA'
        if "CORRECI" in col and "CRED" in col:
            rename_map[col] = "CORRECCION_CRED_PERDIDA"
        # Reemplazar espacios internos por guión bajo
        elif " " in col:
            rename_map[col] = col.replace(" ", "_")

    if rename_map:
        df = df.rename(columns=rename_map)
        log.info(f"[NORM] Columnas renombradas: {rename_map}")

    return df


def verificar_columnas(df: pd.DataFrame) -> None:
    """Reporta columnas esperadas ausentes y columnas inesperadas presentes."""
    log.info("[COLS] Verificando cobertura de columnas")

    ausentes = [c for c in COLUMNAS_ESPERADAS if c not in df.columns]
    extra    = [c for c in df.columns if c not in COLUMNAS_ESPERADAS]

    if ausentes:
        log.warning(
            f"[COLS][WARN] Columnas esperadas no encontradas "
            f"({len(ausentes)}): {ausentes}"
        )
    else:
        log.info("[COLS][OK] Todas las columnas esperadas están presentes")

    if extra:
        log.info(
            f"[COLS][INFO] Columnas adicionales en el input "
            f"({len(extra)}): {extra}"
        )


def verificar_sin_pii(df: pd.DataFrame) -> None:
    """Aborta si alguna columna PII sobrevivió al pipeline de anonimización."""
    log.info("[PII] Verificando ausencia de datos personales")

    encontradas = [
        c for c in df.columns
        if any(p in c.lower() for p in PII_PATTERNS)
    ]
    if encontradas:
        log.error(
            f"[PII][ERROR] Columnas con posible PII detectadas: {encontradas}. "
            "Revisar el pipeline de anonimización antes de continuar."
        )
        sys.exit(1)
    log.info("[PII][OK] Sin columnas PII residuales")


def derivar_periodo(df: pd.DataFrame) -> pd.DataFrame:
    """
    Deriva academic_anio y academic_semester desde PERIODO (formato YYYY-NS,
    e.g. '2023-1S'). Solo se crean si no existen o están completamente vacías.
    """
    log.info("[PERIODO] Derivando academic_anio y academic_semester desde PERIODO")

    if "PERIODO" not in df.columns:
        log.warning(
            "[PERIODO][SKIP] Columna PERIODO ausente — "
            "no se pueden derivar variables de calendario"
        )
        return df

    if "academic_anio" not in df.columns or df["academic_anio"].isna().all():
        df["academic_anio"] = df["PERIODO"].str.extract(r"^(\d{4})")[0]
        log.info("[PERIODO][OK] academic_anio derivado")

    if "academic_semester" not in df.columns or df["academic_semester"].isna().all():
        df["academic_semester"] = df["PERIODO"].str.extract(r"-(\d)")[0]
        log.info("[PERIODO][OK] academic_semester derivado")

    return df


def convertir_tipos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte columnas numéricas a tipo numérico.
    El resto permanece como str para preservar códigos con ceros a la izquierda.
    """
    log.info("[TIPOS] Convirtiendo columnas numéricas")

    cols_num = ["NOTA_NUMERICA", "CREDITOS", "PBM", "PUNTAJE_ADMISION"]
    for col in cols_num:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            log.info(f"[TIPOS][OK] {col} → numérico")

    if "FECHA" in df.columns:
        df["FECHA"] = pd.to_datetime(df["FECHA"], errors="coerce", dayfirst=True)
        log.info("[TIPOS][OK] FECHA → datetime")

    return df


def verificar_unicidad_clave(df: pd.DataFrame) -> None:
    """
    Verifica unicidad de CLAVE_OBS.
    En cancelaciones puede existir más de una cancelación del mismo estudiante-
    período-plan-asignatura si hubo correcciones; se reporta como advertencia,
    no como error fatal.
    """
    log.info(f"[CLAVE] Verificando unicidad de {CLAVE_OBS}")

    clave_presente = [c for c in CLAVE_OBS if c in df.columns]
    if len(clave_presente) < len(CLAVE_OBS):
        log.warning(
            f"[CLAVE][WARN] Columnas de clave ausentes: "
            f"{set(CLAVE_OBS) - set(clave_presente)}"
        )
        return

    dupes = df.duplicated(subset=clave_presente).sum()
    if dupes > 0:
        log.warning(
            f"[CLAVE][WARN] {dupes:,} filas duplicadas en la clave "
            f"{clave_presente}. Pueden corresponder a correcciones o "
            "cancelaciones múltiples. Revisar si se requiere desambiguar."
        )
    else:
        log.info(f"[CLAVE][OK] Clave única — {len(df):,} observaciones")


def seleccionar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    """Selecciona y ordena las columnas aprobadas; añade NaN para las ausentes."""
    log.info("[COLS] Seleccionando variables aprobadas")

    columnas_finales = COLUMNAS_ESPERADAS.copy()
    # Agregar columnas de calendario derivadas si existen
    for col in ["academic_anio", "academic_semester"]:
        if col in df.columns and col not in columnas_finales:
            columnas_finales.append(col)

    ausentes = [c for c in columnas_finales if c not in df.columns]
    if ausentes:
        log.warning(
            f"[COLS][WARN] Columnas no encontradas "
            f"(se crean como NaN): {ausentes}"
        )
        for col in ausentes:
            df[col] = np.nan

    df_sel = df[columnas_finales].copy()
    log.info(f"[COLS][OK] {len(columnas_finales)} variables en la base final")
    return df_sel


def exportar(df: pd.DataFrame, path: Path) -> None:
    """Exporta la base final a CSV."""
    log.info(f"[EXPORT] Escribiendo: {path}")
    df.to_csv(path, index=False, encoding="utf-8")
    size_kb = path.stat().st_size / 1024
    log.info(
        f"[EXPORT][OK] {len(df):,} filas | "
        f"{df.shape[1]} columnas | {size_kb:.1f} KB"
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    sep = "=" * 70
    log.info(sep)
    log.info(
        "FASE 8 — BASE_CANCELACIONES  |  Inicio: "
        + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    log.info(sep)

    # 1. Carga y concatenación
    df = cargar_datos(INPUT_PATH)

    # 2. Normalizar nombres de columnas (encoding roto, espacios)
    df = normalizar_columnas(df)

    # 3. Verificar cobertura de columnas (informativo, no fatal)
    verificar_columnas(df)

    # 4. Verificar ausencia de PII — FATAL si encuentra algo
    verificar_sin_pii(df)

    # 5. Derivar variables de calendario
    df = derivar_periodo(df)

    # 6. Convertir tipos numéricos
    df = convertir_tipos(df)

    # 7. Verificar unicidad de clave (advertencia, no fatal)
    verificar_unicidad_clave(df)

    # 8. Seleccionar y ordenar columnas aprobadas
    df = seleccionar_columnas(df)

    # 9. Exportar
    exportar(df, OUTPUT_PATH)

    log.info(sep)
    log.info(
        "FASE 8 — BASE_CANCELACIONES  |  Fin: "
        + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    log.info(sep)


if __name__ == "__main__":
    main()