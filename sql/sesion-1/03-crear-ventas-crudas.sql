-- Video 3 · Cargar CSV y Excel con tipos correctos
-- La fecha queda como String porque llega en dos formatos (aaaa-mm-dd y dd/mm/aaaa).
-- El video 4 la convierte a Date.
CREATE TABLE IF NOT EXISTS ventas_crudas (
  fecha     String,
  sede      LowCardinality(String),
  categoria LowCardinality(String),
  unidades  UInt32,
  venta     Decimal(12, 2),
  margen    Nullable(Decimal(6, 3))
) ENGINE = MergeTree ORDER BY tuple();

-- Una tabla con la misma forma para las ventas que llegan en Excel.
CREATE TABLE IF NOT EXISTS ventas_excel AS ventas_crudas;
