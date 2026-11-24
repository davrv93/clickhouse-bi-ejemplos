"""De los 3 archivos (Excel, PDF y Word) al tablero, en un solo comando (video 14).

  docker compose run --rm herramientas pipeline.py          usa las reglas ya revisadas (datos/reglas-ia.json)
  docker compose run --rm herramientas pipeline.py --ia     pide reglas nuevas a DeepSeek (necesita DEEPSEEK_API_KEY)

Antes debes haber creado ventas_tablero y resumen_mensual (sql/sesion-2/08 y 12).
"""
import io
import json
import os
import runpy
import sys
import time
from contextlib import redirect_stdout

import ch

T0 = time.time()
AQUI = os.path.dirname(os.path.abspath(__file__))


def correr(script, *args):
    """Ejecuta otro script del curso y devuelve lo que imprimió."""
    sys.argv = [script, *args]
    buf = io.StringIO()
    with redirect_stdout(buf):
        runpy.run_path(os.path.join(AQUI, script), run_name="__main__")
    return buf.getvalue().strip().splitlines()


def paso(nombre, detalle):
    print(f"▶ {nombre:34s} {detalle:46s} {time.time() - T0:6.1f} s")


ch.esperar()
for t in ("ventas_tablero", "resumen_mensual"):
    if ch.valor(f"EXISTS TABLE {t}") != "1":
        sys.exit(f"Falta {t}. Ejecuta antes sql/sesion-2/08-crear-ventas-tablero.sql y sql/sesion-2/12-resumen-mensual.sql.")
paso("1. extraer Excel, PDF y Word", correr("extraer.py")[-1].split("→")[0].replace("TOTAL", "").strip())
correr("perfil_csv.py")
paso("2. perfil (sin datos)", "salida/perfil.json")
reglas = "datos/reglas-ia.json"
if "--ia" in sys.argv:
    correr("reglas_ia.py", "salida/perfil.json", "prompts/07-reglas.txt", "salida/reglas-ia.json")
    reglas = "salida/reglas-ia.json"
    paso("3. reglas de DeepSeek", "salida/reglas-ia.json (revísalas)")
else:
    paso("3. reglas revisadas", f"{len(json.load(open(reglas, encoding='utf-8'))['reglas'])} reglas en {reglas}")
acta = correr("aplicar.py", "--reglas", reglas)
paso("4. aplicar y conciliar", next(l for l in acta if l.startswith("Cuadre")).replace("Cuadre: ", ""))
ch.ejecutar("TRUNCATE TABLE ventas_tablero")
ch.insertar_csv("ventas_tablero", ch.ruta("salida", "limpio.csv"))
paso("5. cargar en ventas_tablero", f"{ch.valor('SELECT count() FROM ventas_tablero')} filas")
ch.ejecutar("SYSTEM REFRESH VIEW resumen_mensual")
ch.ejecutar("SYSTEM WAIT VIEW resumen_mensual")
paso("6. refrescar resumen_mensual", f"{ch.valor('SELECT count() FROM resumen_mensual')} filas")
print("── verificación")
print(ch.ejecutar("SELECT (SELECT sum(venta) FROM ventas_tablero) AS tabla, (SELECT sum(venta) FROM resumen_mensual) AS resumen, "
                  "if(tabla = resumen, 'CUADRA', 'NO CUADRA') AS control FORMAT PrettyCompactMonoBlock").rstrip())
print(f"Abre el tablero: http://127.0.0.1:{os.environ.get('TABLERO_PUERTO', '8080')}")
