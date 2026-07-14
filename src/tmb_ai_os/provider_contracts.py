from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class GenerationRequest:
    prompt: str


@dataclass(frozen=True)
class GenerationResponse:
    text: str
    provider: str
    model: str


class ContentProvider(Protocol):
    name: str

    def generate_content(
        self,
        request: GenerationRequest,
    ) -> GenerationResponse: ...
