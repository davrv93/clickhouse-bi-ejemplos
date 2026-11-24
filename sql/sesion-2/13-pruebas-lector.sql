-- Video 13 · Tres pruebas. Ejecútalo como lector:
--   docker compose run --rm herramientas sql.py sql/sesion-2/13-pruebas-lector.sql --usuario lector --clave lector2026 --seguir
-- Lo esperado: la 1 responde; la 2 y la 3 fallan con ACCESS_DENIED.

-- 1) Leer el resumen: permitido.
SELECT count() AS filas FROM resumen_mensual;

-- 2) Leer el detalle de ventas: no tiene permiso.
SELECT count() FROM ventas_tablero;

-- 3) Escribir en el resumen: no tiene permiso.
INSERT INTO resumen_mensual (mes) VALUES ('2026-12-01');
