def validate_income_proof(fields: dict):
    issues = []

    proof_type = fields.get("income_proof_type")
    employment_status = fields.get("employment_status")

    # -----------------------------
    # Salary Slip Rules
    # -----------------------------
    if proof_type == "salary_slip":
        if not fields.get("company_name"):
            issues.append({
                "issue_type": "Missing",
                "field_name": "company_name",
                "severity": "High",
                "why_flagged": "Company name is mandatory for salaried income proof.",
                "suggested_action": "Upload salary slip with employer details."
            })

        if fields.get("net_income", 0) > fields.get("gross_income", 0):
            issues.append({
                "issue_type": "Invalid",
                "field_name": "net_income",
                "severity": "High",
                "why_flagged": "Net income cannot exceed gross income.",
                "suggested_action": "Verify income figures in the salary slip."
            })

    # -----------------------------
    # Income Certificate Rules
    # -----------------------------
    elif proof_type == "income_certificate":
        company_name = fields.get("company_name", "").upper()

        if company_name not in ["SELF", "NA", "SELF / NA"]:
            issues.append({
                "issue_type": "Invalid",
                "field_name": "company_name",
                "severity": "Medium",
                "why_flagged": (
                    "For income certificate, company name should be SELF or NA."
                ),
                "suggested_action": (
                    "Set company name as SELF or NA for income certificate."
                )
            })

    # -----------------------------
    # Common Income Rules
    # -----------------------------
    if not fields.get("gross_income") or fields["gross_income"] <= 0:
        issues.append({
            "issue_type": "Invalid",
            "field_name": "gross_income",
            "severity": "High",
            "why_flagged": "Income amount must be greater than zero.",
            "suggested_action": "Provide a valid income amount."
        })

    return issues
