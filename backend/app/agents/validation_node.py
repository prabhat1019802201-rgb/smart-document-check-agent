from app.services.salary_slip_rules import validate_salary_slip

def validation_node(state):
    issues = []

    if state["document_type"] == "Salary Slip":
        issues = validate_salary_slip(state["extracted_fields"])

    state["issues"] = issues

    if not issues:
        state["validation_status"] = "PASS"
        state["severity"] = "LOW"
    elif len(issues) <= 2:
        state["validation_status"] = "PARTIAL"
        state["severity"] = "HIGH"
    else:
        state["validation_status"] = "FAIL"
        state["severity"] = "HIGH"

    state["ocr_confidence"] = 0.82

    return state
