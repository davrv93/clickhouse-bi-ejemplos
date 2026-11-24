-- Video 12 · Una venta de prueba en noviembre. Ejecuta este archivo, espera hasta un minuto
-- y ejecuta 12-ver-refresco.sql: la fila aparece en el resumen sin que hagas nada.
INSERT INTO ventas_tablero VALUES ('2026-11-02', 'Surco', 'Bebés', 10, 450.00, 0.300);
SELECT count() AS filas_noviembre_en_resumen FROM resumen_mensual WHERE mes = '2026-11-01';
