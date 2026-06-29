from typing import Dict
import hashlib
from datetime import datetime

from app.telemetry import record_metric

PII_FIELDS = {"ip_address"}


def ingest_transaction(payload: Dict) -> Dict:
    sanitized = {k: (hashlib.sha256(v.encode()).hexdigest() if k in PII_FIELDS else v)
                 for k, v in payload.items()}
    sanitized["normalized_amount"] = round(float(payload["amount"]), 2)
    sanitized["ingested_at"] = datetime.utcnow().isoformat()
    record_metric("ingestion.count", 1)
    return sanitized
