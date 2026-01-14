from sqlalchemy import Column, String, DateTime, JSON
from datetime import datetime
from app.db.base import Base


class CaseDocument(Base):
    __tablename__ = "case_documents"

    id = Column(String, primary_key=True, index=True)
    case_id = Column(String, index=True, nullable=False)
    document_type = Column(String, nullable=False)

    extracted_fields = Column(JSON, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


