# Workplan: Armonización de Datos UNAL
## Semillero de Análisis Econométrico

**Director:** Investigador Principal / Director del Semillero
**Repositorio de código:** `C:\code\SemilleroAnalisisEconometrico`
**Repositorio de datos:** `C:\Drive2023\UNAL_Docente\SemilleroAnalisisEconometrico`
**Fecha de inicio:** 2026-04-13

---

## Datos disponibles

| Dataset | Archivos | Cobertura |
|---|---|---|
| Matriculados | `.xlsx` + `.csv` | 2009-1S, 2023-2S |
| Cursadas | `.xlsx` + `.csv` | 2009-1S, 2023-2S |
| Cancelaciones | `.xlsx` | 2009-2S, 2023-2S |
| Egresados | `.xlsx` | 2009-1S, 2023-2S |
| Retirados | `.xlsx` | Desde 2009 |
| Rendimiento Matemáticas Básicas | `.xlsx` | 2016–2025, Ciencias e Ingeniería |

**Datos procesados heredados (`DatosProcesados/ProcesadosMarcos/`):**
- `BASE_DATOS_REGISTRO_UNAL_BOGOTA_con_id` — panel académico con `id_unal` anónimo (65 variables, panel largo student×period)
- Llave de anonimización, diccionario, muestra 5%

---

## Preguntas clave a responder en Fase 1

1. ¿Los datasets FCE 2025 tienen un campo de ID individual de estudiante (correo, cédula, código)?
2. ¿"2009-1S" y "2023-2S" son extremos de un panel continuo o snapshots puntuales?
3. ¿`Rendimiento_Matemáticas` tiene granularidad de estudiante o es solo agregado por curso?
4. ¿La población FCE 2025 se superpone con `BASE_DATOS_REGISTRO_UNAL_BOGOTA`? ¿Se puede reutilizar `id_unal`?

---

## Fase 0 — Infraestructura

**Objetivo:** dejar el repositorio listo para recibir código reproducible.

- [ ] Actualizar `README.md` con descripción del proyecto
- [ ] Actualizar `.gitignore` para excluir todos los formatos de datos (`*.dta`, `*.csv`, `*.xlsx`, `*.zip`)
- [ ] Crear `code/00_configuracion.do` con globales de rutas
- [ ] Crear carpetas de salida en Drive: `DatosArmonizados/keys/`, `panel/`, `muestras/`, `outputs/`
- [ ] Crear `logs/.gitkeep` para versionar la carpeta vacía
- [ ] Primer commit y push a GitHub con estructura base

---

## Fase 1 — Inventario y Perfilado

**Do-file:** `code/01_inventario_datos.do`
**Salidas:** `logs/session_YYYY-MM-DD.md`, `docs/fuentes_datos.md`

Para cada dataset crudo:
- Variables disponibles, tipos, rangos
- Tasa de missings por variable
- Número de observaciones y períodos cubiertos
- Identificadores candidatos (¿correo UNAL? ¿cédula? ¿código estudiantil?)
- Consistencia entre versiones `.xlsx` y `.csv` del mismo dataset

---

## Fase 2 — Limpieza por Dataset

Un do-file por fuente. Cada uno produce un archivo `*_limpio.dta` en `DatosArmonizados/panel/`.
**Regla:** nunca modificar el archivo original.

| Do-file | Tarea central |
|---|---|
| `02_limpiar_matriculados.do` | Estandarizar variables de programa, período, estrato, PBM; detectar duplicados |
| `03_limpiar_cursadas.do` | Estandarizar código de asignatura, calificación, créditos; verificar escala 0–5 |
| `04_limpiar_cancelaciones.do` | Fecha de cancelación → período `YYYY-NS`; cruce con matriculados |
| `05_limpiar_egresados.do` | Fecha de grado → período; cruce con matriculados para validar |
| `06_limpiar_retirados.do` | Período de retiro; tipo de retiro; cruce con estados académicos |
| `07_limpiar_rendimiento_mat.do` | Determinar granularidad; armonizar con período `YYYY-NS` |

---

## Fase 3 — Anonimización y Armonización de IDs

**Do-files:** `08_crear_llave_ids.do`, `09_armonizar_periodos.do`

### Anonimización (`08_crear_llave_ids.do`)
- Identificar el campo de ID personal en cada dataset crudo
- Evaluar superposición con la población de `BASE_DATOS_REGISTRO_UNAL_BOGOTA`:
  - Si hay superposición total: reutilizar `id_unal` existente (semilla `20260223`)
  - Si hay estudiantes nuevos: extender la llave con semilla nueva documentada
- Guardar crosswalk en `DatosArmonizados/keys/` (confidencial, nunca a GitHub)
- Eliminar identificadores personales de todos los archivos de trabajo

### Formato de períodos (`09_armonizar_periodos.do`)
- Formato canónico: `YYYY-NS` (ej. `2016-1S`, `2023-2S`)
- Manejar variantes: `20161`, `2016-I`, `2016S1`
- Generar `periodo_num` (entero ordinal) para ordenamiento correcto en el panel

---

## Fase 4 — Construcción del Panel Maestro

**Do-file:** `10_construir_panel.do`
**Backbone:** `Matriculados` (define quién es estudiante activo en cada período)

```
Panel maestro: id_unal × periodo × cod_plan
│
├── join Cursadas       → desempeño académico por período
├── join Cancelaciones  → indicador cancelo_semestre
├── join Egresados      → indicador graduado, fecha_grado, titulo
├── join Retirados      → indicador retirado, periodo_retiro
└── join Rendimiento    → puntaje_mat_basicas (si granularidad individual)
```

**Clave del panel:** `(id_unal, periodo, cod_plan)`
**Tipo de panel:** desequilibrado — un estudiante con doble titulación genera múltiples filas por período.

### Variables de estado al cierre de cada período

| Variable | Fuente | Descripción |
|---|---|---|
| `papa_periodo` | Cursadas | GPA acumulado al período |
| `promedio_periodo` | Cursadas | Promedio del semestre |
| `creditos_aprob` | Cursadas | Créditos aprobados en el período |
| `creditos_reprob` | Cursadas | Créditos reprobados en el período |
| `cancelo` | Cancelaciones | 1 si canceló el semestre completo |
| `graduado` | Egresados | 1 si se graduó en este período |
| `retirado` | Retirados | 1 si se retiró del programa |
| `rendimiento_mat` | Rendimiento | Puntaje en matemáticas básicas (si aplica) |

---

## Fase 5 — Control de Calidad

**Do-file:** `11_control_calidad.do`
**Salida:** `logs/QC_report_YYYY-MM-DD.md`

Checklist automatizado:
- [ ] Unicidad de la clave `(id_unal, periodo, cod_plan)`
- [ ] Ningún `id_unal` con datos personales residuales
- [ ] Calificaciones en rango 0–5 en todas las variables de promedio
- [ ] Períodos en rango 2009-1S a 2025-2S
- [ ] Ningún estudiante con `graduado=1` y `retirado=1` simultáneamente
- [ ] Distribución de estrato consistente con promedios UNAL reportados
- [ ] Conteo de observaciones por período vs. totales en fuentes oficiales

---

## Fase 6 — Muestra y Entregables

**Do-file:** `12_crear_muestra.do`

Muestra aleatoria estratificada 5%, estratificada por período y programa. Semilla documentada para replicabilidad.

### Archivos finales

| Archivo | Ubicación en Drive | Descripción |
|---|---|---|
| `BASE_FCE_ARMONIZADA.dta` | `DatosArmonizados/panel/` | Panel maestro completo |
| `BASE_FCE_ARMONIZADA.csv` | `DatosArmonizados/panel/` | Misma base en CSV |
| `MUESTRA_FCE_5PCT.dta` | `DatosArmonizados/muestras/` | Muestra para uso en curso |
| `MUESTRA_FCE_5PCT.csv` | `DatosArmonizados/muestras/` | Misma muestra en CSV |
| `LLAVE_FCE.dta` | `DatosArmonizados/keys/` | Crosswalk `id_unal` ↔ ID real |
| `DICCIONARIO_FCE.md` | `docs/` (repo) | Diccionario de todas las variables |

---

## Cronograma

| Semana | Fase | Do-files |
|---|---|---|
| 1 | Fase 0 — Infraestructura | — |
| 1–2 | Fase 1 — Inventario | `01` |
| 2–4 | Fase 2 — Limpieza | `02` – `07` |
| 4 | Fase 3 — IDs y períodos | `08`, `09` |
| 5–6 | Fase 4 — Panel maestro | `10` |
| 6 | Fase 5 — QC | `11` |
| 7 | Fase 6 — Muestra y entregables | `12` |

---

*Última actualización: 2026-04-13*
