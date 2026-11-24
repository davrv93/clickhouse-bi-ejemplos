"""Arma con las reglas de la IA un CREATE TABLE … AS SELECT y lo ejecuta: ventas_crudas → ventas_limpia (video 4).

  docker compose run --rm herramientas aplicar_sql.py
  docker compose run --rm herramientas aplicar_sql.py --correccion datos/correccion-humana.json
  docker compose run --rm herramientas aplicar_sql.py --reglas salida/reglas-sql.json

--reglas      archivo de reglas (por defecto datos/reglas-sql.json, las del curso ya revisadas)
--correccion  reemplaza la expresión de las columnas que corrigió la revisión humana
"""
import json
import sys

import ch

args = sys.argv[1:]
def opcion(nombre, defecto=None):
    return args[args.index(nombre) + 1] if nombre in args else defecto

reglas = json.load(open(opcion("--reglas", "datos/reglas-sql.json"), encoding="utf-8"))["reglas"]
corr = json.load(open(opcion("--correccion"), encoding="utf-8")) if "--correccion" in args else {}
COLS = ["fecha", "sede", "categoria", "unidades", "venta", "margen"]
expr = {c: c for c in COLS}
distinct = False
for r in reglas:
    if r["sql"].strip().upper() == "DISTINCT":
        distinct = True
    elif r["columna"] in expr:
        expr[r["columna"]] = r["sql"]
expr.update(corr)
sel = ",\n  ".join(f"{expr[c]} AS {c}" if expr[c] != c else c for c in COLS)
sql = (f"CREATE OR REPLACE TABLE ventas_limpia ENGINE = MergeTree ORDER BY (sede, fecha) AS\n"
       f"SELECT {'DISTINCT ' if distinct else ''}\n  {sel}\nFROM ventas_crudas")
print(sql)
ch.esperar()
ch.ejecutar(sql)
print(f"\nOk. → ventas_limpia ({ch.valor('SELECT count() FROM ventas_limpia')} filas)"
      + (f"  · corregidas a mano: {', '.join(corr)}" if corr else ""))
