from fastapi import APIRouter, UploadFile, File, Form, Depends
from datetime import datetime
import uuid
from sqlalchemy.orm import Session

from app.schemas.document import DocumentUploadResponse
from app.db.deps import get_db
from app.models.document import Document
from app.services.salary_slip_rules import validate_salary_slip
from app.services.mock_extraction import mock_extract_salary_slip
from app.services.validation_persistence import persist_validation_results

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

    # Step 1: Extract fields (mocked for now)
    extracted_fields = {}

    if document_type == "Salary Slip":
        extracted_fields = mock_extract_salary_slip()

    # Step 2: Apply rule-based validation
    issues = []
    if document_type == "Salary Slip":
       issues = validate_salary_slip(extracted_fields)

    # Step 3: Determine validation status
    if not issues:
        status = "PASS"
    elif len(issues) <= 2:
       status = "PARTIAL"
    else:
        status = "FAIL"
    # Step 4: Persist validation results   
    validation_id = persist_validation_results(
    db=db,
    document_id=document_id,
    status=status,
    severity="HIGH" if issues else "LOW",
    ocr_confidence=0.82,
    issues=issues
   )
    # Step 5: Return response
    return {
        "document_id": document_id,
        "document_type": document_type,
        "upload_status": "UPLOADED",
        "uploaded_at": datetime.utcnow(),
        "validation_summary": {
        "status": status,
        "issues_found": len(issues),
        "severity": "HIGH" if issues else "LOW",
        "ocr_confidence": 0.82
      },
     "issues": issues
   }

