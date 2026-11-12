"""Pasa un borrador en Markdown a Word usando la plantilla de la Escuela.

Uso:  py herramientas/md_a_word.py <borrador.md> --salida salidas/<nombre>.docx
      [--plantilla plantillas/Plantilla_institucional.docx]

La plantilla pone el formato (encabezado con el logo, letra, márgenes).
El borrador pone el contenido. Reconoce: # títulos, - viñetas, 1. listas,
> recuadros, tablas con | y **negrita**. Si la salida ya existe, agrega la fecha y hora.
"""
import argparse
import re
from datetime import datetime
from pathlib import Path

import docx
from docx.shared import Cm

RAIZ = Path(__file__).resolve().parents[1]


def _texto(parrafo, linea):
    # **negrita** y `nombres de archivo` dentro de la línea
    for trozo in re.split(r"(\*\*.+?\*\*|`[^`]+`)", linea):
        if len(trozo) > 4 and trozo.startswith("**") and trozo.endswith("**"):
            parrafo.add_run(trozo[2:-2]).bold = True
        elif len(trozo) > 2 and trozo.startswith("`") and trozo.endswith("`"):
            parrafo.add_run(trozo[1:-1]).font.name = "Consolas"
        elif trozo:
            parrafo.add_run(trozo)


def convertir(md, salida, plantilla):
    d = docx.Document(str(plantilla))
    marca = next((p for p in d.paragraphs if "{{CONTENIDO}}" in p.text), None)
    if marca is None:
        raise SystemExit("La plantilla no tiene el párrafo {{CONTENIDO}}.")

    lineas = md.read_text(encoding="utf-8").splitlines()
    titulo = next((l[2:].strip() for l in lineas if l.startswith("# ")), "")
    for p in d.paragraphs:
        if "{{TITULO}}" in p.text:
            for r in p.runs:
                r.text = r.text.replace("{{TITULO}}", titulo)

    tabla = []

    def volcar_tabla():
        if not tabla:
            return
        filas = [[c.strip() for c in f.strip().strip("|").split("|")] for f in tabla
                 if not re.fullmatch(r"\|?[\s:\-|]+\|?", f.strip())]
        ncol = max(len(f) for f in filas)
        t = d.add_table(rows=len(filas), cols=ncol)
        t.style = "Table Grid"
        # ancho de cada columna según su texto más largo (entre 4 y 60 caracteres)
        pesos = [min(60, max(4, *(len(f[j]) for f in filas if j < len(f)))) for j in range(ncol)]
        ancho = d.sections[0].page_width - d.sections[0].left_margin - d.sections[0].right_margin
        for fila in t.rows:
            for j, celda in enumerate(fila.cells):
                celda.width = int(ancho * pesos[j] / sum(pesos))
        for i, f in enumerate(filas):
            for j, c in enumerate(f):
                celda = t.cell(i, j).paragraphs[0]
                _texto(celda, c)
                if i == 0:
                    for r in celda.runs:
                        r.bold = True
        marca._p.addprevious(t._tbl)
        tabla.clear()

    for linea in lineas:
        if linea.startswith("# "):
            continue  # el título va en {{TITULO}}
        if linea.strip().startswith("|"):
            tabla.append(linea)
            continue
        volcar_tabla()
        if not linea.strip():
            continue
        m = re.match(r"(#{2,4})\s+(.*)", linea)
        if m:
            p = marca.insert_paragraph_before(style=f"Heading {len(m.group(1)) - 1}")
            _texto(p, m.group(2))
        elif linea.startswith("> "):
            _texto(marca.insert_paragraph_before(style="Quote"), linea[2:].strip())
        elif re.match(r"\s*[-*]\s+", linea):
            _texto(marca.insert_paragraph_before(style="List Bullet"), re.sub(r"^\s*[-*]\s+", "", linea))
        elif re.match(r"\s*\d+[.)]\s+", linea):
            # el número va escrito: "List Number" de Word seguiría contando de una lista a otra
            p = marca.insert_paragraph_before()
            p.paragraph_format.left_indent = Cm(0.6)
            _texto(p, linea.strip())
        else:
            _texto(marca.insert_paragraph_before(), linea.strip())
    volcar_tabla()
    marca._p.getparent().remove(marca._p)

    if salida.exists():
        salida = salida.with_name(f"{salida.stem}_{datetime.now():%Y-%m-%d_%H%M}{salida.suffix}")
    salida.parent.mkdir(parents=True, exist_ok=True)
    d.save(str(salida))
    return salida


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("borrador")
    ap.add_argument("--salida", required=True)
    ap.add_argument("--plantilla", default=str(RAIZ / "plantillas" / "Plantilla_institucional.docx"))
    a = ap.parse_args(argv)
    hecho = convertir(Path(a.borrador), Path(a.salida), Path(a.plantilla))
    print(f"Word generado: {hecho}")
    return hecho


if __name__ == "__main__":
    main()
