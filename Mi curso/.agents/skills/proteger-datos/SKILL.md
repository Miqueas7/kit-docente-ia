---
name: proteger-datos
description: Úsala SIEMPRE antes de trabajar con una tesis, un informe o cualquier trabajo de un alumno. Crea en esta computadora un extracto anonimizado; el agente solo trabaja sobre ese extracto, nunca sobre el original.
---

# Proteger datos (anonimizar en la computadora del docente)

Esta skill es el candado de datos de la carpeta. Ninguna otra skill toca un trabajo de alumno sin pasar antes por aquí.

## Pasos

1. Pide al docente la ruta completa del archivo original (.docx o .pdf). El archivo debe estar FUERA de esta carpeta, en `Documentos\Tesis privadas\`. Si está dentro, pídele que lo mueva antes de seguir.
2. Pregunta si hay nombres que el script podría no detectar (asesor, jurados, empresa, unidad minera). Si los hay, pídele que los escriba él mismo en un archivo `nombres.txt`, uno por línea, en la misma carpeta del original. No los escribas tú y no los repitas en el chat.
3. Ejecuta, sin abrir el original:

   ```
   py .agents/skills/proteger-datos/scripts/preparar_tesis.py "<ruta del original>"
   ```

4. El script muestra solo conteos y la ruta del extracto. Explícale al docente qué significan los conteos en dos o tres líneas.
5. Abre el extracto (`tesis_anonimizadas/T…_extracto.md`) y revisa que no quede ningún nombre propio de persona, empresa o mina fuera de los códigos P01…, E01…. Si encuentras uno, no lo copies en el chat: dile al docente en qué sección está, para que lo agregue a `nombres.txt`, y vuelve al paso 3.
6. Desde aquí se trabaja solo con el extracto.

## Prohibido

- Abrir, leer o mostrar el original con cualquier herramienta o comando.
- Leer el archivo `*_codigos.csv` (la tabla que une códigos y nombres) o `nombres.txt`.
- Deshacer la anonimización o adivinar a quién corresponde un código.

## Si algo falla

- «No se encontró el archivo»: pide la ruta otra vez (clic derecho en el archivo → Copiar como ruta).
- «No module named docx» o «pypdf»: pide permiso y ejecuta `py -m pip install python-docx pypdf`.
- «El archivo no tiene texto»: es un PDF escaneado. Pide la versión en Word.
