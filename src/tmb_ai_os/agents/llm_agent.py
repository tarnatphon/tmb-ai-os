from dataclasses import dataclass

from ..providers import TextGenerator
from .base import AgentContext, AgentResult
from .prompts import build_agent_prompt
from .roles import AgentRole


@dataclass
class LLMAgent:
    role: AgentRole
    generator: TextGenerator

    def run(self, context: AgentContext) -> AgentResult:
        output = self.generator.generate(build_agent_prompt(self.role, context))
        approved, issues = self._decision(output)
        return AgentResult(
            role=self.role,
            output=output,
            approved=approved,
            issues=issues,
        )

    def _decision(self, output: str) -> tuple[bool, tuple[str, ...]]:
        if self.role is not AgentRole.QA_REVIEWER:
            return True, ()

        normalized = output.strip().upper()
        approved = normalized.startswith("APPROVED")
        if approved:
            return True, ()

        issue_text = output.strip()
        return False, (issue_text,) if issue_text else ("QA rejected output",)
