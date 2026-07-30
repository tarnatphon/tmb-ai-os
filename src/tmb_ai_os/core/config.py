from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True, slots=True)
class Settings:
    app_name: str
    environment: str
    log_level: str
    api_prefix: str
    enable_example_plugin: bool


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("TMB_APP_NAME", "Thai Modern Bags AI OS"),
        environment=os.getenv("TMB_ENVIRONMENT", "development"),
        log_level=os.getenv("TMB_LOG_LEVEL", "INFO").upper(),
        api_prefix=os.getenv("TMB_API_PREFIX", "/api/v1"),
        enable_example_plugin=_as_bool(os.getenv("TMB_ENABLE_EXAMPLE_PLUGIN"), True),
    )
