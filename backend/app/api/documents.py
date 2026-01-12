from fastapi import APIRouter, UploadFile, File, Form, Depends
from datetime import datetime
import uuid
from sqlalchemy.orm import Session

from app.schemas.document import DocumentUploadResponse
from app.db.deps import get_db
from app.models.document import Document
from app.services.mock_validation import generate_mock_validation

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    document_type: str | None = Form(default=None),
    db: Session = Depends(get_db)
):
    document_id = str(uuid.uuid4())

    doc = Document(
        document_id=document_id,
        document_type=document_type,
        file_name=file.filename,
        upload_status="UPLOADED"
    )

    db.add(doc)
    db.commit()

    mock_validation = generate_mock_validation(document_type)

    return {
        "document_id": document_id,
        "document_type": document_type,
        "upload_status": "UPLOADED",
        "uploaded_at": datetime.utcnow(),
        **mock_validation
    }

