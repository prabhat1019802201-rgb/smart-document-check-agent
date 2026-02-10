def validate_loan_request_form(fields: dict):
    issues = []

    if not fields.get("applicant_name"):
        issues.append({
            "issue_type": "Missing",
            "field_name": "applicant_name",
            "severity": "High",
            "why_flagged": "Applicant name is mandatory.",
            "suggested_action": "Provide full legal name."
        })

    if not fields.get("pan_number"):
        issues.append({
            "issue_type": "Missing",
            "field_name": "pan_number",
            "severity": "High",
            "why_flagged": "PAN number is mandatory.",
            "suggested_action": "Provide PAN number."
        })

    if not fields.get("loan_amount") or fields["loan_amount"] <= 0:
        issues.append({
            "issue_type": "Invalid",
            "field_name": "loan_amount",
            "severity": "High",
            "why_flagged": "Loan amount must be greater than zero.",
            "suggested_action": "Provide valid loan amount."
        })

    if not fields.get("loan_tenure_months"):
        issues.append({
            "issue_type": "Missing",
            "field_name": "loan_tenure_months",
            "severity": "Medium",
            "why_flagged": "Loan tenure is missing.",
            "suggested_action": "Provide loan tenure in months."
        })

    if not fields.get("monthly_income") or fields["monthly_income"] <= 0:
        issues.append({
            "issue_type": "Invalid",
            "field_name": "monthly_income",
            "severity": "High",
            "why_flagged": "Monthly income must be greater than zero.",
            "suggested_action": "Provide valid income amount."
        })

    return issues
