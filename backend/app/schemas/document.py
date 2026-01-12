from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class ValidationSummary(BaseModel):
    status: str
    issues_found: int
    severity: str
    ocr_confidence: float


class ValidationIssue(BaseModel):
    issue_type: str
    field_name: str
    severity: str
    why_flagged: str
    suggested_action: str


class DocumentUploadResponse(BaseModel):
    document_id: str
    document_type: Optional[str]
    upload_status: str
    uploaded_at: datetime
    validation_summary: ValidationSummary
    issues: List[ValidationIssue]
