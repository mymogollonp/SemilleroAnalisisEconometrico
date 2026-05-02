#%%
## =============================================================================
# 03_limpieza_Cancelaciones_MJC.py
# Semillero de Análisis Econométrico — UNAL FCE
# RA: Maria Jose Cadena
# Fecha: 2026-05-02
#
# Propósito: Limpieza del módulo de Cancelaciones.
#   - Lee los .xlsx originales de DatosOriginales/Cancelaciones/ (READ-ONLY)
#   - Estandariza nombres de variables al esquema canónico
#   - Verifica el formato del período (YYYY-NS)
#   - Detecta y documenta duplicados en el output consolidado
#   - Guarda el CSV limpio en DatosArmonizados/Cancelaciones_limpio.csv
#
# Input:  DatosOriginales/Cancelaciones/*.xlsx
# Output: DatosArmonizados/2_DatosLimpios/Cancelaciones_limpio.csv
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

# =============================================================================
# 0. RUTAS — via config.py centralizado
# =============================================================================

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import DIR_DATOS  # type: ignore
from config import DIR_CODE   # type: ignore

# Input: archivos originales (READ-ONLY — nunca modificar)
RUTA_INPUT  = DIR_DATOS / "DatosOriginales" / "Cancelaciones"

# Output: CSV limpio consolidado
RUTA_OUTPUT = DIR_DATOS / "DatosArmonizados" / "Cancelaciones"
ARCHIVO_SALIDA = RUTA_OUTPUT / "Cancelaciones_limpio.csv"

# Log
RUTA_LOG    = DIR_CODE / "logs"
ARCHIVO_LOG = RUTA_LOG / f"limpieza_Cancelaciones_{date.today().isoformat()}.txt"

assert RUTA_INPUT.exists(),  f"Ruta de datos no encontrada:  {RUTA_INPUT}"
assert RUTA_OUTPUT.exists(), f"Ruta de output no encontrada: {RUTA_OUTPUT}"
RUTA_LOG.mkdir(parents=True, exist_ok=True)


# =============================================================================
# 2. FORMATO DE PERÍODO
#    El inventario confirmó que PERIODO ya viene en formato YYYY-NS en los 32
#    archivos. Aun así validamos con regex para detectar cualquier valor atípico.
# =============================================================================

PERIODO_REGEX = re.compile(r"^\d{4}-[12]S$")


def validar_periodo(serie: pd.Series, archivo: str, log_lines: list) -> pd.Series:
    """
    Verifica que todos los valores de PERIODO cumplan el formato YYYY-NS.
    Registra valores inválidos en el log. No modifica valores — solo reporta.
    Retorna la serie sin cambios (la limpieza se haría aquí si fuera necesaria).
    """
    invalidos = serie[~serie.astype(str).str.match(PERIODO_REGEX)]
    if len(invalidos) > 0:
        log_lines.append(
            f"  [ADVERTENCIA] PERIODO — {len(invalidos)} valor(es) con formato inesperado "
            f"en {archivo}:"
        )
        for val, cnt in invalidos.value_counts().items():
            log_lines.append(f"    '{val}' → {cnt} fila(s)")
    else:
        log_lines.append(f"  [OK] PERIODO — todos los valores cumplen formato YYYY-NS en {archivo}")
    return serie


# =============================================================================
# 3. DETECCIÓN DE DUPLICADOS
#    La unidad de observación es una asignatura cancelada por un estudiante
#    en un período y programa.
#    Clave natural: id_unal + PERIODO + COD_PLAN + COD_ASIGNATURA
#    (equivalente a la llave evaluada en el inventario con correo)
# =============================================================================

LLAVE_OBS = ["correo", "PERIODO", "COD_PLAN", "COD_ASIGNATURA"]


def reportar_duplicados(df: pd.DataFrame, llave: list, contexto: str, log_lines: list) -> pd.DataFrame:
    """
    Identifica filas duplicadas según la llave dada.
    Añade columna is_duplicado al DataFrame retornado.
    Reporta en el log.
    """
    # Filas donde la combinación de llave aparece más de una vez
    mask_dup = df.duplicated(subset=llave, keep=False)
    n_dup = mask_dup.sum()
    n_grupos = df[mask_dup].groupby(llave).ngroups if n_dup > 0 else 0

    log_lines.append(f"\n--- Duplicados ({contexto}) ---")
    log_lines.append(f"  Llave: {' + '.join(llave)}")
    log_lines.append(f"  Filas totales:               {len(df):>10,}")
    log_lines.append(f"  Filas en grupos duplicados:  {n_dup:>10,}  ({100*n_dup/len(df):.2f}%)")
    log_lines.append(f"  Grupos únicos duplicados:    {n_grupos:>10,}")

    if n_dup > 0:
        # Mostrar top 10 llaves repetidas
        top = (df[mask_dup]
               .groupby(llave)
               .size()
               .reset_index(name="n_filas")
               .sort_values("n_filas", ascending=False)
               .head(10))
        log_lines.append("  Top 10 llaves repetidas:")
        for _, row in top.iterrows():
            llave_str = " || ".join(str(row[k]) for k in llave)
            log_lines.append(f"    {llave_str}  →  {row['n_filas']} filas")

    df["is_duplicado"] = mask_dup
    return df


# =============================================================================
# 4. CARGA DE ARCHIVOS
# =============================================================================

def cargar_cancelaciones(ruta_input: Path, log_lines: list) -> pd.DataFrame:
    """
    Carga todos los .xlsx de DatosOriginales/Cancelaciones/, añade columna
    archivo_fuente y los apila en un DataFrame único.
    Caso especial: Cancelaciones_2024-2S usa Sheet2 (detectado en el inventario).
    """
    archivos = sorted(ruta_input.glob("*.xlsx"))

    if len(archivos) == 0:
        log_lines.append(f"[ERROR] No se encontraron .xlsx en: {ruta_input}")
        sys.exit(1)

    log_lines.append(f"\nArchivos encontrados: {len(archivos)}")

    HOJA_ESPECIAL = {"Cancelaciones_2024-2S": "Sheet2"}

    dfs = []
    for ruta in archivos:
        nombre = ruta.stem
        hoja = HOJA_ESPECIAL.get(nombre, 0)  # 0 = primera hoja por defecto
        df_arch = pd.read_excel(ruta, sheet_name=hoja, dtype=str)
        df_arch["archivo_fuente"] = nombre
        n_filas = len(df_arch)
        nota_hoja = f"  [hoja: {hoja}]" if nombre in HOJA_ESPECIAL else ""
        log_lines.append(f"  · {nombre}  →  {n_filas:,} filas,  {df_arch.shape[1]-1} columnas{nota_hoja}")
        dfs.append(df_arch)

    df = pd.concat(dfs, ignore_index=True)
    log_lines.append(f"\nTotal filas apiladas: {len(df):,}")
    return df


# =============================================================================
# 5. LIMPIEZA PRINCIPAL
# =============================================================================

def limpiar_cancelaciones(df: pd.DataFrame, log_lines: list) -> pd.DataFrame:
    """
    Aplica las transformaciones de limpieza al DataFrame apilado.
    """

    # 5a. Verificar presencia de columnas de identificación
    log_lines.append("\n--- Verificación de columnas de identificación ---")
    ID_COLS = ["correo", "numero_documento"]
    for col in ID_COLS:
        if col not in df.columns:
            log_lines.append(f"  [ADVERTENCIA] Columna '{col}' no encontrada.")
        else:
            n_missing = df[col].isna().sum()
            log_lines.append(f"  [OK] '{col}' presente. Missings: {n_missing:,} ({100*n_missing/len(df):.2f}%)")

    # 5c. Validar formato de PERIODO (ya confirmado como YYYY-NS en el inventario)
    log_lines.append("\n--- Validación de PERIODO ---")
    if "PERIODO" in df.columns:
        for arch in df["archivo_fuente"].unique():
            subset = df.loc[df["archivo_fuente"] == arch, "PERIODO"]
            validar_periodo(subset, arch, log_lines)
    else:
        log_lines.append("  [ERROR] Columna PERIODO no encontrada.")

    # 5d. Armonizar nombres canónicos de variables PII
    log_lines.append("\n--- Armonización de nombres canónicos ---")

    # Renombres de columnas al esquema canónico del proyecto
    RENOMBRES = {
        "CORREO_INSTITUCIONAL": "correo",
        "DOCUMENTO":            "numero_documento",
        "NOMBRES_APELLIDOS":    "nombre_completo",
    }
    df = df.rename(columns=RENOMBRES)
    for orig, canon in RENOMBRES.items():
        log_lines.append(f"  {orig} → {canon}")

    # Columnas canónicas ausentes en Cancelaciones — se crean vacías
    for col_ausente in ["tipo_documento", "sexo", "fecha_nacimiento"]:
        df[col_ausente] = np.nan
        log_lines.append(f"  {col_ausente}: no existe en la fuente → columna vacía (NaN)")

    # Limpiar nombre_completo: quitar tildes, ñ→N, mayúsculas
    import unicodedata
    def normalizar_nombre(s: str) -> str:
        if pd.isna(s):
            return s
        s = str(s).upper()
        s = unicodedata.normalize("NFD", s)
        s = "".join(c for c in s if unicodedata.category(c) != "Mn")  # quitar diacríticos
        s = s.replace("Ñ", "N")
        return s

    if "nombre_completo" in df.columns:
        df["nombre_completo"] = df["nombre_completo"].apply(normalizar_nombre)
        log_lines.append("  nombre_completo: tildes eliminadas, Ñ→N, mayúsculas aplicadas.")

    # 5e. Tipos de dato — conversiones básicas
    log_lines.append("\n--- Conversiones de tipo ---")

    # FECHA: ya es datetime en los originales; en el CSV anonimizado viene como string
    if "FECHA" in df.columns:
        df["FECHA"] = pd.to_datetime(df["FECHA"], errors="coerce")
        n_fecha_inv = df["FECHA"].isna().sum()
        log_lines.append(
            f"  FECHA convertida a datetime. Valores no parseables: {n_fecha_inv:,}"
        )

    # Columnas numéricas enteras
    COLS_INT = ["COD_ACCESO", "COD_FACULTAD", "COD_FACULTAD_ASIGNATURA",
                "COD_NODO_INICIO", "COD_SEDE_ASIGNATURA", "COD_SUBACCESO",
                "CREDITOS", "HIST_ACAD"]
    for col in COLS_INT:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Columnas numéricas float
    COLS_FLOAT = ["NOTA_NUMERICA", "PBM", "PUNTAJE_ADMISION",
                  "GRUP_ACTA", "COD_UAB_ASIGNATURA"]
    for col in COLS_FLOAT:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    log_lines.append("  Tipos aplicados: int → COD_*, CREDITOS, HIST_ACAD; "
                     "float → NOTA_NUMERICA, PBM, PUNTAJE_ADMISION, GRUP_ACTA.")

    # 5f. NOTA_NUMERICA: verificar rango 0-5
    log_lines.append("\n--- Validación NOTA_NUMERICA ---")
    if "NOTA_NUMERICA" in df.columns:
        fuera_rango = df["NOTA_NUMERICA"].dropna()
        fuera_rango = fuera_rango[(fuera_rango < 0) | (fuera_rango > 5)]
        if len(fuera_rango) > 0:
            log_lines.append(
                f"  [ADVERTENCIA] {len(fuera_rango):,} valores de NOTA_NUMERICA fuera de [0, 5]. "
                f"Min: {fuera_rango.min():.2f}, Max: {fuera_rango.max():.2f}"
            )
        else:
            log_lines.append("  [OK] NOTA_NUMERICA en rango [0, 5].")

    # 5g. COD_PLAN: en 2009-2011 viene como int64, luego como object
    # Normalizar a string para consistencia en el panel
    if "COD_PLAN" in df.columns:
        df["COD_PLAN"] = df["COD_PLAN"].astype(str).str.strip().str.upper()
        log_lines.append("\n  COD_PLAN normalizado a string (strip + upper).")

    # 5h. Variables de texto: strip de espacios
    COLS_STR = ["PERIODO", "TIPO_CANCELACION", "CAUSA_ANULA", "TIPO_NIVEL",
                "TIPO_USUARIO", "ADMISION", "ACCESO", "SUBACCESO", "SEDE",
                "FACULTAD", "PLAN", "ASIGNATURA"]
    for col in COLS_STR:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace("nan", np.nan)

    log_lines.append("  Columnas string: strip de espacios aplicado.")

    return df


# =============================================================================
# 6. VARIABLES INTERMITENTES — reporte de cobertura
# =============================================================================

VARS_INTERMITENTES = {
    "COD_PROG_CURRICULAR":  "Presente solo 2009-2011 y 2023-2025",
    "DESC_PROG_CURRICULAR": "Presente solo 2009-2011 y 2023-2025",
    "CONVOCATORIA":         "Presente solo 2009-2011 y 2023-2025",
    "PBM":                  "Ausente 2012-2022",
    "PUNTAJE_ADMISION":     "Ausente 2012-2022",
    "DES_GR_ACTIV":         "Ausente 2012-2021 (alta missing en extremos)",
}


def reportar_vars_intermitentes(df: pd.DataFrame, log_lines: list):
    log_lines.append("\n--- Variables intermitentes (cobertura parcial) ---")
    for var, nota in VARS_INTERMITENTES.items():
        if var in df.columns:
            n_total = len(df)
            n_presentes = df[var].notna().sum()
            log_lines.append(
                f"  {var}: {n_presentes:,}/{n_total:,} no-missing "
                f"({100*n_presentes/n_total:.1f}%)  ←  {nota}"
            )
        else:
            log_lines.append(f"  {var}: columna no encontrada en el input.")



# =============================================================================
# 7. SELECCIÓN DE COLUMNAS FINALES
# =============================================================================

VARS_CANONICAS = [
    # Identificación del estudiante — nombres canónicos del proyecto
    "correo",
    "tipo_documento",       # no existe en Cancelaciones → vacía
    "numero_documento",
    "nombre_completo",
    "sexo",                 # no existe en Cancelaciones → vacía
    "fecha_nacimiento",     # no existe en Cancelaciones → vacía
    "LOGIN_USUARIO_ESTUDIANTE",
    # Período y programa
    "PERIODO",
    "COD_PLAN",
    "PLAN",
    "COD_PROG_CURRICULAR",        # ausente 2012-2022
    "DESC_PROG_CURRICULAR",       # ausente 2012-2022
    "CONVOCATORIA",               # ausente 2012-2022
    # Asignatura cancelada
    "COD_ASIGNATURA",
    "ASIGNATURA",
    "CREDITOS",
    "COD_FACULTAD_ASIGNATURA",
    "FACULTAD_ASIGNATURA",
    "COD_UAB_ASIGNATURA",
    "UAB_ASIGNATURA",
    "COD_SEDE_ASIGNATURA",
    # Cancelación
    "TIPO_CANCELACION",
    "CAUSA_ANULA",                # missings masivos (ver inventario)
    "FECHA",
    "USUARIO_CANCELACION",
    # Notas
    "NOTA_NUMERICA",              # missings altos en períodos tempranos
    "NOTA_ALFABETICA",            # missings altos en períodos tempranos
    "GRUP_ACTA",
    "GRUP_ACTI",
    "DES_GR_ACTIV",               # ausente 2012-2021
    # Historial académico
    "HIST_ACAD",
    # Admisión y acceso
    "COD_ACCESO",
    "ACCESO",
    "COD_SUBACCESO",
    "SUBACCESO",
    "ADMISION",
    "PUNTAJE_ADMISION",           # ausente 2012-2022
    "APERTURA",
    # Sede y facultad del estudiante
    "COD_FACULTAD",
    "FACULTAD",
    "SEDE",
    # Nodo
    "COD_NODO_INICIO",
    "NODO_INICIO",
    # Socioeconómico
    "PBM",                        # ausente 2012-2022
    "CONVENIO_PLAN",              # missings ~100% en todos los períodos
    "CORRECIÓN DE CRED. PERDIDA", # missings masivos
    # Tipo de usuario y nivel
    "TIPO_NIVEL",
    "TIPO_USUARIO",
    # Auxiliar
    "archivo_fuente",
]


def seleccionar_columnas(df: pd.DataFrame, log_lines: list) -> pd.DataFrame:
    """
    Retiene las columnas canónicas que existen en el DataFrame.
    Documenta en el log las columnas inesperadas y las ausentes.
    """
    cols_disponibles = set(df.columns)
    cols_esperadas   = set(VARS_CANONICAS)

    inesperadas = cols_disponibles - cols_esperadas
    ausentes    = cols_esperadas   - cols_disponibles

    if inesperadas:
        log_lines.append(
            f"\n  [AVISO] Columnas presentes NO en el esquema canónico "
            f"(se conservan — revisar): {sorted(inesperadas)}"
        )
    if ausentes:
        log_lines.append(
            f"\n  [AVISO] Columnas canónicas AUSENTES en el input: {sorted(ausentes)}"
        )

    # Orden canónico para las que sí existen; las inesperadas van al final
    cols_final  = [c for c in VARS_CANONICAS if c in df.columns]
    cols_final += sorted(inesperadas)
    if "is_duplicado" in df.columns:
        cols_final = ["is_duplicado"] + cols_final

    log_lines.append(f"\n  Columnas en el output final: {len(cols_final)}")
    return df[cols_final]


# =============================================================================
# 8. MAIN
# =============================================================================

def main():
    log_lines = []
    log_lines.append("=" * 70)
    log_lines.append("LIMPIEZA — MÓDULO CANCELACIONES")
    log_lines.append(f"Fecha de ejecución: {date.today().isoformat()}")
    log_lines.append(f"RA: Maria Jose Cadena")
    log_lines.append("=" * 70)

    # 8a. Cargar datos anonimizados
    log_lines.append("\n[1] CARGA DE ARCHIVOS")
    df = cargar_cancelaciones(RUTA_INPUT, log_lines)

    # 8b. Limpieza
    log_lines.append("\n[2] LIMPIEZA")
    df = limpiar_cancelaciones(df, log_lines)

    # 8c. Variables intermitentes
    log_lines.append("\n[3] COBERTURA DE VARIABLES INTERMITENTES")
    reportar_vars_intermitentes(df, log_lines)

    # 8d. Duplicados en el panel apilado
    log_lines.append("\n[4] DUPLICADOS EN EL PANEL CONSOLIDADO")
    # Verificar que las columnas de la llave estén disponibles antes de evaluar
    llave_disponible = [c for c in LLAVE_OBS if c in df.columns]
    if len(llave_disponible) < len(LLAVE_OBS):
        log_lines.append(
            f"  [ADVERTENCIA] Llave incompleta — columnas faltantes: "
            f"{set(LLAVE_OBS) - set(llave_disponible)}"
        )
    df = reportar_duplicados(df, llave_disponible, "panel consolidado", log_lines)

    # 8e. Select final de columnas
    log_lines.append("\n[5] SELECCIÓN DE COLUMNAS FINALES")
    df_final = seleccionar_columnas(df, log_lines)

    # 8f. Resumen del output
    log_lines.append("\n[6] RESUMEN DEL OUTPUT")
    log_lines.append(f"  Filas totales:          {len(df_final):>10,}")
    log_lines.append(f"  Columnas:               {df_final.shape[1]:>10,}")
    log_lines.append(f"  Períodos cubiertos:     {df_final['PERIODO'].nunique():>10,}  "
                     f"({df_final['PERIODO'].min()} → {df_final['PERIODO'].max()})")
    if "correo" in df_final.columns:
        log_lines.append(f"  Estudiantes únicos:     {df_final['correo'].nunique():>10,}")
    n_dup_flag = df_final["is_duplicado"].sum() if "is_duplicado" in df_final.columns else "N/A"
    log_lines.append(f"  Filas marcadas dup:     {n_dup_flag}")

    # 8g. Guardar CSV limpio
    log_lines.append(f"\n[7] GUARDANDO OUTPUT")
    df_final.to_csv(ARCHIVO_SALIDA, index=False, encoding="utf-8-sig")
    log_lines.append(f"  → {ARCHIVO_SALIDA}")

    # 8h. Escribir log
    log_text = "\n".join(log_lines)
    with open(ARCHIVO_LOG, "w", encoding="utf-8") as f:
        f.write(log_text)
    print(log_text)
    print(f"\nLog guardado en: {ARCHIVO_LOG}")


if __name__ == "__main__":
    main()

#%%