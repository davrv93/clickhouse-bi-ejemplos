"""Punto de entrada del contenedor «herramientas».

  docker compose run --rm herramientas <script.py> [argumentos]

Ejecuta herramientas/<script.py> del proyecto (montado en /taller). Sin argumentos, lista los scripts.
"""
import os
import runpy
import sys

CARPETA = "/taller/herramientas"
if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "ayuda"):
    print("Uso: docker compose run --rm herramientas <script.py> [argumentos]\n\nScripts:")
    for f in sorted(os.listdir(CARPETA)):
        if f.endswith(".py") and f not in ("ch.py", "lanzar.py"):
            doc = (open(os.path.join(CARPETA, f), encoding="utf-8").read().split('"""') + ["", ""])[1]
            print(f"  {f:18s} {doc.strip().splitlines()[0] if doc.strip() else ''}")
    sys.exit(0)
script = os.path.join(CARPETA, os.path.basename(sys.argv[1]))
if not os.path.isfile(script):
    sys.exit(f"No existe herramientas/{sys.argv[1]}. Escribe «docker compose run --rm herramientas» para ver la lista.")
sys.path.insert(0, CARPETA)
os.chdir("/taller")
sys.argv = [script] + sys.argv[2:]
runpy.run_path(script, run_name="__main__")
