"""
Application configuration.
"""

from teleflow_common.config import BaseSettings


class Settings(BaseSettings):
    """Auth service settings."""

    # Service
    SERVICE_NAME: str = "auth-service"
    SERVICE_VERSION: str = "0.1.0"
    LOG_LEVEL: str = "INFO"

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"

    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_MINUTES: int = 15
    JWT_REFRESH_TOKEN_DAYS: int = 7

    # Service URLs
    AUTH_SERVICE_URL: str = "http://auth-service:8001"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
