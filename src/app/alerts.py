import httpx
from app.config import get_settings
from app.telemetry import record_metric


def publish_alert_if_needed(record):
    settings = get_settings()
    payload = {
        "id": record.transaction_id,
        "score": record.risk_score,
        "status": record.status,
        "reason": record.reason,
    }
    response = httpx.post(settings.alert_webhook, json=payload, timeout=2.0)
    response.raise_for_status()
    record_metric("alerts.published", 1)
