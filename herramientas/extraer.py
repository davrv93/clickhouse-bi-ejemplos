"""Lee los tres reportes (Excel, PDF y Word) y los junta en una sola tabla: salida/juntos.csv (video 6).

  docker compose run --rm herramientas extraer.py
"""
import csv
import os

import pdfplumber
from docx import Document
from openpyxl import load_workbook

import ch

D = os.path.join(ch.DATOS, "archivos")
todas = []


def agregar(origen, filas):
    filas = [f for f in filas if f and f[0] and f[0] != "Fecha"]
    todas.extend([origen] + ["" if v is None else str(v) for v in f] for f in filas)
    print(f"{origen:34s} {len(filas):5d} filas")


wb = load_workbook(os.path.join(D, "ventas-lima-miraflores.xlsx"), read_only=True)
for ws in wb.worksheets:
    agregar(f"ventas-lima-miraflores.xlsx [{ws.title}]", [list(r) for r in ws.iter_rows(values_only=True)])
with pdfplumber.open(os.path.join(D, "reporte-surco.pdf")) as pdf:
    filas = [r for p in pdf.pages for t in p.extract_tables() for r in t]
    print(f"  (PDF: {len(pdf.pages)} páginas)")
agregar("reporte-surco.pdf", filas)
doc = Document(os.path.join(D, "reporte-arequipa.docx"))
agregar("reporte-arequipa.docx", [[c.text for c in r.cells] for t in doc.tables for r in t.rows])
with open(ch.ruta("salida", "juntos.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["origen", "fecha", "sede", "categoria", "unidades", "venta", "margen"])
    w.writerows(todas)
print(f"{'TOTAL':34s} {len(todas):5d} filas → salida/juntos.csv")
