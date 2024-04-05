# Usamos una imagen base de Python oficial. Puedes elegir la versión específica que necesites.
FROM python:3.8-slim

# Configuramos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo de requerimientos primero para aprovechar la caché de capas de Docker
COPY requirements.txt .

# Instalamos las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Ahora copiamos el resto de los archivos del proyecto al contenedor
COPY . .

# Exponemos el puerto en el que se ejecutará la aplicación
EXPOSE 5000

# Definimos el comando para ejecutar la aplicación
# Reemplaza 'run.py' con el script que inicia tu aplicación de Flask
CMD ["python", "server.py"]
