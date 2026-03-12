"""Application configuration."""
from teleflow_common.config import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "celery-beat"
    SERVICE_VERSION: str = "0.1.0"
    REDIS_URL: str = "redis://redis:6379/0"
    JWT_SECRET: str = ""
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
