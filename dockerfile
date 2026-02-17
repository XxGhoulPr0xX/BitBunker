# Usamos una versión slim para que la imagen no pese GBs
FROM python:3.12-slim

# Evita que Python escriba archivos .pyc y permite ver logs en consola
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalamos dependencias de sistema necesarias para Django
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# AJUSTE: Usamos el nombre exacto de tu captura "requeriments.txt"
COPY requeriments.txt /app/
RUN pip install --no-cache-dir -r requeriments.txt

# Copiamos todo el contenido (BitBunker/, static/, users/, etc.)
COPY . /app/

EXPOSE 8080

# Comando para arrancar. 
# "0.0.0.0" es vital para que Docker pueda sacar el tráfico del contenedor
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8080"]