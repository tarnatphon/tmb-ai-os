from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from .agents import AgentContext, AgentRole
from .agents.factory import build_default_registry
from .agents.registry import AgentRegistry
from .config import get_settings
from .content import ContentRepository
from .knowledge import KeywordKnowledgeRetriever, KnowledgeRepository
from .orchestrator import ContentAgentOrchestrator
from .providers import GeminiGenerator

router = APIRouter(prefix="/v3", tags=["Milestone 3.1"])


class AgentRunRequest(BaseModel):
    role: AgentRole
    task: str = Field(min_length=3)
    source: str = Field(min_length=3)
    channel: str | None = None


class ContentWorkflowRequest(BaseModel):
    path: str


def _registry() -> AgentRegistry:
    settings = get_settings()
    return build_default_registry(GeminiGenerator(settings))


@router.get("/agents")
def list_agents() -> dict[str, list[str]]:
    return {"items": [role.value for role in AgentRole]}


@router.post("/agents/run")
def run_agent(payload: AgentRunRequest) -> dict[str, object]:
    try:
        result = (
            _registry()
            .get(payload.role)
            .run(
                AgentContext(
                    task=payload.task,
                    source=payload.source,
                    channel=payload.channel,
                )
            )
        )
        return {
            "role": result.role.value,
            "output": result.output,
            "approved": result.approved,
            "issues": list(result.issues),
        }
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/workflows/content")
def run_content_workflow(
    payload: ContentWorkflowRequest,
) -> dict[str, object]:
    settings = get_settings()
    try:
        brief = ContentRepository(settings.content_dir).load_brief(Path(payload.path))
        retriever = KeywordKnowledgeRetriever(KnowledgeRepository(Path("knowledge")))
        knowledge = tuple(
            result.document.body
            for result in retriever.search(
                f"{brief.topic} {brief.pillar} {brief.body}",
                limit=4,
            )
        )

        run = ContentAgentOrchestrator(_registry()).run(
            AgentContext(
                task=(f"Create, review, and approve a complete content package for: {brief.topic}"),
                source=brief.body,
                channel=", ".join(brief.channels),
                knowledge=knowledge,
                metadata={"title": brief.title},
            )
        )

        return {
            "approved": run.approved,
            "results": [
                {
                    "role": result.role.value,
                    "output": result.output,
                    "approved": result.approved,
                    "issues": list(result.issues),
                }
                for result in run.results
            ],
        }
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
