import uuid
from sqlalchemy.orm import Session
from app.models.genai_explanation import GenAIExplanation


def persist_genai_explanations(
    db: Session,
    validation_id: str,
    issues: list,
    llm_model: str = "llama3.1"
):
    for issue in issues:
        explanation = GenAIExplanation(
            explanation_id=str(uuid.uuid4()),
            validation_id=validation_id,
            issue_id=issue.get("issue_id"),  # populated earlier
            why_flagged=issue["why_flagged"],
            suggested_action=issue["suggested_action"],
            llm_model=llm_model
        )
        db.add(explanation)

    db.commit()
