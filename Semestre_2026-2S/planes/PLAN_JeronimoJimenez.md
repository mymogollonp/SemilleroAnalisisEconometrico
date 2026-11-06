# Plan de trabajo 2026-2S — Jeronimo Jimenez Castaneda
## Proyectos: (A) Administración del Repositorio de Datos · (B) Datos DANE C600

**Correo:** jerjimenezca@unal.edu.co · **Rama:** `ra/jjimenez`
**Carpeta de trabajo:** `SemilleroAnalisisEconometrico/` (repositorio completo; acceso solo para Jeronimo y Nicolas)
**Supervisión:** Monica Mogollon · **Coadministrador:** Nicolas Jimenez

---

## ⚠ Reglas de datos e IA (obligatorias)

- **Nunca subas datos del proyecto a ningún agente de IA, chatbot o plataforma agéntica** (ChatGPT, Claude, Gemini, Copilot, Cursor, NotebookLM, etc.). Esto incluye bases, extractos, filas de ejemplo, tablas con microdatos y capturas de pantalla de datos. Usa IA solo con código y con documentos públicos (normativa, papers). Esto aplica también a las tareas de administración: auditoría, nuevas versiones y C600.
- Si usas un agente de código, debe trabajar **solo dentro de la carpeta del código del proyecto**: nunca debe buscar ni explorar otras carpetas del computador, ni **leer datos** sin autorización manual de la PI/CoPI. Ver [CLAUDE.md](../../CLAUDE.md).
- En la reunión de arranque mencionaste que actualizar los datos es fácil con Claude. Si usas agentes para el pipeline, el agente **escribe el código** y **tú lo ejecutas** sobre los datos. El agente no lee los datos.
- **Tarea de administrador:** asegurar que `CLAUDE.md` y estas reglas estén en `main`, `BorradoresCodigo`, `Proyectos2026-2S` y todas las ramas de los RAs.
  - *Avance 2026-11-05:* ya están en `BorradoresCodigo`, `Proyectos2026-2S` y las ramas `ra/*`. **Falta `main`** (entra con el `.gitignore` nuevo vía pull request).

---

## Objetivo del semestre

**(A) Administración del repositorio.** Jeronimo es el administrador del banco de datos y apoya a todos los RAs de forma transversal. Sus tareas:
1. **Evaluar el código y las tareas del semestre 2026-1S**: qué se completó, qué falta y qué está duplicado.
2. **Integrar `BorradoresCodigo` en `main`** con un historial limpio y sin datos.
3. **Incorporar nuevas versiones de datos** (2025 y las que consiga Karoll, como las encuestas de egresados) al pipeline.
4. **Atender las solicitudes de datos** de los RAs sin exponer datos con información personal.
5. **Evaluar alternativas de alojamiento** de datos para investigadores.

**(B) DANE C600.** Consolidar la base **C600 del DANE** (formulario de Educación Formal: sedes, matrícula, docentes y resultados de los colegios) como un panel colegio–año dentro del laboratorio de datos. Debe poder pegarse con `cod_colegio` de `BASE_MATRICULADOS`. Lo usarán el proyecto de expectativas en educación media y el proyecto de Monica con Juan Daniel.

## Entregables finales (16 dic)

- **A1** `Semestre_2026-2S/auditoria_2026-1S.md`: auditoría de scripts, tareas y outputs del semestre anterior
- **A2** `main` actualizado con el código de 2026-1S, sin datos y con `.gitignore` correcto
- **A3** Pipeline documentado para incorporar nuevas versiones de datos, más los datos 2025 incorporados si llegan
- **A4** `logs/solicitudes_datos.md`: registro de solicitudes de los RAs
- **A5** `Semestre_2026-2S/opciones_alojamiento_datos.md`: comparación de servicios de alojamiento con una recomendación
- **B1** Panel C600 consolidado (`DatosArmonizados/C600/`) con diccionario y script de construcción

---

## Semana 1 (3 – 6 nov) — Seguridad del repositorio (prioridad máxima)

> **Antes de dar acceso a GitHub a los nuevos RAs**: el archivo `1_LimpiezaDatos/LLAVE_ID_UNAL_FCE.csv` (correo ↔ `id_unal`, unas 148.000 filas) fue subido a `BorradoresCodigo` en el commit `be11291` (2026-06-01). Está en el historial de Git.

- `[ ]` **Revisar el incidente** en [logs/INCIDENTE_llave_id_unal_en_git.md](../../logs/INCIDENTE_llave_id_unal_en_git.md) junto con Nicolas: completar los pasos pendientes y cerrar el incidente cuando el historial esté limpio y verificado. El archivo ya se eliminó de la versión actual (commit `3c32942`)
  - *En curso:* historial purgado y verificado (2026-11-05). Falta: registrar la causa exacta con Nicolas y la confirmación de GitHub Support
- `[x]` Coordinar con Monica y **eliminar la llave del historial** (`git filter-repo --path 1_LimpiezaDatos/LLAVE_ID_UNAL_FCE.csv --invert-paths`, o BFG) y hacer force-push **avisando antes** a todos los que tengan clones
  - *Hecho 2026-11-05:* `git filter-repo --refs be11291~1..BorradoresCodigo` (solo se reescribió `BorradoresCodigo`, nueva punta `20668ec`; las demás ramas no cambiaron). Aviso previo a Nicolas y Monica
- `[x]` Verificar si el repositorio es público o privado. Si fue público, informar a Monica para evaluar regenerar `id_unal` con otra sal
  - *2026-11-05:* el repositorio es **público**. Se informó a Monica, junto con que la sal está escrita en varios scripts. Pendiente: decisión de los PI sobre regenerar `id_unal`
- `[x]` Llevar a `BorradoresCodigo` el `.gitignore` nuevo, que ya está en `Proyectos2026-2S` y excluye datos, `__pycache__/` y `.Rhistory` (por ejemplo, `git checkout Proyectos2026-2S -- .gitignore CLAUDE.md`)
- `[x]` En `BorradoresCodigo`, quitar del índice los archivos ya versionados que el `.gitignore` excluye: `.Rhistory`, `1_LimpiezaDatos/.Rhistory` y los tres `__pycache__/config.cpython-313.pyc` (`git rm --cached`; quedan en disco)
  - *Hecho 2026-11-05* junto con el punto anterior (hoy commit `20668ec` tras la purga)
- `[x]` Hacer push del commit local `3c32942` (eliminación de la llave de la versión actual) a `origin/BorradoresCodigo`, si Monica no lo ha hecho
  - Ya lo había subido Monica
- `[x]` Crear la etiqueta `solicitud-datos` en GitHub (2026-11-06)
- `[ ]` **Dar acceso a los nuevos RAs** y crear sus ramas desde `Proyectos2026-2S` (`ra/jmoreno`, `ra/dtovar`, `ra/jbermudez`, `ra/mcarrillo`, `ra/njimenez`, `ra/jjimenez`)
  - Ya existen `ra/jbermudez`, `ra/jmoreno`, `ra/njimenez` y `ra/jjimenez`. Faltan `ra/dtovar` y `ra/mcarrillo`. **Bloqueo:** dar acceso requiere rol Admin (la cuenta `jerjimenezca` tiene Write)
- `[ ]` Configurar la protección de `main` y `Proyectos2026-2S`: sin push directo y con pull request revisado
  - **Bloqueo:** requiere rol Admin; solicitado a Monica

## Semana 2 (9 – 13 nov) — Auditoría 2026-1S y publicación de bases

- `[ ]` Auditoría: para cada RA de 2026-1S, comparar las tareas de `RAtaskreport/` y `WORKPLAN.md` con los scripts existentes. Marcar qué se completó, qué falta y qué está duplicado (por ejemplo, hay `config.py` en tres carpetas)
- `[ ]` Revisar la consistencia de las bases finales: Cancelaciones **no está publicada** en la carpeta de proyectos; hay dos versiones de Egresados_Retirados (`/` y `_actualizados`); la carpeta se llama `Matriculados (1)`; los nombres de columnas no son uniformes (`ID_UNAL` frente a `id_unal`, `academic_año` frente a `academic_anio`)
- `[ ]` Publicar en `SemilleroMicroeconometriaProyectos/FinalWorkingDataSets/` una **versión única y consistente** (v1) de las cuatro bases, con nombres de carpeta y columnas homogéneos, y un `LEEME.md` con la versión y la fecha
- `[ ]` Revisar que las bases publicadas no contengan cuasi-identificadores de riesgo, como `fecha_nacimiento` completa, `cod_colegio` combinado con municipio o celdas pequeñas, y discutir con Monica si se publican edad y año de nacimiento en vez de la fecha completa

## Semana 3 (17 – 20 nov) — Merge a `main` y C600 (inicio)

- `[ ]` Integrar `BorradoresCodigo` → `main` mediante pull request: resolver conflictos, ordenar carpetas (`1_LimpiezaDatos/`, `2_Armonizacion/`, `3_BasesdeTrabajo/`), unificar archivos de configuración y actualizar `README.md` y `WORKPLAN.md`
- `[ ]` Documentar el **orden de ejecución** del pipeline completo, de originales a bases finales
- `[ ]` **C600:** inventario de años disponibles (micro-datos del DANE en el catálogo ANDA y las versiones que ya tienen limpias otros proyectos, como el de Juan Daniel o el de la estudiante de la profesora); definir los módulos que se incluyen

## Semana 4 (23 – 27 nov) — Pipeline de nuevas versiones y C600

- `[ ]` Diseñar el **procedimiento de nueva versión de datos**: dónde se depositan los originales nuevos, cómo se corren inventario, limpieza, anonimización (misma sal y llave, con `id_unal` nuevos solo para personas nuevas) y bases finales, y cómo se versiona la publicación (v1, v2…)
- `[ ]` Si ya llegaron los datos 2025-2S u otros nuevos: incorporarlos siguiendo el procedimiento
- `[ ]` **C600:** armonizar los nombres de variables entre años (tabla de equivalencias) y construir el panel v0 colegio–año
- `[ ]` **Presentación corta (10 min):** estado del repositorio y del C600

## Semana 5 (30 nov – 4 dic) — Alojamiento de datos y C600

- `[ ]` Investigar opciones de **alojamiento para investigadores** y compararlas por costo, control de acceso, versionado, tamaño, cumplimiento de la Ley 1581 de 2012 (habeas data) y facilidad de uso:
  - Infraestructura UNAL (servidores de la DNTIC o de la Facultad, Google Workspace institucional con Drive compartido y permisos por carpeta)
  - Repositorios con acceso restringido: Harvard Dataverse o un Dataverse institucional, OSF, Zenodo (restricted access), ICPSR
  - Nube: Google Cloud Storage o BigQuery con la cuenta institucional, AWS S3 con *research credits*
  - Formatos y herramientas: Parquet + DuckDB, DVC (Data Version Control) sobre Drive o GCS, Git LFS (no recomendado para datos con información personal)
- `[ ]` Redactar `opciones_alojamiento_datos.md` con una recomendación
- `[ ]` **C600:** validar el pegue con `cod_colegio` de `BASE_MATRICULADOS` (tasa de match por año) y escribir el diccionario

## Semana 6 (9 – 11 dic) — Cierre técnico y presentación

- `[ ]` Revisar los pull requests pendientes de los RAs
- `[ ]` **Presentación final:** auditoría, estado de `main`, procedimiento de versiones, alojamiento y C600

## Cierre (14 – 16 dic)

- `[ ]` Revisar y fusionar a `Proyectos2026-2S` los pull requests finales de todos los RAs; luego integrar `Proyectos2026-2S` → `main` con aprobación de Monica
- `[ ]` Actualizar `README.md` raíz con la estructura final del repositorio
- `[ ]` Pendientes para 2027-1S: encuestas de egresados, datos de admisión y cruce con C600

## Tareas transversales (todo el semestre)

- `[ ]` Atender las **solicitudes de datos** (issues `solicitud-datos`) en menos de 3 días hábiles y registrarlas en `logs/solicitudes_datos.md` (fecha, RA, variables, archivo entregado). Ya hay una prevista: la **modalidad de trabajo de grado** para Manuela, en coordinación con Nicolas
- `[ ]` Revisar cada semana que las ramas de los RAs no contengan datos (`git log --stat` de cada rama)
- `[ ]` Apoyar a los RAs con dudas de Git y de las bases

---

## Bitácora

| Semana | Avances | Problemas o bloqueos | Horas |
|---|---|---|---|
| S1 | Visibilidad verificada (público) e informada; `.gitignore` nuevo y `CLAUDE.md` en `BorradoresCodigo`; `.Rhistory` y `__pycache__` fuera del índice; llave purgada del historial (solo `BorradoresCodigo`) y verificada; solicitud a GitHub Support para borrar caché; etiqueta `solicitud-datos` | Falta rol Admin para proteger ramas y dar acceso a RAs; decisión de PI sobre regenerar `id_unal` (sal expuesta); causa exacta del incidente pendiente con Nicolas |5|
| S2 | | | |
| S3 | | | |
| S4 | | | |
| S5 | | | |
| S6 | | | |
