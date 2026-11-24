# Herramientas del curso: Python con las librerías para leer Excel, PDF y Word.
# Así no hace falta instalar Python en Windows ni en Mac: todo corre aquí dentro.
FROM python:3.12-slim
RUN pip install --no-cache-dir openpyxl==3.1.5 pdfplumber==0.11.7 python-docx==1.2.0
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8
COPY lanzar.py /usr/local/bin/lanzar.py
WORKDIR /taller
ENTRYPOINT ["python", "/usr/local/bin/lanzar.py"]
