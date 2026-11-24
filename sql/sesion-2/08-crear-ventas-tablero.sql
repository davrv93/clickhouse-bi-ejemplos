-- Video 8 · Modelar las tablas en ClickHouse
-- PARTITION BY: una parte por mes. ORDER BY: el orden en que el tablero filtra (sede, categoría, fecha).
CREATE TABLE IF NOT EXISTS ventas_tablero (
  fecha     Date,
  sede      LowCardinality(String),
  categoria LowCardinality(String),
  unidades  UInt32,
  venta     Decimal(12, 2),
  margen    Nullable(Decimal(6, 3))
) ENGINE = MergeTree
PARTITION BY toYYYYMM(fecha)
ORDER BY (sede, categoria, fecha);
