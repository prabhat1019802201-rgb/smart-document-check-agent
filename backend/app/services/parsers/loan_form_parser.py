import re
from typing import Dict, Optional


def _extract(pattern: str, text: str) -> Optional[str]:
    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None


def _clean_amount(value: str) -> float:
    if not value:
        return 0.0

    value = value.replace(",", "")
    value = value.replace("=", "")
    value = value.strip()

    try:
        return float(value)
    except ValueError:
        return 0.0


def parse_loan_form_fields(raw_text: str) -> Dict:
    """
    Parse Loan Application / Loan Request Form
    """

    if not raw_text:
        return {}

    text = raw_text.replace("\n", " ")

    extracted = {}

    # --------------------------------------------------
    # Applicant Name
    # --------------------------------------------------
    extracted["applicant_name"] = _extract(
        r"Full Legal Name[:\-]?\s*([A-Z\s]+)",
        text
    )

    # --------------------------------------------------
    # PAN
    # --------------------------------------------------
    extracted["pan_number"] = _extract(
        r"\b([A-Z]{5}[0-9]{4}[A-Z])\b",
        text
    )

    # --------------------------------------------------
    # Aadhaar
    # --------------------------------------------------
    aadhaar = _extract(
        r"(\d{4}\s\d{4}\s\d{4})",
        text
    )
    if aadhaar:
        extracted["aadhaar_number"] = aadhaar.replace(" ", "")

    # --------------------------------------------------
    # Loan Amount
    # --------------------------------------------------
    amount = _extract(
        r"Requested Amount[:\-]?\s*=?\s*([\d,]+\.\d{2}|\d+)",
        text
    )
    extracted["loan_amount"] = _clean_amount(amount)

    # --------------------------------------------------
    # Tenure
    # --------------------------------------------------
    tenure = _extract(
        r"Tenure\s*\(Months\)[:\-]?\s*(\d+)",
        text
    )
    if tenure:
        extracted["loan_tenure_months"] = int(tenure)

    # --------------------------------------------------
    # Gross Monthly Income
    # --------------------------------------------------
    income = _extract(
        r"Gross Monthly Income[:\-]?\s*([\d,]+)",
        text
    )
    extracted["monthly_income"] = _clean_amount(income)

    # --------------------------------------------------
    # Employer
    # --------------------------------------------------
    extracted["company_name"] = _extract(
        r"Current Employer[:\-]?\s*([A-Za-z\s&\.]+)",
        text
    )

    # --------------------------------------------------
    # Employment Type (derived)
    # --------------------------------------------------
    if extracted.get("monthly_income", 0) > 0:
        extracted["employment_type"] = "Salaried"

    return extracted
