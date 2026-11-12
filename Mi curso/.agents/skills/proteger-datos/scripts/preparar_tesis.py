"""Anonimiza una tesis o trabajo de alumno EN ESTA COMPUTADORA y deja un extracto.

Uso:  py preparar_tesis.py "<ruta del original .docx o .pdf>"

- El original no se modifica.
- La tabla código-nombre (<original>_codigos.csv) se guarda JUNTO AL ORIGINAL,
  fuera de la carpeta del curso. El agente nunca la lee.
- El extracto (índice, resumen, problema, objetivos, hipótesis, conclusiones,
  recomendaciones y referencias) queda en tesis_anonimizadas/ con un código,
  nunca con el nombre del archivo, porque el nombre suele llevar el del alumno.
- En pantalla solo salen conteos, para que nada personal llegue al chat.
"""
import argparse
import csv
import hashlib
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]  # carpeta del curso

TITULOS = r"(?:Bach\.|Bachiller|Ing\.|Ingeniero|Ingeniera|Dr\.|Dra\.|Mg\.|M\.Sc\.|MSc\.|Lic\.)"
NOMBRE = r"[A-ZÁÉÍÓÚÑ][A-Za-zÁÉÍÓÚÑáéíóúñü\.]+(?:\s+[A-ZÁÉÍÓÚÑ][A-Za-zÁÉÍÓÚÑáéíóúñü\.]+){1,5}"
PISTAS = r"(?:presentado\s+por|presentada\s+por|autor(?:a|es)?|tesista|bachiller|asesor(?:a)?|co-?asesor(?:a)?|jurado|miembro)"
EMPRESA = (
    r"(?:(?:Compañía|Compania|Cía\.|Empresa|Sociedad|Corporación|Unidad\s+Minera|U\.\s?M\.|Minera|Mina)"
    r"(?:\s+(?:Minera|de|del|la|las|los|[A-ZÁÉÍÓÚÑ][\w\.\-]*)){1,6}"
    r"|[A-ZÁÉÍÓÚÑ][\w\.\-]*(?:\s+[A-ZÁÉÍÓÚÑ][\w\.\-]*){0,4}\s+(?:S\.A\.C\.|S\.A\.A\.|S\.A\.|E\.I\.R\.L\.|S\.R\.L\.))"
)
SECCIONES = re.compile(
    r"resumen|abstract|problema|formulaci[oó]n|objetivo|hip[oó]tesis|conclusi[oó]n|conclusiones|"
    r"recomendaci[oó]n|recomendaciones|referencias|bibliograf[ií]a|[ií]ndice|contenido",
    re.I,
)
ES_TITULO = re.compile(r"^(CAP[IÍ]TULO\b|\d+(\.\d+)+\.?\s+\S)", re.I)
MAX_SECCION = 4000  # caracteres por sección en el extracto
MAX_REFERENCIAS = 80


def es_titulo(t):
    # una línea solo en mayúsculas cuenta como título si nombra una sección (así un nombre de la carátula no entra al índice)
    return len(t) < 120 and (bool(ES_TITULO.match(t)) or (t.isupper() and len(t) < 80 and bool(SECCIONES.search(t))))


def leer(ruta):
    """Devuelve [(texto, es_titulo)] del .docx o .pdf."""
    if ruta.suffix.lower() == ".docx":
        import docx

        d = docx.Document(str(ruta))
        filas = [(p.text.strip(), p.style.name.lower().startswith(("heading", "título", "titulo")))
                 for p in d.paragraphs]
        for t in d.tables:  # la carátula a veces viene en tabla
            for c in t._cells:
                filas += [(p.text.strip(), False) for p in c.paragraphs]
        return [(t, h or es_titulo(t)) for t, h in filas if t]
    if ruta.suffix.lower() == ".pdf":
        import pypdf

        lineas = []
        for pag in pypdf.PdfReader(str(ruta)).pages:
            lineas += [l.strip() for l in (pag.extract_text() or "").splitlines() if l.strip()]
        return [(l, es_titulo(l)) for l in lineas]
    sys.exit("Solo se aceptan archivos .docx o .pdf.")


def buscar_personas(filas, extra):
    nombres = list(extra)
    for i, (t, _) in enumerate(filas[:200]):  # carátula y primeras páginas
        if re.search(rf"\b{PISTAS}\b", t, re.I):
            resto = re.split(r":", t, maxsplit=1)[-1] if ":" in t else ""
            candidatos = [resto] + [filas[j][0] for j in range(i + 1, min(i + 3, len(filas)))]
            for c in candidatos:
                m = re.search(rf"(?:{TITULOS}\s*)?({NOMBRE})", c.strip())
                if m and not re.search(PISTAS, m.group(1), re.I):
                    nombres.append(m.group(1))
                    break
    for t, _ in filas:
        nombres += re.findall(rf"{TITULOS}\s+({NOMBRE})", t)
    # sin duplicados (sin distinguir mayúsculas), los más largos primero
    vistos = {}
    for n in nombres:
        n = n.strip(" .,;")
        if len(n) > 4:
            vistos.setdefault(n.lower(), n)
    return sorted(vistos.values(), key=len, reverse=True)


def anonimizar(filas, personas):
    tabla, cuenta = {}, {"personas": 0, "dni_o_codigos": 0, "correos": 0, "telefonos": 0, "empresas_o_minas": 0}

    def codigo(valor, prefijo):
        clave = valor.lower()
        if clave not in tabla:
            n = sum(1 for v in tabla.values() if v[0].startswith(prefijo)) + 1
            tabla[clave] = (f"{prefijo}{n:02d}", valor)
        return tabla[clave][0]

    patrones_personas = [(re.compile(re.escape(p), re.I), p) for p in personas]
    salida = []
    for texto, es_titulo in filas:
        for rx, p in patrones_personas:
            if rx.search(texto):
                texto, n = rx.subn(codigo(p, "P"), texto)
                cuenta["personas"] += n
        texto, n = re.subn(r"[\w\.\-+]+@[\w\-]+\.[\w\.\-]+", "[CORREO]", texto)
        cuenta["correos"] += n
        texto, n = re.subn(r"(?:\+51\s?)?\b9\d{2}\s?\d{3}\s?\d{3}\b", "[TELEFONO]", texto)
        cuenta["telefonos"] += n
        texto, n = re.subn(r"\b\d{8}\b", "[DNI/CODIGO]", texto)
        cuenta["dni_o_codigos"] += n

        def emp(m):
            cuenta["empresas_o_minas"] += 1
            return codigo(m.group(0), "E")

        texto = re.sub(EMPRESA, emp, texto)
        salida.append((texto, es_titulo))
    return salida, tabla, cuenta


def extraer(filas):
    """Índice completo y solo las secciones útiles para revisar estructura y coherencia."""
    indice = [t for t, h in filas if h]
    partes, actual, largo = [], None, 0
    for t, h in filas:
        if h:
            actual = t if SECCIONES.search(t) and not re.search(r"marco|antecedente", t, re.I) else None
            largo = 0
            if actual:
                partes.append(f"\n## {t}\n")
            continue
        if actual:
            es_ref = re.search(r"referencia|bibliograf", actual, re.I)
            tope = 10**9 if es_ref else MAX_SECCION
            if largo < tope:
                partes.append(t)
                largo += len(t)
    refs = [p for p in partes if not p.startswith("\n## ")]
    return indice, partes, len(refs)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("original", help="ruta del .docx o .pdf (fuera de la carpeta del curso)")
    ap.add_argument("--salida", help="carpeta del extracto (por defecto tesis_anonimizadas/)")
    a = ap.parse_args(argv)

    original = Path(a.original).expanduser().resolve()
    if not original.is_file():
        sys.exit("No se encontró el archivo. Copia la ruta con clic derecho → «Copiar como ruta».")
    if RAIZ in original.parents and a.salida is None:
        print("AVISO: el original está DENTRO de la carpeta del curso. Muévelo a Documentos\\Tesis privadas.")

    filas = leer(original)
    if not filas:
        sys.exit("El archivo no tiene texto (¿PDF escaneado?). Pide la versión en Word.")

    lista = original.parent / "nombres.txt"
    extra = [l.strip() for l in lista.read_text(encoding="utf-8").splitlines() if l.strip()] if lista.exists() else []
    filas_anon, tabla, cuenta = anonimizar(filas, buscar_personas(filas, extra))
    indice, partes, n_lineas = extraer(filas_anon)

    cod = "T" + hashlib.sha1(str(original).encode()).hexdigest()[:6]
    destino = Path(a.salida) if a.salida else RAIZ / "tesis_anonimizadas"
    destino.mkdir(parents=True, exist_ok=True)
    extracto = destino / f"{cod}_extracto.md"
    extracto.write_text(
        f"# Extracto anonimizado {cod}\n\n"
        "Generado en la computadora del docente. Personas = P01…, empresas y minas = E01…\n\n"
        "## Índice detectado\n\n" + "\n".join(f"- {t}" for t in indice) + "\n" + "\n".join(partes) + "\n",
        encoding="utf-8",
    )
    with open(original.parent / f"{original.stem}_codigos.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["codigo", "original"])
        w.writerows(sorted(tabla.values()))

    print(f"Párrafos leídos: {len(filas)}")
    for k, v in cuenta.items():
        print(f"Reemplazos de {k.replace('_', ' ')}: {v}")
    print(f"Títulos en el índice: {len(indice)} | Líneas en el extracto: {n_lineas}")
    print(f"Extracto: {extracto.relative_to(RAIZ) if RAIZ in extracto.parents else extracto.name}")
    print("La tabla de códigos quedó junto al original. No la abras con el agente.")
    return extracto


if __name__ == "__main__":
    main()
