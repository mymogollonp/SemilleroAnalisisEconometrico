#%%
# =============================================================================
# 04_Verificar_Armonización_MJC.py
# Semillero de Análisis Econométrico — UNAL FCE
# Fecha: 2026-05-31
#
# Propósito: Generar el inventario de variables categóricas del módulo de
#   Cancelaciones para apoyar el proceso de armonización histórica.
#   - Lee los .xlsx originales de DatosOriginales/Cancelaciones/ (READ-ONLY)
#   - Consolida todos los períodos en un único DataFrame
#   - Por cada variable categórica genera una hoja con:
#       * Todos los códigos y etiquetas observados históricamente
#       * N_TOTAL: frecuencia total del código
#       * N_PERIODOS: número de archivos en que aparece
#       * Presencia binaria (0/1) por archivo fuente
#       * Columnas vacías CODIGO_CANONICO y CODIGO_ARMONIZADO para diligenciar
#   - Analiza consistencia de pares código → etiqueta (relaciones 1:1 vs N:1)
#   - Genera hojas MAP_<VAR> con el detalle de cada par código–etiqueta
#   - Guarda un resumen de relaciones en la hoja RESUMEN_RELACIONES
#
# Input:  DatosOriginales/Cancelaciones/*.xlsx
# Output: DatosArmonizados/Cancelaciones/Inventario_Armonizacion.xlsx
#             └── [hoja por variable]   COD | LABEL | N_TOTAL | N_PERIODOS
#                                       | [archivo_1 … archivo_n]
#                                       | CODIGO_CANONICO | CODIGO_ARMONIZADO
#             └── RESUMEN_RELACIONES    análisis de consistencia código–etiqueta
#             └── MAP_<COD>             combinaciones observadas por par
#
# REGLA: nunca modificar los archivos de DatosOriginales/.
# =============================================================================

import sys
from pathlib import Path

import pandas as pd

# =============================================================================
# RUTAS
# =============================================================================

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import DIR_DATOS

RUTA_INPUT  = DIR_DATOS / "DatosArmonizados"  / "Cancelaciones" / "2_DatosLimpios"
RUTA_OUTPUT = DIR_DATOS / "DatosArmonizados" / "Cancelaciones"
ARCHIVO_EXCEL = RUTA_OUTPUT / "Mapeo_Variables_Cancelaciones_limpio.xlsx"

# =============================================================================
# VARIABLES A INVENTARIAR
# =============================================================================

VARIABLES = [
    "SEDE",
    "CONVENIO_PLAN",
    "TIPO_NIVEL",
    "NOMBRES_APELLIDOS",
    "ADMISION",
    "CONVOCATORIA",
    "APERTURA",
    "NOTA_ALFABETICA",
    "NOTA_NUMERICA",
    "CREDITOS",
    "GRUP_ACTA",
    "PERIODO",
    "COD_SEDE_ASIGNATURA",
    "TIPO_CANCELACION",
    "FECHA",
    "CORRECIÓN DE CRED. PERDIDA",
    "CAUSA_ANULA",
    "USUARIO_CANCELACION",
    "TIPO_USUARIO",
    "PBM",
    "PUNTAJE_ADMISION",
]

# Pares código → etiqueta para analizar consistencia
RELACIONES = {
    "COD_FACULTAD"           : "FACULTAD",
    "COD_PLAN"               : "PLAN",
    "COD_PROG_CURRICULAR"    : "DESC_PROG_CURRICULAR",
    "HIST_ACAD"              : "LOGIN_USUARIO_ESTUDIANTE",
    "DOCUMENTO"              : "NOMBRES_APELLIDOS",
    "LOGIN_USUARIO_ESTUDIANTE": "NOMBRES_APELLIDOS",
    "COD_ACCESO"             : "ACCESO",
    "COD_SUBACCESO"          : "SUBACCESO",
    "COD_NODO_INICIO"        : "NODO_INICIO",
    "COD_ASIGNATURA"         : "ASIGNATURA",
    "GRUP_ACTI"              : "DES_GR_ACTIV",
    "COD_FACULTAD_ASIGNATURA": "FACULTAD_ASIGNATURA",
    "COD_UAB_ASIGNATURA"     : "UAB_ASIGNATURA",
}


# =============================================================================
# FUNCIONES
# =============================================================================

def leer_archivos(ruta_input: Path) -> pd.DataFrame:
    archivos = sorted(ruta_input.glob("*.csv"))

    if not archivos:
        raise FileNotFoundError(
            f"No se encontraron archivos CSV en {ruta_input}"
        )

    datos = []

    for ruta in archivos:
        nombre = ruta.stem

        try:
            df = pd.read_csv(
                ruta,
                dtype=str,
                low_memory=False
            )

            df["ARCHIVO_FUENTE"] = nombre
            datos.append(df)

            print(
                f"  [OK]    {nombre} ({len(df):,} filas)"
            )

        except Exception as e:
            print(f"  [ERROR] {nombre}: {e}")

    return pd.concat(datos, ignore_index=True)


def obtener_col_label(df: pd.DataFrame, variable: str) -> str | None:
    """
    Busca una columna de etiqueta asociada a `variable`.
    Prueba los sufijos: _LABEL, _NOMBRE, _DESC.
    Devuelve el nombre de la columna o None si no existe ninguna.
    """
    for sufijo in ("_LABEL", "_NOMBRE", "_DESC"):
        candidata = variable + sufijo
        if candidata in df.columns:
            return candidata
    return None


def construir_hoja_variable(df: pd.DataFrame, variable: str) -> pd.DataFrame:
    """
    Resumen de frecuencias y presencia por archivo para una variable categórica.

    Columnas resultantes:
      COD | LABEL | N_TOTAL | N_PERIODOS | [archivo_1 … archivo_n]
          | CODIGO_CANONICO | CODIGO_ARMONIZADO
    """
    col_label = obtener_col_label(df, variable)

    temp = df[["ARCHIVO_FUENTE", variable]].copy()
    temp[variable] = (
        temp[variable]
        .fillna("NO_INFORMA")
        .str.strip()
    )

    # Etiqueta: columna dedicada o el propio código
    if col_label:
        temp["__LABEL__"] = df[col_label].fillna("NO_INFORMA").str.strip()
        label_map = (
            temp.groupby(variable)["__LABEL__"]
            .agg(lambda s: s.value_counts().idxmax())   # etiqueta más frecuente
        )
    else:
        label_map = None

    # N_TOTAL
    resumen = (
        temp.groupby(variable)
        .size()
        .reset_index(name="N_TOTAL")
    )

    # N_PERIODOS
    n_periodos = (
        temp.groupby(variable)["ARCHIVO_FUENTE"]
        .nunique()
        .reset_index(name="N_PERIODOS")
    )
    resumen = resumen.merge(n_periodos, on=variable, how="left")

    # Presencia binaria (0/1) por archivo
    presencia = (
        pd.crosstab(temp[variable], temp["ARCHIVO_FUENTE"])
        .gt(0)
        .astype(int)
        .reset_index()
    )
    resumen = resumen.merge(presencia, on=variable, how="left")

    # Renombrar y ordenar columnas explícitamente
    resumen = resumen.rename(columns={variable: "COD"})
    resumen["LABEL"] = (
        resumen["COD"].map(label_map) if label_map is not None
        else resumen["COD"]
    )

    cols_archivos = [
        c for c in resumen.columns
        if c not in ("COD", "LABEL", "N_TOTAL", "N_PERIODOS")
    ]
    resumen = resumen[
        ["COD", "LABEL", "N_TOTAL", "N_PERIODOS"] + cols_archivos
    ].copy()

    resumen["CODIGO_CANONICO"]   = ""
    resumen["CODIGO_ARMONIZADO"] = ""

    return resumen


def construir_resumen_relaciones(
    df: pd.DataFrame,
    relaciones: dict[str, str],
) -> pd.DataFrame:
    """
    Analiza la consistencia de cada par código → etiqueta.
    Devuelve un DataFrame con una fila por relación.
    """
    filas = []
    for cod_var, label_var in relaciones.items():
        if cod_var not in df.columns or label_var not in df.columns:
            continue

        tmp = df[[cod_var, label_var]].dropna().astype(str)

        labels_por_codigo     = tmp.groupby(cod_var)[label_var].nunique()
        codigos_problematicos = (labels_por_codigo > 1).sum()

        filas.append({
            "VARIABLE_CODIGO"            : cod_var,
            "VARIABLE_LABEL"             : label_var,
            "N_CODIGOS"                  : tmp[cod_var].nunique(),
            "N_LABELS"                   : tmp[label_var].nunique(),
            "CODIGOS_CON_MULTIPLES_LABELS": codigos_problematicos,
            "TIPO"                       : "1:1" if codigos_problematicos == 0 else "REVISAR",
        })

    return pd.DataFrame(filas)


def construir_hoja_mapa(
    df: pd.DataFrame,
    cod_var: str,
    label_var: str,
) -> pd.DataFrame:
    """
    Detalle de las combinaciones observadas entre un código y su etiqueta,
    ordenado por código y frecuencia descendente.
    """
    tmp = df[[cod_var, label_var]].dropna().astype(str)
    return (
        tmp.groupby([cod_var, label_var])
        .size()
        .reset_index(name="N")
        .sort_values([cod_var, "N"], ascending=[True, False])
        .reset_index(drop=True)
    )


def exportar_excel(
    df_total       : pd.DataFrame,
    variables      : list[str],
    relaciones     : dict[str, str],
    ruta_salida    : Path,
) -> None:
    """
    Escribe todas las hojas en un único ExcelWriter:
      - Una hoja por variable categórica.
      - Hoja RESUMEN_RELACIONES con el análisis de consistencia.
      - Una hoja MAP_<COD> por cada par código → etiqueta.
    """
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------ #
    # BLOQUE ÚNICO — todas las hojas dentro del mismo `with`              #
    # ------------------------------------------------------------------ #
    with pd.ExcelWriter(ruta_salida, engine="openpyxl") as writer:

        # 1. Hojas de variables categóricas
        print("\nHojas de variables:")
        for variable in variables:
            if variable not in df_total.columns:
                print(f"  [SKIP]  {variable} — columna no encontrada")
                continue
            hoja = construir_hoja_variable(df_total, variable)
            nombre_hoja = variable[:31]
            hoja.to_excel(writer, sheet_name=nombre_hoja, index=False)
            print(f"  [OK]    {nombre_hoja}  ({len(hoja)} categorías)")

        # 2. Hoja resumen de relaciones código → etiqueta
        print("\nHoja de relaciones:")
        df_relaciones = construir_resumen_relaciones(df_total, relaciones)
        if not df_relaciones.empty:
            df_relaciones.to_excel(
                writer, sheet_name="RESUMEN_RELACIONES", index=False
            )
            print(f"  [OK]    RESUMEN_RELACIONES  ({len(df_relaciones)} pares)")
        else:
            print("  [SKIP]  RESUMEN_RELACIONES — sin pares válidos")

        # 3. Hojas MAP_ por cada relación
        print("\nHojas de mapeo:")
        for cod_var, label_var in relaciones.items():
            if cod_var not in df_total.columns:
                print(f"  [SKIP]  MAP_{cod_var} — {cod_var} no encontrada")
                continue
            if label_var not in df_total.columns:
                print(f"  [SKIP]  MAP_{cod_var} — {label_var} no encontrada")
                continue
            mapa = construir_hoja_mapa(df_total, cod_var, label_var)
            nombre_hoja = f"MAP_{cod_var}"[:31]
            mapa.to_excel(writer, sheet_name=nombre_hoja, index=False)
            print(f"  [OK]    {nombre_hoja}  ({len(mapa)} combinaciones)")


# =============================================================================
# MAIN
# =============================================================================

def main() -> None:
    print("=" * 60)
    print("Leyendo archivos...")
    print("=" * 60)
    df_total = leer_archivos(RUTA_INPUT)
    print(f"\nTotal filas consolidadas: {len(df_total):,}")

    print("\n" + "=" * 60)
    print("Generando Excel...")
    print("=" * 60)
    exportar_excel(df_total, VARIABLES, RELACIONES, ARCHIVO_EXCEL)

    print(f"\nArchivo generado:\n{ARCHIVO_EXCEL}")


if __name__ == "__main__":
    main()