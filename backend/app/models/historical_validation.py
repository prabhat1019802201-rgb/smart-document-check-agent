from sqlalchemy import Column, String, DateTime
from datetime import datetime
from app.db.base import Base


class HistoricalValidationMemory(Base):
    __tablename__ = "historical_validation_memory"

    record_id = Column(String, primary_key=True, index=True)
    document_type = Column(String, index=True)
    issue_pattern = Column(String)
    resolution = Column(String)
    created_date = Column(DateTime, default=datetime.utcnow)
