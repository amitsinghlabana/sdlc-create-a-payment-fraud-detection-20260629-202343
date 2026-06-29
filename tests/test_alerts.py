import pytest
from types import SimpleNamespace

import httpx
from app.alerts import publish_alert_if_needed


def make_record():
    return SimpleNamespace(
        transaction_id="tx-999",
        risk_score=0.85,
        status="review",
        reason="Threshold breach",
    )


def test_publish_alert_success(monkeypatch):
    settings = SimpleNamespace(alert_webhook="https://alerts.example.com/integrations")
    monkeypatch.setattr("app.alerts.get_settings", lambda: settings)

    captured = {}

    class DummyResponse:
        def raise_for_status(self):
            captured["raised"] = True

    def fake_post(url, json, timeout):
        captured["url"] = url
        captured["json"] = json
        captured["timeout"] = timeout
        return DummyResponse()

    monkeypatch.setattr("app.alerts.httpx.post", fake_post)

    record = make_record()

    publish_alert_if_needed(record)

    assert captured["url"] == settings.alert_webhook
    assert captured["timeout"] == 2.0
    assert captured["json"]["id"] == record.transaction_id
    assert captured["json"]["score"] == record.risk_score


def test_publish_alert_http_failure(monkeypatch):
    settings = SimpleNamespace(alert_webhook="https://alerts.example.com/integrations")
    monkeypatch.setattr("app.alerts.get_settings", lambda: settings)

    class FaultyResponse:
        def raise_for_status(self):
            raise httpx.HTTPStatusError("Boom", request=None, response=None)

    def fake_post(url, json, timeout):
        return FaultyResponse()

    monkeypatch.setattr("app.alerts.httpx.post", fake_post)

    with pytest.raises(httpx.HTTPStatusError):
        publish_alert_if_needed(make_record())
