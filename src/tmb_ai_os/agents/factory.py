from ..providers import TextGenerator
from .llm_agent import LLMAgent
from .registry import AgentRegistry
from .roles import AgentRole


def build_default_registry(generator: TextGenerator) -> AgentRegistry:
    registry = AgentRegistry()
    for role in AgentRole:
        registry.register(LLMAgent(role=role, generator=generator))
    return registry
