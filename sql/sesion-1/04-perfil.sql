-- Video 4 · Lo que está mal en los datos crudos, en una sola consulta.
SELECT count() AS filas,
  countIf(position(fecha, '/') > 0) AS fechas_dd_mm,
  uniqExact(sede) AS sedes, uniqExact(categoria) AS categorias,
  countIf(margen IS NULL) AS margen_vacio,
  count() - (SELECT count() FROM (SELECT DISTINCT * FROM ventas_crudas)) AS repetidas
FROM ventas_crudas;
