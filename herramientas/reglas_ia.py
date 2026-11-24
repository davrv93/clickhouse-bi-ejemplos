"""Pide a DeepSeek reglas de limpieza a partir del PERFIL de la tabla (nunca de los datos).

  docker compose run --rm herramientas reglas_ia.py salida/perfil-sql.json prompts/04-reglas-sql.txt salida/reglas-sql.json
  docker compose run --rm herramientas reglas_ia.py salida/perfil.json prompts/07-reglas.txt salida/reglas-ia.json

Necesita DEEPSEEK_API_KEY en tu archivo .env. Si no la tienes, no pasa nada: el repositorio trae las
reglas que propuso la IA en el curso, ya revisadas (datos/reglas-sql.json y datos/reglas-ia.json).
A DeepSeek solo le llegan el prompt y el perfil (conteos y valores distintos), no tus filas.
Revisa siempre las reglas antes de aplicarlas: la IA propone y tú decides.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

if len(sys.argv) != 4:
    sys.exit(__doc__)
perfil, prompt, salida = sys.argv[1:]
clave = os.environ.get("DEEPSEEK_API_KEY", "").strip()
if not clave:
    sys.exit("No hay DEEPSEEK_API_KEY en tu .env. Usa las reglas ya revisadas que trae el repositorio\n"
             "(datos/reglas-sql.json y datos/reglas-ia.json) o agrega tu llave y vuelve a intentar.")
modelo = os.environ.get("DEEPSEEK_MODEL", "deepseek-flash")
texto = open(prompt, encoding="utf-8").read().strip() + "\n\nPERFIL:\n" + open(perfil, encoding="utf-8").read()
cuerpo = {"model": modelo, "temperature": 0, "thinking": {"type": "disabled"},
          "response_format": {"type": "json_object"}, "messages": [{"role": "user", "content": texto}]}
req = urllib.request.Request("https://api.deepseek.com/chat/completions", data=json.dumps(cuerpo).encode(),
                             headers={"Authorization": "Bearer " + clave, "Content-Type": "application/json"})
t = time.time()
try:
    d = json.load(urllib.request.urlopen(req, timeout=180))
except urllib.error.HTTPError as e:
    sys.exit(f"DeepSeek respondió {e.code}: {e.read().decode('utf-8', 'replace')[:300]}")
reglas = json.loads(d["choices"][0]["message"]["content"])
os.makedirs(os.path.dirname(salida) or ".", exist_ok=True)
json.dump(reglas, open(salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"DeepSeek ({d.get('model')}) propuso {len(reglas.get('reglas', []))} reglas en {time.time() - t:.1f} s → {salida}")
for x in reglas.get("reglas", []):
    print(f"  {x.get('id')} {x.get('columna')}: {x.get('regla')}")
