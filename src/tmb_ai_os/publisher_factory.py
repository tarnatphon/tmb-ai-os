from enum import StrEnum

from .publishing import DryRunPublisher, Publisher


class PublisherName(StrEnum):
    DRY_RUN = "dry_run"


class UnsupportedPublisherError(ValueError):
    pass


def create_publisher(
    name: str | PublisherName = PublisherName.DRY_RUN,
) -> Publisher:
    try:
        resolved = PublisherName(str(name).strip().lower())
    except ValueError as exc:
        raise UnsupportedPublisherError(f"Unsupported publisher: {name}") from exc

    if resolved is PublisherName.DRY_RUN:
        return DryRunPublisher()

    raise UnsupportedPublisherError(f"Unsupported publisher: {resolved}")
