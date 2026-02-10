def validate_cibil_report(fields: dict):
    issues = []

    score = fields.get("cibil_score")

    if score is None:
        issues.append({
            "issue_type": "Missing",
            "field_name": "cibil_score",
            "severity": "High",
            "why_flagged": "CIBIL score is missing from the report.",
            "suggested_action": "Upload a CIBIL report containing the credit score."
        })
    elif score < 300 or score > 900:
        issues.append({
            "issue_type": "Invalid",
            "field_name": "cibil_score",
            "severity": "High",
            "why_flagged": "CIBIL score must be between 300 and 900.",
            "suggested_action": "Upload a valid CIBIL report."
        })

    if not fields.get("report_date"):
        issues.append({
            "issue_type": "Missing",
            "field_name": "report_date",
            "severity": "Medium",
            "why_flagged": "CIBIL report date is missing.",
            "suggested_action": "Upload a recent CIBIL report."
        })

    if not fields.get("name"):
        issues.append({
            "issue_type": "Missing",
            "field_name": "name",
            "severity": "High",
            "why_flagged": "Customer name is missing in the CIBIL report.",
            "suggested_action": "Upload a CIBIL report with customer name visible."
        })

    return issues
