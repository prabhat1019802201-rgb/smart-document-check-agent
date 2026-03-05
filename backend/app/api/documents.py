from fastapi import APIRouter, UploadFile, File, Form, Depends
from datetime import datetime
import uuid
import os
import shutil
from tempfile import NamedTemporaryFile
from sqlalchemy.orm import Session
from typing import List

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

from app.services.extraction.pdf_text_extractor import extract_text_from_pdf
from app.services.classifier.document_classifier import detect_document_type

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/documents", tags=["Documents"])


# -------------------------------------------------
# REQUIRED DOCUMENT CHECKLIST (NEW FEATURE)
# -------------------------------------------------
REQUIRED_DOCUMENTS = {
    "aadhaar",
    "pan",
    "cibil",
    "income_proof",
    "loan_application_form"
}


@router.post("/upload")
async def upload_document(
    files: List[UploadFile] = File(...),
    document_type: str | None = Form(default=None),
    case_id: str | None = Form(default=None),
    db: Session = Depends(get_db)
):

    responses = []

    # -------------------------------------------------
    # Create Case ID if not provided
    # -------------------------------------------------
    if not case_id:
        case_id = str(uuid.uuid4())

    # -------------------------------------------------
    # Process each uploaded file
    # -------------------------------------------------
    for file in files:

        document_id = str(uuid.uuid4())

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
        # Step 2: Save uploaded file to disk
        # -------------------------------------------------
        suffix = os.path.splitext(file.filename)[-1] or ".pdf"

        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            file_path = tmp.name

        print(f"DEBUG | file_path: {file_path}", flush=True)

        # -------------------------------------------------
        # Step 3: AUTO CLASSIFY DOCUMENT
        # -------------------------------------------------
        try:
            raw_text = extract_text_from_pdf(file_path)

            detected_doc_type = detect_document_type(raw_text)

            print(f"DEBUG | Auto-detected document type: {detected_doc_type}", flush=True)

            if detected_doc_type:
                normalized_doc_type = detected_doc_type
                doc.document_type = normalized_doc_type
                db.commit()

        except Exception as e:
            print(f"DEBUG | Document classification failed: {e}", flush=True)

        # -------------------------------------------------
        # Step 4: Load existing case documents
        # -------------------------------------------------
        documents_by_type = load_case_documents(db, case_id)

        # -------------------------------------------------
        # Step 5: Run LangGraph pipeline
        # -------------------------------------------------
        graph = build_validation_graph()

        initial_state = {
            "case_id": case_id,
            "document_id": document_id,
            "document_type": normalized_doc_type,

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
        # Step 6: Persist extracted fields per case
        # -------------------------------------------------
        persist_case_document(
            db=db,
            case_id=case_id,
            document_type=normalized_doc_type,
            extracted_fields=extracted_fields
        )

        # -------------------------------------------------
        # Step 7: Persist validation results
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
        # Step 8: Historical learning
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
        # Step 9: Persist GenAI explanations
        # -------------------------------------------------
        persist_genai_explanations(
            db=db,
            validation_id=validation_id,
            issues=issues,
            llm_model="llama3.1"
        )

        # -------------------------------------------------
        # Step 10: Store response for this document
        # -------------------------------------------------
        responses.append({
            "document_id": document_id,
            "document_type": normalized_doc_type,
            "file_name": file.filename,
            "upload_status": "UPLOADED",
            "uploaded_at": datetime.utcnow(),
            "validation_summary": {
                "status": status,
                "issues_found": len(issues),
                "severity": severity,
                "ocr_confidence": ocr_confidence
            },
            "issues": issues
        })

    # -------------------------------------------------
    # Step 11: Detect uploaded documents
    # -------------------------------------------------
    uploaded_doc_types = {r["document_type"] for r in responses}

    # -------------------------------------------------
    # Step 12: Detect missing documents
    # -------------------------------------------------
    missing_documents = list(REQUIRED_DOCUMENTS - uploaded_doc_types)

    case_status = "COMPLETE"

    if missing_documents:
        case_status = "INCOMPLETE"

    # -------------------------------------------------
    # Step 13: Final API response
    # -------------------------------------------------
    return JSONResponse(
        content=jsonable_encoder({
            "case_id": case_id,
            "case_status": case_status,

            "documents_processed": len(responses),

            "uploaded_documents": list(uploaded_doc_types),

            "missing_documents": missing_documents,

            "results": responses
        })
    )

