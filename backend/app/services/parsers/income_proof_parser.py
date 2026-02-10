import re
from datetime import datetime
from typing import Dict, Optional


def _clean_amount(value: str) -> float:
    """
    Convert amounts like:
    - 85,000.00
    - ₹22,80,000
    - 2280000
    into float
    """
    if not value:
        return 0.0

    value = value.replace(",", "")
    value = value.replace("₹", "")
    value = value.strip()

    try:
        return float(value)
    except ValueError:
        return 0.0


def _extract(pattern: str, text: str) -> Optional[str]:
    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None


def parse_income_proof_fields(raw_text: str) -> Dict:
    """
    Parse salary slip / income proof documents.
    Works for:
    - OCR PDFs
    - HTML-based PDFs
    - Text-based PDFs
    """

    if not raw_text:
        return {}

    text = raw_text.replace("\n", " ")

    extracted = {}

    # --------------------------------------------------
    # Document type
    # --------------------------------------------------
    if re.search(r"payslip|salary slip", text, re.IGNORECASE):
        extracted["income_proof_type"] = "salary_slip"
        extracted["employment_status"] = "Salaried"
    else:
        extracted["income_proof_type"] = "unknown"

    # --------------------------------------------------
    # Employee name
    # --------------------------------------------------
    extracted["employee_name"] = _extract(
        r"Employee Name[:\-]?\s*([A-Za-z\s]+)",
        text
    )

    # --------------------------------------------------
    # Employer / Company name
    # (usually appears at top in caps)
    # --------------------------------------------------
    company_match = re.search(
        r"^([A-Z][A-Z\s&\.]{5,})",
        raw_text.strip(),
        re.MULTILINE
    )
    if company_match:
        extracted["company_name"] = company_match.group(1).strip()

    # --------------------------------------------------
    # PAN number
    # --------------------------------------------------
    extracted["pan_number"] = _extract(
        r"\b([A-Z]{5}[0-9]{4}[A-Z])\b",
        text
    )

    # --------------------------------------------------
    # Payslip month / year
    # --------------------------------------------------
    month_year = _extract(
        r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})",
        text
    )
    if month_year:
        extracted["pay_period"] = month_year

    # --------------------------------------------------
    # Salary components
    # --------------------------------------------------
    basic_salary = _extract(
        r"Basic Salary\s*([\d,]+\.\d{2}|\d+)",
        text
    )
    hra = _extract(
        r"HRA\s*([\d,]+\.\d{2}|\d+)",
        text
    )

    extracted["basic_salary"] = _clean_amount(basic_salary)
    extracted["hra"] = _clean_amount(hra)

    # --------------------------------------------------
    # Gross income (calculated)
    # --------------------------------------------------
    gross_income = extracted["basic_salary"] + extracted["hra"]

    if gross_income > 0:
        extracted["gross_income"] = gross_income

    # --------------------------------------------------
    # Net income (optional)
    # --------------------------------------------------
    net_income = _extract(
        r"Net\s*Salary\s*([\d,]+\.\d{2}|\d+)",
        text
    )
    if net_income:
        extracted["net_income"] = _clean_amount(net_income)

    return extracted
