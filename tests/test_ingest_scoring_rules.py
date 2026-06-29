import hashlib
from datetime import datetime

import pytest

from app.ingestion import ingest_transaction
from app.rules import apply_business_rules
from app import scoring


class FakeSettings:
    """Lightweight settings stub for scoring and rules."""

    def __init__(self, *, threshold: float = 0.75, blacklist: str = "US,CA"):  # pragma: no cover - simple stub
        self.scoring_model_path = "unused"
        self.high_risk_threshold = threshold
        self.blacklist_countries = blacklist


class DummyModel:
    """Predictive model stub returning a deterministic fraud score."""

    def __init__(self, score: float):
        self.score = score

    def predict_proba(self, features):
        assert isinstance(features, list)
        return [[1.0 - self.score, self.score]]


def test_ingest_transaction_hashes_pii_and_normalizes_amount():
    payload = {
        "transaction_id": "tx-123456",
        "account_id": "acct_abc",
        "amount": "42.195",
        "currency": "USD",
        "merchant_category": "5311",
        "timestamp": "2023-09-01T00:00:00Z",
        "merchant_country": "US",
        "ip_address": "192.168.0.1",
    }

    result = ingest_transaction(payload)

    assert result["ip_address"] != payload["ip_address"]
    assert result["ip_address"] == hashlib.sha256(payload["ip_address"].encode()).hexdigest()
    assert result["normalized_amount"] == round(float(payload["amount"]), 2)
    assert "ingested_at" in result


def test_score_transaction_returns_expected_value(monkeypatch):
    fake_settings = FakeSettings(blacklist="CA")
    monkeypatch.setattr(scoring, "get_settings", lambda: fake_settings)
    monkeypatch.setattr(scoring, "_model", None)
    monkeypatch.setattr(scoring.joblib, "load", lambda path: DummyModel(score=0.9234))

    transaction = {
        "amount": 150.0,
        "normalized_amount": 150.0,
        "merchant_category": "5411",
        "merchant_country": "US",
    }

    score = scoring.score_transaction(transaction)

    assert score == pytest.approx(0.9234, abs=0.0001)
    assert 0.0 <= score <= 1.0


def test_apply_business_rules_triggers_review_for_high_risk(monkeypatch):
    fake_settings = FakeSettings(threshold=0.8, blacklist="MX,CA")
    monkeypatch.setattr("app.rules.get_settings", lambda: fake_settings)

    transaction = {
        "merchant_country": "MX",
        "normalized_amount": 20000,
    }
    result = apply_business_rules(transaction, score=0.95)

    assert result["status"] == "review"
    assert "Risk score exceeds threshold" in result["reason"]
    assert "Merchant country is blacklisted" in result["reason"]
    assert "High amount transaction" in result["reason"]
    assert result["should_alert"] is True


def test_apply_business_rules_allows_low_risk(monkeypatch):
    fake_settings = FakeSettings(threshold=0.9, blacklist="FR")
    monkeypatch.setattr("app.rules.get_settings", lambda: fake_settings)

    transaction = {"merchant_country": "US", "normalized_amount": 25}
    result = apply_business_rules(transaction, score=0.2)

    assert result["status"] == "approved"
    assert result["reason"] == "Automated approval"
    assert result["should_alert"] is False
