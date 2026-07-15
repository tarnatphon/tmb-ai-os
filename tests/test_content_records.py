import pytest

from tmb_ai_os.content_records import (
    ContentCreate,
    decode_channels,
    encode_channels,
)


def test_encode_decode_channels_round_trip() -> None:
    channels = {
        "facebook": "โพสต์สำหรับ Facebook",
        "x": "โพสต์สำหรับ X",
    }

    encoded = encode_channels(channels)
    decoded = decode_channels(encoded)

    assert decoded == channels


def test_content_create_rejects_empty_channels() -> None:
    with pytest.raises(ValueError):
        ContentCreate(
            topic="OEM Bags",
            channels={"facebook": "   "},
        )
