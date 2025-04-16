import logging
from pathlib import Path

from pydantic_settings import BaseSettings

PROJECT_DIR = Path(__file__).parent.absolute()


class LogSettings(BaseSettings):
    RICH_LOGGING: bool = False
    LOG_LEVEL: int = logging.INFO


class Config(LogSettings):
        APP_ID_SHOPEE: str
        SECRET_SHOPEE: str
        GEMINI_API_KEY: str


        class Config:
            env_file = ".env"
            env_file_encoding = "utf-8"
            extra = "ignore"


settings = Config()  # type: ignore