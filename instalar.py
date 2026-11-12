"""Instala la carpeta Mi curso, las tesis de práctica, los complementos de Python y el hook de Antigravity.

Lo ejecuta instalar.ps1 después de descargar el material de GitHub. No borra ni reemplaza nada tuyo: si ya tienes Mi curso,
solo agrega lo que falte (skills y plantillas nuevas).
Pruebas:  py instalar.py --documentos <carpeta> --inicio <carpeta>
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
HOOK_NOMBRE = "kit-docente-ia"


def carpeta_documentos():
    r = subprocess.run(["powershell", "-NoProfile", "-Command", "[Environment]::GetFolderPath('MyDocuments')"],
                       capture_output=True, text=True)
    ruta = r.stdout.strip()
    return Path(ruta) if ruta else Path.home() / "Documents"


def copiar_sin_pisar(origen, destino):
    """Copia lo que falte. Nunca reemplaza un archivo que ya existe."""
    nuevos = 0
    for f in origen.rglob("*"):
        if f.is_file() and "__pycache__" not in f.parts:
            d = destino / f.relative_to(origen)
            if not d.exists():
                d.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, d)
                nuevos += 1
    return nuevos


def instalar_hook(inicio, hook):
    ruta = inicio / ".gemini" / "config" / "hooks.json"
    ruta.parent.mkdir(parents=True, exist_ok=True)
    datos = {}
    if ruta.exists():
        datos = json.loads(ruta.read_text(encoding="utf-8") or "{}")
        respaldo = ruta.with_name("hooks.antes-kit.json")
        if not respaldo.exists():
            shutil.copy2(ruta, respaldo)
    # quita el registro anterior de este mismo hook (con otro nombre) para que no corra dos veces
    for k in [k for k, v in datos.items() if "hook_proteger.py" in json.dumps(v)]:
        del datos[k]
    datos[HOOK_NOMBRE] = {"PreToolUse": [{"matcher": "*", "hooks": [
        {"type": "command", "command": f'"{sys.executable}" "{hook}"', "timeout": 30}]}]}
    ruta.write_text(json.dumps(datos, indent=2, ensure_ascii=False), encoding="utf-8")
    return ruta


def paso(n, texto):
    print(f"\n[{n}/5] {texto}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--documentos")
    ap.add_argument("--inicio")
    ap.add_argument("--sin-pip", action="store_true")
    ap.add_argument("--sin-pausa", action="store_true")
    a = ap.parse_args()
    docs = (Path(a.documentos) if a.documentos else carpeta_documentos()).resolve()
    inicio = Path(a.inicio) if a.inicio else Path.home()
    mc = docs / "Mi curso"
    print("Kit docente IA · instalación de la carpeta Mi curso")
    print(f"Tu carpeta Documentos: {docs}")

    paso(1, "Carpeta Mi curso y plantillas")
    existia = mc.exists()
    n = copiar_sin_pisar(KIT / "Mi curso", mc)
    print(f"   {'Ya existía: se agregaron' if existia else 'Creada con'} {n} archivos. No se reemplazó nada tuyo.")
    extras = docs / "Kit docente IA"
    for n_ in ["Plantillas Word", "Plantilla PowerPoint"]:
        copiar_sin_pisar(KIT / n_, extras / n_)
    for f in KIT.glob("*.docx"):
        if not (extras / f.name).exists():
            shutil.copy2(f, extras / f.name)
    print(f"   Plantillas Word, PowerPoint y la guía del agente en: {extras}")

    paso(2, "Carpeta Tesis privadas (fuera de Mi curso)")
    n = copiar_sin_pisar(KIT / "Para Tesis privadas", docs / "Tesis privadas")
    print(f"   Lista ({n} archivos de práctica agregados).")

    paso(3, "Complementos de Python para Word y PDF")
    if a.sin_pip:
        print("   Omitido (modo de prueba).")
    else:
        r = subprocess.run([sys.executable, "-m", "pip", "install", "-q", "python-docx", "pypdf"])
        print("   Listos." if r.returncode == 0 else "   FALLÓ: revisa tu internet y vuelve a ejecutar.")

    paso(4, "Hook de Antigravity (el detector de gases de tu carpeta)")
    hook = mc / "herramientas" / "hook_proteger.py"
    ruta = instalar_hook(inicio, hook)
    r = subprocess.run([sys.executable, str(hook), "--probar"], capture_output=True, text=True)
    print(f"   Instalado en {ruta}")
    print(f"   {r.stdout.strip() or 'La prueba del hook no respondió'}")

    paso(5, "Prueba completa de la carpeta")
    if a.sin_pip:
        print("   Omitida (modo de prueba).")
        ok = r.returncode == 0
    else:
        p = subprocess.run([sys.executable, str(mc / "herramientas" / "probar_todo.py")], cwd=mc)
        ok = r.returncode == 0 and p.returncode == 0

    print("\n" + ("TODO EN ORDEN." if ok else "HUBO UN PROBLEMA: toma una captura de esta ventana y envíasela al facilitador."))
    print("Ahora abre Antigravity, abre la carpeta Mi curso y revisa en Customizations > Hooks que aparezca "
          f"«{HOOK_NOMBRE}».")
    return 0 if ok else 1


if __name__ == "__main__":
    codigo = main()
    if "--documentos" not in sys.argv and "--sin-pausa" not in sys.argv:
        input("\nPulsa Enter para cerrar.")
    sys.exit(codigo)
