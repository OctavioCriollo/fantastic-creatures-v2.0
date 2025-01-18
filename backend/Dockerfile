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

# Exponer el puerto que utilizará la aplicación
EXPOSE 5000

# Establecer la variable de entorno para indicar que estamos en un contenedor Docker
ENV DOCKERIZED=True

# Comando para ejecutar la aplicación usando Gunicorn
CMD ["gunicorn", "app:app", \
     "-w", "2", \
     "-b", "0.0.0.0:5000", \
     "--timeout", "120", \
     "--graceful-timeout", "120", \
     "--keep-alive", "5"]

