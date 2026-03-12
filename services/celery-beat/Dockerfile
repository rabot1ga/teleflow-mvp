FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install shared library first
COPY shared/teleflow-common /tmp/teleflow-common
RUN pip install --no-cache-dir /tmp/teleflow-common

# Install Python dependencies
COPY services/celery-beat/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY services/celery-beat/app /app/app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD celery -A app.celery_app inspect ping || exit 1

# Run Celery Beat
CMD ["celery", "-A", "app.celery_app", "beat", "--loglevel=info"]
