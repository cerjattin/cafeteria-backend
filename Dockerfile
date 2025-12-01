FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# **Instalar uvicorn explícitamente (soluciona el error)**
RUN pip install --no-cache-dir uvicorn

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY app ./app

EXPOSE 8000

# Ejecutar uvicorn usando python -m (SIEMPRE funciona)
CMD python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
