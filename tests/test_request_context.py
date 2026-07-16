from tmb_ai_os.request_context import (
    create_request_id,
    get_request_id,
    set_request_id,
)


def test_request_id_context() -> None:
    request_id = create_request_id()

    set_request_id(request_id)

    assert get_request_id() == request_id
    assert len(request_id) == 32
