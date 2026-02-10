import uuid
from datetime import date, datetime
from sqlalchemy.orm import Session

from app.models.case_document import CaseDocument


# -------------------------------------------------
# Helper: Make extracted fields JSON-serializable
# -------------------------------------------------
def make_json_safe(value):
    """
    Recursively convert non-JSON-serializable objects
    (date, datetime) into ISO format strings.
    """
    if isinstance(value, dict):
        return {k: make_json_safe(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [make_json_safe(v) for v in value]
    elif isinstance(value, (date, datetime)):
        return value.isoformat()
    else:
        return value


# -------------------------------------------------
# Persist document fields for a case
# -------------------------------------------------
def persist_case_document(
    db: Session,
    case_id: str,
    document_type: str,
    extracted_fields: dict
):
    safe_fields = make_json_safe(extracted_fields)

    record = CaseDocument(
        id=str(uuid.uuid4()),
        case_id=case_id,
        document_type=document_type,
        extracted_fields=safe_fields
    )

    db.add(record)
    db.commit()


# -------------------------------------------------
# Load all documents for a case
# -------------------------------------------------
def load_case_documents(db: Session, case_id: str) -> dict:
    records = (
        db.query(CaseDocument)
        .filter(CaseDocument.case_id == case_id)
        .all()
    )

    documents = {}
    for record in records:
        documents[record.document_type] = record.extracted_fields

    return documents
