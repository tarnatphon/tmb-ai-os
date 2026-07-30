import pytest

from tmb_ai_os.core.queue import JobQueue


@pytest.mark.asyncio
async def test_queue_processes_job() -> None:
    queue = JobQueue()
    received: list[str] = []

    async def handler(payload: dict[str, object]) -> None:
        received.append(str(payload["name"]))

    queue.register("content.generate", handler)
    await queue.enqueue("content.generate", {"name": "OEM backpack"})
    job = await queue.process_one()

    assert received == ["OEM backpack"]
    assert job.attempts == 1
    assert queue.size == 0
