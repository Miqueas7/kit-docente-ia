"""Hook de Antigravity (PreToolUse): el detector de gases de tu carpeta.

Antes de cada acción del agente revisa:
  - que los archivos y carpetas que toca estén dentro de Mi curso;
  - que no lea los archivos con nombres reales (_codigos.csv, nombres.txt);
  - que no toque Tesis privadas, salvo con el script de la skill proteger-datos;
  - que no use comandos que muestran documentos completos (type, cat, Get-Content...).
Responde {"decision": "allow"} o {"decision": "deny", "reason": ...}. Si algo falla, bloquea.

Lo instala instalar.py. Prueba:  py herramientas/hook_proteger.py --probar
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]  # la carpeta Mi curso
PROHIBIDOS = ("_codigos.csv", "nombres.txt")
VOLCADO = re.compile(r"(^|[\s;|&(])(type|cat|more|gc|get-content|select-string|findstr)(\s|$)", re.I)
PROTEGER = ".agents/skills/proteger-datos/scripts/preparar_tesis.py"


def dentro(ruta, cwd):
    p = Path(ruta)
    if not p.is_absolute():
        p = Path(cwd) / p
    try:
        p.resolve().relative_to(RAIZ)
        return True
    except ValueError:
        return False


def revisar(datos):
    """Devuelve el motivo del bloqueo, o None si se permite."""
    llamada = datos.get("toolCall") or {}
    nombre, args = llamada.get("name", ""), llamada.get("args") or {}
    cwd = args.get("Cwd") or str(RAIZ)
    textos = [str(v) for v in args.values() if isinstance(v, (str, int, float))]
    if any(p in t.lower() for t in textos for p in PROHIBIDOS):
        return "ese archivo guarda nombres reales y se queda en tu computadora"
    if nombre == "run_command":
        cmd = str(args.get("CommandLine", ""))
        es_proteger = PROTEGER in cmd.replace("\\", "/")
        if "tesis privadas" in cmd.lower() and not es_proteger:
            return "las tesis originales solo se tocan con la skill proteger-datos"
        if VOLCADO.search(cmd):
            return "no se usan comandos que muestran documentos completos"
        if not es_proteger and not dentro(cwd, RAIZ):
            return "el agente solo trabaja dentro de Mi curso"
        return None
    for clave, valor in args.items():
        if isinstance(valor, str) and valor and re.search(r"(Path|File|Directory|Cwd)$", clave):
            if not dentro(valor, cwd):
                return "el agente solo trabaja dentro de Mi curso"
    return None


def probar():
    afuera = str(Path.home() / "Documents" / "Tesis privadas" / "tesis.docx")
    adentro = str(RAIZ / "silabo" / "LEEME.md")
    casos = [
        ({"toolCall": {"name": "view_file", "args": {"AbsolutePath": adentro}}}, False),
        ({"toolCall": {"name": "view_file", "args": {"AbsolutePath": afuera}}}, True),
        ({"toolCall": {"name": "view_file", "args": {"AbsolutePath": str(RAIZ / "tesis_anonimizadas" / "x_codigos.csv")}}}, True),
        ({"toolCall": {"name": "list_dir", "args": {"DirectoryPath": str(Path.home())}}}, True),
        ({"toolCall": {"name": "run_command", "args": {"CommandLine": f'py {PROTEGER} "{afuera}"', "Cwd": str(RAIZ)}}}, False),
        ({"toolCall": {"name": "run_command", "args": {"CommandLine": f'Get-Content "{adentro}"', "Cwd": str(RAIZ)}}}, True),
        ({"toolCall": {"name": "run_command", "args": {"CommandLine": f'py herramientas/word_a_texto.py "{afuera}"', "Cwd": str(RAIZ)}}}, True),
        ({"toolCall": {"name": "run_command", "args": {"CommandLine": "py herramientas/probar_todo.py", "Cwd": str(RAIZ)}}}, False),
    ]
    fallas = sum((revisar(d) is not None) != bloquea for d, bloquea in casos)
    print(f"Hook: {len(casos) - fallas} de {len(casos)} pruebas correctas")
    return fallas == 0


if __name__ == "__main__":
    if "--probar" in sys.argv:
        sys.exit(0 if probar() else 1)
    try:
        motivo = revisar(json.load(sys.stdin))
    except Exception as e:  # ante la duda, bloquea
        motivo = f"el hook no pudo revisar la acción ({type(e).__name__})"
    salida = {"decision": "allow"} if motivo is None else {
        "decision": "deny", "reason": f"Bloqueado por el arnés de Mi curso: {motivo}."}
    print(json.dumps(salida))  # ASCII: se lee bien con cualquier codificación
