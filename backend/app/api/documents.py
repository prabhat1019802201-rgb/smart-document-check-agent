from fastapi import APIRouter, UploadFile, File, Form, Depends
from datetime import datetime
import uuid
import os
import shutil
from tempfile import NamedTemporaryFile
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.document import Document

from app.agents.orchestrator import build_validation_graph

from app.services.validation_persistence import persist_validation_results
from app.services.genai_explanation_persistence import persist_genai_explanations
from app.services.historical_memory_service import store_historical_issue_pattern
from app.services.case_document_store import (
    persist_case_document,
    load_case_documents
)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    document_type: str | None = Form(default=None),
    case_id: str | None = Form(default=None),
    db: Session = Depends(get_db)
):
    # -------------------------------------------------
    # Step 0: IDs
    # -------------------------------------------------
    document_id = str(uuid.uuid4())
    if not case_id:
        case_id = str(uuid.uuid4())

    normalized_doc_type = (
        (document_type or "")
        .strip()
        .lower()
        .replace(" ", "_")
    )

    # -------------------------------------------------
    # Step 1: Persist document metadata
    # -------------------------------------------------
    doc = Document(
        document_id=document_id,
        document_type=normalized_doc_type,
        file_name=file.filename,
        upload_status="UPLOADED"
    )
    db.add(doc)
    db.commit()

    # -------------------------------------------------
    # Step 2: Save uploaded file to disk (CRITICAL)
    # -------------------------------------------------
    suffix = os.path.splitext(file.filename)[-1] or ".pdf"

    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        file_path = tmp.name

    # -------------------------------------------------
    # Step 3: Load existing case documents
    # -------------------------------------------------
    documents_by_type = load_case_documents(db, case_id)

    # -------------------------------------------------
    # Step 4: Run LangGraph pipeline
    # -------------------------------------------------
    graph = build_validation_graph()

    initial_state = {
        "case_id": case_id,
        "document_id": document_id,
        "document_type": normalized_doc_type,

        # 🔑 REQUIRED FOR PyPDF
        "file_path": file_path,

        "extracted_fields": {},
        "documents_by_type": documents_by_type,

        "issues": [],
        "validation_status": "",
        "severity": "",
        "ocr_confidence": 0.0,

        "db": db
    }

    result_state = graph.invoke(initial_state)

    issues = result_state.get("issues", [])
    status = result_state.get("validation_status", "PARTIAL")
    severity = result_state.get("severity", "MEDIUM")
    ocr_confidence = result_state.get("ocr_confidence", 0.0)
    extracted_fields = result_state.get("extracted_fields", {})

    # -------------------------------------------------
    # Step 5: Persist extracted fields per case
    # -------------------------------------------------
    persist_case_document(
        db=db,
        case_id=case_id,
        document_type=normalized_doc_type,
        extracted_fields=extracted_fields
    )

    # -------------------------------------------------
    # Step 6: Persist validation results
    # -------------------------------------------------
    validation_id = persist_validation_results(
        db=db,
        document_id=document_id,
        status=status,
        severity=severity,
        ocr_confidence=ocr_confidence,
        issues=issues
    )

    # -------------------------------------------------
    # Step 7: Historical learning (positive cases)
    # -------------------------------------------------
    if status == "PASS":
        store_historical_issue_pattern(
            db=db,
            document_type=normalized_doc_type,
            issue_type="Resolved",
            field_name="all",
            resolution="Document passed validation"
        )

    # -------------------------------------------------
    # Step 8: Persist GenAI explanations
    # -------------------------------------------------
    persist_genai_explanations(
        db=db,
        validation_id=validation_id,
        issues=issues,
        llm_model="llama3.1"
    )

    # -------------------------------------------------
    # Step 9: API response
    # -------------------------------------------------
    response = {
      "case_id": case_id,
      "document_id": document_id,
      "document_type": normalized_doc_type,
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

    return JSONResponse(content=jsonable_encoder(response))
