from functools import lru_cache
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    database_url: str = Field(..., env="DATABASE_URL")
    alert_webhook: str = Field(..., env="ALERT_WEBHOOK")
    scoring_model_path: str = Field("models/fraud_model.joblib", env="SCORING_MODEL_PATH")
    high_risk_threshold: float = Field(0.8, env="HIGH_RISK_THRESHOLD")
    blacklist_countries: str = Field("", env="BLACKLIST_COUNTRIES")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
