from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "TMB AI OS"
    ai_provider: str = "gemini"
    ai_model: str = "auto"
    ai_temperature: float = 0.7

    gemini_api_key: str = ""
    gemini_model: str = "auto"  # backward-compatible alias
    gemini_retry_attempts: int = 3
    gemini_retry_base_seconds: float = 1.0
    gemini_fallback_models: int = 3

    database_url: str = "sqlite:///./data/marketing.db"
    app_timezone: str = "Asia/Bangkok"
    daily_run_hour: int = 8
    daily_run_minute: int = 0
    auto_publish: bool = False
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
