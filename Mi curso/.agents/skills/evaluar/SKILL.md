---
name: evaluar
description: Prepara instrumentos de evaluación en Word (rúbricas, bancos de preguntas, retroalimentación modelo) alineados al sílabo. Úsala cuando el docente pida una rúbrica, un examen, preguntas, una práctica calificada o criterios de calificación.
---

# Evaluar

La IA propone el instrumento; la nota la pone el docente.

## 1. Datos que necesitas

- Asignatura, ciclo y tema o unidad
- Qué se evalúa: un producto (informe, proyecto, exposición) o conocimientos (examen)
- Instrumento: rúbrica, banco de preguntas o ambos
- Para preguntas: cantidad y tipo (opción múltiple, desarrollo, problema)
- Puntaje total (por ejemplo, 20)

## 2. Pasos

1. Del sílabo en `silabo/` toma la competencia y el resultado de aprendizaje. Cada criterio o pregunta debe salir de ahí.
2. Rúbrica: sigue `plantillas/rubrica.md`.
   - 4 a 6 criterios, cada uno con 4 niveles (Destacado, Logrado, En proceso, Inicio).
   - Cada nivel describe algo que se puede observar en el trabajo, no un adjetivo («bueno», «regular»).
   - Los puntajes suman el total pedido.
3. Banco de preguntas: sigue `plantillas/banco_preguntas.md`.
   - Indica para cada pregunta el nivel de Bloom (recordar, comprender, aplicar, analizar, evaluar, crear). Al menos la mitad deben ser de aplicar o más.
   - En opción múltiple: una sola respuesta correcta y distractores que respondan a errores comunes; explica por qué cada distractor es incorrecto.
   - Las preguntas con cálculo se verifican con Python, igual que en `elaborar-material`.
   - La clave va en una sección aparte al final.
4. Redacta el borrador en `salidas/borradores/Evaluacion_<tema-corto>.md`, muestra al docente los criterios o las preguntas y espera su visto bueno.
5. Genera el Word:
   `py herramientas/md_a_word.py "salidas/borradores/<borrador>.md" --salida "salidas/Evaluacion_<tema-corto>.docx"`

## 3. Candados

- Nunca uses nombres, códigos ni notas reales de estudiantes.
- Si el docente quiere ayuda para revisar trabajos de alumnos, primero pasa cada trabajo por `proteger-datos` y trabaja solo con los extractos. Propón observaciones y un nivel de la rúbrica con su justificación; la nota final la decide el docente.

## 4. Lista de cotejo

- [ ] Cada criterio o pregunta se alinea con la competencia del sílabo
- [ ] Los niveles de la rúbrica son observables y los puntajes suman el total
- [ ] Las preguntas tienen nivel de Bloom y la clave va aparte
- [ ] Los cálculos están verificados
