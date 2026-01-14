
def extract_mock_fields(document_type: str) -> dict:
    """
    Central mock extractor.
    Acts as a placeholder for PyPDF / OCR.
    """

    doc_type = (document_type or "").strip().lower()

    # -------------------------
    # PAN CARD
    # -------------------------
    if doc_type == "pan":
        return {
            "pan_number": "ABCDE1234F",
            "name": "RAVI KUMAR",
            "dob": "1992-05-12"
        }

    # -------------------------
    # AADHAAR CARD
    # -------------------------
    if doc_type == "aadhaar":
        return {
            "aadhaar_number": "123412341234",
            "name": "RAVI KUMAR",
            "dob": "1992-05-12",
            "gender": "Male",
            "address": "Bangalore, Karnataka"
        }

    # -------------------------
    # CIBIL REPORT
    # -------------------------
    if doc_type == "cibil":
        return {
            "name": "RAVI KUMAR",
            "cibil_score": 720,
            "report_date": "2025-12-01"
        }

    # -------------------------
    # LOAN REQUEST FORM
    # -------------------------
    if doc_type == "loan request form":
        return {
            "applicant_name": "RAVI KUMAR",
            "loan_amount": 1500000,
            "loan_tenure_months": 240,
            "employment_type": "Salaried",  # Salaried / Self-employed
            "monthly_income": 85000,
            "company_name": None,  # intentionally missing
            "residential_address": "Bangalore, Karnataka"
        }

    # -------------------------
    # INCOME PROOF - SALARY SLIP
    # -------------------------
    if doc_type == "income_proof_salary_slip":
        return {
            "income_proof_type": "salary_slip",
            "employment_status": "Salaried",
            "company_name": "ABC Technologies Pvt Ltd",
            "employer_address": None,  # missing on purpose
            "gross_income": 570900.00,
            "net_income": 509300.03,
            "income_period": "Monthly"
        }

    # -------------------------
    # INCOME PROOF - CERTIFICATE
    # -------------------------
    if doc_type == "income_proof_certificate":
        return {
            "income_proof_type": "income_certificate",
            "employment_status": "Unemployed",
            "company_name": "SELF / NA",
            "gross_income": 300000.00,
            "net_income": 300000.00,
            "income_period": "Annual"
        }

    # -------------------------
    # DEFAULT
    # -------------------------
    return {}





