"""Pasa todas las hojas de un Excel a un CSV con encabezado (ClickHouse no lee .xlsx).

  docker compose run --rm herramientas excel_a_csv.py datos/archivos/ventas-lima-miraflores.xlsx salida/excel.csv

Escribe el archivo directamente: no uses «>» en PowerShell, que cambia la codificación.
"""
import csv
import os
import sys

from openpyxl import load_workbook

if len(sys.argv) != 3:
    sys.exit(__doc__)
entrada, salida = sys.argv[1:]
os.makedirs(os.path.dirname(salida) or ".", exist_ok=True)
wb = load_workbook(entrada, read_only=True, data_only=True)
n = 0
with open(salida, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["fecha", "sede", "categoria", "unidades", "venta", "margen"])
    for ws in wb.worksheets:
        for fila in ws.iter_rows(min_row=2, values_only=True):
            if fila and fila[0] is not None:
                w.writerow(["" if v is None else v for v in fila[:6]]); n += 1
print(f"{len(wb.worksheets)} hojas, {n} filas → {salida}")
