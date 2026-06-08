#%%
## =============================================================================
# 05_anonimizacion_Cancelaciones_MJC.py
# Semillero de Análisis Econométrico — UNAL FCE
# RA: Maria Jose Cadena
# Fecha: 2026-05-02
#
# Propósito: Anonimización del módulo de Cancelaciones.
#   - Anonimiza CORREO → ID_UNAL usando LLAVE_ID_UNAL_FCE.csv
#   - Elimina columnas PII (nombre, documento, fecha nacimiento, etc.)
#   - Verifica ausencia de PII en el output final
#
# Input:  DatosOriginales/Cancelaciones/*.xlsx
# Output: DatosArmonizados/2_DatosLimpios/Cancelaciones/por_periodo/Cancelaciones_<PERIODO>.csv
#         DatosArmonizados/2_DatosLimpios/Cancelaciones/Cancelaciones_limpio.csv
#         logs/limpieza_Cancelaciones_YYYY-MM-DD.txt
#
# REGLA: nunca modificar los archivos de DatosOriginales/.
# =============================================================================

import pandas as pd
import numpy as np
import re
import sys
from pathlib import Path
from datetime import date
import unicodedata

# =============================================================================
# 1. RUTAS — via config.py centralizado
# =============================================================================

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import DIR_DATOS  # type: ignore
from config import DIR_CODE   # type: ignore

# Input: archivos originales (READ-ONLY — nunca modificar)
RUTA_INPUT  = DIR_DATOS / "DatosArmonizados" / "Cancelaciones" / "2_DatosLimpios"

# Output: CSV limpio consolidado
RUTA_OUTPUT = DIR_DATOS / "DatosArmonizados" / "Cancelaciones"
RUTA_OUTPUT_PERIODOS = RUTA_OUTPUT / "1_DatosAnonimizados"     # un CSV por período
ARCHIVO_SALIDA = RUTA_OUTPUT / "Cancelaciones_anonimizado.csv"

# Llave de anonimización (READ-ONLY — compartida con todos los módulos)
LLAVE_PATH = DIR_DATOS / "DatosArmonizados" / "keys" / "LLAVE_ID_UNAL_FCE.csv"

# Log
RUTA_LOG    = DIR_CODE / "logs"
ARCHIVO_LOG = RUTA_LOG / f"Anonimización_Cancelaciones_{date.today().isoformat()}.txt"

assert RUTA_INPUT.exists(),  f"Ruta de datos no encontrada:  {RUTA_INPUT}"
assert RUTA_OUTPUT.exists(), f"Ruta de output no encontrada: {RUTA_OUTPUT}"
RUTA_OUTPUT_PERIODOS.mkdir(parents=True, exist_ok=True)
RUTA_LOG.mkdir(parents=True, exist_ok=True)


# =============================================================================
# 6b. ANONIMIZACIÓN
# =============================================================================

# Carga diferida para evitar error si la llave no existe en entornos de prueba
def _cargar_mapa_correo() -> dict:
    if not LLAVE_PATH.exists():
        print(f"  [ADVERTENCIA] Llave de anonimización no encontrada: {LLAVE_PATH}")
        return {}
    llave = pd.read_csv(LLAVE_PATH, dtype=str)
    llave["correo"] = llave["correo"].str.lower().str.strip()
    return llave.set_index("correo")["id_unal"].to_dict()


MAPA_CORREO_ID: dict = _cargar_mapa_correo()


# PII que debe eliminarse del output final
COLUMNAS_PII = [
    "NOMBRE_COMPLETO",
    "NUMERO_DOCUMENTO",
    "TIPO_DOCUMENTO",
    "FECHA_NACIMIENTO",
    "SEXO",
    "LOGIN_USUARIO_ESTUDIANTE",
    "HIST_ACAD",
]


def anonimizar_correo(df: pd.DataFrame, log_lines: list) -> pd.DataFrame:
    """
    Reemplaza CORREO por ID_UNAL usando la llave maestra.
    - Correos sin match quedan con ID_UNAL = NaN y se reportan en el log.
    - Elimina la columna CORREO del DataFrame.
    """
    if "CORREO" not in df.columns:
        log_lines.append("  [AVISO] Columna CORREO no encontrada — anonimización omitida.")
        return df

    df = df.copy()
    df["CORREO"] = df["CORREO"].str.lower().str.strip()

    if not MAPA_CORREO_ID:
        log_lines.append(
            "  [ERROR] Mapa de anonimización vacío — "
            "se elimina CORREO pero NO se crea ID_UNAL."
        )
        return df.drop(columns=["CORREO"])

    df["ID_UNAL"] = df["CORREO"].map(MAPA_CORREO_ID)

    sin_match = df.loc[df["ID_UNAL"].isna() & df["CORREO"].notna(), "CORREO"]
    n_sin = sin_match.nunique()
    if n_sin > 0:
        ejemplos = sorted(sin_match.unique())[:5]
        log_lines.append(
            f"  [ADVERTENCIA] {n_sin:,} correos únicos sin match en la llave. "
            f"Ejemplos: {ejemplos}"
        )
    else:
        log_lines.append(
            f"  [OK] Todos los correos mapeados a ID_UNAL "
            f"({df['ID_UNAL'].notna().sum():,} filas)."
        )

    return df.drop(columns=["CORREO"])


def eliminar_pii(df: pd.DataFrame, log_lines: list) -> pd.DataFrame:
    """Elimina columnas PII del DataFrame."""
    cols_a_eliminar = [c for c in COLUMNAS_PII if c in df.columns]
    if cols_a_eliminar:
        log_lines.append(f"  PII eliminadas: {cols_a_eliminar}")
    return df.drop(columns=cols_a_eliminar)


def verificar_ausencia_pii(df: pd.DataFrame, log_lines: list) -> None:
    """Alerta si alguna columna PII sobrevivió al pipeline."""
    pii_restantes = [c for c in COLUMNAS_PII + ["CORREO"] if c in df.columns]
    if pii_restantes:
        log_lines.append(
            f"\n  [ERROR] Columnas PII presentes en el output final: {pii_restantes}"
        )
    else:
        log_lines.append("  [OK] Sin columnas PII en el output final.")

#%%