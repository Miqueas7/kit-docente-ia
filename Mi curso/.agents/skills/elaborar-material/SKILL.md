---
name: elaborar-material
description: Elabora material de clase en Word (guía de práctica, casos de estudio, problemas resueltos) con la plantilla de la Escuela. Úsala cuando el docente pida una guía, una práctica, un caso, ejercicios o problemas.
---

# Elaborar material de clase

## 1. Datos que necesitas

- Asignatura, ciclo y tema (o la sesión de `salidas/` a la que acompaña)
- Tipo de material: guía de práctica, caso de estudio o problemas resueltos
- Cantidad (por ejemplo, 5 problemas) y nivel (básico, intermedio, avanzado)
- Tiempo que tendrán los estudiantes para resolverlo

## 2. Pasos

1. Si acompaña a una sesión, lee el borrador de esa sesión en `salidas/borradores/` para mantener el mismo logro y el mismo vocabulario.
2. Lee `plantillas/guia.md` y sigue sus secciones al pie de la letra.
3. Datos reales: usa datos de minería peruana con fuente (MINEM, INGEMMET, OSINERGMIN, normas en El Peruano, papers). Si el docente investigó con Gemini (Deep Research), pídele que pegue el resumen con sus fuentes. No inventes leyes de mineral, producciones ni costos: si no hay fuente, usa datos claramente ficticios y escribe «(datos ficticios con fines didácticos)».
4. Problemas con números:
   - Resuelve cada problema paso a paso, con fórmula, reemplazo, resultado y unidades del SI.
   - Antes de entregarlo, verifica cada resultado con un script corto de Python en `salidas/borradores/verificacion_<tema>.py` y ejecútalo. Si tu resultado y el del script no coinciden, corrige y vuelve a verificar.
   - Las respuestas van en una sección aparte («Solucionario»), para que el docente pueda quitarla.
5. Redacta el borrador en `salidas/borradores/Material_<tema-corto>.md`.
6. Muestra al docente la lista de problemas o casos (solo enunciados) y espera su visto bueno.
7. Genera el Word:
   `py herramientas/md_a_word.py "salidas/borradores/<borrador>.md" --salida "salidas/Material_<tema-corto>.docx"`
8. Cierra con la lista de cotejo.

## 3. Lista de cotejo

- [ ] Sigue la estructura de `plantillas/guia.md`
- [ ] Cada dato real tiene fuente; lo ficticio está marcado
- [ ] Cada cálculo fue verificado con Python y tiene unidades
- [ ] El solucionario está en su propia sección
- [ ] El tiempo alcanza para lo que se pide
