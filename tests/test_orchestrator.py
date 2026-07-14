from tmb_ai_os.agents import (
    AgentContext,
    AgentRegistry,
    AgentResult,
    AgentRole,
)
from tmb_ai_os.orchestrator import ContentAgentOrchestrator


class FakeAgent:
    def __init__(self, role: AgentRole, approved: bool = True) -> None:
        self.role = role
        self.approved = approved

    def run(self, context: AgentContext) -> AgentResult:
        if self.role is not AgentRole.PLANNER:
            assert context.artifacts
        return AgentResult(
            role=self.role,
            output=f"{self.role.value} output",
            approved=self.approved,
            issues=() if self.approved else ("rejected",),
        )


def build_registry(qa_approved: bool) -> AgentRegistry:
    registry = AgentRegistry()
    for role in AgentRole:
        approved = qa_approved if role is AgentRole.QA_REVIEWER else True
        registry.register(FakeAgent(role, approved=approved))
    return registry


def test_orchestrator_runs_full_sequence() -> None:
    run = ContentAgentOrchestrator(build_registry(True)).run(
        AgentContext(task="Create content", source="Verified source")
    )

    assert run.approved is True
    assert len(run.results) == 7
    assert run.results[-1].role is AgentRole.QA_REVIEWER


def test_orchestrator_returns_rejected_qa_result() -> None:
    run = ContentAgentOrchestrator(build_registry(False)).run(
        AgentContext(task="Create content", source="Verified source")
    )

    assert run.approved is False
    assert run.results[-1].approved is False
