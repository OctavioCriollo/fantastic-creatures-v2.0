# Usa una imagen base de Python
FROM python:3.12-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos de requisitos de la aplicación en el directorio de trabajo
COPY requirements.txt .

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Instalar Gunicorn para servir la aplicación Flask
RUN pip install gunicorn

# Copiar todos los archivos de la aplicación en el contenedor
COPY . .

# Exponer el puerto que utilizará la aplicación --> Gunicorn o uWSGI Server Port
EXPOSE 8000

# Variables de entorno para configurar Flask
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0

# Añadir una variable de entorno de Python para evitar la creación de archivos pyc
ENV PYTHONDONTWRITEBYTECODE=1

# Añadir una variable de entorno de Python para hacer los logs sin buffer
ENV PYTHONUNBUFFERED=1

# Establecer la variable de entorno para indicar que estamos en un contenedor Docker
ENV DOCKERIZED=True

# Limpiar archivos temporales (opcional para reducir el tamaño de la imagen)
#RUN apt-get update && apt-get install -y --no-install-recommends \
#    && rm -rf /var/lib/apt/lists/*

# Clean up
RUN apt-get update && apt-get clean && rm -rf /var/lib/apt/lists/*
    
# Comando para ejecutar la aplicación usando Gunicorn
CMD ["gunicorn", "main:app", \
     "-w", "1", \
     "-b", "0.0.0.0:8000", \
     "--timeout", "120", \
     "--graceful-timeout", "120", \
     "--keep-alive", "5"]

