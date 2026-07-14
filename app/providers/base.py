from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class GenerationResult:
    text: str
    model: str
    provider: str


class AIProvider(ABC):
    @abstractmethod
    def generate(self, *, system_prompt: str, user_prompt: str) -> GenerationResult:
        raise NotImplementedError
