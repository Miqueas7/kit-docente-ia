"""Revisa antes de cada push que el repositorio no lleve marcas de una institución.

Falla si encuentra:
- una imagen dentro de un Word o PowerPoint que no sea el logo o la miniatura de ejemplo;
- alguna palabra de `.marcas_bloqueadas.txt` (nombres de instituciones, dominios de correo). Ese archivo es local y no se
  sube: cada quien anota ahí sus propias marcas, una por línea.
Uso:  py revisar_publicacion.py
"""
import hashlib
import re
import subprocess
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
# shortcut: solo se aceptan las imágenes de ejemplo; si agregas una imagen propia a una plantilla, suma aquí su hash
PERMITIDAS = {
    "dd15447907bcb40d47644518ed6a2f949967fa6f6ed7c120d5dadab3f36990cc",  # logo de ejemplo
    "e8b7dde245038901ffc437b9b64b1ab3540b70a6c030658935782aa05695e31b",  # miniatura de Word
    "df775673efc5314f732450dba0ff2ef830bf6407c010d824a3424b116fe103ea",  # miniatura de PowerPoint
}


def main():
    lista = RAIZ / ".marcas_bloqueadas.txt"
    marcas = [m.strip() for m in lista.read_text(encoding="utf-8").splitlines() if m.strip()] if lista.exists() else []
    if not marcas:
        print("AVISO: no hay .marcas_bloqueadas.txt; solo se revisan las imágenes.")
    patron = re.compile("|".join(map(re.escape, marcas)), re.I) if marcas else None
    archivos = subprocess.run(["git", "-C", str(RAIZ), "ls-files"], capture_output=True, text=True,
                              encoding="utf-8").stdout.splitlines()
    problemas = []
    for rel in archivos:
        f = RAIZ / rel
        textos = [rel]
        if f.suffix in (".docx", ".pptx"):
            with zipfile.ZipFile(f) as z:
                for n in z.namelist():
                    if re.search(r"\.(png|jpe?g|gif|emf|wmf|svg)$", n, re.I):
                        if hashlib.sha256(z.read(n)).hexdigest() not in PERMITIDAS:
                            problemas.append(f"{rel}: imagen no permitida ({n})")
                    elif n.endswith(".xml"):
                        textos.append(re.sub(r"<[^>]+>", "", z.read(n).decode("utf-8", "ignore")))
        else:
            textos.append(f.read_text(encoding="utf-8", errors="ignore"))
        if patron:
            hallados = {m.group(0) for t in textos for m in patron.finditer(t)}
            if hallados:
                problemas.append(f"{rel}: {', '.join(sorted(hallados))}")
    for p in problemas:
        print("NO PUBLICAR:", p)
    print("Listo para publicar." if not problemas else f"{len(problemas)} problema(s).")
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main())
