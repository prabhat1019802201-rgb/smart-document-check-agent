import uuid
from sqlalchemy.orm import Session
from app.models.historical_validation import HistoricalValidationMemory


def store_historical_issue_pattern(
    db: Session,
    document_type: str,
    issue_type: str,
    field_name: str,
    resolution: str
):
    """
    Store recurring issue pattern for learning.
    Called AFTER issue resolution (manual or re-upload).
    """

    record = HistoricalValidationMemory(
        record_id=str(uuid.uuid4()),
        document_type=document_type,
        issue_pattern=f"{issue_type}:{field_name}",
        resolution=resolution
    )

    db.add(record)
    db.commit()
