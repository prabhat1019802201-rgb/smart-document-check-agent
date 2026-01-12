from sqlalchemy import Column, String, DateTime
from datetime import datetime
from app.db.base import Base


class Document(Base):
    __tablename__ = "documents"

    document_id = Column(String, primary_key=True, index=True)
    case_id = Column(String, nullable=True)
    document_type = Column(String, nullable=True)
    file_name = Column(String, nullable=False)
    upload_status = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
