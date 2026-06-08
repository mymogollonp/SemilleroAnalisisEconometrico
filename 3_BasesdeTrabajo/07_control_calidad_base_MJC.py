# =============================================================================
# Script   : 16_control_calidad.py
# Equipo   : Semillero de Análisis Econométrico — UNAL FCE
# Propósito: Fase 9 — Control de Calidad automatizado sobre las bases de trabajo
#            Genera un reporte QC en Markdown: logs/QC_report_YYYY-MM-DD.md
# Input    : FinalWorkingDataSets/*.csv  (todas las bases de la Fase 8)
# Output   : logs/QC_report_YYYY-MM-DD.md
# Regla    : Los archivos en DatosOriginales/ NUNCA se modifican.
# =============================================================================

import pandas as pd
import numpy as np
import os
import re
import sys
import logging
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------------------
try:
    from config import DIR_DATOS
except ImportError:
    DIR_DATOS = Path(__file__).resolve().parent.parent

DIR_DATOS = Path(DIR_DATOS)

BASES_DIR  = DIR_DATOS / "FinalWorkingDataSets"
LOGS_DIR   = DIR_DATOS / "logs"
HOY        = datetime.now().strftime("%Y-%m-%d")
REPORT_PATH = LOGS_DIR / f"QC_report_{HOY}.md"
LOG_PATH    = LOGS_DIR / f"16_control_calidad_{HOY}.log"

LOGS_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Logger de consola/archivo (separado del reporte Markdown)
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
CLAVE_OBS = ["id_unal", "periodo", "cod_plan"]

# Patrón de período válido: 2009-1S a 2025-2S
PERIODO_RE = re.compile(r"^(200[9]|201\d|202[0-5])-(1|2)S$")
PERIODO_MIN = "2009-1S"
PERIODO_MAX = "2025-2S"

# Columnas de promedio/calificación que deben estar en [0, 5]
CALIFICACION_PATRONES = [
    "promedio", "nota", "calificacion", "prom_", "avg_"
]

# PII residual — fragmentos de nombre de columna a detectar
PII_PATRONES = [
    "correo", "nombre", "apellido", "documento",
    "email", "celular", "telefono", "direccion"
]


# ---------------------------------------------------------------------------
# Clase de resultado para cada check
# ---------------------------------------------------------------------------
class CheckResult:
    def __init__(self, nombre: str):
        self.nombre  = nombre
        self.estado  = "✅ OK"          # ✅ OK  |  ⚠️ WARN  |  ❌ ERROR
        self.detalles: list[str] = []

    def warn(self, msg: str):
        self.estado = "⚠️ WARN"
        self.detalles.append(msg)

    def error(self, msg: str):
        self.estado = "❌ ERROR"
        self.detalles.append(msg)

    def info(self, msg: str):
        self.detalles.append(msg)

    def to_md(self) -> str:
        lineas = [f"### {self.estado}  `{self.nombre}`"]
        for d in self.detalles:
            lineas.append(f"- {d}")
        return "\n".join(lineas)


# ---------------------------------------------------------------------------
# Checks individuales
# ---------------------------------------------------------------------------

def check_unicidad_clave(df: pd.DataFrame, nombre_base: str) -> CheckResult:
    r = CheckResult(f"Unicidad clave {CLAVE_OBS} — {nombre_base}")
    cols_presentes = [c for c in CLAVE_OBS if c in df.columns]
    if len(cols_presentes) < len(CLAVE_OBS):
        ausentes = [c for c in CLAVE_OBS if c not in df.columns]
        r.error(f"Columnas de clave ausentes: {ausentes}")
        return r

    dupes = df.duplicated(subset=CLAVE_OBS).sum()
    r.info(f"Total observaciones: {len(df):,}")
    if dupes > 0:
        r.error(f"{dupes:,} filas duplicadas en la clave ({dupes/len(df)*100:.2f}%)")
    else:
        r.info("Clave única en toda la base")
    return r


def check_sin_pii(df: pd.DataFrame, nombre_base: str) -> CheckResult:
    r = CheckResult(f"Ausencia PII — {nombre_base}")
    encontradas = [
        c for c in df.columns
        if any(p in c.lower() for p in PII_PATRONES)
    ]
    if encontradas:
        r.error(f"Columnas con posible PII detectadas: {encontradas}")
    else:
        r.info("Sin columnas PII residuales en encabezados")

    # Verificación adicional: id_unal no debe contener '@' (indicio de correo)
    if "id_unal" in df.columns:
        contiene_arroba = df["id_unal"].astype(str).str.contains("@", na=False).sum()
        if contiene_arroba > 0:
            r.error(f"id_unal contiene {contiene_arroba} valores con '@' (posibles correos)")
        else:
            r.info("id_unal no contiene valores con '@'")

        # id_unal no debe contener espacios ni caracteres de nombre
        contiene_espacio = df["id_unal"].astype(str).str.contains(r"\s", na=False).sum()
        if contiene_espacio > 0:
            r.warn(f"id_unal contiene {contiene_espacio} valores con espacios (revisar)")

    return r


def check_calificaciones_rango(df: pd.DataFrame, nombre_base: str) -> CheckResult:
    r = CheckResult(f"Calificaciones en rango [0, 5] — {nombre_base}")
    cols_nota = [
        c for c in df.columns
        if any(p in c.lower() for p in CALIFICACION_PATRONES)
    ]
    if not cols_nota:
        r.info("No se detectaron columnas de calificación/promedio en esta base")
        return r

    for col in cols_nota:
        serie = pd.to_numeric(df[col], errors="coerce")
        fuera = ((serie < 0) | (serie > 5)).sum()
        nulos = serie.isna().sum()
        r.info(f"`{col}`: {nulos:,} nulos  |  {fuera:,} fuera de [0,5]")
        if fuera > 0:
            r.error(f"`{col}` tiene {fuera:,} valores fuera del rango 0–5")
    return r


def check_periodos_rango(df: pd.DataFrame, nombre_base: str) -> CheckResult:
    r = CheckResult(f"Períodos en rango [{PERIODO_MIN}, {PERIODO_MAX}] — {nombre_base}")
    if "periodo" not in df.columns:
        r.warn("Columna 'periodo' no encontrada en esta base")
        return r

    periodos = df["periodo"].dropna().astype(str)
    total = len(periodos)
    r.info(f"Períodos únicos: {periodos.nunique()}  |  Total filas con periodo: {total:,}")

    # Verificar formato
    formato_invalido = (~periodos.str.match(r"^\d{4}-(1|2)S$")).sum()
    if formato_invalido > 0:
        r.error(f"{formato_invalido:,} valores no siguen el formato YYYY-NS")

    # Verificar rango
    fuera_rango = (~periodos.apply(lambda x: bool(PERIODO_RE.match(x)))).sum()
    if fuera_rango > 0:
        ejemplos = periodos[~periodos.apply(lambda x: bool(PERIODO_RE.match(x)))].unique()[:5]
        r.error(f"{fuera_rango:,} períodos fuera del rango permitido. Ejemplos: {list(ejemplos)}")
    else:
        r.info("Todos los períodos dentro del rango 2009-1S — 2025-2S")
    return r


def check_graduado_retirado(df: pd.DataFrame, nombre_base: str) -> CheckResult:
    r = CheckResult(f"Sin graduado=1 y retirado=1 simultáneo — {nombre_base}")
    if "graduado" not in df.columns or "retirado" not in df.columns:
        r.info("Columnas 'graduado' y/o 'retirado' no presentes en esta base — check omitido")
        return r

    grad  = pd.to_numeric(df["graduado"],  errors="coerce")
    retir = pd.to_numeric(df["retirado"],  errors="coerce")
    conflicto = ((grad == 1) & (retir == 1)).sum()
    r.info(f"Filas con graduado=1: {(grad==1).sum():,}  |  retirado=1: {(retir==1).sum():,}")
    if conflicto > 0:
        r.error(f"{conflicto:,} estudiantes tienen graduado=1 y retirado=1 simultáneamente")
    else:
        r.info("Ningún estudiante con graduado=1 y retirado=1 a la vez")
    return r


# ---------------------------------------------------------------------------
# Resumen estadístico ligero para la base
# ---------------------------------------------------------------------------

def resumen_base(df: pd.DataFrame, archivo: Path) -> str:
    lineas = [
        f"| **Archivo**       | `{archivo.name}` |",
        f"| **Filas**         | {len(df):,} |",
        f"| **Columnas**      | {df.shape[1]} |",
        f"| **Memoria**       | {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB |",
    ]
    if "periodo" in df.columns:
        periodos_uniq = sorted(df["periodo"].dropna().unique())
        rango = f"{periodos_uniq[0]} — {periodos_uniq[-1]}" if periodos_uniq else "N/A"
        lineas.append(f"| **Rango períodos**| {rango} ({len(periodos_uniq)} únicos) |")
    if "id_unal" in df.columns:
        lineas.append(f"| **Estudiantes**   | {df['id_unal'].nunique():,} únicos |")
    return "| Métrica | Valor |\n|---|---|\n" + "\n".join(lineas)


# ---------------------------------------------------------------------------
# Generador del reporte Markdown
# ---------------------------------------------------------------------------

def generar_reporte(resultados: dict[str, list[CheckResult]],
                    resumenes: dict[str, str]) -> str:
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_checks  = sum(len(v) for v in resultados.values())
    total_ok      = sum(1 for v in resultados.values() for r in v if "OK"    in r.estado)
    total_warn     = sum(1 for v in resultados.values() for r in v if "WARN"  in r.estado)
    total_error    = sum(1 for v in resultados.values() for r in v if "ERROR" in r.estado)

    lineas = [
        "# Reporte de Control de Calidad — Semillero de Análisis Econométrico",
        f"**Fecha de generación:** {ahora}  ",
        f"**Script:** `4_BasesdeTrabajo/16_control_calidad.py`  ",
        "",
        "---",
        "",
        "## Resumen ejecutivo",
        "",
        f"| | Cantidad |",
        f"|---|---|",
        f"| Checks ejecutados | {total_checks} |",
        f"| ✅ OK             | {total_ok} |",
        f"| ⚠️ WARN           | {total_warn} |",
        f"| ❌ ERROR          | {total_error} |",
        "",
    ]

    if total_error > 0:
        lineas.append("> ⛔ **Se detectaron errores críticos. Revisar antes de usar las bases.**")
    elif total_warn > 0:
        lineas.append("> ⚠️ **Advertencias detectadas. Revisión recomendada.**")
    else:
        lineas.append("> ✅ **Todas las verificaciones pasaron correctamente.**")

    lineas.append("")
    lineas.append("---")
    lineas.append("")

    for nombre_base, checks in resultados.items():
        lineas.append(f"## Base: `{nombre_base}`")
        lineas.append("")
        if nombre_base in resumenes:
            lineas.append("### Estadísticas de la base")
            lineas.append("")
            lineas.append(resumenes[nombre_base])
            lineas.append("")
        lineas.append("### Resultados de checks")
        lineas.append("")
        for check in checks:
            lineas.append(check.to_md())
            lineas.append("")
        lineas.append("---")
        lineas.append("")

    lineas.append(f"*Reporte generado automáticamente por `16_control_calidad.py` — {ahora}*")
    return "\n".join(lineas)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    log.info("=" * 70)
    log.info(f"FASE 9 — CONTROL DE CALIDAD  |  Inicio: {datetime.now():%Y-%m-%d %H:%M:%S}")
    log.info("=" * 70)

    # Buscar todas las bases CSV en FinalWorkingDataSets/
    archivos = sorted(BASES_DIR.glob("*.csv")) if BASES_DIR.exists() else []

    if not archivos:
        log.warning(f"[WARN] No se encontraron archivos CSV en {BASES_DIR}")
        log.warning("[WARN] Ejecutar primero los scripts de Fase 8.")
    else:
        log.info(f"[CARGA] Bases detectadas: {[a.name for a in archivos]}")

    resultados: dict[str, list[CheckResult]] = {}
    resumenes:  dict[str, str] = {}

    for archivo in archivos:
        nombre = archivo.stem
        log.info(f"[QC] Procesando: {archivo.name}")
        try:
            df = pd.read_csv(archivo, dtype=str, encoding="utf-8")
        except Exception as e:
            log.error(f"[ERROR] No se pudo leer {archivo.name}: {e}")
            r = CheckResult(f"Lectura — {nombre}")
            r.error(f"No se pudo leer el archivo: {e}")
            resultados[nombre] = [r]
            continue

        resumenes[nombre] = resumen_base(df, archivo)

        checks = [
            check_unicidad_clave(df, nombre),
            check_sin_pii(df, nombre),
            check_calificaciones_rango(df, nombre),
            check_periodos_rango(df, nombre),
            check_graduado_retirado(df, nombre),
        ]
        resultados[nombre] = checks

        for c in checks:
            log.info(f"  [{nombre}] {c.estado}  {c.nombre.split('—')[0].strip()}")

    # Si no hay archivos, igual se genera un reporte vacío con advertencia
    if not archivos:
        r_vacio = CheckResult("Bases disponibles")
        r_vacio.warn(f"No se encontraron bases CSV en {BASES_DIR}. "
                     "Ejecutar los scripts de Fase 8 primero.")
        resultados["(sin_bases)"] = [r_vacio]

    # Generar y escribir reporte Markdown
    reporte_md = generar_reporte(resultados, resumenes)
    REPORT_PATH.write_text(reporte_md, encoding="utf-8")
    log.info(f"[EXPORT][OK] Reporte escrito en: {REPORT_PATH}")

    # Resumen final en consola
    total_error = sum(1 for v in resultados.values() for r in v if "ERROR" in r.estado)
    total_warn  = sum(1 for v in resultados.values() for r in v if "WARN"  in r.estado)
    log.info("=" * 70)
    log.info(f"FASE 9 — CONTROL DE CALIDAD  |  Fin: {datetime.now():%Y-%m-%d %H:%M:%S}")
    log.info(f"  Errores: {total_error}  |  Advertencias: {total_warn}")
    log.info("=" * 70)

    # Salir con código de error si hay checks fallidos (útil en CI)
    if total_error > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
