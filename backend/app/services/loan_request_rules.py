def validate_loan_request_form(fields: dict):
    issues = []

    mandatory_fields = [
        "applicant_name",
        "loan_amount",
        "loan_tenure_months",
        "employment_type",
        "monthly_income",
        "residential_address"
    ]

    for field in mandatory_fields:
        if not fields.get(field):
            issues.append({
                "issue_type": "Missing",
                "field_name": field,
                "severity": "High",
                "why_flagged": f"{field.replace('_', ' ').title()} is mandatory for loan processing.",
                "suggested_action": f"Provide {field.replace('_', ' ').title()} in the loan request form."
            })

    # Employment-based conditional rule
    if fields.get("employment_type") == "Salaried" and not fields.get("company_name"):
        issues.append({
            "issue_type": "Missing",
            "field_name": "company_name",
            "severity": "High",
            "why_flagged": "Company name is mandatory for salaried applicants.",
            "suggested_action": "Provide company name in the loan request form."
        })

    # Basic numeric sanity checks
    if fields.get("loan_amount") and fields["loan_amount"] <= 0:
        issues.append({
            "issue_type": "Invalid",
            "field_name": "loan_amount",
            "severity": "High",
            "why_flagged": "Loan amount must be greater than zero.",
            "suggested_action": "Enter a valid loan amount."
        })

    if fields.get("loan_tenure_months") and fields["loan_tenure_months"] <= 0:
        issues.append({
            "issue_type": "Invalid",
            "field_name": "loan_tenure_months",
            "severity": "Medium",
            "why_flagged": "Loan tenure must be a positive number of months.",
            "suggested_action": "Enter a valid loan tenure."
        })

    return issues
