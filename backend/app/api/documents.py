from fastapi import APIRouter, UploadFile, File, Form
from datetime import datetime
import uuid

from app.schemas.document import DocumentUploadResponse

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    document_type: str | None = Form(default=None)
):
    document_id = str(uuid.uuid4())

    return {
        "document_id": document_id,
        "document_type": document_type,
        "upload_status": "UPLOADED",
        "uploaded_at": datetime.utcnow()
    }


