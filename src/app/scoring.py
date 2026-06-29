from typing import Dict
import math
import joblib
from app.config import get_settings
from app.telemetry import record_metric

_model = None


def _load_model():
    global _model
    if _model is None:
        settings = get_settings()
        _model = joblib.load(settings.scoring_model_path)
    return _model


def score_transaction(transaction: Dict) -> float:
    model = _load_model()
    features = _extract_features(transaction)
    score = float(model.predict_proba([features])[0][1])
    record_metric("scoring.score", score)
    return round(score, 4)


def _extract_features(transaction: Dict):
    return [transaction.get("normalized_amount", 0),
            transaction.get("merchant_category", "").startswith("24"),
            transaction.get("merchant_country", "") in get_settings().blacklist_countries.split(",")]   
