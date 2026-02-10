from sqlalchemy import Column, String, DateTime, ForeignKey
from datetime import datetime
from app.db.base import Base


class GenAIExplanation(Base):
    __tablename__ = "genai_explanations"

    explanation_id = Column(String, primary_key=True, index=True)
    validation_id = Column(String, ForeignKey("validation_results.validation_id"))
    issue_id = Column(String, ForeignKey("validation_issues.issue_id"))

    why_flagged = Column(String, nullable=False)
    suggested_action = Column(String, nullable=False)

    llm_model = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
