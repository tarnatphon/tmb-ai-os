from pathlib import Path

from tmb_ai_os.channels import Channel
from tmb_ai_os.content import ContentRepository
from tmb_ai_os.knowledge import (
    KeywordKnowledgeRetriever,
    KnowledgeRepository,
)
from tmb_ai_os.multichannel import MultiChannelContentService
from tmb_ai_os.prompt_sdk import PromptBuilder


def test_preview_builds_one_prompt_per_channel(tmp_path: Path) -> None:
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
This is verified and sufficiently long source content.
""",
        encoding="utf-8",
    )

    service = MultiChannelContentService(
        content_repository=ContentRepository(content_dir),
        retriever=KeywordKnowledgeRetriever(KnowledgeRepository(knowledge_dir)),
        prompt_builder=PromptBuilder(),
    )

    outputs = service.preview(brief)

    assert [output.channel for output in outputs] == [
        Channel.FACEBOOK,
        Channel.X,
    ]
    assert all("TRUST RULES" in output.prompt for output in outputs)
