import re


def _normalize(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).upper()


def detect_document_type(raw_text: str) -> str:

    text = _normalize(raw_text)

    # ---------------------------------------------------
    # Loan Application (CHECK FIRST)
    # ---------------------------------------------------
    if (
        "LOAN APPLICATION FORM" in text
        or "REQUESTED AMOUNT" in text
        or "LOAN TENURE" in text
        or "APPLICANT PRIMARY INFORMATION" in text
        or "INTEREST RATE PREFERENCE" in text
    ):
        return "loan_application_form"

    # ---------------------------------------------------
    # CIBIL
    # ---------------------------------------------------
    if (
        "CIBIL SCORE" in text
        or "TRANSUNION" in text
        or "CIBIL REPORT" in text
    ):
        return "cibil"

    # ---------------------------------------------------
    # Income Proof
    # ---------------------------------------------------
    if (
        "SALARY CERTIFICATE" in text
        or "THIS IS TO CERTIFY" in text
        or "EMPLOYEE ID" in text
        or "MONTHLY EARNINGS" in text
        or "GROSS SALARY" in text
    ):
        return "income_proof"

    # ---------------------------------------------------
    # Aadhaar
    # ---------------------------------------------------
    if (
        re.search(r"\b\d{4}\s\d{4}\s\d{4}\b", text)
        and (
            "AADHAAR" in text
            or "UNIQUE IDENTIFICATION AUTHORITY OF INDIA" in text
            or "VID" in text
        )
    ):
        return "aadhaar"

    # ---------------------------------------------------
    # PAN
    # ---------------------------------------------------
    if (
        re.search(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", text)
        and (
            "INCOME TAX DEPARTMENT" in text
            or "PERMANENT ACCOUNT NUMBER" in text
        )
    ):
        return "pan"

    return "unknown"