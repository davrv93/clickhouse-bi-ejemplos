-- Video 11 · La alerta del tablero para un mes concreto: junio frente a mayo, sede por sede.
SELECT sede, mes, venta, anterior,
  round((toFloat64(venta) - anterior) / anterior * 100, 1) AS var_pct
FROM (SELECT sede, mes, venta,
        lagInFrame(toFloat64(venta)) OVER (PARTITION BY sede ORDER BY mes) AS anterior
      FROM (SELECT sede, toStartOfMonth(fecha) AS mes, sum(venta) AS venta
            FROM ventas_tablero GROUP BY sede, mes))
WHERE mes = '2026-06-01' ORDER BY var_pct;
