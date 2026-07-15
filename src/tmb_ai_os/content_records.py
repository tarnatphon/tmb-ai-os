import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class ContentCreate(BaseModel):
    topic: str = Field(min_length=3, max_length=255)
    pillar: str = Field(default="General", min_length=2, max_length=120)
    status: str = Field(default="generated", min_length=2, max_length=50)
    channels: dict[str, str] = Field(min_length=1)
    prompt_hash: str | None = Field(default=None, max_length=64)

    @field_validator("channels")
    @classmethod
    def validate_channels(
        cls,
        channels: dict[str, str],
    ) -> dict[str, str]:
        cleaned = {
            key.strip(): value.strip()
            for key, value in channels.items()
            if key.strip() and value.strip()
        }
        if not cleaned:
            raise ValueError("channels must contain publishable content")
        return cleaned


class ContentRead(BaseModel):
    id: int
    created_at: datetime
    topic: str
    pillar: str
    status: str
    channels: dict[str, str]
    prompt_hash: str | None = None


@dataclass(frozen=True)
class StoredContent:
    id: int
    created_at: datetime
    topic: str
    pillar: str
    status: str
    channels: dict[str, str]
    prompt_hash: str | None


def encode_channels(channels: dict[str, str]) -> str:
    return json.dumps(channels, ensure_ascii=False, sort_keys=True)


def decode_channels(payload_json: str) -> dict[str, str]:
    payload: Any = json.loads(payload_json)
    if not isinstance(payload, dict):
        raise ValueError("Stored content payload must be a JSON object")

    return {
        key: value
        for key, value in payload.items()
        if isinstance(key, str) and isinstance(value, str)
    }
