"""Conexión a ClickHouse por su API HTTP. La usan todos los scripts.

Lee la conexión de las variables de entorno que pone docker-compose.yml desde tu archivo .env:
  CH_HOST (clickhouse), CH_USER (taller), CH_PASSWORD (taller123)
"""
import base64
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(RAIZ, "datos")
SALIDA = os.path.join(RAIZ, "salida")
HOST = os.environ.get("CH_HOST", "clickhouse")
USUARIO = os.environ.get("CH_USER", "taller")
CLAVE = os.environ.get("CH_PASSWORD", "taller123")


class ErrorCH(Exception):
    pass


def _pedir(cuerpo, params=None, usuario=None, clave=None):
    url = f"http://{HOST}:8123/"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    par = f"{usuario or USUARIO}:{CLAVE if clave is None else clave}"
    req = urllib.request.Request(url, data=cuerpo, headers={
        "Authorization": "Basic " + base64.b64encode(par.encode()).decode()})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        raise ErrorCH(e.read().decode("utf-8", "replace").strip()) from None


def ejecutar(sql, **kw):
    """Ejecuta una sentencia y devuelve el texto que responde ClickHouse."""
    return _pedir(sql.encode("utf-8"), **kw)


def consultar(sql, **kw):
    """Ejecuta un SELECT y devuelve una lista de diccionarios."""
    return json.loads(_pedir((sql + "\nFORMAT JSON").encode("utf-8"), **kw))["data"]


def valor(sql, **kw):
    return ejecutar(sql, **kw).strip()


def insertar_csv(tabla, ruta):
    """Carga un CSV con encabezado en una tabla (INSERT … FORMAT CSVWithNames)."""
    with open(ruta, "rb") as f:
        _pedir(f.read(), params={"query": f"INSERT INTO {tabla} FORMAT CSVWithNames"})


def esperar(segundos=60):
    """Espera a que ClickHouse responda (al arrancar tarda unos segundos)."""
    for _ in range(segundos):
        try:
            urllib.request.urlopen(f"http://{HOST}:8123/ping", timeout=2).read()
            return
        except Exception:
            time.sleep(1)
    raise SystemExit(f"ClickHouse no responde en http://{HOST}:8123. ¿Corriste «docker compose up -d»?")


def ruta(*partes):
    """Ruta dentro del proyecto; crea la carpeta salida/ si hace falta."""
    os.makedirs(SALIDA, exist_ok=True)
    return os.path.join(RAIZ, *partes)
