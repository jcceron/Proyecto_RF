# Usa la imagen base de Python
FROM python:3.8

# Configura el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación
COPY . .

# Comando por defecto para ejecutar la aplicación
CMD ["python", "prueba.py"]
