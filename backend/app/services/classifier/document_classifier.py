import re


def _normalize(text: str) -> str:
    """
    Normalize OCR/PDF text for consistent keyword detection.
    """
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).upper()


def detect_document_type(raw_text: str) -> str:
    """
    Deterministic document classifier using strong keyword fingerprinting.
    Order of checks is CRITICAL to avoid misclassification.
    """

    text = _normalize(raw_text)

    # ---------------------------------------------------
    # Aadhaar Detection (Strong Identity Markers)
    # ---------------------------------------------------
    if (
        "UNIQUE IDENTIFICATION AUTHORITY OF INDIA" in text
        or "AADHAAR" in text
        or "UIDAI" in text
    ):
        return "aadhaar"

    # ---------------------------------------------------
    # PAN Detection (PAN Pattern is Highly Reliable)
    # ---------------------------------------------------
    if (
        "INCOME TAX DEPARTMENT" in text
        or "PERMANENT ACCOUNT NUMBER" in text
        or re.search(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", text)
    ):
        return "pan"

    # ---------------------------------------------------
    # CIBIL Detection  ✅ MUST COME BEFORE LOAN
    # ---------------------------------------------------
    if (
        "CIBIL" in text
        or "TRANSUNION" in text
        or "CIBIL SCORE" in text
        or "SCORE RANGES FROM 300 TO 900" in text
    ):
        return "cibil"

    # ---------------------------------------------------
    # Income Proof Detection
    # ---------------------------------------------------
    if (
        "THIS IS TO CERTIFY" in text
        or "EMPLOYEE ID" in text
        or "MONTHLY EARNINGS" in text
        or "SALARY" in text
    ):
        return "income_proof"

    # ---------------------------------------------------
    # Loan Application Detection (Use Multi-key Match)
    # Avoid false positives from financial documents
    # ---------------------------------------------------
    loan_keywords = [
        "LOAN APPLICATION",
        "REQUESTED AMOUNT",
        "LOAN TENURE",
        "EMPLOYMENT & INCOME",
        "PURPOSE",
    ]

    matches = sum(1 for kw in loan_keywords if kw in text)

    if matches >= 2:
        return "loan_application_form"

    # ---------------------------------------------------
    # Unknown
    # ---------------------------------------------------
    return "unknown"