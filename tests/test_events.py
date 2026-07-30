import pytest

from tmb_ai_os.core.events import Event, EventBus


@pytest.mark.asyncio
async def test_event_bus_delivers_event() -> None:
    bus = EventBus()
    received: list[str] = []

    async def handler(event: Event) -> None:
        received.append(str(event.payload["value"]))

    await bus.subscribe("demo.created", handler)
    await bus.publish(Event("demo.created", {"value": 42}))

    assert received == ["42"]
    assert bus.subscriber_count("demo.created") == 1
