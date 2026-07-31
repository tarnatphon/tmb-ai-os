from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class PromptVariable:
    name: str
    description: str = ""
    required: bool = True
    default: Any = None


@dataclass(slots=True)
class PromptMetadata:
    name: str
    version: str = "1.0.0"
    author: str = "Thai Modern Bags AI"
    description: str = ""


@dataclass(slots=True)
class PromptDefinition:
    metadata: PromptMetadata
    template: str
    variables: list[PromptVariable] = field(default_factory=list)


@dataclass(slots=True)
class RenderedPrompt:
    text: str
    variables: dict[str, Any] = field(default_factory=dict)
