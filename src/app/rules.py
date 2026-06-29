from typing import Dict
from app.config import get_settings
from datetime import datetime


def apply_business_rules(transaction: Dict, score: float) -> Dict:
    settings = get_settings()
    reasons = []
    status = "approved"
    if score >= settings.high_risk_threshold:
        status = "review"
        reasons.append("Risk score exceeds threshold")
    if transaction.get("merchant_country") in settings.blacklist_countries.split(","):
        status = "review"
        reasons.append("Merchant country is blacklisted")
    if float(transaction.get("normalized_amount", 0)) > 10000:
        status = status if status == "review" else "review"
        reasons.append("High amount transaction")
    return {
        "status": status,
        "reason": "; ".join(reasons) if reasons else "Automated approval",
        "should_alert": status == "review",
        "evaluated_at": datetime.utcnow().isoformat()
    }
