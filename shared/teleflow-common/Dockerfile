FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

# Install dev dependencies (optional)
# RUN pip install --no-cache-dir -e ".[dev]"
