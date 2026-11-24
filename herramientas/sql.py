"""Ejecuta un archivo .sql en ClickHouse, sentencia por sentencia, y muestra cada resultado.

  docker compose run --rm herramientas sql.py sql/sesion-1/03-crear-ventas-crudas.sql
  docker compose run --rm herramientas sql.py sql/sesion-2/13-pruebas-lector.sql --usuario lector --clave lector2026 --seguir

--usuario/--clave  ejecuta como otro usuario (por defecto, el de tu .env)
--seguir           si una sentencia falla, muestra el error y sigue con la siguiente
"""
import re
import sys

import ch


def sentencias(texto):
    """Parte el archivo en sentencias por «;», sin cortar dentro de comillas ni comentarios."""
    partes, actual, i, n = [], [], 0, len(texto)
    while i < n:
        c = texto[i]
        if c in "'\"`":
            j = i + 1
            while j < n and texto[j] != c:
                j += 2 if texto[j] == "\\" else 1
            actual.append(texto[i:j + 1]); i = j + 1
        elif texto.startswith("--", i):
            j = texto.find("\n", i); j = n if j < 0 else j
            actual.append(texto[i:j]); i = j
        elif c == ";":
            partes.append("".join(actual)); actual = []; i += 1
        else:
            actual.append(c); i += 1
    partes.append("".join(actual))
    return [p.strip() for p in partes if re.sub(r"--[^\n]*", "", p).strip()]


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    opc = {"usuario": None, "clave": None}
    for k in opc:
        if f"--{k}" in args:
            i = args.index(f"--{k}"); opc[k] = args[i + 1]; del args[i:i + 2]
    seguir = "--seguir" in args
    archivo = [a for a in args if a != "--seguir"][0]
    ch.esperar()
    fallos = 0
    for s in sentencias(open(archivo, encoding="utf-8").read()):
        codigo = re.sub(r"--[^\n]*\n?", "", s).strip()
        print(":) " + "\n   ".join(codigo.splitlines()))
        es_consulta = re.match(r"(SELECT|WITH|SHOW|DESCRIBE|DESC|EXPLAIN|EXISTS)\b", codigo, re.I)
        if es_consulta and not re.search(r"\bFORMAT\s+\w+\s*$", codigo, re.I):
            codigo += "\nFORMAT PrettyCompactMonoBlock"
        try:
            r = ch.ejecutar(codigo, usuario=opc["usuario"], clave=opc["clave"])
            print(r.rstrip() if r.strip() else "Ok.")
        except ch.ErrorCH as e:
            fallos += 1
            print("Error: " + re.sub(r"\s*\(version .*$", "", str(e), flags=re.S).strip()[:500])
            if not seguir:
                sys.exit(1)
        print()
    if fallos:
        print(f"{fallos} sentencia(s) con error.")


if __name__ == "__main__":
    main()
