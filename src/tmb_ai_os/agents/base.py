from dataclasses import dataclass, field
from typing import Any, Protocol

from .roles import AgentRole


@dataclass(frozen=True)
class AgentContext:
    task: str
    source: str
    channel: str | None = None
    knowledge: tuple[str, ...] = ()
    artifacts: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AgentResult:
    role: AgentRole
    output: str
    approved: bool = True
    issues: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


class Agent(Protocol):
    role: AgentRole

    def run(self, context: AgentContext) -> AgentResult: ...
