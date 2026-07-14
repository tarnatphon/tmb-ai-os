from dataclasses import dataclass, replace

from .agents import AgentContext, AgentRegistry, AgentResult, AgentRole


@dataclass(frozen=True)
class WorkflowRun:
    results: tuple[AgentResult, ...]
    approved: bool

    def get(self, role: AgentRole) -> AgentResult:
        for result in self.results:
            if result.role is role:
                return result
        raise KeyError(f"No result for role: {role}")


class ContentAgentOrchestrator:
    sequence = (
        AgentRole.PLANNER,
        AgentRole.WRITER,
        AgentRole.SEO_REVIEWER,
        AgentRole.BRAND_REVIEWER,
        AgentRole.FACT_CHECKER,
        AgentRole.IMAGE_PROMPT,
        AgentRole.QA_REVIEWER,
    )

    def __init__(self, registry: AgentRegistry) -> None:
        self.registry = registry

    def run(self, context: AgentContext) -> WorkflowRun:
        current = context
        results: list[AgentResult] = []

        for role in self.sequence:
            result = self.registry.get(role).run(current)
            results.append(result)
            current = replace(
                current,
                artifacts={
                    **current.artifacts,
                    role.value: result.output,
                },
            )

            if role is AgentRole.QA_REVIEWER and not result.approved:
                return WorkflowRun(results=tuple(results), approved=False)

        return WorkflowRun(results=tuple(results), approved=True)
