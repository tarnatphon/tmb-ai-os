from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env: str = "development"
    ai_provider: str = "gemini"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    content_dir: Path = Path("content")
    output_dir: Path = Path("output")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="TMB_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
