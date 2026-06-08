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
#   - Armoniza tipo_cancelacion → categorías canónicas
#   - Armoniza cod_plan → formato estándar sin ceros ni guiones
#   - Armoniza nivel_formacion si existe → colapsa variantes
#   - Guarda un CSV limpio por semestre en DatosArmonizados/2_DatosLimpios/Cancelaciones/
#   - Guarda el CSV consolidado limpio en DatosArmonizados/2_DatosLimpios/Cancelaciones/
#         logs/limpieza_Cancelaciones_YYYY-MM-DD.txt
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
RUTA_INPUT  = DIR_DATOS / "DatosOriginales" / "Cancelaciones"

# Output: CSV limpio consolidado
RUTA_OUTPUT = DIR_DATOS / "DatosArmonizados" / "Cancelaciones"
RUTA_OUTPUT_PERIODOS = RUTA_OUTPUT / "2_DatosLimpios"     # un CSV por período
ARCHIVO_SALIDA = RUTA_OUTPUT / "Cancelaciones_limpio.csv"


# Log
RUTA_LOG    = DIR_CODE / "logs"
ARCHIVO_LOG = RUTA_LOG / f"limpieza_Cancelaciones_{date.today().isoformat()}.txt"

assert RUTA_INPUT.exists(),  f"Ruta de datos no encontrada:  {RUTA_INPUT}"
assert RUTA_OUTPUT.exists(), f"Ruta de output no encontrada: {RUTA_OUTPUT}"
RUTA_OUTPUT_PERIODOS.mkdir(parents=True, exist_ok=True)
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
        log_lines.append(
            f"  [OK] PERIODO — todos los valores cumplen formato YYYY-NS en {archivo}"
        )
    return serie


# =============================================================================
# 3. DETECCIÓN DE DUPLICADOS
#    La unidad de observación es una asignatura cancelada por un estudiante
#    en un período y programa.
#    Clave natural: ID_UNAL + PERIODO + COD_PLAN + COD_ASIGNATURA
# =============================================================================

LLAVE_OBS = ["ID_UNAL", "PERIODO", "COD_PLAN", "COD_ASIGNATURA"]


def reportar_duplicados(
    df: pd.DataFrame, llave: list, contexto: str, log_lines: list
) -> pd.DataFrame:
    """
    Identifica filas duplicadas según la llave dada.
    Añade columna is_duplicado al DataFrame retornado.
    Reporta en el log.
    """
    mask_dup  = df.duplicated(subset=llave, keep=False)
    n_dup     = mask_dup.sum()
    n_grupos  = df[mask_dup].groupby(llave).ngroups if n_dup > 0 else 0

    log_lines.append(f"\n--- Duplicados ({contexto}) ---")
    log_lines.append(f"  Llave: {' + '.join(llave)}")
    log_lines.append(f"  Filas totales:               {len(df):>10,}")
    log_lines.append(
        f"  Filas en grupos duplicados:  {n_dup:>10,}  ({100 * n_dup / len(df):.2f}%)"
    )
    log_lines.append(f"  Grupos únicos duplicados:    {n_grupos:>10,}")

    if n_dup > 0:
        top = (
            df[mask_dup]
            .groupby(llave)
            .size()
            .reset_index(name="n_filas")
            .sort_values("n_filas", ascending=False)
            .head(10)
        )
        log_lines.append("  Top 10 llaves repetidas:")
        for _, row in top.iterrows():
            llave_str = " || ".join(str(row[k]) for k in llave)
            log_lines.append(f"    {llave_str}  →  {row['n_filas']} filas")

    df["is_duplicado"] = mask_dup
    return df


# =============================================================================
# 3b. ELIMINAR DUPLICADOS EXACTOS
# =============================================================================

def resolver_duplicados(
    df: pd.DataFrame,
    llave: list,
    log_lines: list,
    ruta_dup_nat: Path,
) -> pd.DataFrame:
    """
    Elimina duplicados exactos (todas las columnas iguales), keep='first'.
    Retorna el DataFrame sin duplicados exactos.
    """
    n_antes = len(df)

    mask_exactos        = df.duplicated(keep=False)
    n_exactos_grupos    = mask_exactos.sum()
    df_limpio           = df.drop_duplicates(keep="first").copy()   # BUG FIX: ahora se asigna
    n_eliminados_exactos = n_antes - len(df_limpio)

    log_lines.append("\n--- Resolución de duplicados ---")
    log_lines.append(f"  Filas antes:                    {n_antes:>10,}")
    log_lines.append(f"  Filas en duplicados exactos:    {n_exactos_grupos:>10,}")
    log_lines.append(
        f"  Filas eliminadas (exactos):     {n_eliminados_exactos:>10,}  "
        f"[regla: keep='first']"
    )

    return df_limpio    # BUG FIX: variable existente antes del return


# =============================================================================
# 4. CARGA DE ARCHIVOS
# =============================================================================

def cargar_cancelaciones(ruta_input: Path, log_lines: list) -> pd.DataFrame:
    """
    Carga todos los .xlsx de DatosOriginales/Cancelaciones/, añade columna
    ARCHIVO_FUENTE y los apila en un DataFrame único.
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
        nombre    = ruta.stem
        hoja      = HOJA_ESPECIAL.get(nombre, 0)   # 0 = primera hoja por defecto
        df_arch   = pd.read_excel(ruta, sheet_name=hoja, dtype=str)
        df_arch["ARCHIVO_FUENTE"] = nombre
        n_filas   = len(df_arch)
        nota_hoja = f"  [hoja: {hoja}]" if nombre in HOJA_ESPECIAL else ""
        log_lines.append(
            f"  · {nombre}  →  {n_filas:,} filas,  {df_arch.shape[1] - 1} columnas{nota_hoja}"
        )
        dfs.append(df_arch)

    df = pd.concat(dfs, ignore_index=True)
    log_lines.append(f"\nTotal filas apiladas: {len(df):,}")
    return df


# =============================================================================
# 4b. DIAGNÓSTICO (encapsulado en función — BUG FIX: antes estaba suelto)
# =============================================================================

def diagnosticar_df(df: pd.DataFrame, log_lines: list) -> None:
    """
    Ejecuta auditorías de calidad sobre el DataFrame apilado:
      - Cambios de tipo entre archivos
      - Formato de CORREO_INSTITUCIONAL
      - Auditoría de NUMERO_DOCUMENTO
    """

    # --- Detección de cambios de tipo entre archivos ---
    log_lines.append("\n--- Auditoría de tipos por archivo ---")
    tipos_por_columna: dict = {}

    for archivo_fuente in df["ARCHIVO_FUENTE"].unique():
        df_temp = df[df["ARCHIVO_FUENTE"] == archivo_fuente]
        for col in df_temp.columns:
            dtype_actual = str(df_temp[col].dtype)
            tipos_por_columna.setdefault(col, {})[archivo_fuente] = dtype_actual

    columnas_tipo_inconsistente = {
        col: tipos
        for col, tipos in tipos_por_columna.items()
        if len(set(tipos.values())) > 1
    }

    if columnas_tipo_inconsistente:
        for col, detalle in columnas_tipo_inconsistente.items():
            log_lines.append(f"  [CAMBIO DE TIPO] {col}")
            for archivo, dtype in detalle.items():
                log_lines.append(f"    {archivo}: {dtype}")
    else:
        log_lines.append("  [OK] Sin cambios de tipo entre archivos.")

    # --- Verificar formato CORREO_INSTITUCIONAL ---
    col_correo = "CORREO_INSTITUCIONAL" if "CORREO_INSTITUCIONAL" in df.columns else "CORREO"
    if col_correo in df.columns:
        log_lines.append(f"\n--- Auditoría {col_correo} ---")
        correos      = df[col_correo].astype(str).str.strip().str.lower()
        mask_missing = correos.isin(["", "nan", "none"])
        mask_invalido = ~correos.str.endswith("@unal.edu.co") & ~mask_missing
        log_lines.append(f"  Correos inválidos: {mask_invalido.sum():,}")
        log_lines.append(f"  Correos missing:   {mask_missing.sum():,}")

    # --- Auditoría NUMERO_DOCUMENTO ---
    if "NUMERO_DOCUMENTO" in df.columns:
        log_lines.append("\n=== AUDITORÍA NUMERO_DOCUMENTO ===")
        docs    = df["NUMERO_DOCUMENTO"].astype(str).str.strip()
        resumen = {"missing": 0, "solo_numeros": 0, "con_letras": 0,
                   "con_caracteres_especiales": 0}
        longitudes: dict = {}

        for doc in docs:
            doc_lower = doc.lower()
            if doc_lower in ["", "nan", "none"]:
                resumen["missing"] += 1
                continue
            if re.fullmatch(r"\d+", doc):
                resumen["solo_numeros"] += 1
                longitudes[len(doc)] = longitudes.get(len(doc), 0) + 1
            elif re.search(r"[a-zA-Z]", doc):
                resumen["con_letras"] += 1
            else:
                resumen["con_caracteres_especiales"] += 1

        for k, v in resumen.items():
            log_lines.append(f"  {k}: {v:,}")

        log_lines.append("\n  Distribución por longitud (solo numéricos):")
        for longitud in sorted(longitudes):
            log_lines.append(f"    {longitud} cifras: {longitudes[longitud]:,}")

        mask_problematicos = ~docs.str.fullmatch(r"\d+")
        ejemplos = docs[mask_problematicos].drop_duplicates().head(20).tolist()
        if ejemplos:
            log_lines.append(f"\n  Ejemplos problemáticos: {ejemplos}")


# =============================================================================
# 5. LIMPIEZA PRINCIPAL
# =============================================================================

def normalizar_nombre(s) -> str:
    """Mayúsculas, sin tildes/diacríticos, sin caracteres especiales, sin espacios múltiples."""
    if pd.isna(s):
        return s
    s = str(s).upper()
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^A-Z0-9\s]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def armonizar_convenio_plan(df: pd.DataFrame, log_lines: list) -> pd.DataFrame:
    """
    Armonización de CONVENIO_PLAN
    ─────────────────────────────
    Unifica las dos variantes del convenio UPC en el valor canónico:
      'UNIVERSIDAD POPULAR DEL CESAR'  →  'UNIVERSIDAD POPULAR DEL CESAR - UPC'

    La columna ya fue normalizada (mayúsculas, sin tildes) antes de llamar
    a esta función, por lo que la comparación es directa.
    """
    if "CONVENIO_PLAN" not in df.columns:
        log_lines.append(
            "  [AVISO] CONVENIO_PLAN no existe en el DataFrame — "
            "armonización omitida."
        )
        return df

    MAPA_CONVENIO = {
        "UNIVERSIDAD POPULAR DEL CESAR":       "UNIVERSIDAD POPULAR DEL CESAR UPC",
        "UNIVERSIDAD POPULAR DEL CESAR UPC": "UNIVERSIDAD POPULAR DEL CESAR UPC",
        "UNIVERSIDAD POPULAR DEL CESAR - UPC": "UNIVERSIDAD POPULAR DEL CESAR UPC",
    }

    # Contar sólo las filas que realmente cambian de valor
    mask_cambia = df["CONVENIO_PLAN"].isin(
        [k for k, v in MAPA_CONVENIO.items() if k != v]
    )
    n_corregidos = int(mask_cambia.sum())

    df["CONVENIO_PLAN"] = df["CONVENIO_PLAN"].replace(MAPA_CONVENIO)

    log_lines.append(
        f"  [CONVENIO_PLAN] Registros armonizados a 'UNIVERSIDAD POPULAR DEL CESAR - UPC': "
        f"{n_corregidos:,}"
    )
    return df

def armonizar_asignatura(df: pd.DataFrame, log_lines: list) -> pd.DataFrame:
    """
    Armonización de ASIGNATURA
    ─────────────────────────────
    Unifica las dos variantes del convenio UPC en el valor canónico:
      'UNIVERSIDAD POPULAR DEL CESAR'  →  'UNIVERSIDAD POPULAR DEL CESAR - UPC'

    La columna ya fue normalizada (mayúsculas, sin tildes) antes de llamar
    a esta función, por lo que la comparación es directa.
    """
    if "ASIGNATURA" not in df.columns:
        log_lines.append(
            "  [AVISO] ASIGNATURA no existe en el DataFrame — "
            "armonización omitida."
        )
        return df

    MAPA_ASIGNATURA = {
        "ASPECTOS ARQUITECTONICOS EN EL DISENO SISMORESISTENTE":       "ASPECTOS ARQUITECTONICOS EN EL DISENO SISMORRESISTENTE",
        "TALLER DE PROYECTOS PEDAGOGICOS I 2014710":   "TALLER DE PROYECTOS PEDAGOGICOS I",
    }

    # Contar sólo las filas que realmente cambian de valor
    mask_cambia = df["ASIGNATURA"].isin(
        [k for k, v in MAPA_ASIGNATURA.items() if k != v]
    )
    n_corregidos = int(mask_cambia.sum())

    df["ASIGNATURA"] = df["ASIGNATURA"].replace(MAPA_ASIGNATURA)

    log_lines.append(
    f"  [ASIGNATURA] Registros armonizados: {n_corregidos:,}"
    )

    return df


def limpiar_documento(df: pd.DataFrame, log_lines: list) -> pd.DataFrame:
    """
    Limpieza de DOCUMENTO (antes del renombrado a NUMERO_DOCUMENTO)
    ────────────────────────────────────────────────────────────────
    Elimina ceros a la izquierda en la variable DOCUMENTO. La variable se
    mantiene como texto para preservar identificadores con caracteres especiales
    o longitudes significativas. Si al retirar los ceros el valor queda vacío
    (p. ej. el documento era "000"), se reemplaza por NaN.

    Nota: se aplica sobre la columna 'DOCUMENTO' (nombre original en la fuente),
    antes del paso de renombrado a 'NUMERO_DOCUMENTO'.
    """
    col = "DOCUMENTO" if "DOCUMENTO" in df.columns else (
        "NUMERO_DOCUMENTO" if "NUMERO_DOCUMENTO" in df.columns else None
    )

    if col is None:
        log_lines.append(
            "  [AVISO] Columna DOCUMENTO / NUMERO_DOCUMENTO no encontrada — "
            "limpieza de ceros omitida."
        )
        return df

    original = df[col].astype(str).str.strip()

    # lstrip("0") sobre valores no-nulos; conserva "0" puro como NaN
    def _lstrip_ceros(val: str) -> object:
        low = val.lower()
        if low in ("nan", "none", ""):
            return np.nan
        resultado = val.lstrip("0")
        return resultado if resultado != "" else np.nan

    limpio = original.apply(_lstrip_ceros)

    # Contar filas donde el valor cambió efectivamente
    n_modificados = int((original != limpio.astype(str)).sum())
    # Ajuste: comparar solo sobre filas no-nulas para evitar falsos positivos
    mask_no_nulo  = original.str.lower().isin(["nan", "none", ""]) == False
    n_modificados = int(
        (original[mask_no_nulo] != limpio[mask_no_nulo].astype(str)).sum()
    )

    df[col] = limpio

    log_lines.append(
        f"  [DOCUMENTO] Registros con ceros a la izquierda eliminados: "
        f"{n_modificados:,}"
    )
    return df


def corregir_subacceso(df: pd.DataFrame, log_lines: list) -> pd.DataFrame:
    """
    Corrección de SUBACCESO según COD_SUBACCESO
    ─────────────────────────────────────────────
    Sobrescribe SUBACCESO con el valor canónico para los códigos PEAMA y PAES
    listados en el diccionario. Se aplica después de la conversión numérica de
    COD_SUBACCESO, por lo que la comparación usa el tipo float/int resultante
    del pd.to_numeric(..., errors='coerce').

    Códigos incluidos:
      4  → PAES - MUNICIPIO
     18  → PEAMA - ORINOQUIA - PROGRAMA ESPECIAL DE ADMISION Y MOVILIDAD ACADEMICA
     19  → PEAMA - AMAZONIA  - PROGRAMA ESPECIAL DE ADMISION Y MOVILIDAD ACADEMICA
     20  → PEAMA - CARIBE    - PROGRAMA ESPECIAL DE ADMISION Y MOVILIDAD ACADEMICA
     23  → PEAMA - TUMACO    - PROGRAMA ESPECIAL DE ADMISION Y MOVILIDAD ACADEMICA
     26  → PEAMA - BOGOTA-SUMAPAZ - PROGRAMA ESPECIAL DE ADMISION Y MOVILIDAD ACADEMICA
    """
    if "SUBACCESO" not in df.columns or "COD_SUBACCESO" not in df.columns:
        log_lines.append(
            "  [AVISO] SUBACCESO o COD_SUBACCESO no encontrados — "
            "corrección omitida."
        )
        return df

    MAPA_SUBACCESO = {
        4:  "PAES - MUNICIPIO",
        18: "PEAMA - ORINOQUIA - PROGRAMA ESPECIAL DE ADMISION Y MOVILIDAD ACADEMICA",
        19: "PEAMA - AMAZONIA - PROGRAMA ESPECIAL DE ADMISION Y MOVILIDAD ACADEMICA",
        20: "PEAMA - CARIBE - PROGRAMA ESPECIAL DE ADMISION Y MOVILIDAD ACADEMICA",
        23: "PEAMA - TUMACO - PROGRAMA ESPECIAL DE ADMISION Y MOVILIDAD ACADEMICA",
        26: "PEAMA - BOGOTA-SUMAPAZ - PROGRAMA ESPECIAL DE ADMISION Y MOVILIDAD ACADEMICA",
    }

    # COD_SUBACCESO ya fue convertido a numérico; comparamos con int via map
    # Usamos .astype("Int64") para manejar NaN sin errores
    cod_int = pd.to_numeric(df["COD_SUBACCESO"], errors="coerce")
    n_corregidos = 0

    for codigo, valor_canonico in MAPA_SUBACCESO.items():
        mask = cod_int == codigo
        n_corregidos += int(mask.sum())
        df.loc[mask, "SUBACCESO"] = valor_canonico

    log_lines.append(
        f"  [SUBACCESO] Registros sobrescritos con valor canónico "
        f"(códigos PEAMA/PAES): {n_corregidos:,}"
    )
    return df


def corregir_facultad_asignatura(df: pd.DataFrame, log_lines: list) -> pd.DataFrame:
    """
    Corrección de FACULTAD_ASIGNATURA para COD_FACULTAD_ASIGNATURA = 1004
    ────────────────────────────────────────────────────────────────────────
    Armoniza las dos variantes del nombre de la Escuela de Pregrado La Paz:
      'ESCUELA DE PREGRADO DE LA PAZ'  →  'ESCUELA DE PREGRADO LA PAZ'

    La corrección es estrictamente acotada a registros con
    COD_FACULTAD_ASIGNATURA == 1004 para no afectar otros registros.
    """
    if "FACULTAD_ASIGNATURA" not in df.columns or \
       "COD_FACULTAD_ASIGNATURA" not in df.columns:
        log_lines.append(
            "  [AVISO] FACULTAD_ASIGNATURA o COD_FACULTAD_ASIGNATURA no encontrados — "
            "corrección omitida."
        )
        return df

    VARIANTES_1004 = {"ESCUELA DE PREGRADO LA PAZ", "ESCUELA DE PREGRADO DE LA PAZ"}
    VALOR_CANONICO = "ESCUELA DE PREGRADO LA PAZ"

    # COD_FACULTAD_ASIGNATURA ya es numérico; comparamos como string para
    # tolerar tanto float (1004.0) como int (1004)
    mask_cod  = df["COD_FACULTAD_ASIGNATURA"].astype(str).str.split(".").str[0] == "1004"
    mask_var  = df["FACULTAD_ASIGNATURA"].isin(VARIANTES_1004)
    mask_cambia = mask_cod & mask_var & (df["FACULTAD_ASIGNATURA"] != VALOR_CANONICO)
    n_corregidos = int(mask_cambia.sum())

    df.loc[mask_cod & mask_var, "FACULTAD_ASIGNATURA"] = VALOR_CANONICO

    log_lines.append(
        f"  [FACULTAD_ASIGNATURA] Registros armonizados a "
        f"'ESCUELA DE PREGRADO LA PAZ' (cod 1004): {n_corregidos:,}"
    )
    return df


def limpiar_cancelaciones(df: pd.DataFrame, log_lines: list) -> pd.DataFrame:
    """
    Aplica las transformaciones de limpieza al DataFrame apilado.
    """

    # 5c. Validar formato de PERIODO
    log_lines.append("\n--- Validación de PERIODO ---")
    if "PERIODO" in df.columns:
        for arch in df["ARCHIVO_FUENTE"].unique():
            subset = df.loc[df["ARCHIVO_FUENTE"] == arch, "PERIODO"]
            validar_periodo(subset, arch, log_lines)
    else:
        log_lines.append("  [ERROR] Columna PERIODO no encontrada.")

    # 5d-pre. Limpieza de DOCUMENTO (antes del renombrado canónico)
    #   Se ejecuta aquí porque la columna aún se llama 'DOCUMENTO' en la fuente.
    log_lines.append("\n--- Limpieza de ceros en DOCUMENTO ---")
    df = limpiar_documento(df, log_lines)

    # 5d. Armonizar nombres canónicos de variables
    log_lines.append("\n--- Armonización de nombres canónicos ---")

    RENOMBRES = {
        "CORREO_INSTITUCIONAL": "CORREO",
        "DOCUMENTO":            "NUMERO_DOCUMENTO",
        "NOMBRES_APELLIDOS":    "NOMBRE_COMPLETO",
    }
    df = df.rename(columns=RENOMBRES)
    for orig, canon in RENOMBRES.items():
        if orig in df.columns or canon in df.columns:
            log_lines.append(f"  {orig} → {canon}")

    # Columnas canónicas ausentes en Cancelaciones — se crean vacías
    for col_ausente in ["TIPO_DOCUMENTO", "SEXO", "FECHA_NACIMIENTO"]:
        df[col_ausente] = np.nan
        log_lines.append(
            f"  {col_ausente}: no existe en la fuente → columna vacía (NaN)"
        )

    # 5e. Normalización de columnas string
    COL_STRINGS = [
        "NOMBRE_COMPLETO", "LOGIN_USUARIO_ESTUDIANTE", "PLAN", "DESC_PROG_CURRICULAR",
        "ASIGNATURA", "FACULTAD_ASIGNATURA", "UAB_ASIGNATURA", "TIPO_CANCELACION",
        "CAUSA_ANULA", "USUARIO_CANCELACION", "NOTA_ALFABETICA", "ACCESO",
        "SUBACCESO", "FACULTAD", "SEDE", "TIPO_NIVEL", "TIPO_USUARIO", "NODO_INICIO", "CONVENIO_PLAN"
    ]

    for col in COL_STRINGS:
        if col in df.columns:
            df[col] = df[col].apply(normalizar_nombre)
            df[col] = df[col].astype(str).str.strip().replace("nan", np.nan)
            log_lines.append(
                f"  {col}: normalizado (mayúsculas, sin tildes, strip)"
            )

    log_lines.append("  Columnas string: normalización aplicada.")

    # 5f. Conversiones de tipo
    log_lines.append("\n--- Conversiones de tipo ---")

    if "FECHA" in df.columns:
        df["FECHA"] = pd.to_datetime(df["FECHA"], errors="coerce")
        n_fecha_inv = df["FECHA"].isna().sum()
        log_lines.append(
            f"  FECHA convertida a datetime. Valores no parseables: {n_fecha_inv:,}"
        )

    # BUG FIX: nombre de lista corregido de COLS_INT → COLS_NUM (consistente)
    COLS_NUM = [
        "COD_ACCESO", "COD_FACULTAD", "COD_FACULTAD_ASIGNATURA",
        "COD_NODO_INICIO", "COD_SEDE_ASIGNATURA", "COD_SUBACCESO",
        "CREDITOS", "HIST_ACAD", "PBM", "PUNTAJE_ADMISION",
        "GRUP_ACTA", "COD_UAB_ASIGNATURA",
    ]
    for col in COLS_NUM:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    log_lines.append(
        f"  Tipos aplicados (numérico): {[c for c in COLS_NUM if c in df.columns]}"
    )

    # 5g. Validar rango NOTA_NUMERICA
    log_lines.append("\n--- Validación NOTA_NUMERICA ---")
    if "NOTA_NUMERICA" in df.columns:
        df["NOTA_NUMERICA"] = pd.to_numeric(df["NOTA_NUMERICA"], errors="coerce")
        fuera_rango = df["NOTA_NUMERICA"].dropna()
        fuera_rango = fuera_rango[(fuera_rango < 0) | (fuera_rango > 5)]
        if len(fuera_rango) > 0:
            log_lines.append(
                f"  [ADVERTENCIA] {len(fuera_rango):,} valores de NOTA_NUMERICA "
                f"fuera de [0, 5]. Min: {fuera_rango.min():.2f}, "
                f"Max: {fuera_rango.max():.2f}"
            )
        else:
            log_lines.append("  [OK] NOTA_NUMERICA en rango [0, 5].")

    # 5h-1. Armonizaciones de categorías
    #   Orden: primero las que dependen de columnas numéricas ya convertidas
    #   (SUBACCESO depende de COD_SUBACCESO numérico, FACULTAD_ASIGNATURA de
    #   COD_FACULTAD_ASIGNATURA numérico). CONVENIO_PLAN se aplica después de
    #   la normalización de strings (paso 5e).
    log_lines.append("\n--- Armonizaciones de categorías ---")
    df = armonizar_convenio_plan(df, log_lines)
    df = armonizar_asignatura(df, log_lines)
    df = corregir_subacceso(df, log_lines)
    df = corregir_facultad_asignatura(df, log_lines)

    return df   # BUG FIX: faltaba el return


# =============================================================================
# 6. VARIABLES INTERMITENTES  (BUG FIX: función faltante — ahora definida)
# =============================================================================

def reportar_vars_intermitentes(df: pd.DataFrame, log_lines: list) -> None:
    """
    Reporta columnas que no están presentes en todos los archivos fuente
    (variables intermitentes). Útil para detectar cambios de esquema entre períodos.
    """
    log_lines.append("\n--- Variables intermitentes por archivo fuente ---")
    archivos = df["ARCHIVO_FUENTE"].unique()
    cobertura: dict = {}

    for arch in archivos:
        cols_arch = set(df[df["ARCHIVO_FUENTE"] == arch].dropna(axis=1, how="all").columns)
        cobertura[arch] = cols_arch

    todas_las_cols = set(df.columns)
    intermitentes  = {
        col for col in todas_las_cols
        if any(col not in cobertura[a] for a in archivos)
    }

    if not intermitentes:
        log_lines.append("  [OK] Todas las columnas presentes en todos los archivos.")
        return

    log_lines.append(
        f"  {len(intermitentes)} columna(s) no aparecen en todos los archivos:"
    )
    for col in sorted(intermitentes):
        presente_en = sum(1 for a in archivos if col in cobertura[a])
        log_lines.append(
            f"  · {col:<45}  presente en {presente_en}/{len(archivos)} archivos"
        )


# =============================================================================
# 7. SELECCIÓN DE COLUMNAS FINALES
# =============================================================================

VARS_CANONICAS = [       
    "SEDE",
    "COD_FACULTAD",
    "FACULTAD",
    "COD_PLAN",
    "PLAN",
    "COD_PROG_CURRICULAR",
    "DESC_PROG_CURRICULAR",
    "CONVENIO_PLAN",
    "TIPO_NIVEL",
    "HIST_ACAD",
    "DOCUMENTO",
    "NOMBRES_APELLIDOS",
    "CORREO_INSTITUCIONAL",
    "LOGIN_USUARIO_ESTUDIANTE",
    "ADMISION",
    "CONVOCATORIA",
    "APERTURA",
    "COD_ACCESO",
    "ACCESO",
    "COD_SUBACCESO",
    "SUBACCESO",
    "COD_NODO_INICIO",
    "NODO_INICIO",
    "COD_ASIGNATURA",
    "ASIGNATURA",
    "NOTA_ALFABETICA",
    "NOTA_NUMERICA",
    "CREDITOS",
    "GRUP_ACTI",
    "DES_GR_ACTIV",
    "GRUP_ACTA",
    "PERIODO",
    "COD_SEDE_ASIGNATURA",
    "COD_FACULTAD_ASIGNATURA",
    "FACULTAD_ASIGNATURA",
    "COD_UAB_ASIGNATURA",
    "UAB_ASIGNATURA",
    "TIPO_CANCELACION",
    "FECHA",
    "CORRECIÓN DE CRED. PERDIDA",
    "CAUSA_ANULA",
    "USUARIO_CANCELACION",
    "TIPO_USUARIO",
    "PBM",
    "PUNTAJE_ADMISION",
    "ARCHIVO_FUENTE",
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

    # Excluir columnas auxiliares de diagnóstico del output final
    COLS_EXCLUIR = {"is_duplicado", "is_duplicado.1"}

    cols_final  = [c for c in VARS_CANONICAS if c in df.columns]
    cols_final += sorted(inesperadas - COLS_EXCLUIR)

    log_lines.append(f"\n  Columnas en el output final: {len(cols_final)}")
    return df[cols_final]


# =============================================================================
# 8. DICCIONARIO DE ASIGNATURAS
# =============================================================================

# Ruta de salida del diccionario (mismo directorio que el CSV limpio)
ARCHIVO_DICCIONARIO = RUTA_OUTPUT / "diccionario_asignaturas.csv"

# Columnas de adscripción institucional que se consolidan en el diccionario
COLS_ADSCRIPCION = [
    "COD_SEDE_ASIGNATURA",       # numérico — código de sede
    "COD_FACULTAD_ASIGNATURA",   # numérico — código de facultad
    "FACULTAD_ASIGNATURA",       # textual  — nombre de facultad
    "COD_UAB_ASIGNATURA",        # numérico — código de UAB
    "UAB_ASIGNATURA",            # textual  — nombre de UAB
]


def construir_diccionario_asignaturas(
    df: pd.DataFrame, log_lines: list
) -> pd.DataFrame:
    """
    Construye un diccionario único de asignaturas a partir del panel limpio.

    Llave:    COD_ASIGNATURA
    Atributos: ASIGNATURA, CREDITOS,
               COD_SEDE_ASIGNATURA, COD_FACULTAD_ASIGNATURA, FACULTAD_ASIGNATURA,
               COD_UAB_ASIGNATURA,  UAB_ASIGNATURA

    Estrategia de deduplicación:
      - Para cada COD_ASIGNATURA se toma la moda de cada atributo (valor más
        frecuente en el panel). Si hay empate se elige el primero en orden
        alfabético, lo que hace el proceso determinista.
      - Se reportan en el log los códigos con valores inconsistentes entre
        períodos (p. ej. un mismo código que aparece con dos nombres distintos),
        para que la RA pueda revisarlos manualmente.

    Retorna un DataFrame con una fila por COD_ASIGNATURA, ordenado por código.
    """

    COLS_REQUERIDAS = ["COD_ASIGNATURA", "ASIGNATURA", "CREDITOS"] + COLS_ADSCRIPCION
    cols_disponibles = [c for c in COLS_REQUERIDAS if c in df.columns]
    cols_faltantes   = [c for c in COLS_REQUERIDAS if c not in df.columns]

    log_lines.append("\n--- Construcción del diccionario de asignaturas ---")
    if cols_faltantes:
        log_lines.append(
            f"  [AVISO] Columnas no disponibles (se omiten): {cols_faltantes}"
        )

    if "COD_ASIGNATURA" not in df.columns:
        log_lines.append(
            "  [ERROR] COD_ASIGNATURA no existe en el DataFrame — "
            "diccionario no generado."
        )
        return pd.DataFrame()

    subset = df[cols_disponibles].copy()

    # Moda determinista: para cada grupo toma el valor más frecuente;
    # en caso de empate, el primero en orden alfabético (sort antes de agg).
    def moda_det(s: pd.Series):
        vc = s.dropna().value_counts()
        if vc.empty:
            return np.nan
        max_freq = vc.iloc[0]
        candidatos = sorted(vc[vc == max_freq].index.astype(str).tolist())
        return candidatos[0]

    cols_agg = [c for c in cols_disponibles if c != "COD_ASIGNATURA"]
    dicc = (
        subset
        .groupby("COD_ASIGNATURA", sort=True)[cols_agg]
        .agg(moda_det)
        .reset_index()
    )

    # Restaurar tipo numérico en columnas de código y créditos
    for col in ["CREDITOS"] + [c for c in COLS_ADSCRIPCION if "COD_" in c]:
        if col in dicc.columns:
            dicc[col] = pd.to_numeric(dicc[col], errors="coerce")

    n_asignaturas = len(dicc)
    log_lines.append(f"  Asignaturas únicas:      {n_asignaturas:>8,}")

    # --- Detectar inconsistencias: misma clave, distintos valores ---
    log_lines.append("\n  Inconsistencias detectadas (mismo código, valores distintos):")
    hay_inconsistencias = False

    for col in cols_agg:
        n_vals = (
            subset.dropna(subset=[col])
            .groupby("COD_ASIGNATURA")[col]
            .nunique()
        )
        inconsistentes = n_vals[n_vals > 1]
        if len(inconsistentes) > 0:
            hay_inconsistencias = True
            log_lines.append(
                f"  · {col:<35}  {len(inconsistentes):>5,} código(s) con >1 valor"
            )
            # Mostrar hasta 5 ejemplos
            ejemplos = inconsistentes.head(5).index.tolist()
            for cod in ejemplos:
                vals = (
                    subset.loc[subset["COD_ASIGNATURA"] == cod, col]
                    .dropna()
                    .unique()
                    .tolist()
                )
                log_lines.append(f"      COD {cod}: {vals}")

    if not hay_inconsistencias:
        log_lines.append("  [OK] Sin inconsistencias detectadas.")

    return dicc


# =============================================================================
# 9b. DICCIONARIO DE VARIABLES
# =============================================================================

ARCHIVO_DICCIONARIO_VARS = RUTA_OUTPUT / "diccionario_variables.csv"

# Metadatos estáticos del esquema canónico.
# Campos: variable, tipo, valores_formato, descripcion
# La disponibilidad por año/período se calcula dinámicamente desde df_final.
METADATOS_VARIABLES = [
    ("ID_UNAL",                 "string",    "cadena alfanumérica única (ej. U001234)",
     "Identificador anonimizado del estudiante; reemplaza CORREO usando la llave maestra LLAVE_ID_UNAL_FCE.csv. Parte de la llave natural del panel"),
    ("SEDE",                    "string",    "BOGOTA, MEDELLIN, MANIZALES, PALMIRA, ORINOQUIA, AMAZONIA, CARIBE, TUMACO",
     "Sede de la UNAL donde está matriculado el estudiante"),
    ("COD_FACULTAD",            "numérico",  "entero (ej. 1, 2, 4)",
     "Código numérico de la facultad del programa del estudiante"),
    ("FACULTAD",                "string",    "CIENCIAS ECONOMICAS, INGENIERIA, CIENCIAS, etc.",
     "Nombre de la facultad del programa del estudiante"),
    ("COD_PLAN",                "string",    "sin ceros ni guiones (ej. 2557, 2879)",
     "Código del plan de estudios armonizado"),
    ("PLAN",                    "string",    "texto libre",
     "Nombre del plan de estudios"),
    ("COD_PROG_CURRICULAR",     "string",    "código interno",
     "Código del programa curricular"),
    ("DESC_PROG_CURRICULAR",    "string",    "texto libre",
     "Descripción del programa curricular"),
    ("CONVENIO_PLAN",           "string",    "texto o NaN",
     "Convenio interinstitucional asociado al plan, si aplica"),
    ("TIPO_NIVEL",              "string",    "PREGRADO, POSGRADO, ESPECIALIZACION, MAESTRIA, DOCTORADO",
     "Nivel de formación del programa"),
    ("ADMISION",                "string",    "YYYY-NS",
     "Período de admisión del estudiante al programa"),
    ("CONVOCATORIA",            "string",    "texto",
     "Convocatoria del proceso de admisión"),
    ("APERTURA",                "string",    "texto",
     "Apertura del proceso de admisión"),
    ("COD_ACCESO",              "numérico",  "entero",
     "Código del tipo de acceso con que ingresó el estudiante"),
    ("ACCESO",                  "string",    "REGULAR, ESPECIAL, CONVENIO, MEJORES BACHILLERES, etc.",
     "Modalidad de acceso con que ingresó el estudiante"),
    ("COD_SUBACCESO",           "numérico",  "entero",
     "Código del subtipo de acceso"),
    ("SUBACCESO",               "string",    "texto",
     "Descripción del subtipo de acceso"),
    ("COD_NODO_INICIO",         "numérico",  "entero",
     "Código del nodo de inicio en la estructura curricular"),
    ("NODO_INICIO",             "string",    "texto",
     "Nombre del nodo de inicio en la estructura curricular"),
    ("COD_ASIGNATURA",          "string",    "código numérico como string",
     "Código de la asignatura cancelada; parte de la llave natural"),
    ("ASIGNATURA",              "string",    "texto en mayúsculas",
     "Nombre de la asignatura cancelada"),
    ("NOTA_ALFABETICA",         "string",    "AP, NA, NO_AP, NaN",
     "Nota alfabética si existía registro antes de la cancelación"),
    ("NOTA_NUMERICA",           "numérico",  "0.0 – 5.0",
     "Nota numérica si existía registro; validada en rango [0, 5]"),
    ("CREDITOS",                "numérico",  "entero (típico 1–10)",
     "Número de créditos académicos de la asignatura"),
    ("GRUP_ACTI",               "string",    "texto",
     "Grupo de actividad académica"),
    ("DES_GR_ACTIV",            "string",    "texto",
     "Descripción del grupo de actividad académica"),
    ("GRUP_ACTA",               "numérico",  "entero",
     "Número de acta del grupo"),
    ("PERIODO",                 "string",    "YYYY-1S o YYYY-2S (ej. 2023-1S)",
     "Período académico en que se realizó la cancelación; parte de la llave natural"),
    ("COD_SEDE_ASIGNATURA",     "numérico",  "entero",
     "Código de la sede donde se ofrece la asignatura"),
    ("COD_FACULTAD_ASIGNATURA", "numérico",  "entero",
     "Código de la facultad que ofrece la asignatura"),
    ("FACULTAD_ASIGNATURA",     "string",    "texto",
     "Nombre de la facultad que ofrece la asignatura"),
    ("COD_UAB_ASIGNATURA",      "numérico",  "entero",
     "Código de la Unidad Académica Básica (UAB) que ofrece la asignatura"),
    ("UAB_ASIGNATURA",          "string",    "texto",
     "Nombre de la Unidad Académica Básica que ofrece la asignatura"),
    ("TIPO_CANCELACION",        "string",    "DEFINITIVA, PARCIAL, AUTOMATICA, VOLUNTARIA, etc.",
     "Tipo de cancelación de la matrícula o asignatura"),
    ("FECHA",                   "datetime",  "YYYY-MM-DD",
     "Fecha en que se realizó la cancelación"),
    ("CORRECIÓN DE CRED. PERDIDA", "string", "texto o NaN",
     "Corrección sobre créditos perdidos; nombre con tilde conservado del original"),
    ("CAUSA_ANULA",             "string",    "texto",
     "Causa de la anulación o cancelación registrada en el sistema"),
    ("USUARIO_CANCELACION",     "string",    "texto",
     "Usuario del sistema SIA que ejecutó la cancelación"),
    ("TIPO_USUARIO",            "string",    "ESTUDIANTE, ADMINISTRATIVO, SISTEMA, etc.",
     "Tipo del usuario que realizó la cancelación"),
    ("PBM",                     "numérico",  "0 – 100",
     "Puntaje Básico de Matrícula; proxy del nivel socioeconómico del estudiante"),
    ("PUNTAJE_ADMISION",        "numérico",  "decimal",
     "Puntaje con que el estudiante fue admitido al programa"),
    ("ARCHIVO_FUENTE",          "string",    "Cancelaciones_YYYY-NS",
     "Nombre del archivo Excel original del que proviene la fila"),
]


def construir_diccionario_variables(
    df: pd.DataFrame,
    metadatos: list,
    log_lines: list,
) -> pd.DataFrame:
    """
    Genera el diccionario de variables del módulo Cancelaciones.

    Columnas del output:
      variable         — nombre canónico de la columna
      tipo             — tipo de dato (string, numérico, datetime)
      valores_formato  — rango de valores o formato esperado
      descripcion      — significado sustantivo
      en_datos         — 1/0 si la variable existe en df_final
      periodos_con_datos — lista de períodos YYYY-NS donde la columna
                           tiene al menos un valor no nulo (ej. "2019-1S,2019-2S,…")
      anios_con_datos  — lista de años donde hay al menos un período con datos
                         (ej. "2019,2020,2021")
      cobertura_periodos — fracción de períodos con datos / total períodos
                           (0.00–1.00)
    """
    log_lines.append("\n--- Construcción del diccionario de variables ---")

    periodos_todos: list = []
    if "PERIODO" in df.columns:
        periodos_todos = sorted(df["PERIODO"].dropna().unique().tolist())

    filas = []
    for variable, tipo, valores_formato, descripcion in metadatos:
        en_datos = int(variable in df.columns)

        if en_datos and periodos_todos and "PERIODO" in df.columns:
            # Períodos donde la columna tiene al menos un valor no nulo
            periodos_con = []
            for per in periodos_todos:
                mascara = df["PERIODO"] == per
                if df.loc[mascara, variable].notna().any():
                    periodos_con.append(per)
        elif en_datos and not periodos_todos:
            periodos_con = ["sin_periodo"]
        else:
            periodos_con = []

        # Años únicos derivados de los períodos con datos
        anios_con = sorted({p[:4] for p in periodos_con if len(p) >= 4})

        cobertura = (
            round(len(periodos_con) / len(periodos_todos), 4)
            if periodos_todos else (1.0 if en_datos else 0.0)
        )

        filas.append({
            "variable":           variable,
            "tipo":               tipo,
            "valores_formato":    valores_formato,
            "descripcion":        descripcion,
            "en_datos":           en_datos,
            "periodos_con_datos": ", ".join(periodos_con) if periodos_con else "",
            "anios_con_datos":    ", ".join(anios_con)    if anios_con    else "",
            "cobertura_periodos": cobertura,
        })

    df_vars = pd.DataFrame(filas)

    n_presentes  = df_vars["en_datos"].sum()
    n_ausentes   = len(df_vars) - n_presentes
    log_lines.append(f"  Variables en el esquema canónico: {len(df_vars)}")
    log_lines.append(f"    · presentes en df_final:  {n_presentes}")
    log_lines.append(f"    · ausentes en df_final:   {n_ausentes}")

    # Variables con cobertura parcial (presentes pero no en todos los períodos)
    parciales = df_vars[
        (df_vars["en_datos"] == 1) & (df_vars["cobertura_periodos"] < 1.0)
    ]
    if not parciales.empty:
        log_lines.append(
            f"\n  Variables con cobertura parcial (<100% de períodos):"
        )
        for _, row in parciales.iterrows():
            log_lines.append(
                f"    · {row['variable']:<40}  "
                f"cobertura: {row['cobertura_periodos']:.0%}  "
                f"({row['anios_con_datos']})"
            )
    else:
        log_lines.append(
            "  [OK] Todas las variables presentes tienen cobertura 100%."
        )

    return df_vars


# =============================================================================
# 9. MAIN
# =============================================================================

def main():
    log_lines = []
    log_lines.append("=" * 70)
    log_lines.append("LIMPIEZA — MÓDULO CANCELACIONES")
    log_lines.append(f"Fecha de ejecución: {date.today().isoformat()}")
    log_lines.append("RA: Maria Jose Cadena")
    log_lines.append("=" * 70)

    # 8a. Cargar archivos originales
    log_lines.append("\n[1] CARGA DE ARCHIVOS")
    df = cargar_cancelaciones(RUTA_INPUT, log_lines)

    # 8b. Diagnóstico previo a limpieza
    log_lines.append("\n[1b] DIAGNÓSTICO PREVIO")
    diagnosticar_df(df, log_lines)

    # 8c. Limpieza
    log_lines.append("\n[2] LIMPIEZA")
    df = limpiar_cancelaciones(df, log_lines)

    # 8d. Resolver duplicados exactos
    log_lines.append("\n[3] RESOLUCIÓN DE DUPLICADOS EXACTOS")
    ruta_dup_nat = RUTA_OUTPUT / "duplicados_naturales"
    ruta_dup_nat.mkdir(parents=True, exist_ok=True)
    df = resolver_duplicados(df, LLAVE_OBS, log_lines, ruta_dup_nat)

    # 8e. Variables intermitentes
    log_lines.append("\n[4] COBERTURA DE VARIABLES INTERMITENTES")
    reportar_vars_intermitentes(df, log_lines)

    # 8f. Duplicados en el panel apilado
    log_lines.append("\n[5] DUPLICADOS EN EL PANEL CONSOLIDADO")
    llave_disponible = [c for c in LLAVE_OBS if c in df.columns]
    if len(llave_disponible) < len(LLAVE_OBS):
        log_lines.append(
            f"  [ADVERTENCIA] Llave incompleta — columnas faltantes: "
            f"{set(LLAVE_OBS) - set(llave_disponible)}"
        )
    df = reportar_duplicados(df, llave_disponible, "panel consolidado", log_lines)

    # 8g. Selección de columnas canónicas
    log_lines.append("\n[6] SELECCIÓN DE COLUMNAS FINALES")
    df_final = seleccionar_columnas(df, log_lines)

    # 8h. Diccionario de asignaturas
    log_lines.append("\n[7] DICCIONARIO DE ASIGNATURAS")
    df_dicc = construir_diccionario_asignaturas(df_final, log_lines)
    if not df_dicc.empty:
        df_dicc.to_csv(ARCHIVO_DICCIONARIO, index=False, encoding="utf-8-sig")
        log_lines.append(f"  → {ARCHIVO_DICCIONARIO}")
    else:
        log_lines.append("  [AVISO] Diccionario vacío — no se guardó archivo.")

    # 8i. Resumen del output
    log_lines.append("\n[8] RESUMEN DEL OUTPUT")
    log_lines.append(f"  Filas totales:          {len(df_final):>10,}")
    log_lines.append(f"  Columnas:               {df_final.shape[1]:>10,}")
    if "PERIODO" in df_final.columns:
        log_lines.append(
            f"  Períodos cubiertos:     {df_final['PERIODO'].nunique():>10,}  "
            f"({df_final['PERIODO'].min()} → {df_final['PERIODO'].max()})"
        )
    if "ID_UNAL" in df_final.columns:
        log_lines.append(
            f"  Estudiantes únicos:     {df_final['ID_UNAL'].nunique():>10,}"
        )
    if not df_dicc.empty:
        log_lines.append(f"  Asignaturas en dicc.:   {len(df_dicc):>10,}")

    # 8j. Guardar CSV limpio — por período y consolidado
    log_lines.append("\n[9] GUARDANDO OUTPUT")

    # — Un archivo por período —
    if "PERIODO" in df_final.columns:
        periodos = sorted(df_final["PERIODO"].dropna().unique())
        for periodo in periodos:
            df_per = df_final[df_final["PERIODO"] == periodo].copy()
            nombre_archivo = RUTA_OUTPUT_PERIODOS / f"Cancelaciones_{periodo}.csv"
            df_per.to_csv(nombre_archivo, index=False, encoding="utf-8-sig")
            log_lines.append(
                f"  → {nombre_archivo}  ({len(df_per):,} filas)"
            )
        log_lines.append(
            f"\n  Total archivos por período guardados: {len(periodos)}"
        )
    else:
        log_lines.append(
            "  [ADVERTENCIA] Columna PERIODO ausente — "
            "no se guardaron archivos por período."
        )

    # — Archivo consolidado general —
    df_final.to_csv(ARCHIVO_SALIDA, index=False, encoding="utf-8-sig")
    log_lines.append(f"\n  → {ARCHIVO_SALIDA}  ({len(df_final):,} filas — consolidado)")

    # 8k. Escribir log
    log_text = "\n".join(log_lines)
    with open(ARCHIVO_LOG, "w", encoding="utf-8") as f:
        f.write(log_text)
    print(log_text)
    print(f"\nLog guardado en: {ARCHIVO_LOG}")


if __name__ == "__main__":
    main()

#%%