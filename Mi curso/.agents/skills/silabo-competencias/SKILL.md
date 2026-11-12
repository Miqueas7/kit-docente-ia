---
name: silabo-competencias
description: Elabora o reestructura el sílabo de una asignatura por competencias, en Word con la plantilla de la Escuela, a partir de la competencia del perfil de egreso y la sumilla del plan de estudios. Úsala cuando el docente pida armar, actualizar o revisar un sílabo.
---

# Sílabo por competencias

## 1. Datos que necesitas

Si falta uno, pregúntalo. No lo inventes.

- Asignatura, código y ciclo
- Créditos y horas por semana (teoría y práctica)
- Número de semanas del semestre
- La sumilla, copiada del plan de estudios
- La competencia del perfil de egreso a la que aporta el curso, copiada del plan de estudios

## 2. Pasos

1. Busca en `silabo/` la sumilla, la competencia y el sílabo anterior, si existe. Si están en Word o PDF y no hay un `.md` con el mismo nombre, conviértelos:
   `py herramientas/word_a_texto.py "silabo/<archivo>"`.
2. Si en `plantillas/` hay un formato oficial de sílabo de la Escuela, úsalo. Si no, usa `plantillas/silabo.md`. Sigue sus secciones en el mismo orden y con los mismos títulos.
3. Arma el sílabo de arriba hacia abajo, sin saltarte niveles:
   - **Competencia de la asignatura**: sale de la competencia del perfil y de la sumilla. Una sola, con verbo observable.
   - **Resultados de aprendizaje**: uno por unidad, con verbo observable + contenido + condición. Nunca «conoce», «entiende» ni «comprende».
   - **Unidades y contenidos**: cada contenido de la sumilla aparece en alguna semana. Las semanas suman las del semestre.
   - **Evidencias y criterios**: cada resultado tiene al menos una evidencia, un criterio y un instrumento. Los pesos suman 100 %.
4. Redacta el borrador en `salidas/borradores/Silabo_<asignatura-corta>.md`. La sumilla y la competencia del perfil se copian tal cual, sin cambiar una palabra.
5. Bibliografía: usa la del sílabo anterior o libros y normas que puedas verificar. Lo que no puedas verificar lleva [VERIFICAR]. Normas peruanas con su número y fecha de publicación en El Peruano.
6. Muestra al docente un resumen corto (competencia, resultados por unidad y evaluación con pesos) y espera su visto bueno o sus cambios.
7. Genera el Word:
   `py herramientas/md_a_word.py "salidas/borradores/<borrador>.md" --salida "salidas/Silabo_<asignatura-corta>.docx"`
8. Cierra con la lista de cotejo de abajo y la lista de los [VERIFICAR] que quedaron.

## 3. Candados

- No cambies la sumilla ni la competencia del perfil: son del plan de estudios aprobado.
- No inventes horas, créditos ni códigos: si no están, pregúntalos.
- No pongas nombres de alumnos ni datos personales.

## 4. Lista de cotejo (escríbela al final de tu respuesta)

- [ ] La sumilla y la competencia del perfil están copiadas tal cual
- [ ] Cada resultado de aprendizaje tiene verbo observable
- [ ] Cada contenido de la sumilla está en alguna semana
- [ ] Las semanas suman las del semestre y las horas cuadran con los créditos
- [ ] Cada resultado tiene evidencia, criterio e instrumento
- [ ] Los pesos de la evaluación suman 100 %
- [ ] Los [VERIFICAR] están listados
