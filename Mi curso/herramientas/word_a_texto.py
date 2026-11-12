"""Convierte un sílabo (u otro documento DEL DOCENTE) de Word o PDF a texto .md.

Uso:  py herramientas/word_a_texto.py "<archivo .docx o .pdf>"

Deja el .md junto al archivo, con el mismo nombre. Así el agente puede leerlo.
No lo uses con tesis ni trabajos de alumnos: para eso está la skill proteger-datos.
"""
import sys
from pathlib import Path


def convertir(ruta):
    if ruta.suffix.lower() == ".docx":
        import docx

        d = docx.Document(str(ruta))
        lineas = []
        for p in d.paragraphs:
            t = p.text.strip()
            if not t:
                continue
            nivel = p.style.name.split()[-1] if p.style.name.lower().startswith(("heading", "título")) else ""
            lineas.append(("#" * (int(nivel) + 1) + " " if nivel.isdigit() else "") + t)
        for t in d.tables:
            lineas.append("")
            for i, fila in enumerate(t.rows):
                lineas.append("| " + " | ".join(c.text.strip().replace("\n", " ") for c in fila.cells) + " |")
                if i == 0:
                    lineas.append("|" + "---|" * len(fila.cells))
    elif ruta.suffix.lower() == ".pdf":
        import pypdf

        lineas = [pag.extract_text() or "" for pag in pypdf.PdfReader(str(ruta)).pages]
    else:
        sys.exit("Solo se aceptan archivos .docx o .pdf.")
    salida = ruta.with_suffix(".md")
    salida.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    return salida


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    print(f"Texto generado: {convertir(Path(sys.argv[1]).resolve())}")
