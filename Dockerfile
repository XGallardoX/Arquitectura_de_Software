# Imagen base
FROM python:3.13-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema (ejemplo si usas MySQL; si solo SQLite, no hace falta)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalarlos
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Exponer puertos (8000 para Django, 8501 para Streamlit)
EXPOSE 8000
EXPOSE 8501

# Comando por defecto (Django + Streamlit)
CMD ["sh", "-c", "python webapp/manage.py migrate && python webapp/manage.py runserver 0.0.0.0:8000 & streamlit run datapp/app.py --server.port=8501 --server.address=0.0.0.0"]
