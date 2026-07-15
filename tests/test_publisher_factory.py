import pytest

from tmb_ai_os.publisher_factory import (
    UnsupportedPublisherError,
    create_publisher,
)
from tmb_ai_os.publishing import DryRunPublisher


def test_factory_creates_dry_run_publisher() -> None:
    publisher = create_publisher("dry_run")

    assert isinstance(publisher, DryRunPublisher)


def test_factory_rejects_unknown_publisher() -> None:
    with pytest.raises(UnsupportedPublisherError):
        create_publisher("unknown")
