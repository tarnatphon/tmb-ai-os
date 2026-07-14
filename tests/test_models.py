from datetime import datetime

from tmb_ai_os.models import ContentRun


def test_content_run_contract() -> None:
    row = ContentRun(
        topic="OEM Bags",
        pillar="Manufacturing",
        status="generated",
        payload_json='{"ok": true}',
        prompt_hash="abc123",
    )

    assert row.topic == "OEM Bags"
    assert row.pillar == "Manufacturing"
    assert row.status == "generated"
    assert isinstance(row.created_at, datetime) is False
