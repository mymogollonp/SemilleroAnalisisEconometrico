# Reglas del Proyecto — RAs
## Semillero de Análisis Econométrico

---

### R1 — Commit y push al terminar código

Cada vez que un RA crea o modifica un script, debe:

1. **Hacer commit** con un mensaje descriptivo que indique qué hace el script y para qué módulo.
   ```
   git add 1_LimpiezaDatos/07_anonimizar_matriculados.R
   git commit -m "feat: anonimizar matriculados - reemplaza correo por id_unal"
   ```
2. **Hacer push** al repositorio remoto en GitHub inmediatamente después del commit.
   ```
   git push
   ```

> El repositorio en GitHub es la única fuente de verdad para el código. Un script que no está en GitHub no existe para el equipo.

---

### R2 — Actualizar el reporte de tareas

Cada vez que un RA completa una tarea (o la avanza/bloquea), debe actualizar su archivo de reporte semanal en `RAtaskreport/semanaNN_NombreA.md`:

- Cambiar el estado de la tarea: `[ ]` → `[x]` (completada), `[-]` (en progreso), o `[!]` (bloqueada)
- Llenar la tabla de archivos creados o modificados
- Anotar cualquier problema encontrado en la tabla de problemas
- Hacer commit y push del reporte actualizado junto con el código o de forma independiente

---

### R3 — No datos en GitHub

El repositorio solo contiene código, documentación y logs. Nunca subir archivos de datos (`.csv`, `.xlsx`, `.zip`, etc.). El `.gitignore` ya excluye estos formatos.

---

### R4 — Un script por tarea

Cada script tiene una sola responsabilidad (inventariar un módulo, construir master personas de un módulo, anonimizar un módulo, etc.). No combinar tareas de distintas fases en un mismo script.

---

### R5 — Configurar rutas en el archivo de configuración

El proyecto usa un archivo de configuración de rutas que todos los scripts importan. Crear el equivalente al lenguaje de tu preferencia:

| Lenguaje | Archivo de configuración | Mecanismo |
|---|---|---|
| Stata | `00_configuracion.do` | `global dir_datos "..."` |
| R | `00_config.R` | `dir_datos <- "..."` |
| Python | `00_config.py` | `dir_datos = "..."` |

Cada RA agrega su bloque de rutas al archivo de configuración de su lenguaje y hace **commit y push**.

> Nunca hardcodear rutas absolutas fuera del archivo de configuración. Si un script no corre en otra máquina, la causa es casi siempre una ruta mal configurada aquí.

---

### R6 — Nunca modificar DatosOriginales

La carpeta `DatosOriginales/` es de solo lectura. Ningún script ni acción manual puede crear, editar, renombrar o eliminar archivos dentro de ella.

- Los scripts solo **leen** de `DatosOriginales/` — nunca escriben en ella.
- Todos los outputs (anonimizados, limpios, procesados) se guardan en `DatosArmonizados/` o sus subcarpetas.
- Si un archivo original parece incorrecto o incompleto, documentarlo en el reporte semanal y notificar al PI/CoPI.

---

### R7 — Documentar la semilla y las rutas

Todo script que use una semilla aleatoria debe declararla explícitamente con un comentario. Todas las rutas deben usar las variables definidas en el archivo de configuración, nunca rutas absolutas hardcodeadas.

---

### R8 — Nunca subir datos a herramientas de IA

Nunca subas datos del proyecto a ningún agente de IA, chatbot o plataforma agéntica: ChatGPT, Claude, Gemini, Copilot, Cursor, NotebookLM, etc. Esto incluye bases completas, extractos, filas de ejemplo, tablas con microdatos y capturas de pantalla de datos. La IA se puede usar solo con código y con documentos públicos (normativa, papers).

---

### R9 — Agentes de IA: solo la carpeta del código y sin leer datos

Si usas un agente de código (Claude Code, Copilot, Cursor…):

- El agente trabaja **solo dentro de la carpeta del código del proyecto**. Nunca debe buscar, explorar ni leer otras carpetas del computador, incluidas las carpetas de datos en Drive.
- El agente **nunca lee datos** salvo autorización manual y explícita de la PI/CoPI para una tarea concreta.
- Las reglas para agentes están en [CLAUDE.md](CLAUDE.md).

---

*Ver también: `requirements-spec.md` para las reglas globales del proyecto.*
