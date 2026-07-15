import pytest

from tmb_ai_os.editorial import (
    EditorialStatus,
    InvalidEditorialTransition,
    validate_transition,
)


def test_valid_editorial_transition() -> None:
    validate_transition(
        EditorialStatus.GENERATED,
        EditorialStatus.REVIEWED,
    )


def test_invalid_editorial_transition() -> None:
    with pytest.raises(InvalidEditorialTransition):
        validate_transition(
            EditorialStatus.GENERATED,
            EditorialStatus.PUBLISHED,
        )
