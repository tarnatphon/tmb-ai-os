from sqlalchemy.orm import Session

from tmb_ai_os.content_history import (
    ContentHistoryRepository,
    ContentNotFoundError,
    DuplicatePromptError,
)
from tmb_ai_os.content_records import ContentCreate
from tmb_ai_os.database import Base, build_engine


def make_session() -> Session:
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return Session(engine)


def test_repository_create_list_and_get() -> None:
    session = make_session()
    repository = ContentHistoryRepository()

    created = repository.create(
        session,
        ContentCreate(
            topic="OEM Bags",
            pillar="Manufacturing",
            channels={"facebook": "content"},
            prompt_hash="hash-1",
        ),
    )

    assert repository.list(session)[0].id == created.id
    assert repository.get(session, created.id).channels == {"facebook": "content"}
    session.close()


def test_repository_rejects_duplicate_prompt_hash() -> None:
    session = make_session()
    repository = ContentHistoryRepository()
    payload = ContentCreate(
        topic="OEM Bags",
        channels={"facebook": "content"},
        prompt_hash="same-hash",
    )
    repository.create(session, payload)

    with __import__("pytest").raises(DuplicatePromptError):
        repository.create(session, payload)
    session.close()


def test_repository_raises_not_found() -> None:
    session = make_session()
    repository = ContentHistoryRepository()

    with __import__("pytest").raises(ContentNotFoundError):
        repository.get(session, 999)
    session.close()
