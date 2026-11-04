# ⚠ INCIDENTE CRÍTICO — Llave de anonimización versionada en GitHub

**Estado:** ABIERTO. El archivo se eliminó de la versión actual, pero **sigue en el historial de Git**.
**Detectado:** 2026-11-03 · **Registrado:** 2026-11-04
**Responsable de resolverlo:** Jeronimo Jimenez (administrador del repositorio), con Monica Mogollon
**Prioridad:** máxima. Debe resolverse **antes de dar acceso a GitHub a cualquier RA nuevo**.

---

## Qué pasó

| | |
|---|---|
| Archivo | `1_LimpiezaDatos/LLAVE_ID_UNAL_FCE.csv` |
| Contenido | Llave de anonimización: columnas `correo`, `id_unal`; ~148.565 filas (una por estudiante) |
| Commit que lo agregó | `be11291` ("Division de retirados") |
| Autor | `nijimenezca119` |
| Fecha | 2026-06-01 |
| Rama | `BorradoresCodigo` (local y `origin`) |

Con esta llave, cualquier base "anónima" del proyecto puede reidentificarse pegando por `id_unal`. Eso viola:
- `requirements-spec.md` **Rule 4** (no datos en GitHub) y **Rule 5** (la llave solo puede estar en `DatosArmonizados/keys/` en Drive)
- El acuerdo de confidencialidad firmado por el equipo

**Causa probable:** el `.gitignore` del repositorio es una plantilla genérica (Flash Builder) y **no excluye ningún formato de datos**. Un `git add` de la carpeta incluyó el CSV.

## Lo que ya se hizo

- [x] 2026-11-04: se eliminó el archivo de la versión actual de `BorradoresCodigo` (`git rm`) y se borró la copia local dentro del repositorio
- La copia oficial de la llave en `DatosArmonizados/keys/` (Drive) **no se tocó**

## Lo que falta (crítico)

1. **Verificar la visibilidad del repositorio** en GitHub (público o privado) y quién tiene o tuvo acceso.
   - Si fue **público** en algún momento: tratar la llave como expuesta y evaluar con los PI regenerar `id_unal` con una sal nueva para todas las bases.
2. **Purgar el archivo de todo el historial**:
   ```bash
   # en un clon nuevo (mirror) del repositorio
   git filter-repo --path 1_LimpiezaDatos/LLAVE_ID_UNAL_FCE.csv --invert-paths
   git push --force --all
   git push --force --tags
   ```
   (Alternativa: BFG Repo-Cleaner con `--delete-files LLAVE_ID_UNAL_FCE.csv`.)
3. **Antes del force-push**, avisar a todos los que tengan clones. Después, **todos deben borrar su clon y volver a clonar**: un clon viejo puede volver a subir el archivo. Recordar el incidente del 2026-05-08, cuando un force-push borró commits de los RAs; coordinar con cuidado.
4. **Pedir a GitHub Support** que elimine las vistas en caché del commit `be11291` y de los pull requests que lo referencien, si existen.
5. **Corregir `.gitignore`** en todas las ramas para excluir `*.csv`, `*.xlsx`, `*.xls`, `*.dta`, `*.parquet`, `*.zip`, `*.rar`, `__pycache__/` y `.Rhistory`.
6. **Revisar el resto del historial** por otros datos versionados (`git log --all --stat` filtrando por extensiones de datos).
7. **Cerrar el incidente** en este archivo: fecha, acciones tomadas y quién lo verificó.

---

*Este archivo no contiene datos. No agregar aquí ningún valor de la llave.*
