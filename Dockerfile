# Imagen base
FROM python:3.11-slim

# Ajustes recomendados
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Dependencias del sistema (si en el futuro necesitas otras libs, las agregas aquí)
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copiar requirements del backend
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente del backend
COPY app ./app

# Exponer el puerto (solo informativo)
EXPOSE 8000

# Comando de arranque
# Render expone la variable $PORT; si no existe, usa 8000 para correr localmente con Docker
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
