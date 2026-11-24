"""Perfil de una tabla de ClickHouse: conteos, formatos y valores distintos. NO incluye filas de datos.

Es lo único que se le manda a la IA (video 4).
  docker compose run --rm herramientas perfil_sql.py ventas_crudas
Escribe salida/perfil-sql.json.
"""
import json
import sys

import ch

T = sys.argv[1] if len(sys.argv) > 1 else "ventas_crudas"
q = ch.consultar
ch.esperar()
tipos = {c["name"]: c["type"] for c in q(f"DESCRIBE {T}")}
p = {"tabla": T, "motor": "ClickHouse 26", "filas": int(q(f"SELECT count() n FROM {T}")[0]["n"]), "tipos": tipos}
p["fecha_formatos"] = q(f"""SELECT multiIf(match(fecha, '^\\\\d{{4}}-\\\\d{{2}}-\\\\d{{2}}$'), 'aaaa-mm-dd',
    match(fecha, '^\\\\d{{2}}/\\\\d{{2}}/\\\\d{{4}}$'), 'dd/mm/aaaa', 'otro') AS formato, count() AS filas
    FROM {T} GROUP BY formato ORDER BY filas DESC""")
for c in ("sede", "categoria"):
    p[f"{c}_valores"] = {f"'{r['v']}'": int(r["n"]) for r in q(f"SELECT {c} AS v, count() AS n FROM {T} GROUP BY v ORDER BY n DESC")}
p["nulos"] = {c: int(q(f"SELECT countIf({c} IS NULL) n FROM {T}")[0]["n"]) for c in tipos}
p["filas_identicas_repetidas"] = int(q(f"SELECT (SELECT count() FROM {T}) - (SELECT count() FROM (SELECT DISTINCT * FROM {T})) AS n")[0]["n"])
p["rangos"] = q(f"SELECT min(unidades) u_min, max(unidades) u_max, min(venta) v_min, max(venta) v_max, min(margen) m_min, max(margen) m_max FROM {T}")[0]
destino = ch.ruta("salida", "perfil-sql.json")
json.dump(p, open(destino, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(p, ensure_ascii=False, indent=1))
print(f"\n→ salida/perfil-sql.json (sin filas de datos: es lo único que verá la IA)")
