---
name: preparar-sesion
description: Prepara una sesión de clase (sesión de aprendizaje) en Word con la plantilla de la Escuela. Úsala cuando el docente pida preparar, planificar o armar una clase o una sesión.
---

# Preparar una sesión de clase

## 1. Datos que necesitas

Si falta uno, pregúntalo. No lo inventes.

- Asignatura y ciclo
- Número de sesión y semana
- Tema
- Duración (por ejemplo, 2 horas)
- Modalidad (presencial o virtual)

## 2. Pasos

1. Busca el sílabo en `silabo/`. Si está en Word o PDF y no hay un `.md` con el mismo nombre, conviértelo:
   `py herramientas/word_a_texto.py "silabo/<archivo>"`.
   Si hay varios sílabos, pregunta cuál. Si no hay ninguno, pide al docente la competencia y el resultado de aprendizaje de la unidad.
2. Del sílabo toma: competencia, resultado de aprendizaje de la unidad, contenidos de esa semana y bibliografía.
3. Lee `plantillas/sesion.md` y sigue exactamente sus secciones, en el mismo orden y con los mismos títulos.
4. Redacta el borrador en `salidas/borradores/Sesion_<n>_<tema-corto>.md`, cumpliendo:
   - Los tiempos de la secuencia suman exactamente la duración.
   - El logro de la sesión usa un verbo observable (calcula, diseña, compara, evalúa), no «conoce» ni «entiende».
   - Hay al menos un caso o ejemplo de minería peruana, con su fuente.
   - Las actividades dicen qué hace el docente y qué hacen los estudiantes.
   - La evaluación indica criterio, evidencia e instrumento.
   - Las referencias salen del sílabo o tienen fuente verificable. Lo dudoso lleva [VERIFICAR].
5. Muestra al docente un resumen corto (logro y secuencia con tiempos) y espera su visto bueno o sus cambios.
6. Genera el Word:
   `py herramientas/md_a_word.py "salidas/borradores/<borrador>.md" --salida "salidas/Sesion_<n>_<tema-corto>.docx"`
7. Cierra con la lista de cotejo de abajo y la lista de los [VERIFICAR] que quedaron.

## 3. Lista de cotejo (escríbela al final de tu respuesta)

- [ ] La competencia y el resultado coinciden con el sílabo
- [ ] Los tiempos suman la duración
- [ ] El logro tiene un verbo observable
- [ ] Hay un caso peruano con fuente
- [ ] La evaluación tiene criterio, evidencia e instrumento
- [ ] Los [VERIFICAR] están listados
