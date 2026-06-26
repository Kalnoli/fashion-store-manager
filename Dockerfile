# Dockerfile para Fashion Store Manager
FROM python:3.11-slim

WORKDIR /app

# Instalar curl para healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código de la app
COPY app.py database.py gestor.py ./
COPY seed_db.py ./

# Puerto
EXPOSE 8501

# Seed al construir
RUN DB_PATH=/app/data/tienda.db python3 seed_db.py

# Arranque
CMD DB_PATH=/app/data/tienda.db streamlit run app.py \
    --server.headless true \
    --server.address 0.0.0.0 \
    --server.port 8501 \
    --browser.gatherUsageStats false
