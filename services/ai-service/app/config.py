"""Application configuration."""
from teleflow_common.config import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "ai-service"
    SERVICE_VERSION: str = "0.1.0"
    LOG_LEVEL: str = "INFO"
    DATABASE_URL: str
    REDIS_URL: str = "redis://redis:6379/0"
    JWT_SECRET: str
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    OLLAMA_BASE_URL: str = "http://ollama:11434"
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
