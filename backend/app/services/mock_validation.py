def generate_mock_validation(document_type: str | None):
    # Mocked for now – later replaced by rule engine
    issues = [
        {
            "issue_type": "Missing",
            "field_name": "employer_address",
            "severity": "High",
            "why_flagged": "Employer address is mandatory for salary verification.",
            "suggested_action": "Upload revised salary slip with employer address."
        },
        {
            "issue_type": "Mismatch",
            "field_name": "employee_name",
            "severity": "High",
            "why_flagged": "Employee name does not match across submitted documents.",
            "suggested_action": "Verify name consistency across all documents."
        }
    ]

    return {
        "validation_summary": {
            "status": "PARTIAL",
            "issues_found": len(issues),
            "severity": "HIGH",
            "ocr_confidence": 0.82
        },
        "issues": issues
    }
