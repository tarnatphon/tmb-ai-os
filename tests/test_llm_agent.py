from tmb_ai_os.agents import AgentContext, AgentRole
from tmb_ai_os.agents.llm_agent import LLMAgent


class FakeGenerator:
    def __init__(self, response: str) -> None:
        self.response = response

    def generate(self, prompt: str) -> str:
        assert "TRUST POLICY" in prompt
        return self.response


def test_qa_agent_approves_approved_response() -> None:
    agent = LLMAgent(
        role=AgentRole.QA_REVIEWER,
        generator=FakeGenerator("APPROVED\nReady to publish."),
    )

    result = agent.run(AgentContext(task="Review", source="Verified source"))

    assert result.approved is True
    assert result.issues == ()


def test_qa_agent_rejects_other_response() -> None:
    agent = LLMAgent(
        role=AgentRole.QA_REVIEWER,
        generator=FakeGenerator("REJECTED\nUnsupported MOQ claim."),
    )

    result = agent.run(AgentContext(task="Review", source="Verified source"))

    assert result.approved is False
    assert result.issues
