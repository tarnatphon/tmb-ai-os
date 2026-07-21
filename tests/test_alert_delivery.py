from __future__ import annotations


def test_alert_delivery_module_imports() -> None:
    from tmb_ai_os.alert_delivery import AlertDeliveryService

    assert AlertDeliveryService is not None
