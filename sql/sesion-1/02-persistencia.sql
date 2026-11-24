-- Video 2 · Tu primer contenedor y la persistencia
-- Crea una tabla pequeña. Luego borra y recrea el contenedor (ver README): la fila sigue ahí
-- porque los datos viven en el volumen, no en el contenedor.
CREATE TABLE IF NOT EXISTS notas (id UInt8, texto String) ENGINE = MergeTree ORDER BY id;
INSERT INTO notas VALUES (1, 'sigo aquí después del borrado');
SELECT * FROM notas;
