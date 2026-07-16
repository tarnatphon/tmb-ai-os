from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env: str = "development"
    ai_provider: str = "gemini"
    database_url: str = "sqlite:///data/tmb_ai_os.db"
    app_timezone: str = "Asia/Bangkok"
    scheduler_enabled: bool = False
    scheduler_hour: int = 8
    scheduler_minute: int = 0
    api_key: str = "change-me"
    api_role: str = "admin"
    rate_limit_requests: int = 60
    rate_limit_window_seconds: int = 60
    require_secure_api_key: bool = True
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
