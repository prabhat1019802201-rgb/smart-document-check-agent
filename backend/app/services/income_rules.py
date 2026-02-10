def validate_income_proof(fields: dict):
    issues = []

    income_type = fields.get("income_proof_type")
    gross_income = fields.get("gross_income")
    net_income = fields.get("net_income")

    # 1. Income type
    if not income_type:
        issues.append({
            "issue_type": "Missing",
            "field_name": "income_proof_type",
            "severity": "High",
            "why_flagged": "Income proof type is missing.",
            "suggested_action": "Upload a valid income proof document."
        })

    # 2. Gross income
    if gross_income is None or gross_income <= 0:
        issues.append({
            "issue_type": "Invalid",
            "field_name": "gross_income",
            "severity": "High",
            "why_flagged": "Gross income must be greater than zero.",
            "suggested_action": "Provide a valid gross income value."
        })

    # 3. Net income (optional but sanity check)
    if net_income is not None and net_income <= 0:
        issues.append({
            "issue_type": "Invalid",
            "field_name": "net_income",
            "severity": "Medium",
            "why_flagged": "Net income must be greater than zero.",
            "suggested_action": "Provide a valid net income value."
        })

    return issues
