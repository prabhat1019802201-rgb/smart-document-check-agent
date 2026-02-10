from sqlalchemy.orm import Session
from app.models.historical_validation import HistoricalValidationMemory


def fetch_historical_context(
    db: Session,
    document_type: str,
    issue_type: str,
    field_name: str,
    limit: int = 3
):
    """
    Fetch historical resolution patterns for a given issue.
    Read-only. No decision-making.
    """

    pattern_key = f"{issue_type}:{field_name}"

    records = (
        db.query(HistoricalValidationMemory)
        .filter(
            HistoricalValidationMemory.document_type == document_type,
            HistoricalValidationMemory.issue_pattern == pattern_key
        )
        .order_by(HistoricalValidationMemory.created_date.desc())
        .limit(limit)
        .all()
    )

    if not records:
        return None

    return [r.resolution for r in records]
