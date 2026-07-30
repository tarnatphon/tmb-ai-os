from __future__ import annotations

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str
    environment: str
    version: str


class PluginResponse(BaseModel):
    name: str
    version: str
    enabled: bool
    capabilities: list[str]
