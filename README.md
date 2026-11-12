# Kit docente IA

**Español** · [English](#english)

Un agente de IA listo para trabajar con docentes universitarios: una carpeta con **reglas (arnés)**, **procedimientos (skills)** y un **control automático (hook)**, más plantillas Word y PowerPoint. Se instala con un solo comando y se usa con [Antigravity](https://antigravity.google/).

Sirve para cualquier institución y se mejora con cada curso (ver [MEJORAS.md](MEJORAS.md)).

## Instalación en un paso (Windows)

1. Pulsa **Windows + X** y elige **Terminal** (o **Windows PowerShell**).
2. Copia esta línea, pégala con clic derecho y pulsa **Enter**:

```powershell
irm https://raw.githubusercontent.com/Miqueas7/kit-docente-ia/main/instalar.ps1 | iex
```

3. Espera a que diga **TODO EN ORDEN**. Al terminar se abre la carpeta con tus plantillas.

El comando instala Python y Antigravity si faltan, descarga este material y lo deja listo:

| Dónde queda | Qué es |
|---|---|
| `Documentos\Mi curso` | La carpeta que abres en Antigravity: el arnés (`AGENTS.md`), las skills, las plantillas y el hook |
| `Documentos\Tesis privadas` | Las tesis originales van aquí, fuera de Mi curso. Trae una tesis inventada para practicar |
| `Documentos\Kit docente IA` | Plantillas Word, plantilla PowerPoint y la guía «Tu agente por dentro» |

Si ya tenías la carpeta, el comando **solo agrega lo que falta**: no reemplaza ni borra nada tuyo. Vuelve a ejecutarlo para recibir las mejoras.

## Después de instalar

1. Abre **Antigravity** y entra con tu **Gmail personal**.
2. Abre la carpeta `Documentos\Mi curso`.
3. En **Customizations > Hooks** revisa que aparezca **kit-docente-ia**.
4. Escribe al agente: *Lee el archivo AGENTS.md y explícame en cinco líneas qué puedes hacer y qué no.*

## Qué trae

| Pieza | Qué hace |
|---|---|
| Arnés (`Mi curso/AGENTS.md`) | Reglas que el agente cumple siempre: datos personales, calidad, fuentes, el docente decide |
| Skills (`Mi curso/.agents/skills/`) | `silabo-competencias`, `preparar-sesion`, `elaborar-material`, `evaluar`, `proteger-datos`, `revisar-tesis` |
| Hook (`Mi curso/herramientas/hook_proteger.py`) | Revisa cada acción: nada fuera de la carpeta, nada de nombres reales, tesis solo anonimizadas |
| `Plantillas Word/` | Sílabo, sesión, guía de práctica, rúbrica, banco de preguntas, informe de revisión de tesis, guía de uso responsable y plan de uso de la IA |
| `Plantilla PowerPoint/` | Presentación de clase |
| `Tu agente por dentro - skills, hook y arnes.docx` | Qué es cada pieza y cómo usarla |

Todos los datos de ejemplo son inventados.

## Mantener y mejorar el kit

- **Antes de cada curso**, prueba la instalación en una laptop limpia: que winget instale Python y Antigravity, que diga TODO EN ORDEN y que en Antigravity, en **Customizations > Hooks**, aparezca **kit-docente-ia**. Luego pide al agente que abra la tesis de `Tesis privadas`: el hook debe bloquearlo.
- **Las mejoras llegan solas:** el docente vuelve a pegar el mismo comando y recibe lo nuevo sin perder lo suyo (solo se agregan archivos que falten; los que ya tiene no se reemplazan).
- **Cada cambio** va en un commit y en [MEJORAS.md](MEJORAS.md), con la fecha y la edición.
- **Nunca** subas datos de alumnos, docentes ni empresas, ni logos o membretes de una institución: el repositorio es público. Antes de cada push corre `py revisar_publicacion.py`.
- **Tu institución:** reemplaza `Mi curso/plantillas/Plantilla_institucional.docx` por tu hoja membretada para que tus documentos salgan con tu logo. Las versiones con la marca de una institución se entregan aparte, nunca en este repositorio.
- **Mac** todavía no está soportado: el instalador es solo para Windows.

## Ediciones

| Edición | Modalidad |
|---|---|
| 1 | Capacitación presencial de docentes universitarios |

Autor: Ing. Miqueas Quintanilla Ventura

---

<a id="english"></a>

# AI Teaching Kit

[Español](#kit-docente-ia) · **English**

A ready-to-use AI agent for university teachers: a folder with **rules (harness)**, **procedures (skills)** and an **automatic check (hook)**, plus Word and PowerPoint templates. It installs with a single command and runs in [Antigravity](https://antigravity.google/).

It works for any institution and improves with every course (see [MEJORAS.md](MEJORAS.md)). The kit's materials, skills and templates are in Spanish.

## One-step installation (Windows)

1. Press **Windows + X** and choose **Terminal** (or **Windows PowerShell**).
2. Copy this line, paste it with a right click and press **Enter**:

```powershell
irm https://raw.githubusercontent.com/Miqueas7/kit-docente-ia/main/instalar.ps1 | iex
```

3. Wait until it says **TODO EN ORDEN** (all good). When it finishes, the folder with your templates opens.

The command installs Python and Antigravity if they are missing, downloads this material and sets it up:

| Location | What it is |
|---|---|
| `Documents\Mi curso` | The folder you open in Antigravity: the harness (`AGENTS.md`), the skills, the templates and the hook |
| `Documents\Tesis privadas` | Original theses go here, outside Mi curso. It includes a made-up thesis for practice |
| `Documents\Kit docente IA` | Word templates, the PowerPoint template and the guide «Tu agente por dentro» |

If you already have the folder, the command **only adds what is missing**: it never replaces or deletes your files. Run it again to get the improvements.

## After installing

1. Open **Antigravity** and sign in with your **personal Gmail**.
2. Open the folder `Documents\Mi curso`.
3. In **Customizations > Hooks**, check that **kit-docente-ia** is listed.
4. Ask the agent: *Read AGENTS.md and explain in five lines what you can and cannot do.*

## What's inside

| Piece | What it does |
|---|---|
| Harness (`Mi curso/AGENTS.md`) | Rules the agent always follows: personal data, quality, sources, the teacher decides |
| Skills (`Mi curso/.agents/skills/`) | `silabo-competencias` (competency-based syllabus), `preparar-sesion` (lesson plan), `elaborar-material` (course materials), `evaluar` (assessment), `proteger-datos` (data protection), `revisar-tesis` (thesis review) |
| Hook (`Mi curso/herramientas/hook_proteger.py`) | Checks every action: nothing outside the folder, no real names, theses only when anonymized |
| `Plantillas Word/` | Syllabus, lesson plan, lab guide, rubric, question bank, thesis review report, responsible AI use guide and AI use plan |
| `Plantilla PowerPoint/` | Class presentation |
| `Tu agente por dentro - skills, hook y arnes.docx` | What each piece is and how to use it |

All sample data is made up.

## Maintaining and improving the kit

- **Before each course**, test the installation on a clean laptop: winget installs Python and Antigravity, it says TODO EN ORDEN, and **kit-docente-ia** shows up in Antigravity under **Customizations > Hooks**. Then ask the agent to open the thesis in `Tesis privadas`: the hook must block it.
- **Improvements arrive on their own:** teachers paste the same command again and get the new material without losing theirs (only missing files are added; existing ones are never replaced).
- **Every change** goes into a commit and into [MEJORAS.md](MEJORAS.md), with its date and edition.
- **Never** upload student, teacher or company data, nor an institution's logos or letterheads: this repository is public. Run `py revisar_publicacion.py` before every push.
- **Your institution:** replace `Mi curso/plantillas/Plantilla_institucional.docx` with your letterhead so your documents carry your logo. Institution-branded versions are delivered separately, never in this repository.
- **Mac** is not supported yet: the installer is Windows only.

## Editions

| Edition | Format |
|---|---|
| 1 | In-person training for university teachers |

Author: Ing. Miqueas Quintanilla Ventura
