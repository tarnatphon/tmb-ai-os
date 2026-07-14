from tmb_ai_os.agents import AgentContext, AgentResult, AgentRole
from tmb_ai_os.agents.registry import AgentRegistry


class FakeAgent:
    role = AgentRole.PLANNER

    def run(self, context: AgentContext) -> AgentResult:
        return AgentResult(role=self.role, output=context.task)


def test_registry_registers_and_gets_agent() -> None:
    registry = AgentRegistry()
    registry.register(FakeAgent())

    agent = registry.get(AgentRole.PLANNER)

    assert agent.role is AgentRole.PLANNER
    assert registry.list_roles() == [AgentRole.PLANNER]
