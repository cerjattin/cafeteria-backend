# Imagen base
FROM python:3.11-slim

# Ajustes recomendados
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crea directorio de la app
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y build-essential

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Exponer el puerto que Render usa
EXPOSE 8000

# Comando por defecto
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
