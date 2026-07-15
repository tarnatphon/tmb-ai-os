from tmb_ai_os.publishing import (
    DryRunPublisher,
    PublishRequest,
)


def test_dry_run_publisher_returns_simulated_result() -> None:
    result = DryRunPublisher().publish(
        PublishRequest(
            content_id=7,
            channels={"facebook": "content"},
        )
    )

    assert result.provider == "dry_run"
    assert result.external_id == "dry-run-7"
    assert result.metadata["mode"] == "simulation"
