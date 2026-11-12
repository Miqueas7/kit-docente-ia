# Mejoras

Registro de cambios y pendientes. Cada curso deja aquí lo que aprendió.

## Pendientes

- Probar el hook en Antigravity real (que aparezca en Customizations > Hooks y bloquee una tesis original).
- Instalación para Mac.
- Recoger de los docentes de la edición 1 qué skill les faltó (por ejemplo: informe de visita técnica, guía de laboratorio).

## Historial

### 2026-11-12 · Kit general

- Sin marca de ninguna institución: membrete y logo de ejemplo, que cada docente reemplaza por los suyos.
- Hook `kit-docente-ia`. El instalador quita el registro anterior del mismo hook, así que no queda duplicado.
- `revisar_publicacion.py`: revisa antes de cada push que no se suban logos ni nombres de una institución.

### 2026-11-12 · Edición 1

- Seis skills: `silabo-competencias` (nueva), `preparar-sesion`, `elaborar-material`, `evaluar`, `proteger-datos`, `revisar-tesis`.
- Hook `hook_proteger.py` para Antigravity, con autoprueba.
- Plantillas Word y PowerPoint con membrete institucional.
- Instalación en un paso desde GitHub (`instalar.ps1`): instala Python y Antigravity con winget si faltan y no reemplaza archivos del docente.
