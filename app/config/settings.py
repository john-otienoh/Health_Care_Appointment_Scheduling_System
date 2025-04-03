import os
import urllib.parse
from pathlib import Path
from dotenv import load_dotenv
from functools import lru_cache
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    # App Configuration
    APP_NAME: str = os.environ.get("APP_NAME", "FastAPI")
    DEBUG: bool = bool(os.environ.get("DEBUG", False))

    DB_HOST: str = os.environ.get("DB_HOST")
    DB_USER: str = os.environ.get("DB_USER")
    DB_PASS: str = os.environ.get("DB_PASS")
    DB_PORT: int = int(os.environ.get("DB_PORT"))
    DB_NAME: str = os.environ.get("DB_NAME")
    DATABASE_URI: str = (
        f"postgresql://{urllib.parse.quote_plus(os.getenv('DB_USER'))}:{urllib.parse.quote_plus(os.getenv('DB_PASS'))}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

    # App Secret Key
    # SECRET_KEY: str = os.environ.get("SECRET_KEY", "8deadce9449770680910741063cd0a3fe0acb62a8978661f421bbcbb66dc41f1")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
