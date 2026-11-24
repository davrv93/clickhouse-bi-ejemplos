-- Video 12 · Refresco automático
-- Un resumen por mes, sede y categoría que ClickHouse recalcula solo cada minuto.
-- vxm = venta × margen y vcm = venta con margen: con ellos el tablero saca el margen ponderado.
CREATE MATERIALIZED VIEW IF NOT EXISTS resumen_mensual
REFRESH EVERY 1 MINUTE
ENGINE = MergeTree ORDER BY (mes, sede, categoria) AS
SELECT mes, sede, categoria, sum(v) AS venta, sum(u) AS unidades,
       sum(vxm) AS vxm, sum(vcm) AS vcm
FROM (SELECT toStartOfMonth(fecha) AS mes, sede, categoria, venta AS v, unidades AS u,
             if(margen IS NULL, 0, venta * margen) AS vxm, if(margen IS NULL, 0, venta) AS vcm
      FROM ventas_tablero)
GROUP BY mes, sede, categoria;
