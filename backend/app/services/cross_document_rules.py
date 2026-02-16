import re
from difflib import SequenceMatcher
from datetime import datetime, date

# -------------------------------------------------
# Helper Functions
# -------------------------------------------------

def _normalize_date(value):
    """
    Convert datetime/date/string into a pure date object.
    Ensures safe comparison across documents.
    """
    if not value:
        return None

    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    # Handle string fallback (very important)
    if isinstance(value, str):
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue

    return None


def _normalize(text: str) -> str:
    """Normalize OCR text for comparison."""
    if not text:
        return ""
    text = re.sub(r"[^A-Za-z0-9 ]", "", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def _fuzzy_match(a: str, b: str, threshold: float = 0.85) -> bool:
    """Fuzzy match to handle OCR noise."""
    if not a or not b:
        return False
    return SequenceMatcher(None, _normalize(a), _normalize(b)).ratio() >= threshold


def _valid_pan_format(pan: str) -> bool:
    """Validate PAN structure."""
    if not pan:
        return False
    return bool(re.fullmatch(r"[A-Z]{5}[0-9]{4}[A-Z]", pan.upper()))


# -------------------------------------------------
# Main Cross Document Validation
# -------------------------------------------------

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

    loan = (
    documents.get("loan_application_form")
    or documents.get("loan_request_form")
    or {}
    )
    pan = documents.get("pan", {})
    aadhaar = documents.get("aadhaar", {})
    income = documents.get("income_proof", {})

    # -------------------------------------------------
    # 1️⃣ NAME CONSISTENCY (Fuzzy Match)
    # -------------------------------------------------
    loan_name = loan.get("applicant_name")
    pan_name = pan.get("name")
    aadhaar_name = aadhaar.get("name")

    if loan_name and pan_name and not _fuzzy_match(loan_name, pan_name):
        issues.append({
            "issue_type": "Mismatch",
            "field_name": "applicant_name",
            "severity": "High",
            "why_flagged": "Applicant name in Loan Form does not match PAN.",
            "suggested_action": "Ensure name is identical across KYC documents."
        })

    if pan_name and aadhaar_name and not _fuzzy_match(pan_name, aadhaar_name):
        issues.append({
            "issue_type": "Mismatch",
            "field_name": "name",
            "severity": "High",
            "why_flagged": "Name on PAN does not match Aadhaar.",
            "suggested_action": "Verify identity consistency across documents."
        })

    # -------------------------------------------------
    # 2️⃣ DOB CONSISTENCY
    # -------------------------------------------------
    pan_dob = _normalize_date(pan.get("dob"))
    aadhaar_dob = _normalize_date(aadhaar.get("dob"))

    if pan_dob and aadhaar_dob and pan_dob != aadhaar_dob:
       issues.append({
        "issue_type": "Mismatch",
        "field_name": "dob",
        "severity": "High",
        "why_flagged": "Date of birth differs between PAN and Aadhaar.",
        "suggested_action": "Submit corrected KYC documents."
    })

    # -------------------------------------------------
    # 3️⃣ PAN NUMBER VALIDATION + MATCH
    # -------------------------------------------------
    pan_number = pan.get("pan_number")
    loan_pan = loan.get("pan_number")

    if pan_number and not _valid_pan_format(pan_number):
        issues.append({
            "issue_type": "Invalid",
            "field_name": "pan_number",
            "severity": "High",
            "why_flagged": "PAN format is invalid.",
            "suggested_action": "Upload a valid PAN card."
        })

    if pan_number and loan_pan and pan_number != loan_pan:
        issues.append({
            "issue_type": "Mismatch",
            "field_name": "pan_number",
            "severity": "High",
            "why_flagged": "PAN in Loan Form does not match PAN card.",
            "suggested_action": "Correct PAN details in application."
        })

    # -------------------------------------------------
    # 4️⃣ AADHAAR CONSISTENCY
    # -------------------------------------------------
    aadhaar_number = aadhaar.get("aadhaar_number")
    loan_aadhaar = loan.get("aadhaar_number")

    if aadhaar_number and loan_aadhaar and aadhaar_number != loan_aadhaar:
        issues.append({
            "issue_type": "Mismatch",
            "field_name": "aadhaar_number",
            "severity": "High",
            "why_flagged": "Aadhaar number differs between documents.",
            "suggested_action": "Provide consistent Aadhaar details."
        })

    # -------------------------------------------------
    # 5️⃣ INCOME REASONABILITY CHECK
    # -------------------------------------------------
    declared_income = loan.get("monthly_income")
    proof_income = income.get("net_income") or income.get("gross_income")

    if declared_income and proof_income:
        if abs(declared_income - proof_income) > 0.20 * proof_income:
            issues.append({
                "issue_type": "Mismatch",
                "field_name": "monthly_income",
                "severity": "Medium",
                "why_flagged": "Declared income significantly differs from income proof.",
                "suggested_action": "Upload updated income proof or correct declaration."
            })

    return issues
