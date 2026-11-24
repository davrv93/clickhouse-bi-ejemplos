-- Video 13 · Publicar o compartir sin regalar tu clave
-- Un usuario que solo puede leer el resumen. Cambia 'lector2026' por una clave tuya.
--
-- ¿Por qué readonly = 2 y no 1? El tablero pide un ajuste en cada consulta (add_http_cors_header).
-- Con readonly = 1 ClickHouse no deja cambiar ningún ajuste y responde «Code: 164 … (READONLY)».
-- Con readonly = 2 sí deja cambiar ajustes, pero sigue sin dejar escribir.
CREATE USER IF NOT EXISTS lector IDENTIFIED BY 'lector2026' SETTINGS readonly = 2;
GRANT SELECT ON default.resumen_mensual TO lector;
