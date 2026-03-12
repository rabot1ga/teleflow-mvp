"""
Application configuration.
"""

from teleflow_common.config import BaseSettings


class Settings(BaseSettings):
    """Content service settings."""

    # Service
    SERVICE_NAME: str = "content-service"
    SERVICE_VERSION: str = "0.1.0"
    LOG_LEVEL: str = "INFO"

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"

    # JWT
    JWT_SECRET: str

    # Meilisearch
    MEILISEARCH_URL: str = "http://meilisearch:7700"
    MEILISEARCH_API_KEY: str = "dev-meilisearch-key"

    # MinIO
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "teleflow"

    # Service URLs
    AI_SERVICE_URL: str = "http://ai-service:8009"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
