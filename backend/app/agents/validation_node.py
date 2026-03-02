from app.services.pan_rules import validate_pan_card
from app.services.aadhaar_rules import validate_aadhaar_card
from app.services.cibil_rules import validate_cibil_report
from app.services.income_rules import validate_income_proof
from app.services.loan_rules import validate_loan_request_form


def validation_node(state):
    document_type = (state.get("document_type") or "").lower()
    fields = state.get("extracted_fields", {})

    print("DEBUG | validation_node document_type:", document_type)

    issues = []

    if document_type == "pan":
        issues = validate_pan_card(fields)

    elif document_type == "aadhaar":
        issues = validate_aadhaar_card(fields)

    elif document_type == "cibil":
        issues = validate_cibil_report(fields)

    elif document_type == "income_proof":
        issues = validate_income_proof(fields)

    elif document_type in ["loan_request_form", "loan_application_form"]:
        issues = validate_loan_request_form(fields)

    else:
        issues.append({
            "issue_type": "Unsupported",
            "field_name": "document_type",
            "severity": "Medium",
            "why_flagged": "This document type is not currently supported for automated validation.",
            "suggested_action": "Please submit a supported document or route this document for manual review."
        })

    # --------------------------------------------------
    # Set overall status safely
    # --------------------------------------------------
    if not issues:
        state["validation_status"] = "PASS"
        state["severity"] = "LOW"
    else:
        state["validation_status"] = "PARTIAL"

        # Safe severity handling
        severity_levels = {"LOW": 1, "Medium": 2, "MEDIUM": 2, "High": 3, "HIGH": 3}
        max_issue = max(issues, key=lambda x: severity_levels.get(x.get("severity", "LOW"), 1))
        state["severity"] = max_issue.get("severity", "LOW")

    state["issues"] = issues

    return state