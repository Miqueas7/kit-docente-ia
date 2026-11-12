---
name: revisar-tesis
description: Revisa la estructura y la coherencia de una tesis o proyecto de tesis a partir de su extracto anonimizado y entrega un informe de observaciones en Word. Úsala cuando el docente (asesor o jurado) pida revisar una tesis, un proyecto de tesis o un plan de investigación.
---

# Revisar una tesis (asesor o jurado)

## 1. Antes de empezar (candado)

- Solo trabajas con un extracto `tesis_anonimizadas/T…_extracto.md`. Si no existe, usa primero la skill `proteger-datos`. Nunca pidas ni abras el original.
- No reescribes la tesis. Haces observaciones con su ubicación y una sugerencia. La redacción es del estudiante y el criterio final es del asesor o del jurado.

## 2. Datos que necesitas

- El rol del docente: asesor o jurado
- Etapa: proyecto de tesis o informe final
- Norma de referencias que exige la Facultad (si no lo sabe, revisa con APA 7.ª edición y dilo)
- Si hay un reglamento o guía de la Facultad, pídele que lo copie en `normas/` y léelo

## 3. Qué revisas, en este orden

1. **Estructura:** el índice tiene las partes que exige la guía de la Facultad (o, si no hay guía, las partes usuales: problema, marco teórico, hipótesis, metodología, resultados, discusión, conclusiones, recomendaciones, referencias, anexos).
2. **Matriz de consistencia:** el problema general, el objetivo general y la hipótesis general dicen lo mismo con distinta forma; cada problema específico tiene su objetivo y su hipótesis específica.
3. **Objetivos:** empiezan con un verbo en infinitivo que se pueda medir (determinar, evaluar, diseñar), no «conocer» ni «estudiar».
4. **Conclusiones:** hay una conclusión por cada objetivo, en el mismo orden, y cada una responde a su objetivo con un resultado.
5. **Recomendaciones:** salen de las conclusiones.
6. **Referencias:** formato correcto, años, y proporción de fuentes de los últimos 5 a 10 años. No inventes ni completes referencias: si una se ve incompleta, márcala.

## 4. Pasos

1. Lee el extracto y redacta el informe en `salidas/borradores/Informe_revision_<código T>.md` con la estructura de `plantillas/informe_tesis.md`.
2. Cada observación lleva: número, sección, observación, sugerencia y prioridad (alta, media, baja).
3. Muestra al docente las observaciones de prioridad alta y espera su visto bueno.
4. Genera el Word:
   `py herramientas/md_a_word.py "salidas/borradores/<borrador>.md" --salida "salidas/Informe_revision_<código T>.docx"`
5. Recuérdale que el informe usa códigos (P01, E01): si lo va a entregar al estudiante, él mismo cambia los códigos por los nombres en su computadora.

## 5. Límites que debes decir siempre

- El extracto no incluye todo el texto: no opines sobre el marco teórico, los resultados ni la discusión que no ves.
- Si algo no se puede juzgar con el extracto, dilo en lugar de suponer.
