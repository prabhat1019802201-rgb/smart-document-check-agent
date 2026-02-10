from sqlalchemy import Column, String, DateTime, Integer, Float, ForeignKey
from datetime import datetime
from app.db.base import Base


class ValidationResult(Base):
    __tablename__ = "validation_results"

    validation_id = Column(String, primary_key=True, index=True)
    document_id = Column(String, ForeignKey("documents.document_id"), nullable=False)

    validation_status = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    issues_count = Column(Integer, nullable=False)
    ocr_confidence = Column(Float, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


class ValidationIssue(Base):
    __tablename__ = "validation_issues"

    issue_id = Column(String, primary_key=True, index=True)
    validation_id = Column(String, ForeignKey("validation_results.validation_id"))
    document_id = Column(String, ForeignKey("documents.document_id"))

    issue_type = Column(String, nullable=False)
    field_name = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    issue_description = Column(String, nullable=False)
    suggested_action = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
