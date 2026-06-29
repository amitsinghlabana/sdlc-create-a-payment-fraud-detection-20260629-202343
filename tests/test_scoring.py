import pytest
from fastapi.testclient import TestClient
from app.api import create_app

client = TestClient(create_app())

@pytest.mark.parametrize("amount,status", [
    (10.0, "approved"),
    (20000.0, "review")
])
def test_transaction_assess(amount, status):
    payload = {
        "transaction_id": "tx12345",
        "account_id": "acct1",
        "amount": amount,
        "currency": "USD",
        "merchant_category": "5411",
        "timestamp": "2023-09-01T00:00:00Z",
        "merchant_country": "US",
        "ip_address": "10.0.0.1",
    }
    response = client.post("/transactions/assess", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == status
