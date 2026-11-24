"""Carga un CSV con encabezado en una tabla de ClickHouse y muestra cuántas filas quedaron.

  docker compose run --rm herramientas cargar.py ventas_crudas datos/ventas-sucio.csv
"""
import sys

import ch

if len(sys.argv) != 3:
    sys.exit(__doc__)
tabla, archivo = sys.argv[1:]
ch.esperar()
antes = int(ch.valor(f"SELECT count() FROM {tabla}"))
ch.insertar_csv(tabla, archivo)
despues = int(ch.valor(f"SELECT count() FROM {tabla}"))
print(f"{archivo} → {tabla}: {despues - antes} filas nuevas ({despues} en total)")
