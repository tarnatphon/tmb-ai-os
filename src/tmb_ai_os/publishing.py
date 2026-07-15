from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol


@dataclass(frozen=True)
class PublishRequest:
    content_id: int
    channels: dict[str, str]


@dataclass(frozen=True)
class PublishResult:
    provider: str
    external_id: str
    published_at: datetime
    metadata: dict[str, str]


class Publisher(Protocol):
    name: str

    def publish(
        self,
        request: PublishRequest,
    ) -> PublishResult: ...


class DryRunPublisher:
    name = "dry_run"

    def publish(
        self,
        request: PublishRequest,
    ) -> PublishResult:
        return PublishResult(
            provider=self.name,
            external_id=f"dry-run-{request.content_id}",
            published_at=datetime.now(UTC),
            metadata={
                "channels": ",".join(sorted(request.channels)),
                "mode": "simulation",
            },
        )
