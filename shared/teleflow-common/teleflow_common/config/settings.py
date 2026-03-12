"""
Configuration module for TeleFlow services.
"""

from pydantic_settings import BaseSettings as PydanticBaseSettings


class BaseSettings(PydanticBaseSettings):
    """
    Base settings class for all TeleFlow services.
    Uses environment variables with automatic .env file loading.
    """

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"
