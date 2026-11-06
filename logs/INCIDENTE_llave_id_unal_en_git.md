# ⚠ INCIDENTE CRÍTICO — Llave de anonimización versionada en GitHub

**Estado:** EN CIERRE. El historial de Git ya se purgó (2026-11-05). Pendiente: confirmación de GitHub Support (caché), causa exacta y decisión sobre la sal.
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
- [x] 2026-11-05 — **Visibilidad:** el repositorio es **público**, así que la llave se trata como expuesta. Además, la sal del hash está escrita en scripts versionados en todas las ramas. Se informó a Monica (Jeronimo)
- [x] 2026-11-05 — **`.gitignore` corregido** en `BorradoresCodigo` (excluye formatos de datos, `__pycache__/` y `.Rhistory`) y se sacaron del índice `.Rhistory` y `__pycache__` (Jeronimo)
- [x] 2026-11-05 — **Revisión del historial:** se revisaron los nombres de todos los archivos de todas las ramas (sin abrir contenidos). La llave era el **único** archivo de datos versionado; solo aparecían además `.Rhistory` y `__pycache__` (Jeronimo)
- [x] 2026-11-05 — **Aviso previo** a Nicolas y Monica antes de reescribir el historial (Jeronimo)
- [x] 2026-11-05 — **Purga del historial** en un clon mirror nuevo:
  ```bash
  git filter-repo --refs be11291~1..BorradoresCodigo \
      --path 1_LimpiezaDatos/LLAVE_ID_UNAL_FCE.csv --invert-paths
  git push --force <url> BorradoresCodigo
  ```
  Se limitó a `be11291~1..BorradoresCodigo` porque un `filter-repo` sobre todo el repositorio quita las firmas de GitHub de los commits hechos desde la web y cambia los hashes de **todas** las ramas. Así, solo se reescribió `BorradoresCodigo` (`8eac5e7` → `20668ec`); `main`, `Proyectos2026-2S` y las ramas `ra/*` no cambiaron (Jeronimo)
- [x] 2026-11-05 — **Verificación en GitHub:** `git log --all -- 1_LimpiezaDatos/LLAVE_ID_UNAL_FCE.csv` vacío en un clon nuevo; el árbol de la punta de `BorradoresCodigo` es idéntico al de antes de la purga (`df487cc`). Clon local de Jeronimo borrado y vuelto a clonar; copia del mirror borrada (Jeronimo)
- [x] 2026-11-05 — **Solicitud a GitHub Support** para eliminar las vistas en caché del commit `be11291` (0 pull requests, 0 forks). Ticket: ____ (Jeronimo)

## Lo que falta

1. **Confirmación de GitHub Support**: verificar que el commit `be11291` ya no se pueda ver por su hash.
2. **Decisión de los PI** sobre regenerar `id_unal` con una sal nueva, guardada fuera de GitHub (el repositorio es público y la sal está en los scripts).
3. **Causa exacta** (Nicolas): qué comando y desde qué carpeta se subió el archivo.
4. **Clones viejos de `BorradoresCodigo`** (Nicolas, Monica, RAs de 2026-1S): borrarlos y volver a clonar; nadie debe hacer push desde un clon anterior al 2026-11-05.
5. **`.gitignore` nuevo en `main`** (entra por pull request).
6. **Cerrar el incidente** en este archivo: fecha y quién lo verificó.

---

*Este archivo no contiene datos. No agregar aquí ningún valor de la llave.*
