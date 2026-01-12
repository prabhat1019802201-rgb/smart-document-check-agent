from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DocumentUploadResponse(BaseModel):
    document_id: str
    document_type: Optional[str]
    upload_status: str
    uploaded_at: datetime


    