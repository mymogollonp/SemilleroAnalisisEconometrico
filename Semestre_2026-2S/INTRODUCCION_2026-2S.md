# Semillero de Microeconometría — Semestre 2026-2S
## Del repositorio de datos a los proyectos de investigación

**Coordinación:** Monica Mogollon (CoPI) · **PI:** Karoll Gomez, Hernando Bayona
**Reunión de arranque:** 2026-10-30
**Periodo de trabajo:** 3 de noviembre → 16 de diciembre de 2026

---

## 1. Dónde estamos

Durante el semestre 2026-1S el semillero construyó un **repositorio de datos administrativos de la Universidad Nacional (sede Bogotá), 2009–2025**. Ese repositorio parte de los archivos originales de Matriculados, Cursadas, Cancelaciones, Egresados y Retirados, que se inventariaron, limpiaron, armonizaron y anonimizaron. A partir de ellos se construyeron **bases de trabajo** (`FinalWorkingDataSets`) a nivel estudiante–plan–período, con un identificador anónimo `id_unal`.

Los datos ya están bastante listos para trabajar. Este semestre pasamos de **construir datos** a **usarlos en proyectos de investigación**. Cada RA trabaja en un proyecto distinto. Los proyectos fueron priorizados con los profesores.

> Este semestre es corto: hay **seis semanas efectivas**. No vamos a terminar los proyectos. La meta es que cada uno quede **bien delimitado**, con una base de trabajo propia, estadísticas descriptivas sólidas y la normativa sistematizada.

---

## 2. Proyectos y equipo

| Proyecto | RA | Correo | Pregunta central |
|---|---|---|---|
| **202602_01_CambioPlanesCurriculares** | Jerson Stiven Moreno Blanco | jmorenobl@unal.edu.co | ¿Qué efecto tienen los cambios en los planes de estudio (créditos, flexibilización, nombre) sobre el desempeño de los estudiantes? |
| **202602_02_TimingAdmision** | Dilan Thomas Tovar Roa | ditovarr@unal.edu.co | ¿Qué cambió cuando los aspirantes pasaron de escoger programa *antes* a escogerlo *después* del examen? Doble titulación, reingresos, cupos y normativa |
| **202602_02_TimingAdmision** | Julian Esteban Bermudez Chiguasuque | jbermudezch@unal.edu.co | Mismo proyecto. Julian se encarga de la composición de estudiantes antes y después del cambio |
| **202602_03_ModalidadTrabajoGrado** | Manuela Carrillo Castro | mcarrilloca@unal.edu.co | ¿Se asocia la modalidad de trabajo de grado (pasantía, monografía, asignaturas de posgrado) con la graduación, la deserción y los resultados académicos? |
| **202602_04_AdmisionPandemia** | Nicolas Jimenez Castaneda | nijimenezca@unal.edu.co | ¿Qué pasó cuando, durante el COVID, la UNAL reemplazó su examen de admisión por el Saber 11? Composición, capacidad predictiva e indicadores |
| **Administración del Repositorio de Datos** | Jeronimo Jimenez Castaneda | jerjimenezca@unal.edu.co | Auditar lo hecho en 2026-1S, integrar `BorradoresCodigo` a `main`, cargar nuevas versiones de datos y evaluar opciones de alojamiento |
| **Datos DANE C600** | Jeronimo Jimenez Castaneda | jerjimenezca@unal.edu.co | Consolidar la base C600 de colegios del DANE dentro del laboratorio de datos |

**Roles transversales**
- **Jeronimo Jimenez** administra el banco de datos. Es el único punto de contacto para pedir datos adicionales. También revisa que todos sigan las buenas prácticas de organización de código y datos.
- **Nicolas Jimenez** coadministra el banco de datos y tiene acceso completo junto con Jeronimo.
- **Karen Daniela Castillo** desarrolla su trabajo de grado dentro del proyecto Admisión Pandemia y se coordina con Nicolas.

---

## 3. Los cuatro proyectos de investigación

### 3.1 Cambio en planes curriculares (Jerson)
Muchos programas cambian su plan de estudios con el tiempo. Los cambios pueden ser de tres tipos: (i) **número de créditos**; (ii) **flexibilización**, es decir, asignaturas que pasan de optativas a obligatorias o al revés, o cambios en la ruta de grado; (iii) **solo de nombre o código**. Hasta ahora solo conocemos los cambios de la FCE, y queremos estudiar **toda la universidad**.
**Referencia principal:** Arteaga, C. (2018). *The effect of human capital on earnings: Evidence from a reform at Colombia's top university.* Journal of Public Economics, 157, 212–225.
**Meta del semestre:** identificar en los datos y en la normativa todos los cambios de plan, clasificarlos y cuantificar cuántos estudiantes resultaron afectados.

### 3.2 Timing de la admisión (Dilan y Julian)
Antes, el aspirante escogía el programa **y luego** presentaba el examen. Ahora presenta el examen **y luego** escoge. Según los profesores, este cambio pudo alterar de forma importante cómo se distribuyen los estudiantes, por ejemplo por género. La hipótesis es que más personas terminan en un programa que no era su primera opción, y que eso aumenta la doble titulación y los reingresos. El objetivo de la política era tener **"sillas llenas" con gente que quería estar ahí**. Queremos saber si se logró.
**Meta del semestre:** descriptivas antes y después del cambio (composición, doble titulación, reingresos, ocupación de cupos) y una base sistematizada de la normativa de admisión.
**Antecedente:** ya existe un artículo del profesor Hernando Bayona sobre el tema. Los datos de listas de admisión todavía no están disponibles; la profesora Karoll está gestionándolos.

### 3.3 Modalidad de trabajo de grado (Manuela)
¿Está asociada la modalidad de grado (pasantía, monografía o trabajo investigativo, asignaturas de posgrado) con mayor graduación, menor deserción o mejores resultados? ¿Prepara mejor la monografía para un posgrado?
**Meta del semestre:** describir la distribución de estudiantes por modalidad y sus resultados académicos, y revisar la normativa sobre criterios de selección por facultad.
**Nota de datos:** la variable de trabajo de grado existe en los datos armonizados de Egresados, pero **no** quedó en las bases finales. Hay que solicitarla a Jeronimo.

### 3.4 Admisión durante la pandemia (Nicolas)
Durante el COVID la universidad suspendió su examen de admisión y aceptó el **Saber 11 (ICFES)**. Es un experimento natural sobre el examen como barrera de entrada: es costoso y exige preparación, mientras que el Saber 11 lo toma casi todo el mundo. También sirve para estudiar la capacidad del examen para seleccionar.
**Meta del semestre:** construir la base de trabajo del proyecto; describir la composición (sexo, estrato, tipo de colegio, territorio) y los resultados académicos de quienes entraron con el examen UNAL y con el Saber 11. Además, definir con rigor los **indicadores para el dashboard** de la profesora Karoll.
**Coordinación:** Karen Daniela Castillo (trabajo de grado). Este proyecto se coordina con el de *Timing* para estandarizar los indicadores de composición.

---

## 4. Elementos comunes a todos los proyectos

Todos los proyectos tienen **un componente de datos** y **un componente de normativa**.

**Normativa.** No basta con descargar 50 PDFs. La normativa debe quedar **sistematizada como una base de datos**: una tabla con fecha, norma, órgano emisor, programa o facultad afectada, tipo de cambio, resumen y enlace. Se recomienda usar herramientas modernas (extracción de texto, LLMs) para resumir y clasificar la normativa, siempre verificando contra la fuente. Esto aplica **solo a documentos públicos, nunca a datos**. Fuentes principales: [Sistema de Información Normativa UNAL — legal.unal.edu.co](http://www.legal.unal.edu.co), acuerdos del Consejo Superior Universitario, del Consejo Académico y de los Consejos de Facultad, y resoluciones de admisión.

**Indicadores estandarizados.** Composición por sexo, estrato, PBM, tipo de colegio y territorio; graduación; deserción y retiro; créditos y PAPA. Deben definirse **una sola vez** y usarse igual en todos los proyectos. Julian lidera las definiciones de composición. Nicolas lidera las definiciones para el dashboard.

**Base de trabajo propia.** Cada proyecto construye su base a partir de `FinalWorkingDataSets`. Esa base vive en la carpeta `data/` del proyecto en Drive.

---

## 5. Datos y acceso

| Carpeta en Drive | Contenido | Acceso |
|---|---|---|
| `SemilleroAnalisisEconometrico/` | Repositorio completo: originales con datos personales, llaves, armonizados, bases finales | **Solo Jeronimo y Nicolas** |
| `SemilleroMicroeconometriaProyectos/FinalWorkingDataSets/` | Bases de trabajo anónimas (Matriculados, Cursadas, Egresados-Retirados) y diccionarios | Todos los RAs |
| `SemilleroMicroeconometriaProyectos/202602_0X_*/` | Carpeta de cada proyecto: `code/`, `data/`, `Literatura/`, `output/`, `Revision_normativa/` | Todos los RAs |

**Si necesitas una variable que no está en las bases finales**, la pides a **Jeronimo** con el formulario descrito en el [README de RAs](README.md#5-cómo-pedir-datos-adicionales). Nadie fuera de los administradores accede a datos con identificadores personales. Así protegemos los datos y cumplimos los acuerdos de confidencialidad que todos firmaron.

> **Datos e inteligencia artificial: regla obligatoria.**
> - **Nunca subas datos del proyecto a ningún agente de IA, chatbot o plataforma agéntica** (ChatGPT, Claude, Gemini, Copilot, Cursor, NotebookLM, etc.). Esto incluye bases, extractos, filas de ejemplo, tablas con microdatos y capturas de pantalla de datos.
> - La IA se puede usar con **código** y con **documentos públicos** (normativa, papers).
> - Si usas un agente de código, debe trabajar **solo dentro de la carpeta del código del proyecto**. No debe explorar otras carpetas del computador ni leer datos sin autorización manual de la PI/CoPI. Ver [CLAUDE.md](../CLAUDE.md).

---

## 6. Cómo trabajamos

1. **Planes de trabajo en GitHub.** Cada RA tiene un plan semanal en [`Semestre_2026-2S/planes/`](planes/) y una **rama propia**. Los planes se actualizan después de cada reunión: la transcripción se procesa con Claude y se ajustan las tareas.
2. **Reunión semanal de seguimiento.** Cada RA reporta sus tareas, a partir de los checkboxes de su plan.
3. **El trabajo vive en las carpetas del proyecto**, no en el computador personal. El código va a GitHub; los datos y outputs van a la carpeta del proyecto en Drive.
4. **Lenguaje libre** (R, Python o Stata). El código debe correr en otra máquina con solo cambiar el archivo de configuración.
5. **Calendario corto.** En los primeros 8 días cada RA debe haber revisado su plan y empezado las tareas mínimas.

### Calendario

| Semana | Fechas | Notas |
|---|---|---|
| S1 | 3 – 6 nov | Lun 2 nov festivo. Configuración, lectura, plan revisado |
| S2 | 9 – 13 nov | Base de trabajo v0 y normativa: búsqueda |
| S3 | 17 – 20 nov | Lun 16 nov festivo. Descriptivas iniciales |
| S4 | 23 – 27 nov | Avance de mitad de camino (presentación corta) |
| S5 | 30 nov – 4 dic | Profundización y robustez de las descriptivas |
| S6 | 9 – 11 dic | Mar 8 dic festivo. Documento final y **presentación final** |
| Cierre | 14 – 16 dic | Pull request final, documentación y plan para 2027-1S |

---

*Documento preparado a partir de la reunión del 2026-10-30. Última actualización: 2026-11-03.*
