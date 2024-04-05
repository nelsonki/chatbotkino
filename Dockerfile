# Usa una imagen base oficial de Python 3.
FROM python:3.8-slim

# Configura el directorio de trabajo dentro del contenedor.
WORKDIR /app

# Variables de entorno.
ENV PYTHONUNBUFFERED=true

# Copia e instala los requisitos de dependencia.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos del proyecto en el contenedor.
COPY . .

# Expone el puerto en el que se ejecuta tu aplicación.
EXPOSE 5000

# Define el comando para ejecutar tu aplicación.
# Reemplaza 'run.py' con el script que inicia tu aplicación Flask.
CMD ["python3", "run.py"]
