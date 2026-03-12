"""Application configuration."""
from teleflow_common.config import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "promotion-service"
    SERVICE_VERSION: str = "0.1.0"
    LOG_LEVEL: str = "INFO"
    DATABASE_URL: str
    REDIS_URL: str = "redis://redis:6379/0"
    JWT_SECRET: str
    USERBOT_SERVICE_URL: str = "http://userbot-service:8007"
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
