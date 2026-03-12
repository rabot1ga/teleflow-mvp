FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install shared library first
COPY shared/teleflow-common /tmp/teleflow-common
RUN pip install --no-cache-dir /tmp/teleflow-common

# Install Python dependencies
COPY services/analytics-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY services/analytics-service/app /app/app

# Copy Alembic configuration
COPY services/analytics-service/alembic.ini /app/
COPY services/analytics-service/alembic /app/alembic

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8010/health || exit 1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8010"]
