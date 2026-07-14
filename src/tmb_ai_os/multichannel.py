from dataclasses import dataclass
from pathlib import Path

from .channels import Channel, parse_channels
from .content import ContentRepository
from .knowledge import KeywordKnowledgeRetriever
from .prompt_sdk import PromptBuilder, PromptContext
from .providers import TextGenerator


@dataclass(frozen=True)
class ChannelOutput:
    channel: Channel
    prompt: str
    text: str | None = None


class MultiChannelContentService:
    def __init__(
        self,
        content_repository: ContentRepository,
        retriever: KeywordKnowledgeRetriever,
        prompt_builder: PromptBuilder,
        generator: TextGenerator | None = None,
    ) -> None:
        self.content_repository = content_repository
        self.retriever = retriever
        self.prompt_builder = prompt_builder
        self.generator = generator

    def preview(self, path: Path) -> list[ChannelOutput]:
        brief = self.content_repository.load_brief(path)
        channels = parse_channels(brief.channels)
        if not channels:
            raise ValueError("The brief does not contain a supported channel")

        results = self.retriever.search(
            f"{brief.topic} {brief.pillar} {brief.body}",
            limit=4,
        )
        documents = tuple(result.document for result in results)

        return [
            ChannelOutput(
                channel=channel,
                prompt=self.prompt_builder.build(
                    PromptContext(
                        brief=brief,
                        channel=channel,
                        knowledge=documents,
                    )
                ),
            )
            for channel in channels
        ]

    def generate(self, path: Path) -> list[ChannelOutput]:
        if self.generator is None:
            raise RuntimeError("A text generator is required")

        previews = self.preview(path)
        return [
            ChannelOutput(
                channel=item.channel,
                prompt=item.prompt,
                text=self.generator.generate(item.prompt),
            )
            for item in previews
        ]
