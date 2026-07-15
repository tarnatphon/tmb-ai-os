from pathlib import Path

from sqlalchemy.orm import Session

from tmb_ai_os.channels import Channel
from tmb_ai_os.content import ContentRepository
from tmb_ai_os.content_history import ContentHistoryRepository
from tmb_ai_os.content_workflow import ContentWorkflowService
from tmb_ai_os.database import Base, build_engine
from tmb_ai_os.knowledge import (
    KeywordKnowledgeRetriever,
    KnowledgeRepository,
)
from tmb_ai_os.multichannel import MultiChannelContentService
from tmb_ai_os.prompt_sdk import PromptBuilder


class FakeGenerator:
    def generate(self, prompt: str) -> str:
        assert "TRUST RULES" in prompt
        return "Generated content"


def make_service(
    tmp_path: Path,
) -> tuple[ContentWorkflowService, Path, Session]:
    content_dir = tmp_path / "content"
    knowledge_dir = tmp_path / "knowledge"
    content_dir.mkdir()
    knowledge_dir.mkdir()

    brief = content_dir / "brief.md"
    brief.write_text(
        """---
title: OEM Bag Brief
topic: OEM Bags
pillar: Manufacturing
audience: [Purchasing]
channels: [facebook, x]
objective: educate
---
Verified source content for generation.
""",
        encoding="utf-8",
    )

    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = Session(engine)

    multi_channel = MultiChannelContentService(
        content_repository=ContentRepository(content_dir),
        retriever=KeywordKnowledgeRetriever(KnowledgeRepository(knowledge_dir)),
        prompt_builder=PromptBuilder(),
        generator=FakeGenerator(),
    )

    service = ContentWorkflowService(
        generator_service=multi_channel,
        history_repository=ContentHistoryRepository(),
    )

    return service, brief, session


def test_generate_and_store(
    tmp_path: Path,
) -> None:
    service, brief, session = make_service(tmp_path)

    result = service.generate_and_store(
        session,
        brief,
    )

    assert result.stored is not None
    assert result.stored.channels == {
        Channel.FACEBOOK.value: "Generated content",
        Channel.X.value: "Generated content",
    }
    assert len(result.prompt_hash) == 64
    session.close()


def test_preview_does_not_store(
    tmp_path: Path,
) -> None:
    service, brief, session = make_service(tmp_path)

    result = service.preview(brief)

    assert result.stored is None
    assert len(result.outputs) == 2
    session.close()
