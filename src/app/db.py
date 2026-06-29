from sqlalchemy import create_engine, Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from app.config import get_settings
from contextlib import contextmanager

settings = get_settings()
ENGINE = create_engine(settings.database_url, future=True)
SessionLocal = sessionmaker(bind=ENGINE)
Base = declarative_base()

class TransactionRecord(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True)
    payload = Column(JSON)
    risk_score = Column(Float)
    status = Column(String)
    reason = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
