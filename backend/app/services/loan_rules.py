def validate_loan_request_form(fields: dict):
    issues = []

    applicant_name = fields.get("applicant_name")
    loan_amount = fields.get("loan_amount")
    loan_tenure = fields.get("loan_tenure_months")
    employment_type = fields.get("employment_type")
    monthly_income = fields.get("monthly_income")
    company_name = fields.get("company_name")

    # 1. Applicant name
    if not applicant_name:
        issues.append({
            "issue_type": "Missing",
            "field_name": "applicant_name",
            "severity": "High",
            "why_flagged": "Applicant name is mandatory in loan request form.",
            "suggested_action": "Provide applicant full name."
        })

    # 2. Loan amount
    if loan_amount is None or loan_amount <= 0:
        issues.append({
            "issue_type": "Invalid",
            "field_name": "loan_amount",
            "severity": "High",
            "why_flagged": "Loan amount must be greater than zero.",
            "suggested_action": "Provide a valid loan amount."
        })

    # 3. Loan tenure
    if loan_tenure is None or loan_tenure <= 0:
        issues.append({
            "issue_type": "Invalid",
            "field_name": "loan_tenure_months",
            "severity": "Medium",
            "why_flagged": "Loan tenure must be a positive number.",
            "suggested_action": "Provide a valid loan tenure."
        })

    # 4. Monthly income
    if monthly_income is None or monthly_income <= 0:
        issues.append({
            "issue_type": "Invalid",
            "field_name": "monthly_income",
            "severity": "High",
            "why_flagged": "Monthly income must be greater than zero.",
            "suggested_action": "Provide a valid monthly income."
        })

    # 5. Company name (only if salaried)
    if employment_type == "Salaried":
        if not company_name or company_name.strip().lower() in {"na", "self"}:
            issues.append({
                "issue_type": "Missing",
                "field_name": "company_name",
                "severity": "Medium",
                "why_flagged": "Company name is required for salaried applicants.",
                "suggested_action": "Provide employer company name."
            })

    return issues
