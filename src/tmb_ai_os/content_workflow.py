import hashlib
from dataclasses import dataclass
from pathlib import Path

from sqlalchemy.orm import Session

from .content_history import ContentHistoryRepository
from .content_records import ContentCreate, StoredContent
from .multichannel import (
    ChannelOutput,
    MultiChannelContentService,
)


@dataclass(frozen=True)
class ContentWorkflowResult:
    outputs: tuple[ChannelOutput, ...]
    stored: StoredContent | None
    prompt_hash: str


class ContentWorkflowService:
    def __init__(
        self,
        generator_service: MultiChannelContentService,
        history_repository: ContentHistoryRepository,
    ) -> None:
        self.generator_service = generator_service
        self.history_repository = history_repository

    def preview(self, path: Path) -> ContentWorkflowResult:
        outputs = tuple(self.generator_service.preview(path))
        prompt_hash = self._hash_outputs(outputs)
        return ContentWorkflowResult(
            outputs=outputs,
            stored=None,
            prompt_hash=prompt_hash,
        )

    def generate_and_store(
        self,
        session: Session,
        path: Path,
    ) -> ContentWorkflowResult:
        outputs = tuple(self.generator_service.generate(path))
        prompt_hash = self._hash_outputs(outputs)

        channels = {output.channel.value: output.text or "" for output in outputs if output.text}

        if not channels:
            raise RuntimeError("Generation returned no publishable content")

        brief = self.generator_service.content_repository.load_brief(path)

        stored = self.history_repository.create(
            session,
            ContentCreate(
                topic=brief.topic,
                pillar=brief.pillar,
                status="generated",
                channels=channels,
                prompt_hash=prompt_hash,
            ),
        )

        return ContentWorkflowResult(
            outputs=outputs,
            stored=stored,
            prompt_hash=prompt_hash,
        )

    @staticmethod
    def _hash_outputs(
        outputs: tuple[ChannelOutput, ...],
    ) -> str:
        source = "\n\n".join(f"{output.channel.value}\n{output.prompt}" for output in outputs)
        return hashlib.sha256(source.encode("utf-8")).hexdigest()
