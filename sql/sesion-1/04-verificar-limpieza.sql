-- Video 4 · Después de aplicar las reglas: categorías unificadas y el total que cuadra.
SELECT categoria, count() AS filas FROM ventas_limpia
GROUP BY categoria ORDER BY categoria;

-- La venta limpia debe ser la cruda menos lo que sumaban las filas repetidas.
SELECT antes, duplicados, despues,
  if(antes - duplicados = despues, 'CUADRA', 'NO CUADRA') AS control
FROM (SELECT
  (SELECT sum(venta) FROM ventas_crudas) AS antes,
  (SELECT sum((c - 1) * venta) FROM (SELECT *, count() AS c
     FROM ventas_crudas GROUP BY ALL HAVING c > 1)) AS duplicados,
  (SELECT sum(venta) FROM ventas_limpia) AS despues);
