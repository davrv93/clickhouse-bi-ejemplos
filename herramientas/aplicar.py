"""Aplica las reglas de la IA a salida/juntos.csv y escribe salida/limpio.csv, con un acta que concilia el total (video 7).

  docker compose run --rm herramientas aplicar.py
  docker compose run --rm herramientas aplicar.py --reglas salida/reglas-ia.json

--reglas          archivo de reglas (por defecto datos/reglas-ia.json, las del curso ya revisadas)
--sin-correccion  aplica la regla de mayúsculas tal como la propuso la IA, sin la corrección humana
"""
import collections, csv, json, re, sys
import ch
a = sys.argv[1:]
reglas = json.load(open(a[a.index("--reglas") + 1] if "--reglas" in a else "datos/reglas-ia.json", encoding="utf-8"))["reglas"]
filas = list(csv.DictReader(open(ch.ruta("salida", "juntos.csv"), encoding="utf-8")))
COLS = ["fecha", "sede", "categoria", "unidades", "venta", "margen"]
corregir = "--sin-correccion" not in sys.argv
n0, total0 = len(filas), sum(float(f["venta"]) for f in filas)
print(f"Antes: {n0} filas · venta S/ {total0:,.2f}")

def titulo(v):
    return " ".join(p.capitalize() for p in v.split())

canon = {}
for c in ("sede", "categoria"):               # la forma más frecuente de cada valor, para validar la regla de la IA
    cnt = collections.Counter(f[c].strip() for f in filas)
    for v, _ in cnt.most_common():
        canon.setdefault((c, v.lower()), v)

for r in sorted(reglas, key=lambda r: r["accion"] == "quitar_duplicados"):   # duplicados al final, ya normalizado
    a, col = r["accion"], r["columna"]
    if a == "convertir_fecha":
        k = 0
        for f in filas:
            m = re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", f["fecha"])
            if m: f["fecha"] = f"{m[3]}-{m[2]}-{m[1]}"; k += 1
        print(f"{r['id']} fecha: {k} fechas dd/mm/aaaa → aaaa-mm-dd")
    elif a == "recortar_y_capitalizar":
        antes = len({f[col] for f in filas})
        for f in filas:
            f[col] = titulo(f[col].strip())
            if corregir: f[col] = canon[(col, f[col].lower())]
        print(f"{r['id']} {col}: {antes} variantes → {len({f[col] for f in filas})} ({', '.join(sorted({f[col] for f in filas}))})")
    elif a == "dejar_vacio_como_nulo":
        print(f"{r['id']} {col}: {sum(1 for f in filas if not f[col].strip())} vacíos quedan como nulos (sin inventar)")
    elif a == "convertir_tipo":
        tipo = r["parametros"].get("tipo_destino")
        for f in filas:
            if f[col].strip(): f[col] = str(int(float(f[col]))) if tipo == "entero" else f[col]
        print(f"{r['id']} {col}: a {tipo}")
dups, vistos, salida, quitado = 0, set(), [], 0.0
for f in filas:
    k = tuple(f[c] for c in COLS)
    if k in vistos:
        dups += 1; quitado += float(f["venta"]); continue
    vistos.add(k); salida.append(f)
r4 = next(r for r in reglas if r["accion"] == "quitar_duplicados")
print(f"{r4['id']} duplicados: {dups} filas quitadas (S/ {quitado:,.2f})")
total1 = sum(float(f["venta"]) for f in salida)
print(f"Después: {len(salida)} filas · venta S/ {total1:,.2f}")
ok = abs(total0 - quitado - total1) < 0.01
print(f"Cuadre: {total0:,.2f} − {quitado:,.2f} = {total0 - quitado:,.2f} → {'CUADRA' if ok else 'NO CUADRA'}")
with open(ch.ruta("salida", "limpio.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=COLS, extrasaction="ignore"); w.writeheader(); w.writerows(salida)
print("→ salida/limpio.csv")
