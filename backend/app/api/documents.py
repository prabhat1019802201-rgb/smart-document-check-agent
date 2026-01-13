from fastapi import APIRouter, UploadFile, File, Form, Depends
from datetime import datetime
import uuid
from sqlalchemy.orm import Session

from app.schemas.document import DocumentUploadResponse
from app.db.deps import get_db
from app.models.document import Document
from app.services.validation_persistence import persist_validation_results
from app.agents.orchestrator import build_validation_graph
from app.services.genai_explanation_persistence import persist_genai_explanations
from app.services.historical_memory_service import store_historical_issue_pattern

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    document_type: str | None = Form(default=None),
    db: Session = Depends(get_db)
):
    # -----------------------------
    # Step 0: Create document entry
    # -----------------------------
    document_id = str(uuid.uuid4())

    doc = Document(
        document_id=document_id,
        document_type=document_type,
        file_name=file.filename,
        upload_status="UPLOADED"
    )

    db.add(doc)
    db.commit()

    # -----------------------------
    # Step 1–3: Run LangGraph flow
    # -----------------------------
    graph = build_validation_graph()

    initial_state = {
        "document_id": document_id,
        "document_type": document_type,
        "extracted_fields": {},
        "db": db ,
        "issues": [],
        "validation_status": "",
        "severity": "",
        "ocr_confidence": 0.0
    }

    result_state = graph.invoke(initial_state)
    
    issues = result_state["issues"]
    status = result_state["validation_status"]
    severity = result_state["severity"]
    ocr_confidence = result_state["ocr_confidence"]

    print("DEBUG | Issues from LangGraph:", issues)

    # -----------------------------
    # Step 4: Persist validation results
    # -----------------------------
    persist_validation_results(
        db=db,
        document_id=document_id,
        status=status,
        severity=severity,
        ocr_confidence=ocr_confidence,
        issues=issues
    )
    
    if status == "PASS":
      store_historical_issue_pattern(
        db=db,
        document_type=document_type,
        issue_type="Resolved",
        field_name="all",
        resolution="User uploaded corrected document"
      )
       
    persist_genai_explanations(
    db=db,
    validation_id=None,  # OPTIONAL: fetch latest if needed
    issues=issues,
    llm_model="llama3.1"
    )

    # -----------------------------
    # Step 5: Return API response
    # -----------------------------
    return {
        "document_id": document_id,
        "document_type": document_type,
        "upload_status": "UPLOADED",
        "uploaded_at": datetime.utcnow(),
        "validation_summary": {
            "status": status,
            "issues_found": len(issues),
            "severity": severity,
            "ocr_confidence": ocr_confidence
        },
        "issues": issues
    }
