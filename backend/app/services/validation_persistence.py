import uuid
from sqlalchemy.orm import Session
from app.models.validation import ValidationResult, ValidationIssue


def persist_validation_results(
    db: Session,
    document_id: str,
    status: str,
    severity: str,
    ocr_confidence: float,
    issues: list
):
    validation_id = str(uuid.uuid4())

    validation_result = ValidationResult(
        validation_id=validation_id,
        document_id=document_id,
        validation_status=status,
        severity=severity,
        issues_count=len(issues),
        ocr_confidence=ocr_confidence
    )

    db.add(validation_result)

    for issue in issues:
        validation_issue = ValidationIssue(
            issue_id=str(uuid.uuid4()),
            validation_id=validation_id,
            document_id=document_id,
            issue_type=issue["issue_type"],
            field_name=issue["field_name"],
            severity=issue["severity"],
            issue_description=issue["why_flagged"],
            suggested_action=issue["suggested_action"]
        )
        db.add(validation_issue)

    db.commit()

    return validation_id
