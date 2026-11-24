-- Video 8 · Después de cargar salida/limpio.csv en ventas_tablero.
SELECT count() AS filas, sum(venta) AS venta FROM ventas_tablero;

-- Una partición por mes.
SELECT partition AS mes, sum(rows) AS filas,
  formatReadableSize(sum(data_compressed_bytes)) AS en_disco
FROM system.parts WHERE table = 'ventas_tablero' AND active
GROUP BY partition ORDER BY partition;

-- Cuánto comprime.
SELECT sum(rows) AS filas,
  formatReadableSize(sum(data_uncompressed_bytes)) AS sin_comprimir,
  formatReadableSize(sum(data_compressed_bytes)) AS en_disco,
  round(sum(data_uncompressed_bytes) / sum(data_compressed_bytes), 1) AS veces
FROM system.parts WHERE table = 'ventas_tablero' AND active;

-- Cuántos bloques lee una consulta que filtra por sede y fecha (mira «Granules»).
EXPLAIN indexes = 1
SELECT sum(venta) FROM ventas_tablero WHERE sede = 'Surco' AND fecha >= '2026-10-01';
