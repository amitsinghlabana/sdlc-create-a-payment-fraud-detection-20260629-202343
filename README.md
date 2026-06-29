# Payment Fraud Detection System

## Overview
A FastAPI‑based service that ingests transaction data, applies feature engineering, scores fraud risk using a pre‑trained ML model, evaluates deterministic business rules, and emits alerts for high‑risk transactions.

## Running the Service

1. **Clone the repo**
   ```bash
   git clone https://your.repo.url/payment-fraud-detection.git
   cd payment-fraud-detection
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the API**
   ```bash
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Endpoints

| Endpoint                   | Method | Description                                      |
|----------------------------|--------|--------------------------------------------------|
| `/transactions`            | POST   | Ingests a new transaction for processing         |
| `/transactions/score`      | POST   | Returns fraud risk score and rule evaluation     |
| `/alerts`                  | GET    | Retrieves recent fraud alerts                    |

### Example: Score a Transaction
```bash
curl -X POST http://localhost:8000/transactions/score \
  -H 'Content-Type: application/json' \
  -d '{
        "transaction_id": "txn_12345",
        "user_id": "user_67890",
        "amount": 250.00,
        "currency": "USD",
        "timestamp": "2023-10-05T12:34:56Z",
        "metadata": { "ip": "203.0.113.4" }
      }'
```

_Response:_
```json
{
  "transaction_id": "txn_12345",
  "risk_score": 0.87,
  "flags": ["high_velocity", "blacklisted_ip"]
}
```

## Testing

Run the pytest suite to validate scoring, ingestion, rules, and alerts:

```bash
pytest --maxfail=1 --disable-warnings -q
```

---

*For full details on internal modules and configuration, refer to the `src/app/` directory and `stories.json`.*