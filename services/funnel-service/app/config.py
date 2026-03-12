"""
Application configuration.
"""

from teleflow_common.config import BaseSettings


class Settings(BaseSettings):
    """Funnel service settings."""

    # Service
    SERVICE_NAME: str = "funnel-service"
    SERVICE_VERSION: str = "0.1.0"
    LOG_LEVEL: str = "INFO"

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"

    # JWT
    JWT_SECRET: str

    # Service URLs
    BOT_GATEWAY_URL: str = "http://bot-gateway:8006"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
