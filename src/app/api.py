from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from app.ingestion import ingest_transaction
from app.scoring import score_transaction
from app.rules import apply_business_rules
from app.alerts import publish_alert_if_needed
from app.telemetry import record_latency
from app.db import get_session, TransactionRecord

class TransactionRequest(BaseModel):
    transaction_id: str = Field(..., min_length=6)
    account_id: str
    amount: float
    currency: str
    merchant_category: str
    timestamp: str
    merchant_country: str
    ip_address: str

class TransactionResponse(BaseModel):
    transaction_id: str
    status: str
    risk_score: float
    reason: str


def create_app() -> FastAPI:
    app = FastAPI(title="Payment Fraud Detection")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.post("/transactions/assess", response_model=TransactionResponse)
    async def assess_transaction(req: TransactionRequest, background_tasks: BackgroundTasks):
        with record_latency("api.assess"):
            session = next(get_session())
            ingested = ingest_transaction(req.dict())
            score = score_transaction(ingested)
            rule_result = apply_business_rules(ingested, score)

            transaction = TransactionRecord(
                transaction_id=req.transaction_id,
                payload=req.dict(),
                risk_score=score,
                status=rule_result["status"],
                reason=rule_result["reason"],
            )
            session.add(transaction)
            session.commit()
            if rule_result["should_alert"]:
                background_tasks.add_task(publish_alert_if_needed, transaction)
            return TransactionResponse(
                transaction_id=req.transaction_id,
                status=rule_result["status"],
                risk_score=score,
                reason=rule_result["reason"],
            )

    return app
