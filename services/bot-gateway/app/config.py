"""Application configuration."""
from teleflow_common.config import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "bot-gateway"
    SERVICE_VERSION: str = "0.1.0"
    LOG_LEVEL: str = "INFO"
    DATABASE_URL: str
    REDIS_URL: str = "redis://redis:6379/0"
    JWT_SECRET: str
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_BOT_WEBHOOK_URL: str = "http://localhost/api/v1/bot/webhook"
    FUNNEL_SERVICE_URL: str = "http://funnel-service:8005"
    CONTENT_SERVICE_URL: str = "http://content-service:8002"
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
