-- Video 12 · Después del refresco (máximo 1 minuto): la venta de prueba ya está en el resumen.
SELECT mes, sede, categoria, venta FROM resumen_mensual WHERE mes = '2026-11-01';

-- Era una prueba: se borra. El resumen la quita en el siguiente refresco.
DELETE FROM ventas_tablero WHERE fecha = '2026-11-02';
