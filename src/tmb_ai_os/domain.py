from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator


class ContentBrief(BaseModel):
    source_path: Path
    title: str = Field(min_length=3)
    topic: str = Field(min_length=3)
    pillar: str = Field(min_length=2)
    audience: list[str] = Field(min_length=1)
    channels: list[str] = Field(min_length=1)
    language: str = "th"
    objective: str = Field(min_length=3)
    call_to_action: str = ""
    body: str = Field(min_length=10)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("audience", "channels")
    @classmethod
    def strip_list_values(cls, values: list[str]) -> list[str]:
        cleaned = [value.strip() for value in values if value.strip()]
        if not cleaned:
            raise ValueError("must contain at least one non-empty value")
        return cleaned


class GeneratedContent(BaseModel):
    source_path: Path
    model: str
    text: str
