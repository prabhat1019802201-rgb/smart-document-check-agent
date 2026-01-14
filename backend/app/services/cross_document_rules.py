def validate_cross_document_consistency(documents: dict):
    """
    documents: {
        "loan_request_form": {...},
        "pan": {...},
        "aadhaar": {...},
        "income_proof": {...}
    }
    """
    issues = []

    # -----------------------------
    # 1. Name consistency
    # -----------------------------
    lrf_name = documents.get("loan_request_form", {}).get("applicant_name")
    pan_name = documents.get("pan", {}).get("name")
    aadhaar_name = documents.get("aadhaar", {}).get("name")

    if lrf_name and pan_name and lrf_name != pan_name:
        issues.append({
            "issue_type": "Mismatch",
            "field_name": "applicant_name",
            "severity": "High",
            "why_flagged": (
                "Applicant name in Loan Request Form does not match PAN card."
            ),
            "suggested_action": (
                "Ensure applicant name matches PAN card across documents."
            )
        })

    if pan_name and aadhaar_name and pan_name != aadhaar_name:
        issues.append({
            "issue_type": "Mismatch",
            "field_name": "name",
            "severity": "High",
            "why_flagged": (
                "Name on PAN card does not match Aadhaar card."
            ),
            "suggested_action": (
                "Verify and correct name consistency across PAN and Aadhaar."
            )
        })

    # -----------------------------
    # 2. Date of birth consistency
    # -----------------------------
    pan_dob = documents.get("pan", {}).get("dob")
    aadhaar_dob = documents.get("aadhaar", {}).get("dob")

    if pan_dob and aadhaar_dob and pan_dob != aadhaar_dob:
        issues.append({
            "issue_type": "Mismatch",
            "field_name": "dob",
            "severity": "High",
            "why_flagged": (
                "Date of birth does not match between PAN and Aadhaar."
            ),
            "suggested_action": (
                "Verify date of birth consistency across identity documents."
            )
        })

    # -----------------------------
    # 3. Income consistency
    # -----------------------------
    declared_income = documents.get("loan_request_form", {}).get("monthly_income")
    income_proof = documents.get("income_proof", {})

    proof_income = income_proof.get("net_income") or income_proof.get("gross_income")

    if declared_income and proof_income:
        if abs(declared_income - proof_income) > 0.2 * proof_income:
            issues.append({
                "issue_type": "Mismatch",
                "field_name": "monthly_income",
                "severity": "Medium",
                "why_flagged": (
                    "Declared income in loan request form significantly differs "
                    "from income proof."
                ),
                "suggested_action": (
                    "Recheck declared income or upload updated income proof."
                )
            })

    return issues
