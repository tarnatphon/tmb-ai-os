from .base import Agent
from .roles import AgentRole


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[AgentRole, Agent] = {}

    def register(self, agent: Agent) -> None:
        if agent.role in self._agents:
            raise ValueError(f"Agent already registered: {agent.role}")
        self._agents[agent.role] = agent

    def get(self, role: AgentRole) -> Agent:
        try:
            return self._agents[role]
        except KeyError as exc:
            raise KeyError(f"Agent not registered: {role}") from exc

    def list_roles(self) -> list[AgentRole]:
        return sorted(self._agents, key=lambda role: role.value)
