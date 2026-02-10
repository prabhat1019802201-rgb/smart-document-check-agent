from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


# -------------------------------------------------
# Highlight metadata for document preview
# -------------------------------------------------
class HighlightMeta(BaseModel):
    page: int
    x: int
    y: int
    width: int
    height: int


# -------------------------------------------------
# Validation issue schema
# -------------------------------------------------
class ValidationIssue(BaseModel):
    issue_type: str
    field_name: str
    severity: str
    why_flagged: str
    suggested_action: str
    highlight: Optional[HighlightMeta] = None


# -------------------------------------------------
# Validation summary schema
# -------------------------------------------------
class ValidationSummary(BaseModel):
    status: str
    issues_found: int
    severity: str
    ocr_confidence: float


# -------------------------------------------------
# Document upload response
# -------------------------------------------------
class DocumentUploadResponse(BaseModel):
    document_id: str
    document_type: Optional[str]
    upload_status: str
    uploaded_at: datetime
    validation_summary: ValidationSummary
    issues: List[ValidationIssue]


