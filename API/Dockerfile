
# Cómo se construye la imagen docke:



FROM python:3.11-slim 
 #crea un entorno que ya tare instalado python 3.11. la parte d slim signfifica que es una versión más ligera, con menos cosas instaladas

WORKDIR /app 
#Crea una carpeta dentro dle contenedor llamda app. A partir de esa linea, todo los comandos se ejecutan dentro de esa carpeta.

COPY requirements.txt . 
 #Copia mi archivo requierements.txt desde mi ordenador hacia la carpeta actual del contenedor

RUN pip install --no-cache-dir -r requirements.txt
 #Instala dentro del contenedor toda sdlas librerías que aparecen en requirements

COPY . . 
 #Copia todo el contenido de mi carpeta actual al contenedor

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]  
#El --host 0.0.0.0 significa que la API acepta conexiones desde fuera del de contenedor
#Para construir la imagen: docker build -t mi-api .
#Para ejecutar el contenedor: docker run -p 8000:8000 mi-api
#Para pasarle las variables de entorno desde el archivo env: docker run --env-file .env -p 8000:8000 mi-api