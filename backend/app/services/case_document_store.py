import uuid
from sqlalchemy.orm import Session
from app.models.case_document import CaseDocument


def persist_case_document(
    db: Session,
    case_id: str,
    document_type: str,
    extracted_fields: dict
):
    record = CaseDocument(
        id=str(uuid.uuid4()),
        case_id=case_id,
        document_type=document_type,
        extracted_fields=extracted_fields
    )

    db.add(record)
    db.commit()


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


