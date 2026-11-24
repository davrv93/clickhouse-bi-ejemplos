-- Video 9 · Las 5 consultas clave del tablero

-- 1. KPIs: venta, unidades y margen ponderado por venta (sin contar los márgenes vacíos).
SELECT sum(venta) AS venta_total, sum(unidades) AS unidades_total,
  round(sumIf(venta * margen, margen IS NOT NULL)
      / sumIf(venta, margen IS NOT NULL) * 100, 1) AS margen_pct
FROM ventas_tablero;

-- 2. Venta por mes (el gráfico de línea).
SELECT toStartOfMonth(fecha) AS mes, sum(venta) AS venta
FROM ventas_tablero GROUP BY mes ORDER BY mes;

-- 3. Venta por sede y su participación.
SELECT sede, sum(venta) AS total,
  round(toFloat64(total) / (SELECT toFloat64(sum(venta)) FROM ventas_tablero) * 100, 1) AS pct
FROM ventas_tablero GROUP BY sede ORDER BY total DESC;

-- 4. Lo más vendido por sede y categoría.
SELECT sede, categoria, sum(venta) AS venta
FROM ventas_tablero GROUP BY sede, categoria
ORDER BY venta DESC LIMIT 5;

-- 5. Alerta: sedes que cayeron más de 15 % frente al mes anterior.
SELECT sede, mes, venta, anterior,
  round((toFloat64(venta) - anterior) / anterior * 100, 1) AS var_pct
FROM (SELECT sede, mes, venta,
        lagInFrame(toFloat64(venta)) OVER (PARTITION BY sede ORDER BY mes) AS anterior
      FROM (SELECT sede, toStartOfMonth(fecha) AS mes, sum(venta) AS venta
            FROM ventas_tablero GROUP BY sede, mes))
WHERE anterior > 0 AND var_pct < -15;
