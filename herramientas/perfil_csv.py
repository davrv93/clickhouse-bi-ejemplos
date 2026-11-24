"""Perfil de salida/juntos.csv: conteos, formatos y valores distintos. NO incluye filas (es lo que ve la IA, video 7).

  docker compose run --rm herramientas perfil_csv.py
Escribe salida/perfil.json.
"""
import collections
import csv
import json
import re

import ch

filas = list(csv.DictReader(open(ch.ruta("salida", "juntos.csv"), encoding="utf-8")))
COLS = ["fecha", "sede", "categoria", "unidades", "venta", "margen"]
fmt = collections.Counter("aaaa-mm-dd" if re.fullmatch(r"\d{4}-\d{2}-\d{2}", f["fecha"]) else
                          "dd/mm/aaaa" if re.fullmatch(r"\d{2}/\d{2}/\d{4}", f["fecha"]) else "otro" for f in filas)
num = lambda c: [float(f[c]) for f in filas if f[c].strip()]
p = {"filas": len(filas), "columnas": COLS,
     "origenes": dict(collections.Counter(f["origen"].split(" [")[0] for f in filas)),
     "fecha_formatos": dict(fmt),
     "sede_valores": {repr(k): v for k, v in collections.Counter(f["sede"] for f in filas).most_common()},
     "categoria_valores": {repr(k): v for k, v in collections.Counter(f["categoria"] for f in filas).most_common()},
     "vacios": {c: sum(1 for f in filas if not f[c].strip()) for c in COLS},
     "filas_identicas_repetidas": len(filas) - len({tuple(f[c].strip().lower() for c in COLS) for f in filas}),
     "rangos": {c: [min(num(c)), max(num(c))] for c in ("unidades", "venta", "margen")}}
json.dump(p, open(ch.ruta("salida", "perfil.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(p, ensure_ascii=False, indent=1))
print("\n→ salida/perfil.json")
