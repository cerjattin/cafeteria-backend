# Usamos una imagen ligera de Python
FROM python:3.10-slim

# Evita que Python genere archivos .pyc y buffer de salida
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo en el contenedor
WORKDIR /code

# Copiamos requirements e instalamos dependencias
COPY requirements.txt /code/
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copiamos todo el código del backend
COPY ./app /code/app

# Comando para iniciar el servidor (Render inyectará el PORT)
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]