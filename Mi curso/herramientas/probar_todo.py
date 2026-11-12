"""Prueba que la carpeta funciona en esta computadora. Uso:  py herramientas/probar_todo.py

Usa una tesis inventada en una carpeta temporal; no toca tus archivos.
"""
import importlib.util
import tempfile
from pathlib import Path

import docx

RAIZ = Path(__file__).resolve().parents[1]
FALSOS = ["Rosa Elvira Huamaní Cárdenas", "Teodoro Quispe Llamocca", "45871236", "rhuamani@ejemplo.pe",
          "987 654 321", "Los Andes Altos", "Santa Victoria"]


def cargar(ruta):
    spec = importlib.util.spec_from_file_location(ruta.stem, ruta)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def tesis_falsa(ruta):
    d = docx.Document()
    for t in ["UNIVERSIDAD NACIONAL DE EJEMPLO", "TESIS",
              "Presentado por:", "Bach. Rosa Elvira Huamaní Cárdenas", "Asesor: Ing. Teodoro Quispe Llamocca",
              "DNI 45871236 – rhuamani@ejemplo.pe – 987 654 321"]:
        d.add_paragraph(t)
    d.add_heading("RESUMEN", 1)
    d.add_paragraph("Se evaluó la ventilación de la Unidad Minera Santa Victoria de la Compañía Minera Los Andes Altos S.A.C.")
    d.add_heading("1.2 Formulación del problema", 2)
    d.add_paragraph("¿Cuál es el caudal requerido en el nivel 3900?")
    d.add_heading("1.3 Objetivos", 2)
    d.add_paragraph("Determinar el caudal de aire requerido.")
    d.add_heading("2.1 Marco teórico", 2)
    d.add_paragraph("TEXTO QUE NO DEBE SALIR EN EL EXTRACTO")
    d.add_heading("CONCLUSIONES", 1)
    d.add_paragraph("El caudal requerido es 85 m3/s. Agradezco a Rosa Elvira Huamaní Cárdenas.")
    d.add_heading("REFERENCIAS", 1)
    d.add_paragraph("McPherson, M. J. (1993). Subsurface ventilation and environmental engineering. Chapman & Hall.")
    d.save(str(ruta))


def main():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        original = tmp / "Tesis Rosa Huamani.docx"
        tesis_falsa(original)
        pt = cargar(RAIZ / ".agents/skills/proteger-datos/scripts/preparar_tesis.py")
        extracto = pt.main([str(original), "--salida", str(tmp / "anon")])
        texto = extracto.read_text(encoding="utf-8")
        for f in FALSOS:
            assert f not in texto, f"Quedó un dato personal en el extracto: {f!r}"
        assert "Rosa" not in extracto.name, "El nombre del archivo del extracto lleva el nombre del alumno"
        assert "P01" in texto and "E01" in texto, "No se pusieron códigos"
        assert "Determinar el caudal" in texto and "McPherson" in texto, "Faltan secciones en el extracto"
        assert "NO DEBE SALIR" not in texto, "El marco teórico no debe ir en el extracto"
        assert (tmp / "Tesis Rosa Huamani_codigos.csv").exists(), "Falta la tabla de códigos junto al original"

        md = tmp / "borrador.md"
        md.write_text("# Sesión de prueba\n\n## I. Datos\n\n| Dato | Detalle |\n|---|---|\n| Ciclo | VII |\n\n"
                      "- viñeta con **negrita**\n1. paso uno\n", encoding="utf-8")
        mw = cargar(RAIZ / "herramientas/md_a_word.py")
        salida = mw.main([str(md), "--salida", str(tmp / "prueba.docx")])
        d = docx.Document(str(salida))
        todo = "\n".join(p.text for p in d.paragraphs)
        assert "{{" not in todo, "Quedó una marca {{…}} de la plantilla"
        assert "Sesión de prueba" in todo and d.tables[-1].cell(1, 1).text == "VII", "El Word no tiene el contenido"

        wt = cargar(RAIZ / "herramientas/word_a_texto.py")
        assert "paso uno" in wt.convertir(salida).read_text(encoding="utf-8")
    print("\nTodo en orden: el anonimizador y la conversión a Word funcionan en esta computadora.")


if __name__ == "__main__":
    main()
