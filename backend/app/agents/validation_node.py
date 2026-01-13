from app.services.salary_slip_rules import validate_salary_slip
from app.core.constants import SUPPORTED_DOCUMENT_TYPES
from app.services.highlight_generator import generate_mock_highlight
from app.services.pan_rules import validate_pan_card
from app.services.aadhaar_rules import validate_aadhaar_card
from app.services.cibil_rules import validate_cibil_report
from app.services.loan_request_rules import validate_loan_request_form
from app.services.income_proof_rules import validate_income_proof



def validation_node(state):
    """
    Deterministic validation agent.

    Responsibilities:
    - Perform rule-based validation for supported document types
    - Handle unsupported documents transparently
    - Attach highlight metadata for document preview
    - NEVER use GenAI for decisions
    """

    doc_type_raw = (state.get("document_type") or "").strip().lower()
    issues = []

    # -------------------------------------------------
    # 1. Unsupported document handling (early exit)
    # -------------------------------------------------
    if doc_type_raw not in SUPPORTED_DOCUMENT_TYPES:
        issues.append({
            "issue_type": "Unsupported",
            "field_name": "document_type",
            "severity": "Medium",
            "why_flagged": (
                "This document type is not currently supported for "
                "automated validation."
            ),
            "suggested_action": (
                "Please submit a supported document or route this "
                "document for manual review."
            )
        })

        # Attach highlight metadata if available
        for issue in issues:
            highlight = generate_mock_highlight(issue["field_name"])
            if highlight:
                issue["highlight"] = highlight

        state["issues"] = issues
        state["validation_status"] = "PARTIAL"
        state["severity"] = "MEDIUM"
        state["ocr_confidence"] = 0.0

        return state

    # -------------------------------------------------
    # 2. Supported document validation
    # -------------------------------------------------
    # Always initialize
    fields = state.get("extracted_fields") or {}
    issues = []

    if doc_type_raw == "income_proof":
       issues = validate_income_proof(fields)

    elif doc_type_raw == "pan":
        issues = validate_pan_card(fields)

    elif doc_type_raw == "aadhaar":
       issues = validate_aadhaar_card(fields)

    elif doc_type_raw == "cibil":
       issues = validate_cibil_report(fields)

    elif doc_type_raw == "loan request form":
       issues = validate_loan_request_form(fields)

    else:
       # Explicit fallback (VERY IMPORTANT)
      issues.append({
        "issue_type": "Unsupported",
        "field_name": "document_type",
        "severity": "Medium",
        "why_flagged": (
            f"Validation rules are not defined for document type: {doc_type_raw}"
        ),
        "suggested_action": (
            "Please submit a supported document or route for manual review."
        )
    })

    state["issues"] = issues

    
    # -------------------------------------------------
    # 3. Attach highlight metadata to issues
    # -------------------------------------------------
    for issue in issues:
        highlight = generate_mock_highlight(issue["field_name"])
        if highlight:
            issue["highlight"] = highlight

    state["issues"] = issues

    # -------------------------------------------------
    # 4. Determine validation outcome
    # -------------------------------------------------
    if not issues:
        state["validation_status"] = "PASS"
        state["severity"] = "LOW"
    elif len(issues) <= 2:
        state["validation_status"] = "PARTIAL"
        state["severity"] = "HIGH"
    else:
        state["validation_status"] = "FAIL"
        state["severity"] = "HIGH"

    # -------------------------------------------------
    # 5. OCR confidence (mocked for now)
    # -------------------------------------------------
    state["ocr_confidence"] = 0.82

    return state
